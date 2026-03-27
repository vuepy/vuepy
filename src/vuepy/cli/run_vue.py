# ---------------------------------------------------------
# Copyright (c) vuepy.org. All rights reserved.
# ---------------------------------------------------------
from __future__ import annotations

import argparse
import importlib
import json
import os
import shlex
import sys
from pathlib import Path

from vuepy import VuepyAppStore
from vuepy.compiler_sfc.codegen_backends import TEXTUAL_BACKEND
from vuepy.runtime.core.api_create_app import create_app
from vuepy.runtime.core.import_sfc import import_sfc


def _import_plugin(plugin_path: str):
    """Import a plugin from a dotted path like 'ipywui.wui' or 'textual_vuepy.vtextual'."""
    parts = plugin_path.rsplit('.', 1)
    if len(parts) == 2:
        module_path, attr = parts
        try:
            module = importlib.import_module(module_path)
            return getattr(module, attr)
        except (ImportError, AttributeError) as e:
            raise ImportError(f"Cannot import plugin '{plugin_path}': {e}")
    else:
        try:
            return importlib.import_module(plugin_path)
        except ImportError as e:
            raise ImportError(f"Cannot import plugin '{plugin_path}': {e}")


def _flatten_plugins(args) -> list[str]:
    plugins: list[str] = []
    for p in args.plugins:
        if isinstance(p, list):
            plugins.extend(p)
        else:
            plugins.append(p)
    return plugins


def _textual_serve_run_command(vue_file: str, args) -> str:
    """Shell command for the child process: same as this CLI but without --servable (avoids nested HTTP serve)."""
    if vue_file in VuepyAppStore.get_all_registry():
        target = vue_file
    else:
        target = str(Path(vue_file).resolve())
    parts = [sys.executable, "-m", "vuepy", "run", target, "--backend", "textual"]
    if getattr(args, "dev", False):
        parts.append("--dev")
    if getattr(args, "devtools_host", None) is not None:
        parts.extend(["--devtools-host", str(args.devtools_host)])
    if getattr(args, "devtools_port", None) is not None:
        parts.extend(["--devtools-port", str(args.devtools_port)])
    for pl in _flatten_plugins(args):
        parts.extend(["--plugins", pl])
    return shlex.join(parts)


def _apply_textual_dev_environment(args) -> None:
    """Mirror ``textual run --dev``: merge TEXTUAL features and optional devtools host/port."""
    try:
        from textual.features import parse_features
    except ImportError:
        return
    features = set(parse_features(os.environ.get("TEXTUAL", "")))
    if getattr(args, "dev", False):
        features.add("debug")
        features.add("devtools")
    os.environ["TEXTUAL"] = ",".join(sorted(features))
    if getattr(args, "devtools_host", None) is not None:
        os.environ["TEXTUAL_DEVTOOLS_HOST"] = str(args.devtools_host)
    if getattr(args, "devtools_port", None) is not None:
        os.environ["TEXTUAL_DEVTOOLS_PORT"] = str(args.devtools_port)


def run_vue(args):
    vue_file = args.vue_file

    if args.backend == TEXTUAL_BACKEND:
        _load_builtin_app_registrations()
        _apply_textual_dev_environment(args)

    if args.servable and args.backend == TEXTUAL_BACKEND:
        try:
            from textual_serve.server import Server
        except ImportError as e:
            raise ImportError(
                "`vuepy run --servable` in textual backend needs textual-serve, please execute: pip install textual-serve"
            ) from e
        run_command = _textual_serve_run_command(vue_file, args)
        server = Server(
            run_command,
            args.serve_host,
            args.serve_port,
            title=args.serve_title or run_command,
            public_url=args.serve_public_url,
        )
        server.serve(debug=args.serve_debug)
        return

    if vue_file in VuepyAppStore.get_all_registry():
        App = VuepyAppStore.get(vue_file)
    else:
        App = import_sfc(vue_file)

    app = create_app(App, backend=args.backend, servable=args.servable)

    plugins = _flatten_plugins(args)

    for plugin_path in plugins:
        plugin = _import_plugin(plugin_path)
        app.use(plugin)

    if args.show_code:
        print(json.dumps({
            'vue': f'<!-- {vue_file} -->\n',
            'setup': '',
        }))

    app.mount()


def _load_builtin_app_registrations() -> None:
    """Import modules that register apps with VuepyAppStore (e.g. textual_vuepy.apps)."""
    try:
        import textual_vuepy.apps  # noqa: F401
    except ImportError:
        pass


def _run_subcommand_epilog() -> str:
    _load_builtin_app_registrations()
    apps = VuepyAppStore.get_all_registry()
    if not apps:
        return (
            "\nVuepyAppStore: (no registered names). "
            "Packages such as textual_vuepy register names when imported."
        )
    lines = ["", "VuepyAppStore registered names (valid as vue_file):"]
    for app_name, app in apps.items():
        lines.append(f"  - {app_name}: {app.setup.__doc__.strip()}")
    return "\n".join(lines)


def register_subcommand(subparsers):
    p = subparsers.add_parser(
        "run",
        help="Run a Vuepy app from a .vue file or a VuepyAppStore name.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=_run_subcommand_epilog(),
    )
    p.add_argument(
        'vue_file',
        type=str,
        help='Path to a .vue file, or a VuepyAppStore name listed in the epilog below.',
    )
    p.add_argument(
        '--backend',
        type=str,
        default=TEXTUAL_BACKEND,
        help='Codegen backend: ipywidgets, panel, textual, etc. (default: textual).',
    )
    p.add_argument(
        '--plugins',
        required=False,
        nargs='+',
        default=[],
        type=lambda v: [i.strip() for i in v.split(',')],
        help='List of plugins as importable dotted paths, comma-separated or space-separated '
             '(e.g. ipywui.wui or textual_vuepy.vtextual)',
    )
    p.add_argument(
        '--show-code',
        required=False,
        action='store_true',
        help='Print the vue source code before running',
    )
    p.add_argument(
        '--dev',
        action='store_true',
        help=(
            'Textual backend only: enable development mode (TEXTUAL debug + devtools), '
            'same idea as ``textual run --dev``.'
        ),
    )
    p.add_argument(
        '--devtools-host',
        default=None,
        metavar='HOST',
        help='Textual backend only: devtools console host (sets TEXTUAL_DEVTOOLS_HOST).',
    )
    p.add_argument(
        '--devtools-port',
        type=int,
        default=None,
        metavar='PORT',
        help='Textual backend only: devtools console port (sets TEXTUAL_DEVTOOLS_PORT).',
    )
    p.add_argument(
        '--servable',
        required=False,
        action='store_true',
        help=(
            'Servable mode: panel backend uses Panel.servable(); textual backend starts '
            'textual-serve (child runs the same vuepy run command without this flag).'
        ),
    )
    p.add_argument(
        '--serve-host',
        default='127.0.0.1',
        help='With --servable and textual backend: HTTP bind address (default 127.0.0.1).',
    )
    p.add_argument(
        '--serve-port',
        type=int,
        default=8000,
        help='With --servable and textual backend: HTTP port (default 8000).',
    )
    p.add_argument(
        '--serve-title',
        default=None,
        help='With --servable and textual backend: browser page title (default: run command).',
    )
    p.add_argument(
        '--serve-public-url',
        default=None,
        help='With --servable and textual backend: public URL shown to users (default from host/port).',
    )
    p.add_argument(
        '--serve-debug',
        action='store_true',
        help='With --servable and textual backend: enable textual-serve debug mode.',
    )
    p.set_defaults(func=run_vue)

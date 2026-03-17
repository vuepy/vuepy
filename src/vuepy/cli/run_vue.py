# ---------------------------------------------------------
# Copyright (c) vuepy.org. All rights reserved.
# ---------------------------------------------------------
import argparse
import importlib
import json

from vuepy.compiler_sfc.codegen_backends import IPYWIDGETS_BACKEND
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


def run_vue(args):
    vue_file = args.vue_file
    App = import_sfc(vue_file)

    app = create_app(App, backend=args.backend, servable=args.servable)

    plugins = []
    for p in args.plugins:
        plugins.extend(p) if isinstance(p, list) else plugins.append(p)

    for plugin_path in plugins:
        plugin = _import_plugin(plugin_path)
        app.use(plugin)

    if args.show_code:
        print(json.dumps({
            'vue': f'<!-- {vue_file} -->\n',
            'setup': '',
        }))

    app.mount()


def register_subcommand(subparsers):
    p = subparsers.add_parser('run', help='run a Vuepy app from a .vue file')
    p.add_argument(
        'vue_file',
        type=str,
        help='Path to the .vue file to run',
    )
    p.add_argument(
        '--backend',
        type=str,
        default=IPYWIDGETS_BACKEND,
        help='Backend of codegen: ipywidgets, panel, textual, etc. default: ipywidgets',
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
        '--servable',
        required=False,
        action='store_true',
        help='Make the app servable (for panel backend)',
    )
    p.set_defaults(func=run_vue)

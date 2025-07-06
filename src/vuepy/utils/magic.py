# coding: utf-8
import argparse
import json
import logging
import shlex
from pathlib import Path

import IPython
from IPython.core.magic import register_line_cell_magic
from IPython.core.magic import register_line_magic

from ipywui import wui
from vuepy import log
from vuepy.compiler_sfc.codegen_backends import ipywidgets as iw_backend
from vuepy.compiler_sfc.sfc_parser import SFCMetadata
from vuepy.runtime.core.api_create_app import create_app
from vuepy.runtime.core.import_sfc import import_sfc
from vuepy.utils.appstore import VuepyAppStore


def get_curr_ipynb_dir():
    ipy = IPython.get_ipython()
    if '__vsc_ipynb_file__' in ipy.user_ns:
        return Path(ipy.user_ns['__vsc_ipynb_file__']).parent
    else:
        return Path().absolute()


class LogLevelScope:
    def __init__(self, logger: logging.Logger, level=logging.ERROR):
        self.logger = logger
        self.org_level = logger.level
        self.level = level

    def __enter__(self):
        self.logger.setLevel(self.level)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logger.setLevel(self.org_level)


@register_line_cell_magic
def vuepy_import(vue_sfc, cell=''):
    """
    import Component from sfc_file or raw_content of sfc

    usage:

    ```python
    from vuepy import create_app
    from vuepy.utils import magic

    App=%vuepy_import test.vue
    app = create_app(App)
    app.mount()
    ```

    usage:
    ```
    %%vuepy_import Component1
    <template>
      <Button description="add"
              button_style="info"
      ></Button>
    </template>
    ```

    :param vue_sfc:
    :param cell:
    :return: App
    """
    if cell:
        component_var_name = vue_sfc.strip()
        ipython = IPython.get_ipython()
        ipython.user_ns[component_var_name] = import_sfc(cell, raw_content=True)
        print(f"import Component {component_var_name} success.")
    else:
        return import_sfc(vue_sfc)


@register_line_magic
def vuepy_demo(vue_sfc):
    """
    %vuepy_demo test.vue

    :param vue_sfc:
    :return:
    """
    args = vue_sfc.strip().split()
    if len(args) == 2:
        vue_sfc, return_app = args
    else:
        return_app = 'no'

    sfc_file_path = Path(vue_sfc.strip())
    sfc_metadata = SFCMetadata.load(sfc_file_path)

    script_content = 0
    if sfc_metadata.script_src:
        _script_file = sfc_metadata.file.parent / sfc_metadata.script_src
        with open(_script_file) as f:
            _comment = f'# {sfc_metadata.script_src}\n\n'
            script_content = _comment + f.read()

    sfc_file_comment = f'<!-- {sfc_file_path} -->\n'
    print(json.dumps({
        'vue': sfc_file_comment + sfc_metadata.content,
        'setup': script_content,
    }))

    with LogLevelScope(log.getLogger()):
        App = import_sfc(sfc_file_path)
        app = create_app(App).use(wui)
        if return_app != 'no':
            return app
        else:
            return app.mount()


@register_line_magic
def vuepy_log(cmd):
    """
    show log.

    :param cmd: clear
    :return:
    """
    if cmd == 'clear':
        log.logout.clear_output()
    return log.logout


@register_line_cell_magic
def vuepy_run(vue_file, cell=''):
    """
    run Vuepy app from vue_file or raw_content of vue file or Component

    Usage 1: cell magic: from raw_content of vue file
    ```
    ------cell--------
    %%vuepy_run
    <template>
      <Button description="add"
              button_style="info"
      ></Button>
    </template>
    ------------------
    ```

    Usage 2: cell magic: with plugins and app_var
    ```
    ------cell--------
    [1] from ipywui import wui
    ------cell--------
    %%vuepy_run --plugins wui --app app
    <template><p>hello</p></template>
    ------cell--------
    [2] app
    App at 0x100000000
    ------------------
    ```

    Usage 3: line magic: from vue_file
    ```
    ------cell--------
    %vuepy_run app.vue
    ------------------
    ```

    Usage 4: line magic: from Component
    ```
    ------cell--------
    %%vuepy_import Component1
    <template>
      <Button description="add"
              button_style="info"
      ></Button>
    </template>
    ------cell--------
    # Equivalent to create_app(Component1).mount()
    %vuepy_run $$Component1
    ------------------
    ```

    Usage 5: line magic: with plugins and app_var
    ```
    ------cell--------
    [1] from ipywui import wui
    [2] from vleaflet import leaflet
    ------cell--------
    [2] %vuepy_run test.vue --plugins wui,leaflet --app app
    ------cell--------
    [3] app
    App at 0x100000000
    ------------------
    ```

    :param vue_file: vue_file | Component
    :param cell: raw_content of vue file | None
    :return:
    """

    def add_codegen_backend_params(parser: argparse.ArgumentParser):
        parser.add_argument(
            '--backend',
            type=str,
            default=iw_backend.NAME,
            help='backend of codegen: ipywidgets, panel, etc. default: ipywidgets'
        )
        return parser

    def add_vue_file_params(parser: argparse.ArgumentParser):
        parser.add_argument('vue_file',
                            type=str,
                            help='Vue file to run')
        return parser

    def add_plugins_params(parser: argparse.ArgumentParser):
        parser.add_argument('--plugins',
                            required=False,
                            nargs='+',
                            default=[],
                            type=lambda v: [i.strip() for i in v.split(',')],
                            help='List of plugins (comma-separated or space-separated)')
        return parser

    def add_app_var_params(parser: argparse.ArgumentParser):
        parser.add_argument('--app',
                            required=False,
                            type=str,
                            help='Name of the variable to store the app instance')
        return parser

    def add_show_code_params(parser: argparse.ArgumentParser):
        parser.add_argument('--show-code',
                            required=False,
                            action='store_true',
                            help='show code')
        return parser
    
    def add_servable_params(parser: argparse.ArgumentParser):
        parser.add_argument('--servable',
                            required=False,
                            action='store_true',
                            help='make app servable')
        return parser

    parser = argparse.ArgumentParser()
    ipython = IPython.get_ipython()
    if cell:
        add_plugins_params(parser)
        add_app_var_params(parser)
        add_show_code_params(parser)
        add_codegen_backend_params(parser)
        add_servable_params(parser)
        args, _ = parser.parse_known_args(shlex.split(vue_file))
        App = import_sfc(cell, raw_content=True)
    else:
        add_vue_file_params(parser)
        add_plugins_params(parser)
        add_app_var_params(parser)
        add_show_code_params(parser)
        add_codegen_backend_params(parser)
        add_servable_params(parser)
        args, _ = parser.parse_known_args(shlex.split(vue_file))
        vue_file = args.vue_file
        if vue_file.startswith('$'):
            App = ipython.user_ns[vue_file[1:]]
        elif vue_file in VuepyAppStore.get_all_registry():
            App = VuepyAppStore.get(vue_file)
        else:
            App = import_sfc(vue_file)

    app = create_app(App, backend=args.backend, servable=args.servable)
    plugins = []
    for _p in args.plugins:
        plugins.extend(_p) if isinstance(_p, list) else plugins.append(_p)

    for plugin in plugins:
        if plugin not in ipython.user_ns:
            raise ValueError(f"Plugin {plugin} not found in user namespace")
        app.use(ipython.user_ns[plugin])

    if args.app:
        ipython = IPython.get_ipython()
        ipython.user_ns[args.app] = app

    if args.show_code:
        # sfc_file_comment = f'<!-- {sfc_file_path} -->\n'
        print(json.dumps({
            'vue': f'<!-- {vue_file} -->\n{cell}',
            'setup': '',
        }))

    return app.mount()


def load_ipython_extension(ipython):
    def vuepy_run_complete(self, event):
        return VuepyAppStore.get_all_registry().keys()

    ipython.set_hook('complete_command', vuepy_run_complete, re_key='%vuepy_run')


load_ipython_extension(IPython.get_ipython())

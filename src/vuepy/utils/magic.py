# coding: utf-8
import json
import logging
from pathlib import Path

import IPython
from IPython.core.magic import register_line_cell_magic
from IPython.core.magic import register_line_magic

from ipywui import wui
from vuepy import log
from vuepy.compiler_sfc.compile import SFCFile
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
    sfc_file = SFCFile.load(sfc_file_path)

    script_content = 0
    if sfc_file.script_src:
        _script_file = sfc_file.file.parent / sfc_file.script_src
        with open(_script_file) as f:
            _comment = f'# {sfc_file.script_src}\n\n'
            script_content = _comment + f.read()

    sfc_file_comment = f'<!-- {sfc_file_path} -->\n'
    print(json.dumps({
        'vue': sfc_file_comment + sfc_file.content,
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

    usage:
    cell magic: from raw_content of vue file
    ```
    ------------------
    %%vuepy_run
    <template>
      <Button description="add"
              button_style="info"
      ></Button>
    </template>
    ------------------
    ```

    line magic: from vue_file
    ```
    ------------------
    %vuepy_run app.vue
    ------------------
    ```

    line magic: from Component
    ```
    ------------------
    %%vuepy_import Component1
    <template>
      <Button description="add"
              button_style="info"
      ></Button>
    </template>

    ------------------
    # Equivalent to create_app(Component1).mount()
    %vuepy_run $$Component1

    ------------------
    ```

    :param vue_file: vue_file | Component
    :param cell: raw_content of vue file | None
    :return:
    """
    if cell:
        App = import_sfc(cell, raw_content=True)
    else:
        vue_file = vue_file.strip()
        if vue_file.startswith('$'):
            ipython = IPython.get_ipython()
            App = ipython.user_ns[vue_file[1:]]
        elif vue_file in VuepyAppStore.get_all_registry():
            App = VuepyAppStore.get(vue_file)
        else:
            App = import_sfc(vue_file)

    app = create_app(App)
    return app.mount()


def load_ipython_extension(ipython):
    def vuepy_run_complete(self, event):
        return VuepyAppStore.get_all_registry().keys()

    ipython.set_hook('complete_command', vuepy_run_complete, re_key='%vuepy_run')


load_ipython_extension(IPython.get_ipython())

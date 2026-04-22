# ---------------------------------------------------------
# Copyright (c) vuepy.org. All rights reserved.
# ---------------------------------------------------------
from __future__ import annotations

import importlib.util
import inspect
import os
import pathlib
import sys
import textwrap

from vuepy.compiler_sfc import sfc_compiler, sfc_parser


VUE_AOT_MODULE_PREFIX = "_vue_aot_"


def find_content_start_line(sub_content, content_lines):
    sub_content_lines = sub_content.split('\n')
    offset = 0
    if sub_content_lines[0] == '':
        offset = -1
        sub_content_lines = sub_content_lines[1:]

    sub_content_lc = len(sub_content_lines)
    compare_line = 0
    for line_num, line in enumerate(content_lines):
        sub_content_line = sub_content_lines[compare_line]
        if sub_content_line in line:
            compare_line += 1
        else:
            compare_line = 0

        if compare_line == sub_content_lc:
            return offset + line_num + 1 - compare_line + 1

    return None


def from_vue_aot_import_component(vue_py_path: pathlib.Path):
    module_name = None
    for p in sys.path:
        if not p:
            p = os.getcwd()
        p_path = pathlib.Path(p).resolve()
        try:
            rel = vue_py_path.resolve().relative_to(p_path)
            parts = list(rel.parts)
            parts[-1] = vue_py_path.stem
            candidate = ".".join(parts)
            if module_name is None or len(candidate) < len(module_name):
                module_name = candidate
        except ValueError:
            pass
            
    module_name = module_name or vue_py_path.stem

    spec = importlib.util.spec_from_file_location(module_name, str(vue_py_path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    comp = module.Component
    comp.__module__ = module_name
    return comp


def get_vue_aot_modules():
    return {
        k: m
        for k, m in sys.modules.items()
        if k.rsplit('.', 1)[-1].startswith(VUE_AOT_MODULE_PREFIX)
    }


def get_vue_aot_module_names():
    return get_vue_aot_modules().keys()


def import_sfc_aot(vue_path: str, force_compile=False):
    vue_path = pathlib.Path(vue_path).resolve()
    module_name = f"{VUE_AOT_MODULE_PREFIX}{vue_path.stem}"
    vue_py_path = vue_path.with_name(f"{module_name}.py")

    if not vue_path.exists() and not vue_py_path.exists():
        # 1. Check if the module is already available (e.g. compiled by Nuitka)
        # We try combinations of parent directories to form the package name
        # e.g., _vue_aot_Child2, comps._vue_aot_Child2, etc.
        parts = vue_path.parts
        try_modules = [module_name]
        
        # Build potential package names from the path parts backwards
        current_pkg = []
        for i in range(len(parts)-2, -1, -1):
            # Ignore root/drive parts
            if not parts[i] or parts[i] in ("/", "\\"):
                break
            current_pkg.insert(0, parts[i])
            pkg_name = ".".join(current_pkg)
            try_modules.append(f"{pkg_name}.{module_name}")

        for m in try_modules[::-1]:
            try:
                module = importlib.import_module(m)
                return module.Component
            except ImportError:
                pass

        raise FileNotFoundError(f"File not found: {vue_path}")
    
    if (
        not force_compile or (
            (not vue_path.exists())  # for nuitka aot, the vue_path may not exist
            or (vue_py_path.exists() and vue_py_path.stat().st_mtime > vue_path.stat().st_mtime)
        )
    ):
        return from_vue_aot_import_component(vue_py_path)

    sfc_meta = sfc_parser.parse(vue_path)
    
    script_content = sfc_meta.script_py or ""
    
    # We need to preserve line numbers of the original script_py inside the setup function
    # so that tracebacks match the .vue file! But wait, `script_content` already lacks the offset.
    # Nuitka will use the generated .py file for tracebacks anyway, so it's fine.
    
    if script_content:
        indented_script = "\n".join("    " + line for line in script_content.split("\n"))
    else:
        indented_script = "    pass"
        
    py_code = f"""# Auto-generated from {vue_path.name}
from vuepy.compiler_sfc.sfc_codegen import SFCType

def setup(props, ctx, app):
{indented_script}
    return locals()

Component = SFCType(
    setup=setup,
    template={repr(sfc_meta.template)},
    style_str={repr(sfc_meta.style_str or "")},
    style_src={repr(sfc_meta.style_src or "")},
    _file={repr(str(vue_path))}
)
"""
    
    # Output to _vue.py
    with open(vue_py_path, "w", encoding="utf-8") as f:
        f.write(py_code)
        f.flush()
        os.fsync(f.fileno())
   
    return from_vue_aot_import_component(vue_py_path)


def import_sfc(sfc_file, raw_content=False, force_aot_compile=False):
    """
    import Component from sfc_file or raw_content fo sfc

    :param sfc_file:
    :param raw_content:
    :param force_aot_compile:
    :return:
    """
    en_vuepy_aot = os.environ.get("EN_VUEPY_AOT", "0").lower() in ["1", "true"]
    if en_vuepy_aot and not raw_content:
        return import_sfc_aot(sfc_file, force_compile=force_aot_compile)

    # if raw_content=True, try to get the original file name from the call stack
    if raw_content:
        try:
            frame = inspect.currentframe()
            if frame and frame.f_back:
                caller_frame = frame.f_back
                caller_filename = caller_frame.f_code.co_filename
                if caller_filename:
                    caller_line = caller_frame.f_lineno
                    caller_filename = pathlib.Path(caller_filename)
                    with open(caller_filename, 'r', encoding='utf-8') as f:
                        caller_lines = f.readlines()

                    sfc_start_line = None
                    for i in range(caller_line - 1, caller_line + 1):
                        line_content = caller_lines[i]
                        # if 'import_sfc' in line_content:
                        if not('"""' in line_content or "'''" in line_content):
                            continue
                        sfc_start_line = i + 1
                        break
                    else:
                        sfc_start_line = find_content_start_line(sfc_file, caller_lines)

                    if sfc_start_line is not None:
                        return sfc_compiler.compile(
                            textwrap.dedent(sfc_file), 
                            raw_content=raw_content,
                            source_file=caller_filename,
                            source_start_line=sfc_start_line
                        )
        except Exception:
            return sfc_compiler.compile(textwrap.dedent(sfc_file), raw_content)
    
    return sfc_compiler.compile(sfc_file, raw_content)

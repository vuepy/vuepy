from __future__ import annotations

import ast
import importlib.util
import types


class ScriptCompiler:
    @staticmethod
    def compile_script_block_bak(code_str, source_file_path):
        indent_code_str = '\n'.join([f"  {line}" for line in code_str.split('\n')])
        code = '\n'.join([
            "def setup(props, ctx, app):",
            indent_code_str,
            "\n",
            "  return locals()",
        ])

        module = types.ModuleType('tmp_module')
        module.__dict__['__file__'] = source_file_path
        exec(code, module.__dict__)
        return module.setup

    @staticmethod
    def compile_script_block(code_str, source_file_path):
        module = ast.parse(code_str)
        func_name = 'setup'
        func_ast = ast.FunctionDef(
            name=func_name,
            args=ast.arguments(
                posonlyargs=[],
                args=[
                    ast.arg(arg='props', annotation=None),
                    ast.arg(arg='ctx', annotation=None),
                    ast.arg(arg='app', annotation=None)
                ],
                vararg=None,
                kwonlyargs=[],
                kw_defaults=[],
                kwarg=None,
                defaults=[],
            ),
            body=module.body + [ast.parse('return locals()').body[0]],
            decorator_list=[],
            returns=None
        )

        module.body = [func_ast]
        ast.fix_missing_locations(module)
        code = compile(module, filename='<ast>', mode='exec')

        pymodule = types.ModuleType('tmp_module')
        pymodule.__dict__['__file__'] = source_file_path
        exec(code, pymodule.__dict__)
        return pymodule.setup

    @staticmethod
    def compile_script_src(dir_path, src):
        _script_path = dir_path.joinpath(src)
        if not _script_path.exists():
            raise ValueError(f"sfc script {_script_path} not exists.")

        _spec = importlib.util.spec_from_file_location('sfc', str(_script_path))
        _module = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_module)
        return getattr(_module, 'setup')

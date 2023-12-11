# coding: utf-8
import ast
from _ast import Call, Name
from typing import Any


class CodeTransformer(ast.NodeTransformer):
    def __init__(self, data, methods):
        self.data = data
        self.methods = methods
        self._deps = []

    def visit_Call(self, node: Call) -> Any:
        func = node.func
        if isinstance(func, ast.Name) and func.id not in self.methods:
            raise ValueError(f"func {func.id} is not valid")

        self.generic_visit(node)
        return node

    def visit_Name(self, node: Name) -> Any:
        if node.id in self.data:
            print(f'add {node.id} to watcher')
        elif node.id in self.methods:
            pass
        else:
            raise ValueError(f"var {node.id} is not defined")

        return node

    def get_deps(self, code_ast):
        self._deps = []
        self.visit(code_ast)
        return self._deps


def obj_to_ns(obj):
    data = vars(obj)
    methods = {
        m: getattr(obj, m) for m in dir(obj) if not m.startswith('_')
    }
    return data, methods


class F:
    def __init__(self):
        self.x = 1

    def f(self, x):
        return self.x + x


def _eval(code, data, methods, l=None):
    ast_org = ast.parse(code, mode='eval')
    tr = CodeTransformer(data, methods)
    ast_new = tr.visit(ast_org)
    code_obj = compile(ast_new, "<string>", "eval")
    return eval(code_obj, {**data, **methods}, l)


code = "__import__('os').system('echo aa')"
code = 'a.f(x+1)'
code = 'f(x+1)'

fo = F()
data, methods = obj_to_ns(fo)
a = _eval(code, data, methods, {'x': 100})
print(f'a is {a}')

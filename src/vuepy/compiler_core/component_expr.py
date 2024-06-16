from __future__ import annotations

import ast
import types

from _ast import Attribute
from typing import Any


# todo rename VueCompExpr
class VueCompExpr:
    def __init__(self, exp_ast, _vars=None, exp_str=''):
        self.vars = _vars if _vars else []
        self.exp_ast = exp_ast
        self.exp_str = exp_str

    def add_var(self, var):
        self.vars.append(var)

    @classmethod
    def parse(cls, expr_str) -> VueCompExpr:
        # return VueCompExprParser.parse(expr_str)
        expr_ast = ast.parse(expr_str, mode='eval')
        comp_expr_ast = VueCompExprTransformer().transformer(expr_ast)
        comp_expr_ast.exp_str = expr_str
        return comp_expr_ast

    @classmethod
    def compile(cls, exp_ast):
        if isinstance(exp_ast, types.CodeType):
            return exp_ast

        return compile(exp_ast, "<string>", "eval")

    def eval(self, ns: "VueCompNamespace", local_vars=None):
        # return vue_comp_expr_eval(self, ns, local_vars)
        code_obj = self.compile(self.exp_ast)
        return eval(code_obj, {"__builtin__": None}, ns.to_py_eval_ns(local_vars))


class VueCompExprTransformer(ast.NodeTransformer):
    def __init__(self):
        self.vars = []
        self._in_attr = False

    @classmethod
    def get_attr_chain(cls, node):
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            base = cls.get_attr_chain(node.value)
            return f"{base}.{node.attr}"

    def visit_Attribute(self, node: Attribute) -> Any:
        if self._in_attr:
            return node

        self._in_attr = True
        self.vars.append(self.get_attr_chain(node))

        self.generic_visit(node)
        self._in_attr = False
        return node

    def transformer(self, exp_ast: ast.Expression):
        if isinstance(exp_ast.body, ast.Name):
            self.vars = [exp_ast.body.id]
        else:
            self.visit(exp_ast)

        return VueCompExpr(exp_ast, self.vars)

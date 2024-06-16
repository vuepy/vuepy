from __future__ import annotations

import re
from typing import Any
from typing import Callable
from typing import List
from typing import Tuple

import ipywidgets as widgets

from vuepy import log
from vuepy.compiler_core.ast import NodeAst
from vuepy.compiler_core.ast import VForAst
from vuepy.compiler_core.ast import VueCompAst
from vuepy.compiler_core.component_expr import VueCompExpr
from vuepy.compiler_core.utils import VueCompNamespace
from vuepy.reactivity.reactive import to_raw
from vuepy.reactivity.watch import WatchOptions
from vuepy.reactivity.watch import watch

logger = log.getLogger()


def v_for_stack_to_iter(stack: List[VForAst], fn: VForIterFn, ns: dict,
                        for_block_stack_idxs: Tuple[int] = (),
                        for_block_stack_vars: dict = None) -> List[Any]:
    """
    s1 = [1,2]
    s2 = [3,4,5]
    s3 = [6,7]
    for_stack = [s1, s2, s3]
    --
    [ [ [ fn((0, 0, 0), (1, 3, 6)),
          fn((0, 0, 1), (1, 3, 7)) ],
        [ fn((0, 1, 0), (1, 4, 6)),
          fn((0, 1, 1), (1, 4, 7)) ],
        [ fn((0, 2, 0), (1, 5, 6)),
          fn((0, 2, 1), (1, 5, 7)) ]],
      [ [ fn((1, 0, 0), (2, 3, 6)),
          fn((1, 0, 1), (2, 3, 7)) ],
        [ fn((1, 1, 0), (2, 4, 6)),
          fn((1, 1, 1), (2, 4, 7)) ],
        [ fn((1, 2, 0), (2, 5, 6)),
          fn((1, 2, 1), (2, 5, 7)) ]]]

    :param stack:
    :param fn:
    :param ns:
    :param for_block_stack_idxs:
    :param for_block_stack_vars:
    :return:
    """
    if not stack:
        return []

    for_block_stack_vars = for_block_stack_vars or {}
    v_for_ast = stack[0]
    if len(stack) == 1:
        ret = []
        with VForBLockScope(v_for_ast, ns) as for_block_scope:
            for i, val in enumerate(for_block_scope):
                _idxs = (*for_block_stack_idxs, i)
                _vars = {**for_block_stack_vars, **for_block_scope.for_vars}
                ret.append(fn(_idxs, _vars, v_for_ast))
        return ret

    ret = []
    with VForBLockScope(v_for_ast, ns) as for_block_scope:
        for i, val in enumerate(for_block_scope):
            _idxs = (*for_block_stack_idxs, i)
            _vars = {**for_block_stack_vars, **for_block_scope.for_vars}
            ret.append(v_for_stack_to_iter(stack[1:], fn, for_block_scope.ns, _idxs, _vars))

    return ret


class VForBLockScope:
    def __init__(self, v_for_ast: VForAst, ns):
        self.ns = ns
        self.v_for_ast = v_for_ast

        self.iter = None
        self.target = None
        self.idx = 0
        self.vars_bak = {}
        self.for_vars = {}

    def __enter__(self):
        iter_exp = self.v_for_ast.iter
        if iter_exp in self.ns:
            self.iter = self.ns[iter_exp]
        else:
            self.iter = eval(iter_exp, {}, self.ns)

        target_var = self.v_for_ast.target
        if target_var in self.ns:
            self.vars_bak[target_var] = self.ns[target_var]

        idx_var = self.v_for_ast.idx
        if idx_var in self.ns:
            self.vars_bak[idx_var] = self.ns[idx_var]

        self.for_vars[iter_exp] = self.iter

        return self

    def __iter__(self):
        self.idx = 0
        return self

    def __next__(self):
        if self.idx >= len(self.iter):
            self.idx = 0
            raise StopIteration()

        # set target
        target_exp = self.v_for_ast.target
        target = self.iter[self.idx]
        self.for_vars[target_exp] = target
        self.ns[target_exp] = target

        if self.v_for_ast.idx is not None:
            # set idx
            idx_exp = self.v_for_ast.idx
            self.for_vars[idx_exp] = self.idx
            self.ns[idx_exp] = self.idx

        self.idx += 1

        return target

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ns.update(self.vars_bak)
        self.vars_bak = {}
        self.for_vars = {}


VForIterFn = Callable[[Tuple[int], dict, VForAst], Any]


class VueHtmlTemplateRender:
    DELIMITERS_PATTERN = r"\{\{\s*(.*?)\s*\}\}"

    @staticmethod
    def _replace(ns: VueCompNamespace, for_idx):
        def warp(match):
            expr_str = match.group(1)
            expr_ast = VueCompExpr.parse(expr_str)
            # TODO html可以设置value，按需更新
            _value = expr_ast.eval(ns)
            return str(_value)

        return warp

    @classmethod
    def should_render(cls, template):
        return bool(re.search(cls.DELIMITERS_PATTERN, template))

    @classmethod
    def render(cls, template, ns: VueCompNamespace, for_idx=-1):
        result = re.sub(cls.DELIMITERS_PATTERN, cls._replace(ns, for_idx), template)
        return result


class VueHtmlCompCodeGen:
    @classmethod
    def gen(cls, node: NodeAst, ns: VueCompNamespace):
        comp_ast = VueCompAst.transform(node.tag, node.attrs)

        # @computed
        def __html_tag_exit_gen_html():
            # v-if or v-show
            if_cond = comp_ast.v_if or comp_ast.v_show
            if if_cond and not if_cond.eval(ns):
                return ''

            # v-html
            if comp_ast.v_html:
                attr_chain = comp_ast.v_html
                return ns.getattr(attr_chain)

            # innerHtml
            inner = []
            for child in node.children:
                if callable(child):
                    inner.append(child())
                elif isinstance(child, widgets.HTML):
                    inner.append(child.value)
                else:
                    inner.append(child)
            inner_html = ' '.join(inner)

            attrs = [f"{k}='{v}'" for k, v in comp_ast.kwargs.items()]

            # v-bind:
            for attr, exp_ast in comp_ast.v_binds.items():
                attrs.append(f"{attr}='{to_raw(exp_ast.eval(ns))}'")

            html = f'''
                <{node.tag} {' '.join(attrs)}>
                  {inner_html}
                </{node.tag}>'''

            return html

        return __html_tag_exit_gen_html

    @classmethod
    def gen_from_fn(cls, fn):
        widget = widgets.HTML()

        @watch(fn, WatchOptions(immediate=True))
        def _update_html_widget_value(new_html, old_html, on_cleanup):
            widget.value = new_html

        return widget

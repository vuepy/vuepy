from __future__ import annotations

import functools
from html.parser import HTMLParser
from typing import List
from typing import Tuple

import ipywidgets as widgets

from vuepy import log
from vuepy.compiler_core.ast import NodeAst
from vuepy.compiler_core.ast import NodeAstType
from vuepy.compiler_core.ast import VForAst
from vuepy.compiler_core.ast import VForNodeAst
from vuepy.compiler_core.ast import VForScopes
from vuepy.compiler_core.ast import VueCompAst
from vuepy.compiler_core.errors import CompilerSyntaxError
from vuepy.compiler_core.utils import VueCompNamespace
from vuepy.compiler_dom.codegen import VueHtmlCompCodeGen
from vuepy.compiler_dom.codegen import VueHtmlTemplateRender
from vuepy.compiler_dom.codegen import v_for_stack_to_iter
from vuepy.compiler_sfc.codegen import VueCompCodeGen
from vuepy.compiler_sfc.codegen import VueComponent
from vuepy.reactivity.watch import watch
from vuepy.runtime.core.api_create_app import App
from vuepy.utils.common import Nil

logger = log.getLogger()


class DomCompiler(HTMLParser):
    """
    @vue/compiler-dom
    """

    def __init__(self, vm: VueComponent, app: 'App'):
        super().__init__()
        self.vm = vm
        self.app = app
        self.widgets = NodeAst('dummy', children=[])
        self.widgets_by_id = {}
        self.parent_node_stack: List[NodeAst | VForNodeAst] = []
        self.v_for_stack: List[VForAst] = []
        self.v_if_stack: List[str] = []
        self._tag = self.widgets.tag

    def _get_element_by_id(self, el_id):
        return self.widgets_by_id.get(el_id)

    @property
    def is_in_for_stmt(self):
        return bool(self.v_for_stack)

    def _process_directive(self):
        pass

    def _gen_widget(self, node: NodeAst, for_scope: VForScopes = None):
        local_vars = for_scope and for_scope.to_ns()
        ns = VueCompNamespace(self.vm.to_ns(), self.vm.to_ns(), local_vars)
        if self.vm.component(node.tag):
            widget = VueCompCodeGen.gen(node, self.vm, ns, self.app)
        else:
            widget = VueHtmlCompCodeGen.gen(node, ns)

        return widget

    def _get_raw_tag(self, tag):
        row, col = self.getpos()
        row_idx = row - 1
        col_idx = col + 1
        return self.html_lines[row_idx][col_idx: col_idx + len(tag)]

    def _to_camel_case_tag(self, tag):
        words = tag.split('-')
        if len(words) == 1:
            return tag
        return ''.join(w.title() for w in words)

    def handle_starttag(self, case_insensitive_tag, attrs):
        def _gen_node_ast(tag, attrs, for_processed: bool = False, idxs: Tuple[int] = None,
                          vars: dict = None, v_for: VForAst = None) -> NodeAst:
            idxs = idxs or []
            if self.parent_node_stack:
                _parent = self.parent_node_stack[-1]
                _parent = _parent.children if isinstance(_parent, VForNodeAst) else _parent
            else:
                _parent = self.widgets

            for idx in (idxs[:-1] if for_processed else idxs):
                _parent = _parent[idx]

            _for_scopes = VForScopes(idxs=idxs, vars=vars) if idxs and vars else None
            _node = NodeAst(
                tag=tag, attrs=attrs, parent=_parent, children=[], plain=False, v_for=v_for,
                v_for_scopes=_for_scopes, for_processed=for_processed,
                type=node_type
            )
            return _node

        raw_tag = self._get_raw_tag(case_insensitive_tag)
        tag = self._to_camel_case_tag(raw_tag)
        node_type = NodeAstType.WIDGET if self.vm.component(tag) else NodeAstType.HTML
        self._tag = tag
        attrs = dict(attrs)
        self._transformer_node_attrs(attrs)

        v_for_expr = attrs.pop(VueCompAst.V_FOR, None)
        v_for_ast = VForAst.parse(v_for_expr)
        for_processed = False
        if v_for_ast:
            for_processed = True
            self.v_for_stack.append(v_for_ast)

        if self.v_for_stack:
            nodes = v_for_stack_to_iter(
                self.v_for_stack,
                functools.partial(_gen_node_ast, tag, attrs, for_processed),
                self.vm._data
            )
            node = VForNodeAst(tag, attrs, children=nodes, for_processed=for_processed,
                               type=node_type)
        else:
            node = _gen_node_ast(tag, attrs, for_processed)
        self.parent_node_stack.append(node)

    def _transformer_node_attrs(self, attrs: dict) -> None:
        prev_v_if_expr = self.v_if_stack.pop() if self.v_if_stack else ''

        _v_if_expr = attrs.get(VueCompAst.V_IF)
        if _v_if_expr:
            return

        v_else_if_expr = attrs.pop(VueCompAst.V_ELSE_IF, '')
        if v_else_if_expr:
            if not prev_v_if_expr:
                _err_msg = f"v-else-if={v_else_if_expr} error, there is no corresponding v-if"
                raise CompilerSyntaxError(_err_msg)

            v_else_if_expr = f"(not ({prev_v_if_expr})) and ({v_else_if_expr})"
            attrs[VueCompAst.V_IF] = v_else_if_expr
            return

        v_else_expr = attrs.pop(VueCompAst.V_ELSE, Nil)
        if v_else_expr is not Nil:
            if not prev_v_if_expr:
                _err_msg = f"v-else error, there is no corresponding v-if"
                raise CompilerSyntaxError(_err_msg)

            v_else_expr = f"not ({prev_v_if_expr})"
            attrs[VueCompAst.V_IF] = v_else_expr
            return

    def handle_data(self, data: str) -> None:
        if not self.parent_node_stack:
            return

        if not data.strip():
            return

        tag = self._tag

        def _gen_text(node: NodeAst, should_render: bool):
            if isinstance(node, VForNodeAst):
                for _node in node.children_flat:
                    _gen_text(_node, should_render)
                return

            ns = VueCompNamespace(self.vm.to_ns(), self.vm.to_ns(),
                                  node.v_for_scopes and node.v_for_scopes.to_ns())
            i = -1
            if node.v_for_scopes:
                i = node.v_for_scopes.idxs[-1]

            def __handle_data_gen_html(_ns=ns, _i=i, _should_render=should_render):
                if _should_render:
                    logger.debug("for_stmt_gen_html index=%s <%s> tmpl=`%s`", _i, tag, data)
                    return VueHtmlTemplateRender.render(data, _ns, _i)
                else:
                    return data

            if node.type == NodeAstType.HTML:
                node.add_child(__handle_data_gen_html)
            else:
                node.add_child(VueHtmlCompCodeGen.gen_from_fn(__handle_data_gen_html))

        should_render = VueHtmlTemplateRender.should_render(data)
        parent = self.parent_node_stack[-1]
        _gen_text(parent, should_render)

    def handle_endtag(self, tag):
        def _gen_element(_node: NodeAst):
            if isinstance(_node, VForNodeAst):
                for _node in _node.children_flat:
                    _gen_element(_node)
                return

            widget = self._gen_widget(_node, _node.v_for_scopes)
            # not v-for
            if not _node.v_for_scopes:
                widget = VueHtmlCompCodeGen.gen_from_fn(widget) if callable(widget) else widget
                _node.parent.add_child(widget)
            # curr v-for end
            elif _node.for_processed:
                widget = VueHtmlCompCodeGen.gen_from_fn(widget) if callable(widget) else widget
                _node.parent.add_child(widget)

                # todo 加到v-for的解析处
                ns = VueCompNamespace(self.vm.to_ns(), self.vm.to_ns())
                attr_chain = _node.v_for.iter

                def __track_list_change():
                    # track list replacements
                    obj_iter = ns.getattr(attr_chain)
                    # track changes in the list itself, such as append, pop...
                    return id(obj_iter), [id(item) for item in obj_iter]

                @watch(__track_list_change)
                def __track_list_change_rerender(new, old, on_cleanup):
                    self.vm.render()
            # v-for in process
            else:
                _node.parent.add_child(widget)

        node = self.parent_node_stack.pop()
        _gen_element(node)
        if node.for_processed:
            self.v_for_stack.pop()

        v_if_expr = node.attrs.get(VueCompAst.V_IF)
        if v_if_expr:
            self.v_if_stack.append(v_if_expr)

    def compile(self, html):
        self.html_lines = [line for line in html.splitlines()]
        self.feed(html)
        if len(self.widgets.children) == 1:
            return self.widgets.children[0]
        return widgets.VBox(self.widgets.children)

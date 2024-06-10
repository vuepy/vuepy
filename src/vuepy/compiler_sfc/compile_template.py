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

    # def _gen_ast_node(self, tag, attrs, for_scope=None):
    #     if self.vm.component(tag):
    #         # node = self._component_tag_enter(tag, attrs, for_scope)
    #         node = {"tag": tag, 'attrs': attrs, 'body': []}
    #     else:
    #         # node = self._html_tag_enter(tag, attrs)
    #         node = {'tag': tag, 'attrs': attrs, 'body': [], 'type': 'html'}
    #     return node

    def _gen_widget(self, node: NodeAst, for_scope: VForScopes = None):
        local_vars = for_scope and for_scope.to_ns()
        ns = VueCompNamespace(self.vm.to_ns(), self.vm.to_ns(), local_vars)
        if self.vm.component(node.tag):
            widget = VueCompCodeGen.gen(node, self.vm, ns, self.app)
        else:
            widget = VueHtmlCompCodeGen.gen(node, ns)

        return widget

    # def _component_tag_enter(self, tag, attrs, for_scope=None):
    #     return {"tag": tag, 'attrs': attrs, 'body': []}
    #
    # def _component_tag_exit(self, node: NodeAst, for_scope: ForScope | VForScopes =None):
    #     comp_ast = VueCompAst.parse(node.tag, node.attrs)
    #     local = for_scope.to_ns() if for_scope else None
    #     ns = VueCompNamespace(self.vm._data, self.vm.to_ns(), local)
    #     widget = VueCompCodeGen.gen(comp_ast, node.children, self.vm, ns, self.app)
    #     return widget
    #
    # def _html_tag_enter(self, tag, attrs):
    #     ast_node = {'type': 'html', 'tag': tag, 'attrs': attrs, 'body': []}
    #     return ast_node
    #
    # def _html_tag_exit(self, node, for_scope: ForScope = None):
    #     # TODO 重构
    #     comp_ast = VueCompAst.parse(node['tag'], node['attrs'])
    #     local = for_scope.to_ns() if for_scope else None
    #     ns = VueCompNamespace(self.vm._data, self.vm.to_ns(), local)
    #     # v-if
    #     widget = widgets.HTML("")
    #     if comp_ast.v_if:
    #         watcher = WatcherForRerender(self.vm, f'v_if {comp_ast.v_if}')
    #         with ActivateEffect(watcher):
    #             if not comp_ast.v_if.eval(ns):
    #                 return widget
    #
    #     tag = node['tag']
    #     attr = ' '.join([f"{k}='{v}'" for k, v in node['attrs'].items()])
    #     html_temp = f"<{tag} {attr}>{{inner_html}}</{tag}>"
    #
    #     def gen_html(inner_html):
    #         return html_temp.format(inner_html=inner_html)
    #
    #     def handle_value_change_vm_to_view(widget, attr):
    #         def warp(val, old_val):
    #             if val == old_val:
    #                 return
    #             setattr(widget, attr, gen_html(val))
    #         return warp
    #
    #     # v-html
    #     if comp_ast.v_html:
    #         attr_chain = comp_ast.v_html
    #         update_vm_to_view = handle_value_change_vm_to_view(widget, 'value')
    #         watcher = WatcherForAttrUpdate(ns, lambda: ns.getattr(attr_chain), update_vm_to_view)
    #         with ActivateEffect(watcher):
    #             _value = ns.getattr(attr_chain)
    #         update_vm_to_view(_value, None)
    #     else:
    #         body = [
    #             child.value if isinstance(child, widgets.HTML) else child
    #             for child in node['body']
    #         ]
    #         widget.value = gen_html(' '.join(body))
    #
    #     return widget

    # def _html_tag_exit(self, node: NodeAst, for_scope: ForScope | VForScopes = None):
    #     # TODO 重构 移到gen里
    #     # comp_ast = VueCompAst.parse(node['tag'], node['attrs'])
    #     comp_ast = VueCompAst.parse(node.tag, node.attrs)
    #     local = for_scope.to_ns() if for_scope else None
    #     ns = VueCompNamespace(self.vm._data, self.vm.to_ns(), local)
    #
    #     def __html_tag_exit_gen_outerhtml(inner_html):
    #         tag = node.tag
    #         attr = ' '.join([f"{k}='{v}'" for k, v in node.attrs.items()])
    #         html_temp = f"<{tag} {attr}>{{inner_html}}</{tag}>"
    #         return html_temp.format(inner_html=inner_html)
    #
    #     # @computed
    #     def __html_tag_exit_gen_html():
    #         # v-if or v-show
    #         if_cond = comp_ast.v_if or comp_ast.v_show
    #         if if_cond and not if_cond.eval(ns):
    #             return ''
    #
    #         # v-html
    #         if comp_ast.v_html:
    #             attr_chain = comp_ast.v_html
    #             return ns.getattr(attr_chain)
    #
    #         # innerHtml
    #         inner = []
    #         # for child in node['body']:
    #         for child in node.children:
    #             if callable(child):
    #                 inner.append(child())
    #             elif isinstance(child, widgets.HTML):
    #                 inner.append(child.value)
    #             else:
    #                 inner.append(child)
    #
    #         return __html_tag_exit_gen_outerhtml(' '.join(inner))
    #
    #     return __html_tag_exit_gen_html

    # def _for_stmt_enter(self, for_stmt: VForStatement, tag, attrs, is_body):
    #     body = []
    #     _iter = VueCompNamespace.get_by_attr_chain(self.vm._data, for_stmt.iter)
    #     for i, target in enumerate(_iter):
    #         for_scope = (i, target)
    #         body.append(self._gen_ast_node(tag, attrs, for_scope))
    #
    #     if is_body:
    #         ast_node = {
    #             "tag": 'v_for',
    #             'v_for_body': for_stmt,
    #             "body": body,
    #         }
    #     else:
    #         ast_node = {
    #             "tag": 'v_for',
    #             'v_for': for_stmt,
    #             "body": body,
    #         }
    #     return ast_node
    #
    # def _for_stmt_exit(self, v_for_ast_node, is_body=False):
    #     _widgets = []
    #     v_for_stmt = self.v_for_stack[-1]
    #     _iter = VueCompNamespace.get_by_attr_chain(self.vm._data, v_for_stmt.iter)
    #     for i, target in enumerate(_iter):
    #         for_scope = ForScope(i, v_for_stmt, self.vm)
    #         node = v_for_ast_node['body'][i]
    #         widget = self._gen_widget(node, for_scope)
    #         if widget:
    #             _widgets.append(widget)
    #
    #     # todo 加到v-for的解析处
    #     if not is_body:
    #         ns = VueCompNamespace(self.vm._data, self.vm.to_ns())
    #         attr_chain = v_for_stmt.iter
    #
    #         def __track_list_change():
    #             # track list replacements
    #             obj_iter = ns.getattr(attr_chain)
    #             # track changes in the list itself, such as append, pop...
    #             return id(obj_iter), [id(item) for item in obj_iter]
    #
    #         @watch(__track_list_change)
    #         def __track_list_change_rerender(new, old, on_cleanup):
    #             self.vm.render()
    #
    #         # _attrs = attr_chain.split('.', 1)
    #         # if len(_attrs) > 1:
    #         #     base_attr, sub_attr_chain = _attrs
    #         #     obj = ns.getattr(base_attr)
    #         #     watcher = WatcherForRerender(self.vm, f"for_stme {v_for_stmt.iter} replace")
    #         #     with ActivateEffect(watcher):
    #         #         VueCompNamespace.get_by_attr_chain(obj, sub_attr_chain)
    #         #
    #         # # 处理list本身的变化，append、pop等操作
    #         # # watcher = WatcherForRerender(self.vm, f"{v_for_stmt.iter} modified")
    #         # # with ActivateEffect(watcher):
    #         # obj_iter = ns.getattr(v_for_stmt.iter)
    #         # if isinstance(obj_iter, Reactive):
    #         #     obj_iter.add_dep(WatcherForRerender(self.vm, f"{v_for_stmt.iter} modified"))
    #
    #     return _widgets

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

        # v_for_stmt = attrs.pop(VueCompAst.V_FOR, None)
        #
        # if v_for_stmt or self.v_for_stack:
        #     is_header = bool(v_for_stmt)
        #     if is_header:
        #         v_for = VForStatement.parse(v_for_stmt)
        #         self.v_for_stack.append(v_for)
        #     v_for = self.v_for_stack[-1]
        #     node = self._for_stmt_enter(v_for, tag, attrs, not is_header)
        # else:
        #     node = self._gen_ast_node(tag, attrs)
        # self.parent_node_stack.append(node)

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
            # self.v_if_stack.append(v_else_if_expr)
            return

        v_else_expr = attrs.pop(VueCompAst.V_ELSE, Nil)
        if v_else_expr is not Nil:
            if not prev_v_if_expr:
                _err_msg = f"v-else error, there is no corresponding v-if"
                raise CompilerSyntaxError(_err_msg)

            # if_expr = self.v_if_stack.pop()
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

        #
        #
        # if not self.is_in_for_stmt:
        #     if parent.type != NodeType.RAW_HTML:
        #         logger.warning(f"<{tag}> not support innerText.")
        #         return
        #
        #     ns = VueCompNamespace(self.vm._data, self.vm.to_ns())
        #
        #     # result = VueCompHtmlTemplateRender.render(data, self.vm, ns, -1)
        #     # parent['body'].append(result)
        #
        #     def __handle_data_gen_html(_should_render=should_render):
        #         return VueCompHtmlTemplateRender.render(data, self.vm, ns, -1) if _should_render else data
        #
        #     parent.add_child(__handle_data_gen_html)
        #     # parent['body'].append(__handle_data_gen_html)
        #
        # # v-for
        # # TODO node的类型判断可以优化
        # elif parent['body'] and parent['body'][0].get('type') == 'html':
        #     v_for_stmt = self.v_for_stack[-1]
        #     _iter = VueCompNamespace.get_by_attr_chain(self.vm._data, v_for_stmt.iter)
        #     for i, _ in enumerate(_iter):
        #         for_scope = ForScope(i, v_for_stmt, self.vm)
        #         ns = VueCompNamespace(self.vm._data, self.vm.to_ns(), for_scope.to_ns())
        #
        #         def __handle_data_for_stmt_gen_html(_ns=ns, _i=i, _should_render=should_render) -> str:
        #             if _should_render:
        #                 logger.debug("for_stmt_gen_html index=%s <%s> tmpl=`%s`", _i, tag, data)
        #                 return VueCompHtmlTemplateRender.render(data, self.vm, _ns, _i)
        #             else:
        #                 return data
        #
        #         parent['body'][i]['body'].append(__handle_data_for_stmt_gen_html)
        # else:
        #     logger.error(f"miss match `{repr(data)}`")

    # def handle_endtag_bak(self, tag):
    #     node = self.parent_node_stack.pop()
    #     if self.is_in_for_stmt:
    #         is_body = 'v_for' not in node
    #         _widgets = self._for_stmt_exit(node, is_body)
    #         if is_body:
    #             for i, widget in enumerate(_widgets):
    #                 self.parent_node_stack[-1]['body'][i]['body'].append(widget)
    #         else:
    #             for i, _widget in enumerate(_widgets):
    #                 if callable(_widget):
    #                     _widgets[i] = VueHtmlCompRender.gen_from_fn(_widget)
    #             self.parent_node_stack[-1]['body'].extend(_widgets)
    #             self.v_for_stack.pop()
    #     else:
    #         widget = self._gen_widget(node)
    #         if not widget:
    #             return
    #
    #         if callable(widget):
    #             widget = VueHtmlCompRender.gen_from_fn(widget)
    #
    #         if self.parent_node_stack:
    #             self.parent_node_stack[-1]['body'].append(widget)
    #         else:
    #             self.widgets.add_child(widget)

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

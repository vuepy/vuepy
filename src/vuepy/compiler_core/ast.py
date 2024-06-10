from __future__ import annotations

import ast
import dataclasses
import enum
from _ast import Load
from _ast import Name
from _ast import Starred
from _ast import keyword
from dataclasses import field
from typing import Dict
from typing import List
from typing import Tuple

from vuepy.compiler_core.component_expr import VueCompExpr
from vuepy.runtime.core.api_setup_helpers import defineModel


@dataclasses.dataclass
class VForAst:
    iter: str
    target: str
    idx: str = None

    @classmethod
    def parse(cls, exp):
        """
        (i, target) in iter
        :param exp:
        :return:
        """
        if not exp:
            return None

        try:
            i_target, iters = [i.strip() for i in exp.split(' in ')]
            i_target = [i.strip() for i in i_target.strip('()').split(',')]
            if len(i_target) == 1:
                i, target = None, i_target[0]
            else:
                i, target = i_target[0], i_target[1]
        except Exception as err:
            msg = f"parse v-for='{exp}' failed, {err}"
            raise ValueError(msg)

        return cls(iter=iters, target=target.strip(), idx=i)


@dataclasses.dataclass
class VForScopes:
    idxs: Tuple[int]
    vars: dict

    def to_ns(self):
        return self.vars


class NodeAstType(enum.Enum):
    HTML = 'html'
    WIDGET = 'widget'


@dataclasses.dataclass
class NodeAst:
    tag: str
    attrs: dict = field(default_factory=dict)
    parent: "NodeAst" = None
    children: List["NodeAst"] = field(default_factory=list)
    plain: bool = False
    v_for: VForAst = None
    v_for_scopes: VForScopes = None
    for_processed: bool = False
    type: NodeAstType = NodeAstType.WIDGET

    def add_child(self, child):
        self.children.append(child)


@dataclasses.dataclass
class VForNodeAst(NodeAst):

    @property
    def children_flat(self) -> List["NodeAst"]:
        ret = []

        def _travel(children):
            if not isinstance(children, list):
                ret.append(children)
                return

            for child in children:
                _travel(child)

        _travel(self.children)
        return ret


class VueCompAst:
    V_IF = 'v-if'
    V_ELSE_IF = 'v-else-if'
    V_ELSE = 'v-else'
    V_FOR = 'v-for'
    V_SHOW = 'v-show'
    V_SLOT = 'v-slot:'
    V_SLOT_ABBR = '#'
    V_JS_LINK = 'v-js-link'
    V_REF = 'ref'
    V_MODEL = 'v-model:'
    V_MODEL_DEFAULT = 'v-model'
    V_HTML = 'v-html'
    V_ON = 'v-on:'
    V_ON_ABBR = '@'
    V_BIND = 'v-bind:'
    V_BIND_ABBR = ':'

    LAYOUT_ATTRS = {'width', 'height', 'padding', 'border'}

    # todo 和h函数的参数保持一致
    def __init__(self, tag):
        self.tag = tag
        # todo rename to attrs
        self.kwargs = {}
        self.layout = {}

        self.v_if: VueCompExpr = None
        self.v_else_if: VueCompExpr = None
        self.v_else = False
        self.v_show: VueCompExpr = None
        self.v_binds: Dict[str, VueCompExpr] = {}
        self.v_model: List[(str, str)] = []
        self.v_html = None
        self.v_on: Dict[str, VueCompExpr] = {}
        self.v_slot = None
        self.v_ref = None

    @classmethod
    def is_v_if(cls, attr):
        return attr == cls.V_IF

    @classmethod
    def is_v_else_if(cls, attr):
        return attr == cls.V_ELSE_IF

    @classmethod
    def is_v_else(cls, attr):
        return attr == cls.V_ELSE

    @classmethod
    def is_v_show(cls, attr):
        return attr == cls.V_SHOW

    @classmethod
    def is_v_slot(cls, attr):
        return attr.startswith(cls.V_SLOT)

    @classmethod
    def is_v_slot_addr(cls, attr):
        return attr.startswith(cls.V_SLOT_ABBR)

    @classmethod
    def is_v_ref(cls, attr):
        return attr == cls.V_REF

    @classmethod
    def is_v_model_default(cls, attr):
        return attr == cls.V_MODEL_DEFAULT

    @classmethod
    def is_v_model(cls, attr):
        return attr.startswith(cls.V_MODEL)

    @classmethod
    def is_v_html(cls, attr):
        return attr == cls.V_HTML

    @classmethod
    def is_v_on(cls, attr):
        return attr.startswith(cls.V_ON)

    @classmethod
    def is_v_on_abbr(cls, attr):
        return attr.startswith(cls.V_ON_ABBR)

    @classmethod
    def is_v_bind(cls, attr):
        return attr.startswith(cls.V_BIND)

    @classmethod
    def is_v_bind_abbr(cls, attr):
        return attr.startswith(cls.V_BIND_ABBR)

    @classmethod
    def is_layout(cls, attr):
        return attr in cls.LAYOUT_ATTRS

    @classmethod
    def transform(cls, tag, attr_dict):
        comp = cls(tag)
        for attr, value in attr_dict.items():
            if cls.is_v_if(attr):
                comp.v_if = VueCompExpr.parse(value)

            elif cls.is_v_else_if(attr):
                comp.v_else_if = VueCompExpr.parse(value)

            elif cls.is_v_else(attr):
                comp.v_else = True

            elif cls.is_v_show(attr):
                comp.v_show = VueCompExpr.parse(value)

            elif cls.is_v_bind(attr):
                attr = attr.split(cls.V_BIND, 1)[1]
                comp.v_binds[attr] = VueCompExpr.parse(value)

            elif cls.is_v_bind_abbr(attr):
                attr = attr.split(cls.V_BIND_ABBR, 1)[1]
                comp.v_binds[attr] = VueCompExpr.parse(value)

            elif cls.is_v_model_default(attr):
                comp.v_model.append((defineModel.DEFAULT_KEY, value))

            elif cls.is_v_model(attr):
                _define_model_key = attr.split(cls.V_MODEL, 1)[1]
                comp.v_model.append((_define_model_key, value))

            elif cls.is_v_html(attr):
                comp.v_html = value

            elif cls.is_v_on(attr) or cls.is_v_on_abbr(attr):
                _prefix = cls.V_ON if cls.is_v_on(attr) else cls.V_ON_ABBR
                event = attr.split(_prefix, 1)[1]
                func_ast = VueCompExpr.parse(value)
                if isinstance(func_ast.exp_ast.body, (ast.Name, ast.Attribute)):
                    exp_ast = ast.Expression(
                        ast.Call(
                            func=func_ast.exp_ast.body,
                            args=[Starred(value=Name(id='__vp_args', ctx=Load()), ctx=Load())],
                            keywords=[keyword(value=Name(id='__vp_kwargs', ctx=Load()))],
                        )
                    )
                    ast.fix_missing_locations(exp_ast)
                    func_ast.exp_ast = exp_ast

                comp.v_on[event] = func_ast

            elif tag == 'template' and cls.is_v_slot(attr):
                comp.v_slot = attr.split(cls.V_SLOT, 1)[1]

            elif tag == 'template' and cls.is_v_slot_addr(attr):
                comp.v_slot = attr.split(cls.V_SLOT_ABBR, 1)[1]

            elif cls.is_v_ref(attr):
                comp.v_ref = value

            elif cls.is_layout(attr):
                comp.layout[attr] = value

            else:
                comp.kwargs[attr] = value

        if comp.layout:
            comp.kwargs['layout'] = comp.layout

        return comp

#!coding: utf-8
import pathlib

import ipywidgets as widgets
import markdown

from vuepy import Vue
from vuepy import VueComponent
from vuepy import VuePlugin
from vuepy.utils.factory import FactoryMeta


class IPywidgets(VuePlugin, metaclass=FactoryMeta):
    @classmethod
    def install(cls, vm: Vue, options: dict):
        components = cls.get_all_registry()
        for name, component in components.items():
            vm.component(name, component)


class IPywidgetsComponent(VueComponent):
    @classmethod
    def name(cls):
        # todo
        # return f'Ipw{cls.__name__}'
        return cls.__name__.lower()


@IPywidgets.register()
class AppLayout(IPywidgetsComponent):
    def render(self, ctx, props, setup_returned):
        slots = ctx.get('slots', {})
        attrs = ctx.get('attrs', {})
        return widgets.AppLayout(**slots, **props, **attrs)


@IPywidgets.register()
class VBox(IPywidgetsComponent):
    def render(self, ctx, props, setup_returned):
        slots = ctx.get('slots', {})
        attrs = ctx.get('attrs', {})
        return widgets.VBox(children=slots.get('default', []), **props, **attrs)


@IPywidgets.register()
class Template(VBox):
    pass


@IPywidgets.register()
class Box(IPywidgetsComponent):
    def render(self, ctx, props, setup_returned):
        slots = ctx.get('slots', {})
        attrs = ctx.get('attrs', {})
        return widgets.VBox(children=slots.get('default', []), **props, **attrs)


@IPywidgets.register()
class HBox(IPywidgetsComponent):
    def render(self, ctx, props, setup_returned):
        slots = ctx.get('slots', {})
        attrs = ctx.get('attrs', {})
        return widgets.HBox(children=slots.get('default', []), **props, **attrs)


@IPywidgets.register()
class AccordionItem(IPywidgetsComponent):
    def render(self, ctx, props, setup_returned):
        slots = ctx.get('slots', {})
        attrs = ctx.get('attrs', {})
        title = attrs.pop('title', '-')
        widget = widgets.VBox(children=slots.get('default', []), **props, **attrs)
        widget.title = title
        return widget


@IPywidgets.register()
class Accordion(IPywidgetsComponent):
    v_model_default = 'selected_index'

    def render(self, ctx, props, setup_returned):
        slots = ctx.get('slots', {})
        attrs = ctx.get('attrs', {})
        children = slots.get('default', [])
        titles = [child.title for child in children]
        return widgets.Accordion(children=children, titles=titles, **props, **attrs)


@IPywidgets.register()
class Button(IPywidgetsComponent):
    v_model_default = 'description'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.Button(**props, **attrs)


@IPywidgets.register()
class Checkbox(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.Checkbox(**props, **attrs)


@IPywidgets.register()
class ColorsInput(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.ColorsInput(**props, **attrs)


@IPywidgets.register()
class Combobox(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.Combobox(**props, **attrs)


@IPywidgets.register()
class Controller(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.Controller(**props, **attrs)


@IPywidgets.register()
class Dropdown(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.Dropdown(**props, **attrs)


@IPywidgets.register()
class FileUpload(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.FileUpload(**props, **attrs)


@IPywidgets.register()
class FloatsInput(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.FloatsInput(**props, **attrs)


@IPywidgets.register()
class FloatSlider(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.FloatSlider(**props, **attrs)


@IPywidgets.register()
class HTMLMath(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.HTMLMath(**props, **attrs)


@IPywidgets.register()
class ColorsInput(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.ColorsInput(**props, **attrs)


@IPywidgets.register()
class Image(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.Image(**props, **attrs)


@IPywidgets.register()
class InputNumber(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.IntText(**props, **attrs)


@IPywidgets.register()
class IntsInput(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.IntsInput(**props, **attrs)


@IPywidgets.register()
class Label(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.Label(**props, **attrs)


class _MarkdownViewer(widgets.HTML):
    codehilite = pathlib.Path(__file__).parent / 'md_codehilite.css'
    with open(codehilite) as f:
        css_style = ''.join(f.read())

    extra = [
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.tables',
        # 'markdown.extensions.nl2br',
    ]

    def __init__(self, value='', **kwargs):
        super().__init__(self.render(value), **kwargs)

    def render(self, md):
        html = markdown.markdown(md, extensions=self.extra)
        return f"<style>{self.css_style}</style>" + html

    def __setattr__(self, key, value):
        if key == 'value':
            value = self.render(value)

        super().__setattr__(key, value)


@IPywidgets.register()
class MarkdownViewer(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return _MarkdownViewer(**props, **attrs)


@IPywidgets.register()
class Password(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.Password(**props, **attrs)


@IPywidgets.register()
class Play(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.Play(**props, **attrs)


@IPywidgets.register()
class Progress(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.FloatProgress(**props, **attrs)


@IPywidgets.register()
class RadioButtons(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.RadioButtons(**props, **attrs)


@IPywidgets.register()
class Select(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.Select(**props, **attrs)


@IPywidgets.register()
class Slider(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        # todo
        attrs = ctx.get('attrs', {})
        return widgets.FloatSlider(**props, **attrs)


@IPywidgets.register()
class Stack(IPywidgetsComponent):
    v_model_default = 'selected_index'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.Stack(**props, **attrs)


@IPywidgets.register()
class TabPane(IPywidgetsComponent):
    def render(self, ctx, props, setup_returned):
        slots = ctx.get('slots', {})
        attrs = ctx.get('attrs', {})
        title = attrs.pop('title', '-')
        widget = widgets.VBox(children=slots.get('default', []), **props, **attrs)
        widget.title = title
        return widget


@IPywidgets.register()
class Tabs(IPywidgetsComponent):
    v_model_default = 'selected_index'

    def render(self, ctx, props, setup_returned):
        slots = ctx.get('slots', {})
        attrs = ctx.get('attrs', {})
        children = slots.get('default', [])
        titles = [child.title for child in children]
        return widgets.Tab(children=children, titles=titles, **props, **attrs)


@IPywidgets.register()
class TagsInput(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.TagsInput(**props, **attrs)


@IPywidgets.register()
class Text(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.Text(**props, **attrs)


@IPywidgets.register()
class Textarea(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.Textarea(**props, **attrs)


@IPywidgets.register()
class ToggleButton(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.ToggleButton(**props, **attrs)


@IPywidgets.register()
class ToggleButtons(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.ToggleButtons(**props, **attrs)


@IPywidgets.register()
class Valid(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.Valid(**props, **attrs)

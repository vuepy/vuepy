<template>
  <Container>
    <Button label="btn"></Button>
  </Container>
</template>

<script lang="py">
import anywidget
import traitlets
import ipywidgets as widgets

from vuepy import ref, VueComponent

# 使用anywidget开发Widget
class ContainerWidget(anywidget.AnyWidget):
    _esm = """
    async function unpack_models(model_ids, manager) {
      return Promise.all(
        model_ids.map(id => manager.get_model(id.slice("IPY_MODEL_".length)))
      );
    }
    export async function render(view) {
      let model = view.model;
      let el = view.el;
      let div = document.createElement("div");
      div.innerHTML = `<p>hello world</p>`;

      // 将子组件添加到父组件中
      let model_ids = model.get("children"); /* ["IPY_MODEL_{model_id>}", ...] */
      let children_models = await unpack_models(model_ids, model.widget_manager);
      for (let model of children_models) {
        let child_view = await model.widget_manager.create_view(model);
        div.appendChild(child_view.el);
      }

      el.appendChild(div);
    }
    """
    # slot
    children = traitlets.List(trait=traitlets.Instance(widgets.DOMWidget)) \
        .tag(sync=True, **widgets.widget_serialization)

# 集成ContainerWidget
class Container(VueComponent):
    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        slots = ctx.get('slots', {})
        # 从slot中取出子组件并赋值给children
        return ContainerWidget(children=slots.get('default', []), **props, **attrs)

</script>

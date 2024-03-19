async function unpack_models(model_ids, manager) {
  return Promise.all(
    model_ids.map(id => manager.get_model(id.slice("IPY_MODEL_".length)))
  );
}


export async function render(view) {
  let model = view.model;
  let el = view.el;

  let shouldShowDialog = model.get('value');
  if (!shouldShowDialog) {
    el.style.display = 'None';
  }

  const dialog_container = document.createElement('div');

  let model_ids = model.get("children"); // ["IPY_MODEL_<model_id>", ...]
  let children_models = await unpack_models(model_ids, model.widget_manager);
  for (let model of children_models) {
    let child_view = await model.widget_manager.create_view(model);
    dialog_container.appendChild(child_view.el);
  }
  model.on("change:value", () => {
      el.style.display = shouldShowDialog ? 'block' : 'None';
  })

  el.appendChild(dialog_container);
  el.className += " ipywui-dialog";
}

async function unpack_models(model_ids, manager) {
  return Promise.all(
    model_ids.map(id => manager.get_model(id.slice("IPY_MODEL_".length)))
  );
}

async function copyToClipboardAsync(textToCopy) {
  if (navigator.clipboard && window.isSecureContext) {
    return navigator.clipboard.writeText(textToCopy);
  }

  let textArea = document.createElement("textarea");
  textArea.value = textToCopy;
  let styles = {
    display: 'none',
    position: 'absolute',
    opacity: 0,
    top: '-999999px',
    left: '-999999px',
  }
  Object.assign(textArea.style, styles);

  document.body.appendChild(textArea);
  textArea.focus();
  textArea.select();
  return new Promise((res, rej) => {
    document.execCommand('copy') ? res() : rej();
    textArea.remove();
  });
}

export async function render(view) {
  let model = view.model;
  let el = view.el;

  const tag = model.get('tag');
  const copyWrap = document.createElement(tag);

  let model_ids = model.get("children"); // ["IPY_MODEL_<model_id>", ...]
  let children_models = await unpack_models(model_ids, model.widget_manager);
  for (let model of children_models) {
    let child_view = await model.widget_manager.create_view(model);
    copyWrap.appendChild(child_view.el);
  }

  copyWrap.addEventListener("click", async () => {
    try {
      await copyToClipboardAsync(model.get("copy"));
      model.set("value", model.get("value")+1);
      model.save_changes();
    } catch (e) {
      console.error(e)
    }
  });

  el.appendChild(copyWrap);
}

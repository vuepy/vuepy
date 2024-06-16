async function unpack_models(model_ids, manager) {
  return Promise.all(
    model_ids.map(id => manager.get_model(id.slice("IPY_MODEL_".length)))
  );
}


export async function render(view) {
  let model = view.model;

  let shouldShowDialog = () => model.get('value');
  const modalRoot = view.el;
  const modalDialogContainer = document.createElement('div');
  const modalDialog = document.createElement('div');
  modalRoot.className += ' wui-modal-root';
  modalRoot.setAttribute('data-state', shouldShowDialog() ? 'open' : 'close');
  modalDialogContainer.className += ' wui-modal-dialog-container';
  modalDialog.className += ' wui-modal-dialog';
  const modalDialogWidth = model.get("width", '50%');
  if (modalDialogWidth) {
    modalDialog.style.width = modalDialogWidth;
  }
  modalRoot.appendChild(modalDialogContainer);
  modalDialogContainer.appendChild(modalDialog);

  const modalTitle = document.createElement('div');
  modalTitle.className += ' wui-modal-header';
  modalTitle.innerText = model.get('title');
  const modalBody = document.createElement('div');
  modalBody.className += ' wui-modal-body';
  const modalFooter = document.createElement('div');
  modalFooter.className += ' wui-modal-footer';
  modalDialog.appendChild(modalTitle);
  modalDialog.appendChild(modalBody);
  modalDialog.appendChild(modalFooter);

  let model_ids = model.get("body");  /* ["IPY_MODEL_{model_id>}", ...] */
  let body_models = await unpack_models(model_ids, model.widget_manager);
  for (let model of body_models) {
    let child_view = await model.widget_manager.create_view(model);
    modalBody.appendChild(child_view.el);
  }
  model_ids = model.get("footer");  /* ["IPY_MODEL_{model_id>}", ...] */
  let footer_models = await unpack_models(model_ids, model.widget_manager);
  for (let model of footer_models) {
    let child_view = await model.widget_manager.create_view(model);
    modalFooter.appendChild(child_view.el);
  }
  const emit = (evt, payload) => {
    model.set("event", {"event": evt, "payload": payload});
    model.save_changes();
  }
  const openDialog = () => {
    modalRoot.setAttribute('data-state', 'open');
    emit("open");
  }
  const closeDialog = () => {
    modalRoot.setAttribute('data-state', 'close');
    emit("close");
  }
  modalDialogContainer.addEventListener('click', () => {
    console.info('click')
    model.set("value", false);
    model.save_changes()
  })
  modalDialog.addEventListener('click', (ev) => {
    ev.stopPropagation();
  })
  model.on("change:value", () => {
    console.info('change value')
    shouldShowDialog() ? openDialog() : closeDialog();
  })
}

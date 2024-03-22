function closeMsg(msgDom) {
  if (!msgDom) {
    return;
  }
  msgDom.setAttribute('data-state', 'exiting');
  msgDom.remove();
}

function createMsg(options) {
  const {message, msg_id, type = 'info', show_close = false} = options;
  const msgDom = document.createElement('div');
  msgDom.className += ` wui-message--${type} wui-message`;
  msgDom.setAttribute('data-state', 'entered');
  msgDom.setAttribute('id', msg_id);
  const msgContent = document.createElement('p');
  msgContent.className += ` wui-message--${type} wui-message__content`;
  msgContent.innerText = message;
  msgDom.appendChild(msgContent);
  if (show_close) {
    const closeBtn = document.createElement('i');
    closeBtn.className += 'wui-message__closeBtn';
    closeBtn.innerText = 'x';
    closeBtn.addEventListener('click', (ev) => {
      closeMsg(msgDom);
    })
    msgDom.appendChild(closeBtn);
  }
  return msgDom;
}

export async function render(view) {
  let model = view.model;
  const msgRoot = view.el;
  msgRoot.className += ' wui-message-root'

  const msgContainer = document.createElement('div');
  msgContainer.className += ' wui-message-container';
  msgRoot.appendChild(msgContainer)

  model.on("change:message_options", () => {
    const options = model.get("message_options");
    const msg = createMsg(options);
    msgContainer.appendChild(msg);
    const {duration = 3000} = options;
    if (duration > 0) {
      setTimeout(() => {
        closeMsg(msg)
      }, duration);
    }
  })

  model.on("change:close_msg_id", () => {
    const msg_id = model.get("close_msg_id");
    const msgDom = document.getElementById(msg_id);
    closeMsg(msgDom);
  })
}

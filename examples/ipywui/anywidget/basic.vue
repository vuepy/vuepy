<template>
  <p>count: {{ count.value }}</p>
  <Counter v-model="count.value" @btn2_click=reset></Counter>
</template>

<script lang="py">
import anywidget
import traitlets

from vuepy import ref, VueComponent, defineEmits

# 使用anywidget开发Widget
class CounterWidget(anywidget.AnyWidget):
    _esm = """
    function render({ model, el }) {
      let count = () => model.get("value");
      // btn1为双向绑定的方式
      let btn1 = document.createElement("button");
      btn1.classList.add("counter-button");
      btn1.innerHTML = `btn1: count is ${count()}`;
      // btn1接收click事件时更新value值
      btn1.addEventListener("click", () => {
        model.set("value", count() + 1);
        model.save_changes();
      });
      // 接收value值的变化，并更新btn1的值
      model.on("change:value", () => {
        btn1.innerHTML = `btn1: count is ${count()}`;
      });
      el.appendChild(btn1);

      // btn2为事件通知方式
      let btn2 = document.createElement("button");
      btn2.classList.add("counter-button");
      btn2.innerHTML = `btn2`;
      let keep_change = 0;
      // btn2接收btn2_click事件并更新event的值
      btn2.addEventListener("click", () => {
        const btn2_event = "btn2_click"
        keep_change += 1; // 每次点击更新值以保证触发event值的更新
        model.set("event", {"event": btn2_event, "payload": keep_change});
        model.save_changes();
      });
      el.appendChild(btn2);
    }
    export default { render };
    """
    _css = """
    .counter-button {
      background-image: linear-gradient(to right, #a1c4fd, #c2e9fb);
      border: 0;
      border-radius: 10px;
      padding: 10px 50px;
      color: white;
    }
    """
    value = traitlets.Int(0).tag(sync=True) # 用于双向同步
    event = traitlets.Dict().tag(sync=True) # 用于事件机制


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 通过观察event值的变化来模拟事件监听机制
        self.observe(self._on_event, ['event'])
        # Counter组件注册监听事件btn2_click
        self.emits = defineEmits(['btn2_click'])

    def on_btn2_click(self, callback, remove=False):
        '''btn2_click事件回调注册函数'''
        self.emits.add_event_listener('btn2_click', callback, remove)

    def _on_event(self, change):
        '''事件分发函数'''
        event = change.get("new", {})
        # 获取event字段来确定事件类型
        ev = event.get("event")
        payload = event.get("payload")
        # 使用emits触发对应事件类型
        self.emits(ev, payload)

# 集成CounterWidget
class Counter(VueComponent):
    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return CounterWidget(**props, **attrs)

count = ref(0)

def reset(payload):
    count.value = 0
    print(payload) # 1, 2, 3
</script>

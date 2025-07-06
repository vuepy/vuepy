# panel-vuepy

Panel-vuepy 是基于 Vue.py 和 Panel 开发的现代化 Python 组件库。它结合了 Vuepy 的响应式开发能力与 Panel 强大的数据探索功能，为开发者提供了一套完整的解决方案：

* 丰富的交互式 UI 组件 - 开箱即用的现代化组件，轻松构建专业级界面
* 深度 PyData 生态集成 - 无缝对接 Python 数据科学生态，实现流畅的数据可视化与分析
* 高效的应用开发框架 - 结合 Vue.py 的响应式特性和 Panel 的灵活后端，快速开发交互式 Web 应用

无论是构建数据仪表盘、开发分析工具，还是创建复杂的业务应用，Panel-vuepy 都能让开发者以前端框架的体验享受 Python 的高效开发流程。 是基于 Vue.py 和 ipyleaflet 开发的响应式地图组件库，在 Jupyter 中实现交互式地图。vleaflet 中的每个对象（包括地图、TileLayers、图层、控件等）都是响应式的：您可以从 Python 或浏览器动态更新属性。

## 安装

```sh
pip install 'vuepy-core[panel]'
```

## 运行 

use 插件方式:

```python{2,7}
from vuepy import create_app, import_sfc
from panel_vuepy import vpanel

App = import_sfc("""
<template>
  <PnButton name='click'/>
</template>
""", raw_content=True)
# or
# App = import_sfc('App.vue')  # 根据 App.vue 实际位置修改
app = create_app(App)
app.use(vpanel)
app.mount()
```

`%vuepy_run` 方式：

```python
from vuepy.utils import magic
from panel_vuepy import vpanel

%vuepy_run app.vue --plugins vpanel
```

`%%vuepy_run` 方式：

```python
from vuepy.utils import magic
from panel_vuepy import vpanel

# -- cell --
%%vuepy_run --plugins vpanel
<template>
  <PnButton name='click'/>
</template>
```

## 部署应用 

将 `ipynb` 文件中的 `app` 声明为`servable`

```python
from vuepy import create_app, import_sfc
from panel_vuepy import vpanel

App = import_sfc("""
<template>
  <PnButton name='click'/>
</template>
""", raw_content=True)
# or
# App = import_sfc('App.vue')  # 根据 App.vue 实际位置修改
app = create_app(App, backend='panel', servable=True)
app.use(vpanel)
app.mount()
```

使用 Panel 运行 ipynb 文件

```bash
panel server app.ipynb
```

打开 http://localhost:5006/app 查看应用

参考：
* [Panel: Serve Apps](https://panel.holoviz.org/tutorials/intermediate/serve.html)


# ChatAreaInput 聊天输入组件

多行文本输入组件，继承自 TextAreaInput，允许通过文本输入框输入任意多行字符串。支持使用 Enter 键或可选的 Ctrl-Enter 键提交消息。

与 TextAreaInput 不同，ChatAreaInput 默认 auto_grow=True 且 max_rows=10，并且 value 在消息实际发送前不会同步到服务器。如果需要访问输入框中当前的文本，请使用 value_input。

底层实现为`panel.chat.ChatAreaInput`，参数基本一致，参考文档：https://panel.holoviz.org/reference/chat/ChatAreaInput.html


## 基本用法

根据 enter_sends 参数的值(默认为 True)，按 Enter 键或 Ctrl-Enter/Cmd-Enter 键提交消息：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnChatAreaInput v-model='output_text.value'
                   placeholder="Type something, and press Enter to clear!" />
  <p> value: {{ output_text.value }}</p>
</template>
<script lang='py'>
from vuepy import ref
            
output_text = ref("")
</script>

```


## 实时更新

要查看当前输入的内容而不等待提交，可以使用 value_input 属性：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnChatAreaInput 
    :enter_sends='False'
    v-model:value_input="output_text.value"
    placeholder="Type something, do not submit it" 
  />
  <p> value: {{ output_text.value }}</p>
</template>
<script lang='py'>
from vuepy import ref

output_text = ref("")
</script>

```


## API

### 属性

| 属性名           | 说明                                                                 | 类型                          | 默认值        |
|----------------|--------------------------------------------------------------------|-----------------------------|--------------|
| disabled_enter | 是否禁用回车键发送消息                                                 | ^[bool]                     | -            |
| enter_sends    | 发送方式（True=回车键发送，False=Ctrl+回车键发送）                        | ^[bool]                     | True         |
| value          | 按下发送键时的消息内容（发送后自动重置为空，需配合watch/bind使用）            | ^[str]                      | ""           |
| value_input    | 实时更新的当前输入内容                                                  | ^[str]                      | ""           |
| enter_pressed  | 回车键/Ctrl+回车键按下事件                                              | ^[bool]                     | -            |
| auto_grow   | 是否自动增加高度以适应内容                                              | ^[bool]                     | True         |
| cols        | 输入框列数                                                           | ^[int]                      | 2            |
| disabled    | 是否禁用编辑                                                         | ^[bool]                     | False        |
| max_length  | 最大输入字符数                                                       | ^[int]                      | 50000        |
| max_rows    | 自动增长时的最大行数                                                  | ^[int]                      | 10           |
| name        | 组件标题                                                            | ^[str]                      | ""           |
| placeholder | 空白时的占位文本                                                     | ^[str]                      | ""           |
| rows        | 输入框行数                                                           | ^[int]                      | 2            |
| resizable   | 是否可调整大小（'width'-宽度, 'height'-高度, 'both'-双向, False-不可调整） | ^[bool\|str]                | 'both'       |

### Events

| 事件名    | 说明           | 类型                                  |
| -------- | ------------- | ------------------------------------- |
| change   | value 值改变时触发   | ^[Callable]`(value: str) -> None`    |





# PanelCallbackHandler LangChain 回调处理器

用于在 Panel 聊天组件中渲染和流式显示 LangChain 对象（如工具、代理和链）的思维链。继承自 LangChain 的 BaseCallbackHandler。

底层实现为`panel.chat.langchain.PanelCallbackHandler`，参数基本一致，参考文档：https://panel.holoviz.org/reference/chat/PanelCallbackHandler.html


## 基本用法

基本的 LangChain 集成示例：



## 流式输出

通过设置 LLM 的 streaming=True 来启用流式输出：


## API

### 属性

| 属性名    | 说明                  | 类型                                 | 默认值  |
| -------- | -------------------- | ----------------------------------- | ------- |
| instance | 目标聊天组件实例       | ^[ChatFeed \| ChatInterface]        | —      |
| user     | 用户名               | ^[str]                              | —      |
| avatar   | 用户头像              | ^[str \| BinaryIO]                  | —      |

### 方法

| 方法名    | 说明                  | 参数                                    |
| -------- | ------------------- | --------------------------------------- |
| -        | -                  | -                                       |




# ChatInterface 聊天界面组件

高级布局组件，提供用户友好的前端界面，用于输入不同类型的消息：文本、图片、PDF等。该组件提供前端方法来：
- 输入(附加)消息到聊天记录
- 重新运行(重新发送)最近的用户输入消息
- 删除消息直到上一个用户输入消息
- 清空聊天记录，删除所有消息

底层实现为`panel.chat.ChatInterface`，参数基本一致，参考文档：https://panel.holoviz.org/reference/chat/ChatInterface.html

![image.png](https://panel.holoviz.org/assets/ChatDesignSpecification.png)

## 基本用法

基本的聊天界面组件：

```vue
<!-- --plugins vpanel --show-code -->
<template>
<PnChatInterface 
  v-model='messages.value'
  :callback="get_response" user='Asker' avatar='?' 
  @change='on_change'
/>
<p> messages: {{ messages.value }}</p>
</template>
<script lang='py'>
from vuepy import ref
import asyncio

messages = ref([])

def on_change(event):
    print('onchange', event.new)

async def get_response(contents, user, instance):
    print(contents, user, instance) # hello Asker ChatInterface...
    await asyncio.sleep(0.5)  # Simulate processing
    return f"Got your message: {contents}"
</script>

```


## 输入组件

可以自定义输入组件，支持多种输入类型：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
<PnChatInterface :callback="get_num">
  <template #inputs>
    <PnIntSlider name='Number Input' :end='10' />
    <PnIntSlider name='Number Input2' :end='10' />
  </template>
</PnChatInterface>
</template>
<script lang='py'>
from vuepy import ref
import panel as pn

def get_num(contents, user):
    return f"You selected: {contents}"
</script>

```


可以添加文件上传等其他输入组件：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
<!-- use widgets prop -->
<PnChatInterface :callback="handle_file" 
  :widgets="[
    pn.widgets.FileInput(name='CSV File', accept='.csv')
  ]"
/>
<!-- use inputs slot -->
<PnChatInterface :callback="handle_file">
  <template #inputs>
    <PnFileInput name='CSV File' accept='.csv' />
  </template>
</PnChatInterface>
</template>
<script lang='py'>
from vuepy import ref
import panel as pn

def handle_file(contents, user):
    if hasattr(contents, 'filename'):
        return f"Received file: {contents.filename}"
    return "Please upload a file"
</script>

```


可以使用 `reset_on_send` 参数控制发送后是否重置输入值：

```vue
<!-- --plugins vpanel --show-code -->
<template>
<PnChatInterface 
  :callback="echo_message"
  :reset_on_send="False"
/>
</template>
<script lang='py'>
from vuepy import ref

def echo_message(contents):
    return f"Echo: {contents}"
</script>

```


## 按钮控制

可以通过 `show_rerun`、`show_undo`、`show_clear` 等参数控制底部按钮的显示：

```vue
<!-- --plugins vpanel --show-code -->
<template>
<PnChatInterface 
  :callback="get_response"
  :show_rerun="False"
  :show_undo="False"
/>
</template>
<script lang='py'>
from vuepy import ref

def get_response(contents):
    return f"Got: {contents}"
</script>

```


使用 `show_button_name=False` 可以隐藏按钮标签，创建更紧凑的界面：

```vue
<!-- --plugins vpanel --show-code -->
<template>
<PnChatInterface 
  :callback="get_response"
  :show_button_name="False"
  :width="400"
/>
</template>
<script lang='py'>
from vuepy import ref

def get_response(contents):
    return f"Got: {contents}"
</script>

```


可以通过 `button_properties` 添加自定义功能按钮：

```vue
<!-- --plugins vpanel --show-code -->
<template>
<PnChatInterface 
  ref='chat_ref'
  :button_properties="{
    # new button
    'help': {
      'icon': 'help','callback': show_notice,
    },
    # override clear button 
    'clear': {
        'icon': 'star', 'callback': run_before, 'post_callback': run_after,
    },
  }"
/>
</template>
<script lang='py'>
from vuepy import ref

chat_ref = ref(None)

def show_notice(instance, event):
    instance.send("This is how you add buttons!", respond=False, user="System")

def run_before(instance, event):
    instance.send(
        "This will be cleared so it won't show after clear!",
        respond=False,
        user="System",
    )

def run_after(instance, event):
    instance.send("This will show after clear!", respond=False, user="System")

</script>

```



## API

### 核心属性
| 属性名               | 说明                                                                 | 类型                          | 默认值          |
|---------------------|--------------------------------------------------------------------|-----------------------------|----------------|
| v-model | 消息列表                     | ^[List[ChatMessage]]     | []    |
| widgets             | 输入控件（单个或列表），未设置时默认使用[TextInput]                     | ^[Widget\|List[Widget]]     | [TextInput]    |
| user                | 聊天界面用户名                                                      | ^[str]                      | ""             |
| avatar              | 用户头像（支持文字/emoji/图片等，未设置时使用用户名首字母）               | ^[str\|bytes\|Image]        | None           |
| reset_on_send       | 发送后是否重置控件值（对TextInput无效）                                | ^[bool]                     | False          |
| auto_send_types     | 支持回车自动发送的控件类型                                             | ^[tuple]                    | [TextInput]    |
| button_properties   | 按钮配置字典（可覆盖默认按钮或创建新按钮）                               | ^[Dict[Dict[str, Any]]]     | {}             |

### 样式属性
| 属性名            | 说明                                                                 | 类型                          | 默认值        |
|------------------|--------------------------------------------------------------------|-----------------------------|--------------|
| show_send        | 是否显示发送按钮                                                     | ^[bool]                     | True         |
| show_stop        | 是否显示停止按钮（异步回调时替换发送按钮）                              | ^[bool]                     | False        |
| show_rerun       | 是否显示重新运行按钮                                                  | ^[bool]                     | True         |
| show_undo        | 是否显示撤销按钮                                                     | ^[bool]                     | True         |
| show_clear       | 是否显示清空按钮                                                     | ^[bool]                     | True         |
| show_button_name | 是否显示按钮名称                                                     | ^[bool]                     | True         |

### 计算属性
| 属性名          | 说明                                                                 | 类型                          |
|---------------|--------------------------------------------------------------------|-----------------------------|
| active_widget | 当前活动控件                                                        | ^[Widget]                   |
| active        | 当前活动标签页索引（单控件无标签页时为-1）                             | ^[int]                      |

### Events

| 事件名   | 说明                  | 类型                                     |
| ------- | -------------------- | ---------------------------------------- |
| change | 消息变化时触发        | ^[Callable]`(event: Event) -> None`     |

<!-- todo 
| send    | 发送消息时触发        | ^[Callable]`(message: dict) -> None`     |
| rerun   | 重新运行时触发        | ^[Callable]`() -> None`                  |
| undo    | 撤销时触发           | ^[Callable]`() -> None`                  |
| clear   | 清空时触发           | ^[Callable]`() -> None`                  |
-->

### Slots

| 插槽名   | 说明               |
| ------- | ----------------- |
| inputs   | 自定义输入区域      |

### 方法

| 方法名    | 说明                  | 参数                                    |
| -------- | ------------------- | --------------------------------------- |
| send     | 发送消息            | value, user, avatar, respond            |
| rerun    | 重新运行最后消息     | -                                       |
| clear    | 清空所有消息         | -                                       |
| undo     | 撤销最后的消息       | count: int = 1                          |




# ChatStep 聊天步骤组件

用于显示和管理聊天中的中间步骤组件，比如思维链中的步骤。该组件提供了对步骤状态的管理，包括挂起、运行中、成功和失败等状态，以及相应的标题和内容控制。

底层实现为`panel.chat.ChatStep`，参数基本一致，参考文档：https://panel.holoviz.org/reference/chat/ChatStep.html


## 基本用法

基本的步骤组件初始化：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnChatStep/>
</template>
<script lang='py'>
</script>

```


通过 `stream` 方法对内容实现以下操作：
- 附加内容，支持`Markdown`、图像等任何内容
- 覆盖内容

标题也可以通过 `stream_title` 方法对标题实现类似操作。
```vue
<!-- --plugins vpanel --show-code -->
<template>
<PnColumn>
  <PnChatStep ref="step_ref" :width='200' />
  <PnButton name="Add Content" @click="add_content()" />
</PnColumn>
</template>
<script lang='py'>
import asyncio
import panel as pn
from vuepy import ref

step_ref = ref(None)

async def add_content():
    step = step_ref.value.unwrap()
    step.title = ('Thinking...')
    step.stream("Just thinking...")
    await asyncio.sleep(0.5)
    
    # Calling stream again will concatenate the text
    step.stream(" about `ChatStep`!")
    await asyncio.sleep(0.5)
    
    step.stream('clear', replace=True)
    await asyncio.sleep(0.5)
    
    step.title = ('Ok')
    step.append(pn.pane.Image("https://assets.holoviz.org/panel/samples/png_sample.png", width=50, height=50))
    
</script>

```

## Badges

默认头像是 `BooleanStatus` 组件，但可以通过提供 `default_badges` 进行更改。值可以是表情符号、图像、文本或 Panel 对象
```vue
<!-- --plugins vpanel --show-code -->
<template>
<PnChatStep 
    :default_badges='default_badges'
    status="success"
/>
</template>
<script lang='py'>

default_badges={
    "pending": "🤔",
    "running": "🏃",
    "success": "🎉",
    "failed": "😞",
}
</script>

```


## 状态管理

为了显示该步骤正在处理，您可以将`status`设置为 `running` 并提供 `running_title`，使用 `success_title` 在成功时更新标题。
```vue
<!-- --plugins vpanel --show-code -->
<template>
<PnCol>
  <PnChatStep
    :width='300'
    status="running" 
    running_title="Processing this step..."
    success_title="Pretend job done!"
    ref="step_ref"
  />
  <PnButton name="Set status" @click="on_click()" />
</PnCol>
</template>
<script lang='py'>
from vuepy import ref
import time

step_ref = ref(None)

def on_click():
    step = step_ref.value.unwrap()
    step.stream("Pretending to do something.")
    time.sleep(1)
    step.status = "success"
</script>

```


## 错误处理

处理失败状态：

```vue
<!-- --plugins vpanel --show-code -->
<template>
<PnCol>
  <PnChatStep 
    running_title="Processing this step..." 
    success_title="Pretend job done!"
    ref="step_ref"
  />
  <PnButton name="Click" @click="on_click()" />
</PnCol>
</template>
<script lang='py'>
import time
from vuepy import ref

step_ref = ref(None)

def on_click():
    step = step_ref.value.unwrap()
    step.status = "running"
    try:
        step.stream("Breaking something")
        time.sleep(0.5)
        raise RuntimeError("Just demoing!")
    except RuntimeError as e:
        step.status = "failed"
        step.stream(f"Error: {str(e)}", replace=True)
</script>

```


## 标题流式显示

支持标题的流式更新：

```vue
<!-- --plugins vpanel --show-code -->
<template>
<PnColumn>
  <PnChatStep :width='200' ref="step_ref" />
  <PnButton name="Stream Title" @click="stream_title()" />
</PnColumn>
</template>
<script lang='py'>
from vuepy import ref
import time

step_ref = ref(None)

def stream_title():
    step = step_ref.value.unwrap()
    step.status = "running"
    for char in "It's streaming a title!":
        time.sleep(0.1)
        step.stream_title(char)
</script>

```


## API

### 核心属性
| 属性名                | 说明                                                                 | 类型                          | 默认值          |
|----------------------|--------------------------------------------------------------------|-----------------------------|----------------|
| collapsed_on_success | 成功时是否折叠卡片                                                   | ^[bool]                     | True           |
| context_exception    | 异常处理方式（"raise"-抛出/"summary"-摘要/"verbose"-完整追踪/"ignore"-忽略） | ^[str]                      | "raise"        |
| success_title        | 成功状态标题（未设置时使用最后对象的字符串）                            | ^[str]                      | None           |
| default_title        | 默认标题（其他标题未设置时使用）                                       | ^[str]                      | ""             |
| failed_title         | 失败状态标题                                                        | ^[str]                      | None           |
| margin               | 外边距（(垂直,水平)或(上,右,下,左)）                                  | ^[tuple]                    | (5,5,5,10)     |
| objects              | 聊天步骤内容列表（按列布局，通常应整体替换）                            | ^[list]                     | []             |
| pending_title        | 等待状态标题                                                        | ^[str]                      | None           |
| running_title        | 运行状态标题                                                        | ^[str]                      | None           |
| status               | 步骤状态（"pending"/"running"/"success"/"failed"）                   | ^[str]                      | "pending"      |

### 样式属性
| 属性名            | 说明                                                                 | 类型                          | 默认值        |
|------------------|--------------------------------------------------------------------|-----------------------------|--------------|
| collapsed        | 是否折叠内容                                                        | ^[bool]                     | False        |
| default_badges   | 状态徽章映射（键必须为'pending'/'running'/'success'/'failed'）        | ^[dict]                     | 系统默认徽章    |

### Events

| 事件名   | 说明           | 类型                                      |
| ------- | ------------- | ----------------------------------------- |
| status  | 状态改变时触发  | ^[Callable]`(status: str) -> None`       |

### Slots

| 插槽名   | 说明               |
| ------- | ----------------- |
| default | 自定义步骤内容      |
| title   | 自定义标题内容      |

### 方法

| 方法名         | 说明            | 参数                                    |
| ------------- | -------------- | --------------------------------------- |
| stream        | 流式添加内容     | value, replace=False                    |
| stream_title  | 流式更新标题     | value, replace=False, status="running"  |
| serialize     | 序列化内容       | -                                      |





# ChatFeed 聊天流

PnChatFeed是一个中层布局组件，用于管理一系列聊天消息(ChatMessage)项。该组件提供后端方法来发送消息、流式传输令牌、执行回调、撤销消息以及清除聊天记录。

底层实现为`panel.chat.ChatFeed`，参数基本一致，参考文档：https://panel.holoviz.org/reference/chat/ChatFeed.html


## 基本用法

`PnChatFeed`可以不需要任何参数初始化，通过`send`方法发送聊天消息。

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
<PnCol>
  <PnChatFeed ref="chat_feed" />
  <PnButton name='send' @click='on_click()'/>
</PnCol>
</template>

<script lang='py'>
import panel as pn
from vuepy import ref, onMounted

chat_feed = ref(None)

def on_click():
    message = chat_feed.value.unwrap().send(
        "Hello world!",
        user="Bot",
        avatar="B",
        footer_objects=[pn.widgets.Button(name="Footer Object")]
    )
_ = onMounted(on_click)
</script>

```


## 回调函数

添加回调函数可以使`PnChatFeed`更加有趣。回调函数的签名必须包含最新可用的消息值`contents`。
除了`contents`之外，签名还可以包含最新可用的`user`名称和聊天`instance`。

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnChatFeed :callback="echo_message" ref="chat_feed" />
  <PnButton name='send' @click='send_message()'/>
</template>
<script lang='py'>
from vuepy import ref, onMounted

chat_feed = ref(None)

# def echo_message(contents, user, instance):
def echo_message(contents):
    return f"Echoing... {contents}"

def send_message():
    message = chat_feed.value.unwrap().send("Hello!")

_ = onMounted(send_message)
</script>

```


可以更新`callback_user`和`callback_avatar`来分别更改响应者的默认名称和头像。

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnChatFeed :callback='echo_message' 
              callback_user='Echo Bot' callback_avatar='🛸' ref="chat_feed" />
  <PnButton name='send' @click='send_message()'/>
</template>

<script lang='py'>
from vuepy import ref, onMounted

chat_feed = ref(None)

def echo_message(contents, user):
    return f"Echoing {user!r}... {contents}"

def send_message():
    message = chat_feed.value.unwrap().send("Hey!")

d = onMounted(send_message)
</script>

```


指定的`callback`也可以返回一个包含`value`、`user`和`avatar`键的字典，这将覆盖默认的`callback_user`和`callback_avatar`。

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnChatFeed :callback="parrot_message" 
              callback_user='Echo Bot' 
              callback_avatar='🛸' ref="chat_feed" />
</template>

<script lang='py'>
from vuepy import ref, onMounted

chat_feed = ref(None)

def parrot_message(contents):
    return {"value": f"No, {contents.lower()}", "user": "Parrot", "avatar": "🦜"}

def send_message():
    message = chat_feed.value.unwrap().send("Are you a parrot?")

_ = onMounted(send_message)
</script>

```


如果不希望与`send`一起触发回调，请将`respond`设置为`False`。

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnChatFeed :callback="parrot_message" callback_user='Echo Bot' callback_avatar='🛸' ref="chat_feed" />
</template>

<script lang='py'>
from vuepy import ref, onMounted

chat_feed = ref(None)

def parrot_message(contents):
    return {"value": f"No, {contents.lower()}", "user": "Parrot", "avatar": "🦜"}

def send_message():
    message = chat_feed.value.unwrap().send("Don't parrot this.", respond=False)

_ = onMounted(send_message)
</script>

```


可以通过将`callback_exception`设置为`"summary"`来显示异常。

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnChatFeed :callback="bad_callback" callback_exception='summary' ref="chat_feed" />
</template>

<script lang='py'>
from vuepy import ref, onMounted

chat_feed = ref(None)

def bad_callback(contents):
    return 1 / 0

def send_message():
    chat_feed.value.unwrap().send("This will fail...")

_ = onMounted(send_message)
</script>

```


## 异步回调

`PnChatFeed`还支持*异步*`callback`。我们建议尽可能使用*异步*`callback`以保持应用程序的快速响应，*只要函数中没有阻塞事件循环的内容*。

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnChatFeed :callback="parrot_message" callback_user='Echo Bot' ref="chat_feed" />
</template>

<script lang='py'>
import asyncio
from vuepy import ref, onMounted

chat_feed = ref(None)

async def parrot_message(contents):
    await asyncio.sleep(2.8)
    return {"value": f"No, {contents.lower()}", "user": "Parrot", "avatar": "🦜"}

def send_message():
    message = chat_feed.value.unwrap().send("Are you a parrot?")

_ = onMounted(send_message)
</script>

```


流式输出的最简单和最优方式是通过*异步生成器*。如果您不熟悉这个术语，只需在函数前加上`async`，并用`yield`替换`return`。

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnChatFeed :callback="stream_message" ref="chat_feed" />
</template>

<script lang='py'>
import asyncio
from vuepy import ref, onMounted

chat_feed = ref(None)

async def stream_message(contents):
    message = ""
    for character in contents:
        message += character
        await asyncio.sleep(0.1)
        yield message

def send_message():
    message = chat_feed.value.unwrap().send("Streaming...")

_ = onMounted(send_message)
</script>

```


如果不连接字符，也可以持续替换原始消息。

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnChatFeed :callback="replace_message" ref="chat_feed" />
</template>

<script lang='py'>
import asyncio
from vuepy import ref, onMounted

chat_feed = ref(None)

async def replace_message(contents):
    for character in contents:
        await asyncio.sleep(0.1)
        yield character

def send_message():
    message = chat_feed.value.unwrap().send("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

_ = onMounted(send_message)
</script>

```


也可以手动触发回调与`respond`。这对于从初始消息实现一系列响应很有用！

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnChatFeed :callback="chain_message" ref="chat_feed" />
</template>

<script lang='py'>
import asyncio
from vuepy import ref, onMounted

chat_feed = ref(None)

async def chain_message(contents, user, instance):
    await asyncio.sleep(1.8)
    if user == "User":
        yield {"user": "Bot 1", "value": "Hi User! I'm Bot 1--here to greet you."}
        instance.respond()
    elif user == "Bot 1":
        yield {
            "user": "Bot 2",
            "value": "Hi User; I see that Bot 1 already greeted you; I'm Bot 2.",
        }
        instance.respond()
    elif user == "Bot 2":
        yield {
            "user": "Bot 3",
            "value": "I'm Bot 3; the last bot that will respond. See ya!",
        }

def send_message():
    message = chat_feed.value.unwrap().send("Hello bots!")

_ = onMounted(send_message)
</script>

```


## 编辑回调

可以将`edit_callback`附加到`PnChatFeed`以处理消息编辑。签名必须包含最新可用的消息值`contents`、编辑消息的索引和聊天`instance`。

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnChatFeed :callback="echo_callback" :edit_callback="edit_callback" callback_user="Echo Guy" ref="chat_feed" />
</template>

<script lang='py'>
from vuepy import ref, onMounted

chat_feed = ref(None)

def echo_callback(content):
    return content

def edit_callback(content, index, instance):
    instance.objects[index + 1].object = content

def send_message():
    chat_feed.value.unwrap().send("Edit this")

_ = onMounted(send_message)
</script>

```


## 步骤

可以通过一系列`ChatStep`提供中间步骤，如思想链。

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnChatFeed ref="chat_feed" />
</template>

<script lang='py'>
import time
from vuepy import ref, onMounted

chat_feed = ref(None)

def demo_steps():
    # First step
    with chat_feed.value.unwrap().add_step(
        "To answer the user's query, I need to first create a plan.", 
        title="Create a plan", user='Agent'
    ) as step:
        step.stream("\n\n...Okay the plan is to demo this!")
    
    # Second step - append to existing message
    with chat_feed.value.unwrap().add_step(
        title="Execute the plan", status="running"
    ) as step:
        step.stream("\n\n...Executing plan...")
        time.sleep(1)
        step.stream("\n\n...Handing over to SQL Agent")
    
    # Third step - new user creates a new message
    with chat_feed.value.unwrap().add_step(
        title="Running SQL query", user='SQL Agent'
    ) as step:
        step.stream('Querying...')
        time.sleep(1)
        step.stream('\nSELECT * FROM TABLE')

_ = onMounted(demo_steps)
</script>

```


## 提示用户

可以使用`prompt_user`暂时暂停代码执行并提示用户回答问题或填写表单，该方法接受任何Panel `component`和后续`callback`（带有`component`和`instance`作为args）在提交后执行。

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnChatFeed :callback="show_interest" callback_user="Ice Cream Bot" ref="chat_feed" />
</template>

<script lang='py'>
from vuepy import ref, onMounted

chat_feed = ref(None)

def repeat_answer(component, instance):
    contents = component.value
    instance.send(f"Wow, {contents}, that's my favorite flavor too!", respond=False, user="Ice Cream Bot")

def show_interest(contents, user, instance):
    if "ice" in contents or "cream" in contents:
        answer_input = {"component": "PnTextInput", "props": {"placeholder": "Enter your favorite ice cream flavor"}}
        instance.prompt_user(answer_input, callback=repeat_answer)
    else:
        return "I'm not interested in that topic."

def send_message():
    chat_feed.value.unwrap().send("ice cream")

_ = onMounted(send_message)
</script>

```


还可以设置一个`predicate`来评估组件的状态，例如小部件是否有值。如果提供，当谓词返回`True`时，提交按钮将被启用。

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnChatFeed :callback="show_interest" callback_user="Ice Cream Bot" ref="chat_feed" />
</template>

<script lang='py'>
from vuepy import ref, onMounted

chat_feed = ref(None)

def is_chocolate(component):
    return "chocolate" in component.value.lower()

def repeat_answer(component, instance):
    contents = component.value
    instance.send(f"Wow, {contents}, that's my favorite flavor too!", respond=False, user="Ice Cream Bot")

def show_interest(contents, user, instance):
    if "ice" in contents or "cream" in contents:
        answer_input = {"component": "PnTextInput", "props": {"placeholder": "Enter your favorite ice cream flavor"}}
        instance.prompt_user(answer_input, callback=repeat_answer, predicate=is_chocolate)
    else:
        return "I'm not interested in that topic."

def send_message():
    chat_feed.value.unwrap().send("ice cream")

_ = onMounted(send_message)
</script>

```


## 序列化

聊天历史可以通过`serialize`并设置`format="transformers"`来序列化，以供`transformers`或`openai`包使用。

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnChatFeed ref="chat_feed" />
  <PnCol>
    <PnButton @click="send_messages()" name="Send Messages" />
    <PnButton @click="serialize_chat()" name="Serialize" />
    <PnTextAreaInput v-model="serialized.value" :rows="10" />
  </PnCol>
</template>

<script lang='py'>
from vuepy import ref, onMounted

chat_feed = ref(None)
serialized = ref("")

def send_messages():
    chat_feed.value.unwrap().send("Hello!", user="User")
    chat_feed.value.unwrap().send("Hi there!", user="Bot 1")
    chat_feed.value.unwrap().send("How are you?", user="User")
    chat_feed.value.unwrap().send("I'm doing well!", user="Bot 2")

def serialize_chat():
    serialized.value = str(chat_feed.value.unwrap().serialize(format="transformers"))
  
m1 = onMounted(send_messages)
m2 = onMounted(serialize_chat)
</script>

```


可以设置`role_names`来显式映射角色到ChatMessage的用户名。

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnChatFeed ref="chat_feed" />
  <PnCol>
    <PnButton @click="send_messages()" name="Send Messages" />
    <PnButton @click="serialize_chat()" name="Serialize with role_names" />
    <PnTextAreaInput v-model="serialized.value" :rows="10" />
  </PnCol>
</template>

<script lang='py'>
from vuepy import ref, onMounted

chat_feed = ref(None)
serialized = ref("")

def send_messages():
    chat_feed.value.unwrap().send("Hello!", user="User")
    chat_feed.value.unwrap().send("Hi there!", user="Bot 1")
    chat_feed.value.unwrap().send("How are you?", user="User")
    chat_feed.value.unwrap().send("I'm doing well!", user="Bot 2")

def serialize_chat():
    serialized.value = str(chat_feed.value.unwrap().serialize(
        format="transformers", 
        role_names={"assistant": ["Bot 1", "Bot 2", "Bot 3"]}
    ))

m1 = onMounted(send_messages)
m2 = onMounted(serialize_chat)
</script>

```


## 流式传输

如果返回的对象不是生成器（特别是LangChain输出），仍然可以使用`stream`方法流式传输输出。

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnChatFeed ref="chat_feed" />
</template>

<script lang='py'>
import time
import panel as pn
from vuepy import ref, onMounted

chat_feed = ref(None)

def demo_stream():
    # Create a new message
    message = chat_feed.value.unwrap().stream("Hello", user="Aspiring User", avatar="🤓")
    
    # Stream (append) to the previous message
    message = chat_feed.value.unwrap().stream(
        " World!",
        user="Aspiring User",
        avatar="🤓",
        message=message,
        footer_objects=[pn.widgets.Button(name="Footer Object")]
    )
    
    # Demonstrate streaming with a loop
    message = None
    for n in "12":
        time.sleep(0.1)
        message = chat_feed.value.unwrap().stream(n, message=message)

@onMounted
def demo():
    pn.state.add_periodic_callback(demo_stream, 500, count=1)
</script>

```


## 自定义

可以通过`message_params`传递`ChatEntry`参数。

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnChatFeed 
    :message_params="message_params"
    ref="chat_feed" />
</template>

<script lang='py'>
from vuepy import ref, onMounted

chat_feed = ref(None)
message_params = {
    "default_avatars": {"System": "S", "User": "👤"}, 
    "reaction_icons": {"like": "thumb-up"}
}

def send_messages():
    chat_feed.value.unwrap().send(user="System", value="This is the System speaking.")
    chat_feed.value.unwrap().send(user="User", value="This is the User speaking.")

m1 = onMounted(send_messages)
</script>

```


直接将这些参数传递给ChatFeed构造函数，它将自动转发到`message_params`中。

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnChatFeed 
    :default_avatars='{"System": "S", "User": "👤"}'
    :reaction_icons='{"like": "thumb-up"}'
    ref="chat_feed" />
</template>

<script lang='py'>
from vuepy import ref, onMounted

chat_feed = ref(None)

def send_messages():
    chat_feed.value.unwrap().send(user="System", value="This is the System speaking.")
    chat_feed.value.unwrap().send(user="User", value="This is the User speaking.")

m1 = onMounted(send_messages)
</script>

```


也可以通过设置`message_params`参数来自定义聊天流的外观。

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnChatFeed 
    :show_activity_dot="True"
    :message_params="message_params"
    ref="chat_feed" />
</template>

<script lang='py'>
from vuepy import ref, onMounted

chat_feed = ref(None)
message_params = {
    "stylesheets": [
        """
        .message {
            background-color: tan;
            font-family: "Courier New";
            font-size: 24px;
        }
        """
    ]
}

def send_message():
    chat_feed.value.unwrap().send("I am so stylish!")

m1 = onMounted(send_message)
</script>

```


## 自定义聊天界面

您也可以在`PnChatFeed`的基础上构建自己的自定义聊天界面。

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnCol>
    <PnChatFeed
      ref="chat_feed"
      :callback="get_response"
      :height="500"
      :message_params="message_params"
    />
    <PnLayout.Divider />
    <PnRow>
      <span>Click a button</span>
      <PnButton name="Andrew" @click="send_andrew()" />
      <PnButton name="Marc" @click="send_marc()" />
      <PnButton name="Undo" @click="undo_messages()" />
      <PnButton name="Clear" @click="clear_messages()" />
    </PnRow>
  </PnCol>
</template>

<script lang='py'>
import asyncio
from vuepy import ref, onMounted

chat_feed = ref(None)
ASSISTANT_AVATAR = "https://upload.wikimedia.org/wikipedia/commons/6/63/Yumi_UBports.png"

message_params = {
    "default_avatars": {"Assistant": ASSISTANT_AVATAR}
}

async def get_response(contents, user):
    await asyncio.sleep(0.88)
    return {
        "Marc": "It is 2",
        "Andrew": "It is 4",
    }.get(user, "I don't know")

def send_marc():
    chat_feed.value.unwrap().send(
        "What is the square root of 4?", user="Marc", avatar="🚴"
    )

def send_andrew():
    chat_feed.value.unwrap().send(
        "What is the square root of 4 squared?", user="Andrew", avatar="🏊"
    )

def undo_messages():
    chat_feed.value.unwrap().undo(2)

def clear_messages():
    chat_feed.value.unwrap().clear()

def init_chat():
    chat_feed.value.unwrap().send("Hi There!", user="Assistant", avatar=ASSISTANT_AVATAR)

m1 = onMounted(init_chat)
</script>

```


## API

### 属性

| 属性名    | 说明                 | 类型                                                           | 默认值 |
| -------- | ------------------- | ---------------------------------------------------------------| ------- |
| objects | 添加到聊天流的消息 | ^[List[ChatMessage]] | [] |
| renderers | 接受值并返回Panel对象的可调用对象或可调用对象列表 | ^[List[Callable]] | None |
| callback | 当用户发送消息或调用`respond`时执行的回调 | ^[callable] | None |
| card_params | 传递给Card的参数 | ^[Dict] | {} |
| message_params | 传递给每个ChatMessage的参数 | ^[Dict] | {} |
| header | 聊天流的标题 | ^[Any] | None |
| callback_user | 回调提供的消息的默认用户名 | ^[str] | "AI" |
| callback_avatar | 回调提供的条目的默认头像 | ^[str, BytesIO, bytes, ImageBase] | None |
| callback_exception | 如何处理回调引发的异常 | ^[str, Callable] | "raise" |
| edit_callback | 当用户编辑消息时执行的回调 | ^[callable] | None |
| help_text | 初始化聊天记录中的聊天消息 | ^[str] | None |
| placeholder_text | 显示在占位符图标旁边的文本 | ^[str] | "Thinking..." |
| placeholder_params | 传递给占位符`ChatMessage`的参数 | ^[dict] | {} |
| placeholder_threshold | 显示占位符前缓冲的最小持续时间（秒） | ^[float] | 0.2 |
| post_hook | 在新消息完全添加后执行的钩子 | ^[callable] | None |
| auto_scroll_limit | 从Column中最新对象到激活更新时自动滚动的最大像素距离 | ^[int] | 10 |
| scroll_button_threshold | 从Column中最新对象到显示滚动按钮的最小像素距离 | ^[int] | 100 |
| load_buffer | 在可见对象每侧加载的对象数 | ^[int] | 10 |
| show_activity_dot | 是否在流式传输回调响应时在ChatMessage上显示活动点 | ^[bool] | False |
| view_latest | 是否在初始化时滚动到最新对象 | ^[bool] | True |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | 自定义默认内容      |

### 方法

| 方法名 | 说明 | 类型 |
| --- | --- | --- |
| send | 发送一个值并在聊天记录中创建一个新消息 | ^[Callable]`(value, user=None, avatar=None, respond=True, **kwargs) -> ChatMessage` |
| serialize | 将聊天记录导出为字典 | ^[Callable]`(format='transformers', role_names=None, default_role='user', filter_by=None, exclude_users=None, custom_serializer=None) -> Dict` |
| stream | 流式传输令牌并更新提供的消息 | ^[Callable]`(token, message=None, user=None, avatar=None, **kwargs) -> ChatMessage` |
| clear | 清除聊天记录并返回已清除的消息 | ^[Callable]`() -> List[ChatMessage]` |
| respond | 使用聊天记录中的最新消息执行回调 | ^[Callable]`() -> None` |
| trigger_post_hook | 使用聊天记录中的最新消息触发后钩子 | ^[Callable]`() -> None` |
| stop | 如果可能，取消当前回调任务 | ^[Callable]`() -> None` |
| scroll_to | 列滚动到指定索引处的对象 | ^[Callable]`(index: int) -> None` |
| undo | 从聊天记录中删除最后`count`条消息并返回它们 | ^[Callable]`(count: int = 1) -> List[ChatMessage]` |




# ChatMessage 聊天消息组件

用于显示聊天消息的组件，支持多种内容类型。该组件提供结构化的消息显示功能，包括：
- 显示用户头像（可以是文本、emoji或图片）
- 显示用户名
- 以自定义格式显示消息时间戳
- 支持消息反应并映射到图标
- 渲染各种内容类型，包括文本、图片、音频、视频等

底层实现为`panel.chat.ChatMessage`，参数基本一致，参考文档：https://panel.holoviz.org/reference/chat/ChatMessage.html


## 基本用法

基本的消息展示：

```vue
<!-- --plugins vpanel --show-code -->
<template>
<PnChatMessage object="Hi and welcome!" />
</template>
<script lang='py'>
from vuepy import ref
</script>

```


ChatMessage可以显示任何Panel可以显示的Python对象，例如Panel组件、数据框和图表：

```vue
<!-- --plugins vpanel --show-code -->
<template>
<PnColumn>
  <PnChatMessage :object="df" />
  <PnChatMessage :object="vgl_pane" />
</PnColumn>
</template>
<script lang='py'>
from vuepy import ref
import pandas as pd
import panel as pn

# Create sample data
df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})

# Create a Vega-Lite spec
vegalite = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "data": {"url": "https://raw.githubusercontent.com/vega/vega/master/docs/data/barley.json"},
    "mark": "bar",
    "encoding": {
        "x": {"aggregate": "sum", "field": "yield", "type": "quantitative"},
        "y": {"field": "variety", "type": "nominal"},
        "color": {"field": "site", "type": "nominal"}
    },
    "width": "container",
}
vgl_pane = pn.pane.Vega(vegalite, height=240)
</script>

```


可以指定自定义用户名和头像：

```vue
<!-- --plugins vpanel --show-code -->
<template>
<PnChatMessage object="Want to hear some beat boxing?" 
               user="Beat Boxer" avatar="🎶" />
<PnChatMessage object="Want to hear some beat boxing?" 
               user="Beat Boxer" 
               :avatar="r'\N{musical note}'" />
</template>

```


## 消息更新

组件的值、用户名和头像都可以动态更新：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
<PnColumn>
  <PnChatMessage ref='msg_ref' 
                 object='Initial message' 
                 user='Jolly Guy' avatar="🎅" />
  <PnButton name="Update Message" @click="update_message()" />
</PnColumn>
</template>
<script lang='py'>
from vuepy import ref
import asyncio

msg_ref = ref(None)

def update_message():
    msg = msg_ref.value.unwrap()
    msg.object = "Updated message!"
    msg.user = "Updated Guy"
    msg.avatar = "😎"
</script>

```

将输出流式传输到`ChatMessage`最简单、最好的方式是通过异步生成器。

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
<PnColumn>
  <PnChatMessage :object='response.value' 
                 user='Jolly Guy' avatar="🎅" />
  <PnButton name="Update Message" @click="on_click()" />
</PnColumn>
</template>
<script lang='py'>
import asyncio
import panel as pn
from vuepy import ref, onMounted

response = ref('')

sentence = """
    The greatest glory in living lies not in never falling,
    but in rising every time we fall.
"""

async def append_response():
    value = ""
    for token in sentence.split():
        value += f" {token}"
        await asyncio.sleep(0.1)
        # yield value
        response.value = value
        # yield value
        response.value = value

def on_click():
    print('xxxx')

pn.state.add_periodic_callback(append_response, count=1)

</script>

```


## 样式

如果您想要一个仅显示 `value` 的普通界面，请将 `show_user` 、 `show_copy_icon` 、 `show_avatar` 和 `show_timestamp` 设置为 `False` ，并为 `reaction_icons` 提供一个空的 `dict` 。

可以设置常用的样式和布局参数，如 `sizing_mode` 、 `height` 、 `width` 、 `max_height` 、 `max_width` 和 `styles` 。
```vue
<!-- --plugins vpanel --show-code -->
<template>
<PnChatMessage object="Want to hear some beat boxing?"
    :show_avatar=False
    :show_user=False
    :show_timestamp=False
    :show_copy_icon=False
    :reaction_icons='ChatReactionIcons(options={})'
/>
</template>
<script lang='py'>
from panel.chat import ChatReactionIcons

</script>

```


## 代码高亮

支持代码块的语法高亮（需要安装 pygments）：

```vue
<!-- --plugins vpanel --show-code -->
<template>
<PnChatMessage :object='code_content' user='Bot' avatar="🤖" />
</template>
<script lang='py'>
from vuepy import ref

# code_content = """```python
# print('hello world')
# ```"""
code_content = """```
print('hello world')
```"""
</script>

```


## API

### 核心属性
| 属性名               | 说明                                                                 | 类型                          | 默认值          |
|---------------------|--------------------------------------------------------------------|-----------------------------|----------------|
| object             | 消息内容（支持字符串/面板/控件/布局等）                                | ^[object]                   | None           |
| renderers          | 内容渲染器（可调用对象列表，首个成功执行的将被使用）                      | ^[List[Callable]]           | None           |
| user               | 发送者用户名                                                        | ^[str]                      | ""             |
| avatar             | 用户头像（支持文字/emoji/图片等，未设置时使用用户名首字母）               | ^[str\|BinaryIO]            | None           |
| default_avatars    | 用户名到默认头像的映射字典（键值不区分大小写和特殊字符）                   | ^[Dict[str, str\|BinaryIO]] | {}             |
| edited             | 消息编辑触发事件                                                     | ^[bool]                     | False          |
| footer_objects     | 消息底部显示的组件列表                                                | ^[List]                     | []             |
| header_objects     | 消息头部显示的组件列表                                                | ^[List]                     | []             |
| avatar_lookup      | 头像查找函数（设置后将忽略default_avatars）                            | ^[Callable]                 | None           |
| reactions          | 消息关联的反应列表                                                    | ^[List]                     | []             |
| reaction_icons     | 反应图标映射（未设置时默认{"favorite": "heart"}）                     | ^[dict]                     | {"favorite": "heart"} |
| timestamp          | 消息时间戳（默认使用实例化时间）                                       | ^[datetime]                 | 当前时间         |
| timestamp_format   | 时间戳显示格式                                                       | ^[str]                      | -              |
| timestamp_tz       | 时区设置（仅timestamp未设置时生效）                                    | ^[str]                      | 系统默认时区      |

### 显示属性
| 属性名              | 说明                                     | 类型           | 默认值        |
|--------------------|-----------------------------------------|----------------|--------------|
| show_avatar        | 是否显示用户头像                           | ^[bool]                     | True         |
| show_user          | 是否显示用户名                            | ^[bool]                     | True         |
| show_timestamp     | 是否显示时间戳                            | ^[bool]                     | True         |
| show_reaction_icons| 是否显示反应图标                           | ^[bool]                     | True         |
| show_copy_icon     | 是否显示复制图标                           | ^[bool]                     | False        |
| show_edit_icon     | 是否显示编辑图标                           | ^[bool]                     | False        |
| show_activity_dot  | 是否显示活动状态指示点                      | ^[bool]                     | False        |
| name               | 消息组件标题                               | ^[str]                      | ""           |

### Events

| 事件名  | 说明           | 类型                                  |
| ------ | ------------- | ------------------------------------- |
| change | 值改变时触发   | ^[Callable]`(value: Any) -> None`    |

### Slots

| 插槽名   | 说明               |
| ------- | ----------------- |
| default | 消息内容           |
| header  | 消息头部内容       |
| footer  | 消息底部内容       |

### 方法

| 方法名 | 说明 | 参数 |
| ------ | --- | ---- |
| serialize | 将消息序列化为字符串 | - |



# Notifications 通知

NotificationsArea 组件是一个全局组件，允许用户显示所谓的“toast”，以向用户提供信息。可以通过 pn.extension 设置 notifications=True 或直接设置 pn.config.notifications = True 来启用通知。

参考文档：https://panel.holoviz.org/reference/global/Notifications.html

## 基本用法

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnButton name='notify' @click='msg()'/>
</template>
<script lang='py'>
import panel as pn

pn.extension(notifications=True)

def msg():
    pn.state.notifications.error('This is error.', duration=1000)
    pn.state.notifications.info('This is info.', duration=2000)
    pn.state.notifications.success('This is success.', duration=0)
    pn.state.notifications.warning('This is warning.', duration=4000)
</script>

```




# Trend 趋势指示器

趋势指示器提供了一个值及其最近趋势的可视化表示。它支持向图表组件流式传输数据，使得能够对某个值的最近趋势提供高性能的实时更新。

底层实现为`panel.widgets.Trend`，参数基本一致，参考文档：https://panel.holoviz.org/reference/indicators/Trend.html


## 基本用法

最简单的`Trend`只需要提供带有x和y值的`data`，可以声明为字典或`pandas.DataFrame`。`value`和`value_change`值将从数据中自动计算：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnTrend 
    name="Price" 
    :data="data" 
    :width="200" 
    :height="200" 
  />
</template>

<script lang='py'>
import numpy as np

np.random.seed(8)
data = {'x': np.arange(50), 'y': np.random.randn(50).cumsum()}
</script>

```


## 数据流式传输

`Trend`指示器还提供了一个方便的方法来流式传输新数据，支持`rollover`参数来限制显示的数据量。我们将使用`setInterval`来定期更新图表：

```vue
<!-- --plugins vpanel --show-code -->
<template>
 <PnCol>
  <PnTrend 
    ref="trend_ref"
    name="Price" 
    :data="data" 
    :width="200" 
    :height="200" 
  />
  <PnButton name="Start Streaming" @click="start()" />
 </PnCol>
</template>

<script lang='py'>
import numpy as np
import panel as pn
from vuepy import ref

data = {'x': np.arange(10), 'y': np.random.randn(10).cumsum()}
interval_id = None
trend_ref = ref(None)

def stream_data():
    trend = trend_ref.value.unwrap()
    trend.stream({
        'x': [trend.data['x'][-1]+1],
        'y': [trend.data['y'][-1]+np.random.randn()]
    },  rollover=50)
    

def start():
    pn.state.add_periodic_callback(stream_data, period=250, count=15);
</script>

```


## 图表类型

除了默认的`plot_type`外，流指示器还支持其他几种选项：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnRow>
    <PnTrend 
      v-for="plot_type in plot_types"
      :name="plot_type" 
      :data="data" 
      :plot_type="plot_type"
      :width="150" 
      :height="150" 
    />
  </PnRow>
</template>

<script lang='py'>
import numpy as np

data = {'x': np.arange(50), 'y': np.random.randn(50).cumsum()}
plot_types = ['line', 'bar', 'step', 'area']
</script>

```


## API

### 属性

| 属性名        | 说明                      | 类型                                                           | 默认值 |
| ------------ | ------------------------ | --------------------------------------------------------------| ------- |
| data         | 图表数据                   | ^[object\|object[]] 字典或pandas DataFrame形式的数据            | —      |
| layout       | 指示器的布局               | ^[string] 可选值: 'column', 'row'                             | column  |
| plot_x       | 数据中对应图表x值的列       | ^[string]                                                      | y      |
| plot_y       | 数据中对应图表y值的列       | ^[string]                                                      | x      |
| plot_color   | 图表中使用的颜色            | ^[string]                                                      | #428bca |
| plot_type    | 绘制图表数据的图表类型      | ^[string] 可选值: 'line', 'bar', 'step', 'area'                | bar     |
| pos_color    | 用于指示正向变化的颜色      | ^[string]                                                      | #5cb85c |
| neg_color    | 用于指示负向变化的颜色      | ^[string]                                                      | #d9534f |
| value        | 要显示的主值               | ^[number\|string] 数字或"auto"                                 | auto    |
| value_change | 值变化表示为分数           | ^[number\|string] 数字或"auto"                                 | auto    |
| disabled     | 是否禁用                  | ^[boolean]                                                     | false   |

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |
| change | 当值变化时触发的事件   | ^[Callable]`(event: dict) -> None`     |

### 方法

| 名称      | 说明                             | 参数                                                  |
| -------- | -------------------------------- | ----------------------------------------------------|
| stream   | 向图表流式传输新数据，支持限制显示的数据量 | data: 要添加的新数据, rollover: 保留的最大数据点数量    |




# TooltipIcon 提示图标

提示图标组件提供了一个带有工具提示的图标。`value`将是工具提示内的文本。

底层实现为`panel.widgets.TooltipIcon`，参数基本一致，参考文档：https://panel.holoviz.org/reference/indicators/TooltipIcon.html


## 基本用法

`TooltipIcon`指示器可以使用字符串进行实例化：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnTooltipIcon value="This is a simple tooltip by using a string" />
</template>

```


## 使用Bokeh.models.Tooltip

也可以使用`bokeh.models.Tooltip`进行实例化：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnTooltipIcon :value="tooltip_value" />
</template>

<script lang='py'>
from bokeh.models import Tooltip

tooltip_value = Tooltip(content="This is a tooltip using a bokeh.models.Tooltip", position="right")
</script>

```


## 与其他组件组合使用

`TooltipIcon`可以用来为组件添加更多信息：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnRow>
    <PnButton name="Click me!" />
    <PnTooltipIcon value="Nothing happens when you click the button!" />
  </PnRow>
</template>

```


## API

### 属性

| 属性名    | 说明                 | 类型                                                           | 默认值 |
| -------- | ------------------- | ---------------------------------------------------------------| ------- |
| value    | 工具提示内的文本      | ^[string\|object] 字符串或`bokeh.models.Tooltip`对象           | —       |
| disabled | 是否禁用             | ^[boolean]                                                     | false   |

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |
| change | 当值变化时触发的事件   | ^[Callable]`(event: dict) -> None`     |




# Gauge 仪表盘

仪表盘提供了一个值的可视化表示，以仪表或速度计形式展示。`Gauge`组件使用ECharts库渲染。

底层实现为`panel.widgets.Gauge`，参数基本一致，参考文档：https://panel.holoviz.org/reference/indicators/Gauge.html


## 基本用法

最简单的仪表盘只需要设置一个在指定范围内的`value`。默认的格式化器和范围假设你提供的是百分比值：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnGauge name="Failure Rate" :value="10" :bounds="(0, 100)" />
</template>

```


## 自定义格式与颜色阈值

如果我们想要显示其他值，例如发动机每分钟转速，我们可以设置不同的`bounds`值并重写`format`。此外，我们还可以提供一组不同的颜色，定义应在提供范围的哪个点上更改颜色。`colors`接受一个元组列表，定义分数和颜色：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnGauge 
    name="Engine" 
    :value="2500" 
    :bounds="(0, 3000)" 
    format="{value} rpm"
    :colors="[[0.2, 'green'], [0.8, 'gold'], [1, 'red']]" 
  />
</template>

```


## 自定义指针颜色

您还可以通过传递自定义选项来更改指针的颜色：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnGauge 
    name="Engine" 
    :value="2500" 
    :bounds="(0, 3000)" 
    format="{value} rpm"
    :colors="[[0.2, 'green'], [0.8, 'gold'], [1, 'red']]" 
    :custom_opts="{'pointer': {'itemStyle': {'color': 'red'}}}"
  />
</template>

```


## API

### 属性

| 属性名           | 说明                                                                 | 类型                          | 默认值        |
|----------------|--------------------------------------------------------------------|-----------------------------|--------------|
| value          | 仪表当前值（需在bounds范围内）                                         | ^[float\|int]               | 25           |
| annulus_width  | 仪表环宽度（像素）                                                   | ^[int]                      | 10           |
| bounds         | 仪表数值范围（最小值, 最大值）                                         | ^[tuple]                    | (0, 100)     |
| colors         | 颜色阈值配置（[(阈值比例, 颜色), ...]）                                | ^[list]                     | []           |
| custom_opts    | ECharts仪表盘额外配置选项                                             | ^[dict]                     | {}           |
| end_angle      | 仪表结束角度（度）                                                   | ^[float\|int]               | -45          |
| format         | 数值显示格式（支持{value}占位符）                                      | ^[str]                      | '{value}%'   |
| num_splits     | 仪表刻度分割数量                                                     | ^[int]                      | 10           |
| show_ticks     | 是否显示刻度线                                                       | ^[bool]                     | True         |
| show_labels    | 是否显示刻度标签                                                     | ^[bool]                     | True         |
| start_angle    | 仪表起始角度（度）                                                   | ^[float\|int]               | 225          |
| tooltip_format | 悬停提示框格式（{b}:名称, {c}:值）                                     | ^[str]                      | '{b}: {c}%'  |
| title_size     | 标题字体大小（像素）                                                  | ^[int]                      | 18           |

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |
| change | 当值变化时触发的事件   | ^[Callable]`(event: dict) -> None`     |




# Tqdm 进度指示器

Tqdm指示器包装了著名的[`tqdm`](https://github.com/tqdm/tqdm)进度指示器，并显示某个目标的进度。可以在笔记本或Panel Web应用程序中使用它。

[![Tqdm](https://raw.githubusercontent.com/tqdm/tqdm/master/images/logo.gif)](https://github.com/tqdm/tqdm)

底层实现为`panel.widgets.Tqdm`，参数基本一致，参考文档：https://panel.holoviz.org/reference/indicators/Tqdm.html


## 基本用法

要使用`Tqdm`指示器，只需实例化该对象，然后像使用`tqdm.tqdm`一样使用生成的变量，即可迭代任何可迭代对象：

```vue
<!-- --plugins vpanel --show-code -->
<template>
 <PnCol>
  <PnTqdm ref="tqdm_ref" />
  <PnButton name="Run Loop" @click="run_loop()" />
 </PnCol>
</template>

<script lang='py'>
import time
import numpy as np
import panel as pn
from vuepy import ref

tqdm_ref = ref(None)


def run_loop():
    tqdm = tqdm_ref.value.unwrap()
    for i in tqdm(range(0, 10), desc="My loop bar", leave=True, colour='#666666'):
        if pn.state._is_pyodide:
            # time.sleep does not work in pyodide
            np.random.random((10**6, 30))  
        else:
            time.sleep(0.2)
</script>

```


大多数[tqdm支持的参数](https://github.com/tqdm/tqdm#parameters)都可以传递给`Tqdm`指示器的call方法。

## 嵌套使用

当嵌套使用`Tqdm`指示器时，使用`margin`参数可以直观地表示嵌套级别。

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnCol>
    <PnTqdm ref="tqdm_outer_ref" />
    <PnTqdm ref="tqdm_inner_ref" :margin="(0, 0, 0, 20)" />
    <PnButton name="Run Nested Loop" @click="run_nested_loop()" />
  </PnCol>
</template>

<script lang='py'>
import time
import numpy as np
import panel as pn
from vuepy import ref

tqdm_outer_ref = ref(None)
tqdm_inner_ref = ref(None)

def run_nested_loop():
    tqdm_outer = tqdm_outer_ref.value.unwrap()
    tqdm_inner = tqdm_inner_ref.value.unwrap()
    for i in tqdm_outer(range(10)):
        for j in tqdm_inner(range(10)):
            if pn.state._is_pyodide:
                # time.sleep does not work in pyodide
                np.random.random((10**6, 30))  
            else:
                time.sleep(0.01)
</script>

```


## Pandas集成

要使用tqdm pandas集成，可以通过调用`tqdm.pandas`并传入所有配置选项来激活它。激活后，`progress_apply`方法在`pandas.DataFrame`上可用：

```vue
<!-- --plugins vpanel --show-code -->
<template>
 <PnCol>
  <PnTqdm ref="tqdm_pandas_ref" :width="500" />
  <PnButton name="Run Pandas Apply" button_type="success" @click="run_df()" />
 </PnCol>
</template>

<script lang='py'>
import numpy as np
import pandas as pd
from vuepy import ref

df = pd.DataFrame(np.random.randint(0, 100, (100000, 6)))
tqdm_pandas_ref = ref(None)

def run_df():
    tqdm_pandas = tqdm_pandas_ref.value.unwrap()
    # Register Pandas. This gives DataFrame.progress_apply method
    tqdm_pandas.pandas(desc="Pandas Progress")
    df.progress_apply(lambda x: x**2)
</script>

```


## API

### 属性

| 属性名          | 说明                           | 类型                                                          | 默认值 |
| -------------- | ----------------------------- | -------------------------------------------------------------| ------- |
| value          | 当前进度值                      | ^[number]                                                    | —       |
| max            | 最大进度值                      | ^[number]                                                    | —       |
| text           | 当前由tqdm输出的文本             | ^[string]                                                    | —       |
| layout         | `progress`指示器和`text_pane`的布局 | ^[object] Column或Row                                    | —       |
| progress       | 显示进度的Progress指示器         | ^[object]                                                    | —       |
| text_pane      | 显示进度`text`的Pane            | ^[object]                                                    | —       |
| write_to_console | 是否也写入控制台，仅在服务器上有效 | ^[boolean]                                                  | —       |
| disabled       | 是否禁用                        | ^[boolean]                                                   | false   |

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |
| change | 当值变化时触发的事件   | ^[Callable]`(event: dict) -> None`     |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |

### 方法

| 名称      | 说明                                   | 参数                                               |
| -------- | ------------------------------------- | --------------------------------------------------|
| pandas   | 注册Pandas，提供DataFrame.progress_apply | **kwargs: tqdm.pandas支持的参数                    |



# LinearGauge 线性仪表

线性仪表提供了某个范围内值的简单线性可视化表示。它类似于`Dial`和`Gauge`元素，但在视觉上更紧凑。

底层实现为`panel.widgets.LinearGauge`，参数基本一致，参考文档：https://panel.holoviz.org/reference/indicators/LinearGauge.html


## 基本用法

最简单的线性仪表只需要设置一个在指定范围内的`value`。默认的格式化器和范围假设你提供的是百分比值：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnLinearGauge name="Failure Rate" :value="30" :bounds="(0, 100)" />
</template>

```


## 自定义格式与颜色

如果我们想要显示其他值，例如发动机每分钟转速，我们可以设置不同的`bounds`值并重写`format`。此外，我们还可以提供一组不同的颜色，定义应在提供范围的哪个点上更改颜色。`colors`可以接受颜色列表或元组列表：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnLinearGauge 
    name="Engine" 
    :value="2500" 
    :bounds="(0, 3000)" 
    format="{value:.0f} rpm"
    :colors="['green', 'gold', 'red']" 
    :horizontal="True" 
    :width="125" 
  />
</template>

```


## 显示颜色边界

如果我们想要显示不同颜色之间的过渡点，我们也可以启用`show_boundaries`：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnLinearGauge 
    name="Engine" 
    :value="2800" 
    :bounds="(0, 3000)" 
    format="{value:.0f} rpm"
    :colors="[(0.2, 'green'), (0.8, 'gold'), (1, 'red')]" 
    show_boundaries
  />
</template>

```


## API

### 属性

| 属性名          | 说明                      | 类型                                                           | 默认值 |
| -------------- | ------------------------ | --------------------------------------------------------------| ------- |
| value          | 仪表上指示的值            | ^[number]                                                      | 25      |
| bounds         | 仪表的上下限              | ^[array]                                                       | [0, 100] |
| colors         | 仪表的颜色阈值            | ^[array] 可以是均匀分布的颜色列表或元组列表，每个元组包含阈值分数和切换颜色 | —       |
| default_color  | 如果未提供颜色阈值，使用的颜色 | ^[string]                                                   | lightblue |
| format         | 值指示器的格式化字符串     | ^[string]                                                      | {value}% |
| nan_format     | 如何格式化nan值           | ^[string]                                                      | -        |
| needle_color   | 指针的颜色                | ^[string]                                                      | black    |
| show_boundaries | 是否显示颜色之间的过渡    | ^[boolean]                                                     | false    |
| unfilled_color | 仪表未填充区域的颜色      | ^[string]                                                      | whitesmoke |
| horizontal     | 是否水平显示              | ^[boolean]                                                     | false    |
| show_value     | 是否显示值                | ^[boolean]                                                     | true     |
| disabled       | 是否禁用                  | ^[boolean]                                                     | false    |

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |
| change | 当值变化时触发的事件   | ^[Callable]`(event: dict) -> None`     |




# Progress 进度条

进度条组件根据当前`value`和`max`值显示朝着某个目标的进度。如果未设置`value`或设置为-1，则`Progress`组件处于不确定模式，若`active`设置为True，将会显示动画效果。

底层实现为`panel.widgets.Progress`，参数基本一致，参考文档：https://panel.holoviz.org/reference/indicators/Progress.html


## 基本用法

`Progress`组件可以使用或不使用值来实例化。如果给定`value`，进度条将根据`max`值（默认为100）的进度进行填充：

```vue
<!-- --plugins vpanel --show-code -->
<template>
 <PnCol>
  <PnProgress name="Progress" v-model="progress.value" :width="200" />
  <PnIntSlider v-model="progress.value" 
              :start="0" :end="100" name="Progress Value" />
 </PnCol>
</template>

<script lang='py'>
from vuepy import ref

progress = ref(20)
</script>

```


## 不确定状态

`Progress`也可以在不设置`value`的情况下实例化，显示不确定状态：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnProgress name="Indeterminate Progress" :active="True" :width="200" />
</template>

```


## 不同颜色

`Progress`组件支持多种条形颜色：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnCol>
    <PnRow v-for="(index, color) in bar_colors">
      <PnStaticText :value="color" :width="100" />
      <PnProgress :width="300" :value="10 + index * 10" :bar_color="color" />
    </PnRow>
  </PnCol>
</template>

<script lang='py'>
bar_colors = ['primary', 'secondary', 'success', 'info', 'warning', 'danger', 'light', 'dark']
</script>

```


## API

### 属性

| 属性名    | 说明                     | 类型                                                           | 默认值 |
| -------- | ----------------------- | ---------------------------------------------------------------| ------- |
| value    | 当前进度值，设置为-1表示不确定状态 | ^[number]                                               | —       |
| max      | 最大进度值               | ^[number]                                                      | 100     |
| active   | 在不确定模式下是否显示动画 | ^[boolean]                                                     | false   |
| bar_color | 条形的颜色              | ^[string] 可选值: 'primary', 'secondary', 'success', 'info', 'warning', 'danger', 'light', 'dark' | — |
| style    | 应用于进度条的CSS样式字典 | ^[object]                                                      | —       |
| disabled | 是否禁用                | ^[boolean]                                                      | false    |

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |
| change | 当值变化时触发的事件   | ^[Callable]`(event: dict) -> None`     |




# LoadingSpinner 加载旋转器

加载旋转器提供了加载状态的可视化表示。当`value`设置为`True`时，旋转部分会旋转；设置为`False`时，旋转部分会停止旋转。

底层实现为`panel.widgets.LoadingSpinner`，参数基本一致，参考文档：https://panel.holoviz.org/reference/indicators/LoadingSpinner.html


## 基本用法

`LoadingSpinner`可以实例化为旋转或静止状态：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnRow>
    <PnLoadingSpinner :value="False" name="Idle..." />
    <PnLoadingSpinner :value="True" :size="20" name="Loading..." />
  </PnRow>
</template>

```


## 颜色与背景

`LoadingSpinner`支持多种旋转部分颜色和背景：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <!--<PnGridBox :ncols="3">
    <PnLabel value="" />
    <PnLabel value="light" />
    <PnLabel value="dark" />-->
    <PnStaticText value="" />
    <PnStaticText value="light" />
    <PnStaticText value="dark" />
    
    <PnRow v-for="color in colors">
      <!--<PnLabel :value="color" />-->
      <PnStaticText :value="color" :width='80' />
      <PnLoadingSpinner :size="50" :value="True" :color="color" bgcolor="light" />
      <PnLoadingSpinner :size="50" :value="True" :color="color" bgcolor="dark" />
    </PnRow>
  <!--</PnGridBox>-->
</template>

<script lang='py'>
colors = ['primary', 'secondary', 'success', 'info', 'warning', 'danger', 'light', 'dark']
</script>

```


## API

### 属性

| 属性名    | 说明                 | 类型                                                           | 默认值 |
| -------- | ------------------- | ---------------------------------------------------------------| ------- |
| value    | 指示器是否旋转        | ^[boolean]                                                     | false   |
| color    | 旋转部分的颜色        | ^[string] 可选值: 'primary', 'secondary', 'success', 'info', 'warning', 'danger', 'light', 'dark' | — |
| bgcolor  | 旋转器背景部分的颜色  | ^[string] 可选值: 'light', 'dark'                              | —       |
| name     | 显示在旋转器旁边的标签 | ^[string]                                                      | —       |
| size     | 旋转器的大小（像素）   | ^[number]                                                      | —       |
| disabled | 是否禁用              | ^[boolean]                                                     | false   |

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |
| change | 当值变化时触发的事件   | ^[Callable]`(event: dict) -> None`     |




# Number 数字指示器

数字指示器提供了一个值的可视化表示，该值可以根据提供的阈值进行着色。

底层实现为`panel.widgets.Number`，参数基本一致，参考文档：https://panel.holoviz.org/reference/indicators/Number.html


## 基本用法

`Number`指示器可用于指示一个简单的数字，并根据需要进行格式化：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnNumber name="Failure Rate" :value="10" format="{value}%" />
</template>

```


## 颜色阈值

如果我们想要指定特定的阈值，在这些阈值下指示器会改变颜色：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnRow>
    <PnNumber 
      name="Failure Rate" 
      :value="10" 
      format="{value}%"
      :colors="[[33, 'green'], [66, 'gold'], [100, 'red']]" 
    />
    <PnNumber 
      name="Failure Rate" 
      :value="42" 
      format="{value}%"
      :colors="[[33, 'green'], [66, 'gold'], [100, 'red']]" 
    />
    <PnNumber 
      name="Failure Rate" 
      :value="93" 
      format="{value}%"
      :colors="[[33, 'green'], [66, 'gold'], [100, 'red']]" 
    />
  </PnRow>
</template>

```


## API

### 属性

| 属性名        | 说明                      | 类型                                                          | 默认值 |
| ------------ | ------------------------ | -------------------------------------------------------------| ------- |
| value        | 数字指示器的值             | ^[number]                                                     | —       |
| colors       | 数字指示器的颜色阈值        | ^[array] 指定为元组列表，每个元组包含绝对阈值和切换颜色         | —       |
| default_color | 如果未提供颜色阈值，使用的颜色 | ^[string]                                                  | black   |
| format       | 接受{value}的格式化字符串   | ^[string]                                                     | {value} |
| font_size    | 数字本身的大小             | ^[string]                                                     | 54pt    |
| nan_format   | 如何格式化nan值            | ^[string]                                                     | -       |
| title_size   | 数字标题的大小             | ^[string]                                                     | 18pt    |
| disabled     | 是否禁用                  | ^[boolean]                                                     | false   |

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |
| change | 当值变化时触发的事件   | ^[Callable]`(event: dict) -> None`     |




# BooleanStatus 布尔状态指示器

布尔状态指示器提供了布尔状态的可视化表示，以填充或非填充圆圈的形式展示。当`value`设置为`True`时，指示器将被填充；设置为`False`时，指示器将不被填充。

底层实现为`panel.widgets.BooleanStatus`，参数基本一致，参考文档：https://panel.holoviz.org/reference/indicators/BooleanStatus.html


## 基本用法

BooleanStatus组件可以实例化为`False`或`True`状态：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnRow>
    <PnBooleanStatus :value="False" />
    <PnBooleanStatus :value="True" />
  </PnRow>
</template>

```


## 颜色设置

BooleanStatus指示器支持多种颜色：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnRow>
    <PnStaticText value="" />
    <PnStaticText value="False" />
    <PnStaticText value="True" />
  </PnRow>
    
    <PnRow v-for="color in colors">
      <PnStaticText :value="color" :width='80' />
      <PnBooleanStatus :width="50" :height="50" :value="False" :color="color" />
      <PnBooleanStatus :width="50" :height="50" :value="True" :color="color" />
    </PnRow>
</template>

<script lang='py'>
colors = ['primary', 'secondary', 'success', 'info', 'warning', 'danger', 'light', 'dark']
</script>

```


## API

### 属性

| 属性名    | 说明                 | 类型                                                           | 默认值 |
| -------- | ------------------- | ---------------------------------------------------------------| ------- |
| value/`v-model`    | 指示器是否填充        | ^[boolean]                                                      | false   |
| color    | 指示器的颜色,可选值: 'primary', 'secondary', 'success', 'info', 'warning', 'danger', 'light', 'dark'          | ^[string]  | — |
| disabled | 是否禁用             | ^[boolean]                                                     | false   |

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |
| change | 当值变化时触发的事件   | ^[Callable]`(event: dict) -> None`     |




# Dial 刻度盘指示器

刻度盘指示器提供了一个简单的径向刻度盘来可视化表示数值。

底层实现为`panel.widgets.Dial`，参数基本一致，参考文档：https://panel.holoviz.org/reference/indicators/Dial.html


## 基本用法

最简单的刻度盘只需要设置一个在指定范围内的`value`。默认的格式化器和范围假设你提供的是百分比值：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnDial name="Failure Rate" :value="10" :bounds="(0, 100)" />
</template>

```


## 自定义格式与颜色阈值

如果我们想要显示其他值，例如发动机每分钟转速，我们可以设置不同的`bounds`值并重写`format`。此外，我们还可以提供一组不同的颜色，定义应在提供范围的哪个点上更改颜色。`colors`接受一个元组列表，定义分数和颜色：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnDial 
    name="Engine" 
    :value="2500" 
    :bounds="(0, 3000)" 
    format="{value} rpm"
    :colors="[[0.2, 'green'], [0.8, 'gold'], [1, 'red']]" 
  />
</template>

```


## API

### 属性

| 属性名            | 说明                                                                 | 类型                          | 默认值         |
|------------------|--------------------------------------------------------------------|-----------------------------|---------------|
| annulus_width    | 仪表环宽度（像素）                                                   | ^[int]                      | 10            |
| bounds           | 仪表数值范围（最小值, 最大值）                                         | ^[tuple]                    | (0, 100)      |
| colors           | 颜色阈值配置（[(阈值比例, 颜色), ...]）                                | ^[list]                     | []            |
| default_color    | 默认填充颜色（无颜色阈值时使用）                                        | ^[str]                      | 'lightblue'   |
| end_angle        | 仪表结束角度（度）                                                   | ^[float\|int]               | -45           |
| format           | 数值显示格式（支持{value}占位符）                                      | ^[str]                      | '{value}%'    |
| nan_format       | NaN值显示格式                                                       | ^[str]                      | '-'           |
| needle_color     | 指针颜色                                                            | ^[str]                      | 'black'       |
| needle_width     | 指针径向宽度（弧度）                                                  | ^[float]                    | 0.1           |
| start_angle      | 仪表起始角度（度）                                                   | ^[float\|int]               | 225           |
| tick_size        | 刻度标签字体大小                                                     | ^[int]                      | -             |
| title_size       | 标题字体大小                                                        | ^[int]                      | -             |
| unfilled_color   | 未填充区域颜色                                                       | ^[str]                      | 'whitesmoke'  |
| value            | 仪表当前值（需在bounds范围内）                                         | ^[float\|int]               | 25            |
| value_size       | 数值标签字体大小                                                     | ^[str]                      | -             |

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |
| change | 当值变化时触发的事件   | ^[Callable]`(event: dict) -> None`     |




# FlexBox 弹性布局

FlexBox是一种基于CSS Flexbox的列表式布局组件，提供了灵活的内容排列方式，可以自动换行和调整元素布局。

底层实现为`panel.layout.FlexBox`，参数基本一致，参考文档：https://panel.holoviz.org/reference/layouts/FlexBox.html


## 基本用法

默认情况下，FlexBox使用`direction='row'`和`flex_wrap='wrap'`，使得元素按行排列并在必要时换行：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnFlexBox>
    <PnHTML v-for="i in range(24)" 
            :object="str(i)" 
            :style="f'background: {rcolor()}; width:100px;height:100px'" 
    />
  </PnFlexBox>
</template>
<script lang='py'>
from vuepy import ref
import random

random.seed(7)

# Function to generate random colors
def rcolor():
    return "#%06x" % random.randint(0, 0xFFFFFF)
    
</script>

```


## 列式布局

可以通过设置`flex_direction='column'`让FlexBox按列排列元素：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnFlexBox flex_direction="column" :height='450'>
    <PnHTML v-for="i in range(24)" 
            :object="str(i)" 
            :style="f'background: {rcolor()}; width:100px;height:100px'" 
    />
  </PnFlexBox>
</template>
<script lang='py'>
from vuepy import ref
import random

random.seed(7)
# Function to generate random colors
def rcolor():
    return "#%06x" % random.randint(0, 0xFFFFFF)
</script>

```


## 元素对齐方式

可以通过`align_content`、`align_items`和`justify_content`控制元素如何在容器中对齐和分布：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
    <PnCol>
      <PnMarkdown>
       ##### justify_content: space-between
      </PnMarkdown>
      <PnFlexBox justify_content="space-between" style='background: #f5f5f5'>
         <PnHTML v-for="i in range(3)" 
            :object="str(i)" 
            :style="f'background: {rcolor()}; width:100px;height:100px'" 
         />
      </PnFlexBox>
    </PnCol>
    
    <PnCol>
      <PnMarkdown>
       ##### align_items: center
      </PnMarkdown>
      <PnFlexBox align_items="center" align_content="center" style='background: #f5f5f5'>
         <PnHTML v-for="i in range(3)" 
            :object="str(i)" 
            :style="f'background: {rcolor()}; width:100px;height:100px'" 
         />
      </PnFlexBox>
    </PnCol>
</template>
<script lang='py'>
from vuepy import ref
import random

# Function to generate random colors
def rcolor():
    return "#%06x" % random.randint(0, 0xFFFFFF)
</script>

```


## API

### 属性

| 属性名                | 说明                                       | 类型                | 默认值  |
|---------------------|-------------------------------------------|---------------------|--------|
| direction           | 主轴方向，决定了flex项目放置的方向            | ^[String]           | row   |
| flex_direction      | 与direction相同，为了兼容性保留                | ^[String]           | row   |
| align_content       | 当交叉轴有多余空间时，如何分配行之间的空间      | ^[String]           | —      |
| align_items         | 定义项目在交叉轴上如何对齐                    | ^[String]           | —      |
| flex_wrap           | 是否允许换行及如何换行                       | ^[String]           | wrap   |
| gap                 | 定义flex项目之间的间距                       | ^[String]           | —      |
| justify_content     | 定义项目在主轴上的对齐方式                    | ^[String]           | —      |
| scroll              | 是否启用滚动条                              | ^[Boolean]          | False  |

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |
| change | 当布局内容改变时触发   | ^[Callable]`(event: dict) -> None` |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | FlexBox的内容      |




# Divider 分割线

分割线用于分隔内容，在视觉上创建一个水平分隔，自动占据容器的全宽。

底层实现为`panel.layout.Divider`，参数基本一致，参考文档：https://panel.holoviz.org/reference/layouts/Divider.html


## 基本用法

使用分割线将不同组件清晰地分隔开：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnCol :width='400' style='background: whitesmoke'>
    <PnMarkdown>
      # Lorem Ipsum
    </PnMarkdown>
    <PnDivider />
    <PnMarkdown>
      Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt
      ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation 
      ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in
      reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
      Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt
      mollit anim id est laborum.  
      $$ x^{2} - 1 $$
    </PnMarkdown>
  </PnCol>
</template>

```


## 响应式布局

启用响应式尺寸后，分割线会自动占据全宽：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnColumn sizing_mode="stretch_width">
    <PnMarkdown>
      ## Slider
    </PnMarkdown>
    <PnDivider :margin="(-20, 0, 0, 0)" />
    <PnRow>
      <PnFloatSlider name="Float" />
      <PnIntSlider name="Int" />
      <PnRangeSlider name="Range" />
      <PnIntRangeSlider name="Int Range" />
    </PnRow>
    <PnMarkdown>
      ## Input
    </PnMarkdown>
    <PnDivider :margin="(-20, 0, 0, 0)" />
    <PnRow>
      <PnTextInput name="Text" />
      <PnDatetimeInput name="Date" />
      <PnPasswordInput name="Password" />
      <PnNumberInput name="Number" />
    </PnRow>
  </PnColumn>
</template>
<script lang='py'>
from vuepy import ref
import panel as pn

pn.config.sizing_mode = 'stretch_width'
</script>

```


## API

### 属性

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| style | 分割线的样式 | ^[Object] | — |
| margin | 分割线的外边距 | ^[Tuple] | — |




# Row 行容器

Row 允许在水平容器中排列多个组件。它拥有类似列表的 API，包含 append 、 extend 、 clear 、 insert 、 pop 、 remove 和 __setitem__ 方法，从而可以交互式地更新和修改布局

底层实现为`panel.Row`，参数基本一致，参考文档：https://panel.holoviz.org/reference/layouts/Row.html


## 基本用法

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnRow>
    <PnTextInput name="Text:" />
    <PnIntSlider name="Slider" />
  </PnRow>
</template>
<script lang='py'>
from vuepy import ref
</script>

```


## API

### 属性

| 属性名    | 说明                 | 类型   | 默认值 |
| -------- | ------------------- | ------ | ------ |
| objects  | List of child nodes  | list   | —      |
| scroll   | Enable scrollbars    | bool   | False  |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | Custom content     |





# Feed 信息流

Feed组件继承自Column布局，允许在垂直容器中排列多个组件，但限制了任何时刻渲染的对象数量，适用于显示大量条目。

底层实现为`panel.layout.Feed`，参数基本一致，参考文档：https://panel.holoviz.org/reference/layouts/Feed.html


## 基本用法

Feed组件可以显示大量条目，但只会加载和渲染当前可见的部分和缓冲区内的内容：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnFeed :load_buffer="20" :height="300">
    <PnMarkdown v-for="i in range(0, 100)">
      Content for item {{ i }}
    </PnMarkdown>
  </PnFeed>
</template>
<script lang='py'>
from vuepy import ref
</script>

```


## 初始化显示最新条目

通过设置`view_latest=True`，可以让Feed在初始化时显示最新条目：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnFeed :view_latest="True" :height="300">
    <PnMarkdown v-for="i in range(0, 100)">
      Content for item {{ i }}
    </PnMarkdown>
  </PnFeed>
</template>
<script lang='py'>
from vuepy import ref
</script>

```


## 添加滚动按钮

通过设置`scroll_button_threshold`，可以让Feed显示一个可点击的滚动按钮，帮助用户快速滚动到底部：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnFeed :scroll_button_threshold="20" :width="300" :height="300">
    <PnMarkdown v-for="i in range(0, 100)">
      Content for item {{ i }}
    </PnMarkdown>
  </PnFeed>
</template>
<script lang='py'>
from vuepy import ref
</script>

```


## API

### 属性

| 属性名                 | 说明                                       | 类型                | 默认值  |
|----------------------|-------------------------------------------|---------------------|--------|
| v-model              | 当前的posts数据                              | ^[Array]            | []     |
| load_buffer          | 可见对象两侧加载的对象数量                    | ^[Number]           | —      |
| scroll               | 是否启用滚动条                              | ^[Boolean]          | True |
| scroll_position      | 当前滚动位置                                | ^[Number]           | —      |
| auto_scroll_limit    | 自动滚动激活的最大像素距离                   | ^[Number]           | —      |
| scroll_button_threshold | 显示滚动按钮的最小像素距离                | ^[Number]           | —      |
| view_latest          | 初始化时是否滚动到最新对象                   | ^[Boolean]          | False |
| visible_range        | 当前可见Feed对象的上下边界（只读）            | ^[Array]            | —      |

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |
| change | 当Feed内容改变时触发   | ^[Callable]`(event: dict) -> None` |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | Feed的内容         |

### 方法

| 方法名 | 说明 | 类型 |
| --- | --- | --- |
| scroll_to | 滚动到指定索引的对象 | ^[Function]`(index: int) -> None` |




# Column 垂直布局

Column组件允许在垂直容器中排列多个组件。

底层实现为`panel.layout.Column`，参数基本一致，参考文档：https://panel.holoviz.org/reference/layouts/Column.html


## 基本用法

Column组件可以垂直排列多个元素。

`Col`是`Column`的同名组件。
```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnCol style="background: WhiteSmoke">
    <PnTextInput name="Text:" />
    <PnFloatSlider name="Slider" />
    <PnSelect :options="['A', 'B', 'C']" />
  </PnCol>
</template>
<script lang='py'>
from vuepy import ref
</script>

```


## 固定尺寸

可以给Column设置固定的宽度和高度，内部元素会根据布局模式进行调整。

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnColumn :height="300" :width="200">
    <PnSpacer style="background: red" sizing_mode="stretch_both" />
    <PnSpacer style="background: green" sizing_mode="stretch_both" />
    <PnSpacer style="background: blue" sizing_mode="stretch_both" />
  </PnColumn>
</template>
<script lang='py'>
from vuepy import ref
</script>

```


## 自适应宽度

当没有指定固定尺寸时，Column会根据其内容的大小自动调整。

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnColumn>
    <PnSpacer style="background: red; " />
    <PnSpacer style="background: green" sizing_mode="stretch_both" />
    <PnDisplay :obj="p1" />
    <PnDisplay :obj="p2" />
  </PnColumn>
</template>
<script lang='py'>
from vuepy import ref
from bokeh.plotting import figure

p1 = figure(height=150, sizing_mode='stretch_width')
p2 = figure(height=150, sizing_mode='stretch_width')

p1.line([1, 2, 3], [1, 2, 3])
p2.scatter([1, 2, 3], [1, 2, 3])
</script>

```


## 启用滚动条

当内容超出容器大小时，可以启用滚动条。

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnColumn scroll :height="420">
    <PnSpacer style="background: red" :width="200" :height="200" />
    <PnSpacer style="background: green" :width="200" :height="200" />
    <PnSpacer style="background: blue" :width="200" :height="200" />
  </PnColumn>
</template>
<script lang='py'>
from vuepy import ref
</script>

```


## API

### 属性

| 属性名                 | 说明                                       | 类型                | 默认值  |
|----------------------|-------------------------------------------|---------------------|--------|
| scroll               | 是否启用滚动条                              | ^[Boolean]          | False  |
| scroll_position      | 当前滚动位置                                | ^[Number]           | —      |
| auto_scroll_limit    | 自动滚动激活的最大像素距离                   | ^[Number]           | —      |
| scroll_button_threshold | 显示滚动按钮的最小像素距离                | ^[Number]           | —      |
| view_latest          | 初始化时是否滚动到最新对象                   | ^[Boolean]          | False  |

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |
| change | 当布局内容改变时触发   | ^[Callable]`(event: dict) -> None` |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | Column的内容       |

### 方法

| 方法名 | 说明 | 类型 |
| --- | --- | --- |
| scroll_to | 滚动到指定索引的对象 | ^[Function]`(index: int) -> None` |




# Swipe 滑动对比布局

滑动对比布局使您能够快速比较两个面板，通过滑块控制显示前后两个面板的比例。

底层实现为`panel.layout.Swipe`，参数基本一致，参考文档：https://panel.holoviz.org/reference/layouts/Swipe.html


## 基本用法

Swipe布局可以接受任意两个对象进行比较，为了获得最佳效果，这两个对象应具有相同的尺寸设置。

以下示例比较了1945-1949年和2015-2019年的平均地表温度图像：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnSwipe :before="gis_1945" :after="gis_2015" />
</template>
<script lang='py'>
from vuepy import ref

# URLs of images to compare
gis_1945 = 'https://earthobservatory.nasa.gov/ContentWOC/images/globaltemp/global_gis_1945-1949.png'
gis_2015 = 'https://earthobservatory.nasa.gov/ContentWOC/images/globaltemp/global_gis_2015-2019.png'
</script>

```


## 比较数据可视化

该布局可以比较任何类型的组件，例如，我们可以比较两个小提琴图：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnSwipe :before="plot1" :after="plot2" :value="51" />
</template>
<script lang='py'>
import pandas as pd
import hvplot.pandas
from vuepy import ref

# Load dataset
penguins = pd.read_csv('https://datasets.holoviz.org/penguins/v1/penguins.csv')

# Create plots to compare
plot1 = penguins[penguins.species=='Chinstrap'].hvplot.violin('bill_length_mm', color='#00cde1')
plot2 = penguins[penguins.species=='Adelie'].hvplot.violin('bill_length_mm', color='#cd0000')
</script>

```


## 自定义滑块样式

您可以自定义滑块的宽度和颜色：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnRow>
    <PnSwipe :before="gis_1945" :after="gis_2015" :slider_width="20" slider_color="red" />
  </PnRow>
</template>
<script lang='py'>
from vuepy import ref

# URLs of images to compare
gis_1945 = 'https://earthobservatory.nasa.gov/ContentWOC/images/globaltemp/global_gis_1945-1949.png'
gis_2015 = 'https://earthobservatory.nasa.gov/ContentWOC/images/globaltemp/global_gis_2015-2019.png'
</script>

```


## API

### 属性

| 属性名        | 说明                            | 类型            | 默认值    |
| ------------ | ------------------------------- | --------------- | --------- |
| before       | 左侧显示的组件                   | ^[any]          | —         |
| after        | 右侧显示的组件                   | ^[any]          | —         |
| value        | 右侧面板显示的百分比              | ^[int]          | 50        |
| slider_width | 滑块的宽度（像素）                | ^[int]          | 12        |
| slider_color | 滑块的颜色                       | ^[str]          | 'black'   |
| width        | 组件宽度                         | ^[int, str]     | —         |
| height       | 组件高度                         | ^[int, str]     | —         |
| margin       | 组件边距                         | ^[int, tuple]   | —         |
| css_classes  | 应用于组件的CSS类                 | ^[list]         | []        |

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |
| change | 当滑块值改变时触发     | ^[Callable]`(value: int) -> None`      |




# WidgetBox 组件容器

用于分组小部件的垂直容器，具有默认样式。

底层实现为`panel.WidgetBox`，参数基本一致，参考文档：https://panel.holoviz.org/reference/layouts/WidgetBox.html


## 基本用法

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnWidgetBox>
    <PnTextInput name="Text:" />
    <PnIntSlider name="Slider" />
  </PnWidgetBox>
</template>
<script lang='py'>
from vuepy import ref
</script>

```


## API

### 属性

| 属性名     | 说明                                                                 | 类型           | 默认值   |
|----------|--------------------------------------------------------------------|--------------|--------|
| objects  | 组件框内显示的对象列表（通常应整体替换而非直接修改）                       | ^[list]      | []     |
| disabled | 是否禁用组件框内的所有控件                                               | ^[bool]      | False  |

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |
|       |                      |                                        |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | Custom content     |

### 方法

| 属性名 | 说明 | 类型 |
| --- | --- | --- |





# GridStack 可拖拽网格

GridStack布局允许将多个Panel对象排列在网格中，并支持用户拖拽和调整单元格大小。

底层实现为`panel.layout.GridStack`，参数基本一致，参考文档：https://panel.holoviz.org/reference/layouts/GridStack.html


## 基本用法

GridStack可以创建可拖拽和调整大小的网格布局：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnGridStack :height="300" :width='300'>
    <PnGridStackItem :row_start="0" :row_end="3" :col_start="0" :col_end="1">
      <PnSpacer style="background: red" />
    </PnGridStackItem>
    
    <PnGridStackItem :row_start="0" :row_end="1" :col_start="1" :col_end="3">
      <PnSpacer style="background: green" />
    </PnGridStackItem>
    
    <PnGridStackItem :row_start="1" :row_end="2" :col_start="2" :col_end="4">
      <PnSpacer style="background: orange" />
    </PnGridStackItem>
    
    <PnGridStackItem :row_start="2" :row_end="3" :col_start="1" :col_end="4">
      <PnSpacer style="background: blue" />
    </PnGridStackItem>
    
    <PnGridStackItem :row_start="0" :row_end="1" :col_start="3" :col_end="4">
      <PnSpacer style="background: purple" />
    </PnGridStackItem>
  </PnGridStack>
</template>

```


## 响应式网格

通过设置合适的响应式布局参数，GridStack可以适应不同的屏幕尺寸：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnGridStack :width='600' :height='400'>
    <PnGridStackItem :row_start="0" :row_end="1" :col_start="0" :col_end="3">
      <PnSpacer style="background: #FF0000" />
    </PnGridStackItem>
    
    <PnGridStackItem :row_start="1" :row_end="3" :col_start="0" :col_end="1">
      <PnSpacer style="background: #0000FF" />
    </PnGridStackItem>
    
    <PnGridStackItem :row_start="1" :row_end="3" :col_start="1" :col_end="3">
      <PnDisplay :obj="fig" />
    </PnGridStackItem>
    
    <PnGridStackItem :row_start="3" :row_end="5" :col_start="0" :col_end="1">
      <PnDisplay :obj="hv.Curve([1, 2, 3])" />
    </PnGridStackItem>

<!--
    <PnGridStackItem :row_start="3" :row_end="5" :col_start="1" :col_end="2">
      <PnImage :object="image_url" />
    </PnGridStackItem>
-->

    <PnGridStackItem :row_start="3" :row_end="5" :col_start="2" :col_end="3">
      <PnColumn>
        <PnFloatSlider />
        <PnColorPicker />
        <PnToggle name="Toggle Me!" />
      </PnColumn>
    </PnGridStackItem>
  </PnGridStack>
</template>
<script lang='py'>
from vuepy import ref
import holoviews as hv
from bokeh.plotting import figure

fig = figure()
fig.scatter([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 1, 2, 3, 2, 1, 0, -1, -2, -3])

image_url = "https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png"
</script>

```


## 禁用拖拽或调整大小

可以通过设置`allow_drag`和`allow_resize`参数来控制是否允许拖拽和调整大小：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnCol>
    <PnMarkdown>
      ### 禁用拖拽和调整大小
    </PnMarkdown>
    <PnGridStack :allow_drag="False" :allow_resize="False" :height="200" :width="200">
      <PnGridStackItem :row_start="0" :row_end="1" :col_start="0" :col_end="1">
        <PnCard title="Card 1">Fixed position and size</PnCard>
      </PnGridStackItem>
      <PnGridStackItem :row_start="0" :row_end="1" :col_start="1" :col_end="2">
        <PnCard title="Card 2">Fixed position and size</PnCard>
      </PnGridStackItem>
    </PnGridStack>

    <PnMarkdown>
      ### 只允许拖拽，不允许调整大小
    </PnMarkdown>
    <PnGridStack :allow_drag="True" :allow_resize="False" :height="200" :width="200">
      <PnGridStackItem :row_start="0" :row_end="1" :col_start="0" :col_end="1">
        <PnCard title="Card 1">Can drag but not resize</PnCard>
      </PnGridStackItem>
      <PnGridStackItem :row_start="0" :row_end="1" :col_start="1" :col_end="2">
        <PnCard title="Card 2">Can drag but not resize</PnCard>
      </PnGridStackItem>
    </PnGridStack>
    
    <PnMarkdown>
      ### 只允许调整大小，不允许拖拽
    </PnMarkdown>
    <PnGridStack :allow_drag="False" :allow_resize="True" :height="200" :width="200">
      <PnGridStackItem :row_start="0" :row_end="1" :col_start="0" :col_end="1">
        <PnCard title="Card 1">Can resize but not drag</PnCard>
      </PnGridStackItem>
      <PnGridStackItem :row_start="0" :row_end="1" :col_start="1" :col_end="2">
        <PnCard title="Card 2">Can resize but not drag</PnCard>
      </PnGridStackItem>
    </PnGridStack>
  </PnCol>
</template>
<script lang='py'>
from vuepy import ref
</script>

```


## GridStack API

### 属性

| 属性名        | 说明                                       | 类型                | 默认值  |
|--------------|-------------------------------------------|---------------------|--------|
| allow_resize | 是否允许调整网格单元格大小                   | ^[Boolean]          | True   |
| allow_drag   | 是否允许拖动网格单元格                       | ^[Boolean]          | True   |
| ncols        | 固定列数                                    | ^[Number]           | 3     |
| nrows        | 固定行数                                    | ^[Number]           | 5      |
| mode         | 重叠分配时的行为模式（warn、error、override） | ^[String]           | warn   |

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |
| change | 当网格内容改变时触发   | ^[Callable]`(event: dict) -> None` |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | GridStack的内容，通过PnGridStackItem组件包裹 |

## GridStackItem API

### 属性

| 属性名        | 说明                             | 类型    | 默认值  |
|--------------|-------------------------------------------|---------------------|--------|
| row_start    | 开始行的索引                      | ^[Number]           | 0 |
| row_end      | 结束行的索引，开区间               | ^[Number]           | `row_start+1` |
| col_start    | 开始列的索引                      | ^[Number]           | 0 |
| col_end      | 结束列的索引，开区间               | ^[Number]           | `col_start+1` |


### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | 默认内容 |




# GridBox 网格布局

GridBox是一种列表式布局，将对象按照指定的行数和列数包装成网格。

底层实现为`panel.layout.GridBox`，参数基本一致，参考文档：https://panel.holoviz.org/reference/layouts/GridBox.html


## 基本用法

GridBox可以将元素按指定的列数排列，自动换行形成网格：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnGridBox :ncols="6">
    <PnHTML v-for="i in range(24)"
            :object='str(i)'
            :style="f'background: {rcolor()};width:50px;height:50px;'" 
    />
  </PnGridBox>
</template>
<script lang='py'>
from vuepy import ref
import random

random.seed(7)
def rcolor():
    return "#%06x" % random.randint(0, 0xFFFFFF)
</script>

```


## 动态调整列数

可以动态地调整GridBox的列数，从而改变网格的排列：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnColumn>
    <PnRow>
      <PnButton name="2" @click="ncols(2)" />
      <PnButton name="3" @click="ncols(3)" />
      <PnButton name="4" @click="ncols(4)" />
      <PnButton name="6" @click="ncols(6)" />
    </PnRow>
    <PnGridBox :ncols="columns.value">
        <PnHTML v-for="i in range(24)"
                :object='str(i)'
                :style="f'background: {rcolor()};width:50px;height:50px;'" 
        />
    </PnGridBox>
  </PnColumn>
</template>
<script lang='py'>
from vuepy import ref
import random

random.seed(7)
columns = ref(4)

def ncols(n):
    columns.value = n

def rcolor():
    return "#%06x" % random.randint(0, 0xFFFFFF)
</script>

```


## 按行数排列

除了指定列数，也可以使用`nrows`指定行数：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnGridBox :nrows="4">
    <PnHTML v-for="i in range(24)"
            :object='str(i)'
            :style="f'background: {rcolor()};width:50px;height:50px;'" 
    />
  </PnGridBox>
</template>
<script lang='py'>
from vuepy import ref
import random

# Function to generate random colors
def rcolor():
    return "#%06x" % random.randint(0, 0xFFFFFF)
</script>

```


## API

### 属性

| 属性名   | 说明        | 类型        | 默认值  |
|---------|------------|-------------|--------|
| ncols   | 列数        | ^[Number]   | —      |
| nrows   | 行数        | ^[Number]   | —      |
| scroll  | 是否启用滚动条 | ^[Boolean] | False  |

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |
| change | 当布局内容改变时触发   | ^[Callable]`(event: dict) -> None` |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | GridBox的内容      |




# FloatPanel 浮动面板

FloatPanel提供一个可拖动的容器，可以放置在其父容器内部或完全自由浮动。

底层实现为`panel.layout.FloatPanel`，参数基本一致，参考文档：https://panel.holoviz.org/reference/layouts/FloatPanel.html


## 基本用法

浮动面板可以包含在父容器内：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnColumn :height="250">
    <PnMarkdown>
      **Example: Basic `FloatPanel`**
    </PnMarkdown>
    <PnFloatPanel name="Basic FloatPanel" :margin="20">
      <PnTextInput name="Text:" />
    </PnFloatPanel>
  </PnColumn>
</template>

```


## 自由浮动

浮动面板也可以配置为自由浮动，不受父容器限制：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnFloatPanel name="Free Floating FloatPanel" 
               :contained="False" 
               position="center">
    <p>
      Try dragging me around.
    </p>
  </PnFloatPanel>
</template>
<script lang='py'>
from vuepy import ref
</script>

```


## 自定义配置

FloatPanel可以通过`config`参数进行高度自定义，比如移除关闭按钮：

要了解更多配置选项，请查看 [jsPanel 文档](https://jspanel.de/)

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnColumn :height="200">
    <PnMarkdown>
      Example: `FloatPanel` without *close button*
    </PnMarkdown>
    <PnFloatPanel name="FloatPanel without close button" 
                 :margin="20" 
                 :config="config">
      <PnMarkdown>
        You can't close me!
      </PnMarkdown>
    </PnFloatPanel>
  </PnColumn>
</template>
<script lang='py'>
from vuepy import ref

# Custom configuration to remove close button
config = {"headerControls": {"close": "remove"}}
</script>

```


## 状态控制

可以通过`status`属性控制FloatPanel的状态：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnColumn>
    <PnRow>
      <PnButton name="Norm" @click="set_normal()" />
      <PnButton name="Max" @click="set_max()" />
      <PnButton name="Min" @click="set_min()" />
      <PnButton name="Small" @click="set_small()" />
      <PnButton name="Closed" @click="set_closed()" />
    </PnRow>
    <PnFloatPanel name="FloatPanel with Status Control" 
                 v-model="status.value"
                 :contained="False"
                 @change="handle_change">
      <PnMarkdown>
        Try changing my status with the buttons above.
      </PnMarkdown>
    </PnFloatPanel>
  </PnColumn>
</template>
<script lang='py'>
from vuepy import ref

status = ref("normalized")

def set_normal():
    status.value = 'normalized'

def set_max():
    status.value = 'maximized'
    
def set_min():
    status.value = 'minimized'
    
def set_small():
    status.value = 'smallified'
    
def set_closed():
    status.value = 'closed'

def handle_change(event):
    print(event.new)
</script>

```


## API

### 属性


| 属性名        | 说明                     | 类型           | 默认值        |
|-------------|---------------------------|--------------|--------------|
| contained   | 组件是否包含在父容器内（否则自由浮动）| ^[bool]                     | True |
| config      | 优先级高于参数值的额外jsPanel配置   | ^[dict]                     | {}           |
| objects     | 列中显示的对象列表（通常不应直接修改）| ^[list]                     | []           |
| position    | 自由浮动时的初始位置               | ^[str]                      | -            |
| offsetx     | 水平偏移量（像素）                 | ^[int]                      | 0            |
| offsety     | 垂直偏移量（像素）                 | ^[int]                      | 0            |
| theme       | 主题样式（内置选项/颜色值/Material Design颜色系统，可带修饰符） | ^[str]                      | 'default'    |
| v-model/status      | 面板当前状态（"normalized"/"maximized"/"minimized"等） | ^[str]                      | 'normalized' |

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |
| change | 当面板状态改变时触发   | ^[Callable]`(event: dict) -> None` |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | 浮动面板内容        |




# Accordion 折叠面板

折叠面板将内容区域组织进多个折叠面板，通过点击面板的标题可以展开或收缩内容。

底层实现为`panel.layout.Accordion`，参数基本一致，参考文档：https://panel.holoviz.org/reference/layouts/Accordion.html


## 基本用法

折叠面板可以包含任意数量的子项，每个子项可以包含任意内容。

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnAccordion v-model="active.value" @change='on_change'>
    <PnAccordionItem name="Scatter Plot">
      <!--<PnDisplay :obj="p1" />-->
      <PnButton name='accordion item1'/>
    </PnAccordionItem>
    <PnAccordionItem name="Line Plot">
      <!--<PnDisplay :obj="p2" />-->
      <PnButton name='accordion item2'/>
    </PnAccordionItem>
    <PnAccordionItem name="Square Plot">
      <!--<PnDisplay :obj="p3" />-->
      <PnButton name='accordion item3'/>
    </PnAccordionItem>
  </PnAccordion>
  <p>active: {{ active.value }} </p>
</template>
<script lang='py'>
from vuepy import ref
from bokeh.plotting import figure

# Create sample figures
p1 = figure(width=300, height=300, margin=5)
p1.scatter([0, 1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 2, 1, 0])

p2 = figure(width=300, height=300, margin=5)
p2.line([0, 1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 2, 1, 0])

p3 = figure(width=300, height=300, margin=5)
p3.scatter([0, 1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 2, 1, 0], marker='square', size=10)

# Define active panels (can be multiple when toggle is False)
active = ref([0, 2])

def on_change(event):
    print(event.new)
</script>

```


## 切换模式

当`toggle`属性设置为`True`时，同一时间只能展开一个面板。

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnAccordion :toggle="True" v-model="active.value" @change='on_change'>
    <PnAccordionItem name="Panel 1">
      <PnButton name='Panel1'/>
    </PnAccordionItem>

    <PnAccordionItem name="Panel 2">
      <PnButton name='Panel2'/>
    </PnAccordionItem>

    <PnAccordionItem name="Panel 3">
      <PnButton name='Panel3'/>
    </PnAccordionItem>
  </PnAccordion>
  <p>active: {{ active.value }} </p>
</template>
<script lang='py'>
from vuepy import ref

# When toggle=True, only one panel can be active
active = ref([0])

def on_change(event):
    print(event.new)
</script>

```


## Accordion API

### 属性

| 属性名                   | 说明                                    | 类型                | 默认值  |
|------------------------|----------------------------------------|---------------------|--------|
| v-model                | 当前激活的面板索引列表                     | ^[Array]            | []     |
| toggle                 | 是否在面板之间切换，只激活一个面板           | ^[Boolean]          | True   |
| scroll                 | 启用滚动条                               | ^[Boolean]          | False  |
| active_header_background | 展开面板时的标题背景颜色                  | ^[String]           | —      |
| header_color           | 标题文本颜色                             | ^[String]           | —      |
| header_background      | 标题背景颜色                             | ^[String]           | —      |

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |
| change | 当激活的面板改变时触发  | ^[Callable]`(event: dict) -> None` |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | 折叠面板内容，应该是 PnAccordionItem 组件 |

### 方法

| 方法名 | 说明 | 类型 |
| --- | --- | --- |
| append | 添加面板 | ^[Callable]`(any) -> None` |
| insert | 插入面板 | ^[Callable]`(idx: int, any) -> None` |
| remove | 移除面板 | ^[Callable]`(idx: int) -> any` |

## Accordion Item API

### 属性

| 属性名        | 说明                 | 类型                                                           | 默认值 |
| --------     | ------------------- | ---------------------------------------------------------------| ------- |
| name | 面板标题 | ^[str]                                                       | —       |

### Slots

| 插槽名   | 说明               | 
| ---     | ---               |
| default | 自定义默认内容      |



# Modal 模态框

Modal 布局在布局顶部提供了一个对话框窗口。它基于 [a11y-dialog](https://a11y-dialog.netlify.app/) 构建。它拥有类似列表的 API，包含`append`, `extend`, `clear`, `insert`, `pop`, `remove`, `__setitem__`方法，从而可以交互式地更新和修改布局。其中的组件以列的形式布局。

底层实现为`panel.layout.Modal`，参数基本一致，参考文档：https://panel.holoviz.org/reference/layouts/Modal.html


## 基本用法

Modal 组件以对话框叠加层的形式展示内容。通过 `open` 属性控制显示状态，您可以通过插槽添加任意内容。
<img style='width:400px' src="data:image/png;base64,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X3/JQQcdJBEzPZyfhQDspybnQgABBBBAAIFqFyAA57gDCg3AGzdulKefftoOxNZTjR49WubPn28Hfp933nnJs+/YsUMuvPBC6e3ttUMZ7r///uQ+XdizZ4/d397eLvq9e+65R/QYHfqgwdotGrC13HHHHXLxxRe7m0XHCet4Zn04j4IAAggggAACCCCQW4AAnMOmkADc2tpqQ+v+/fuznuXOO++UJUuWJPe98MIL8vjjj9v1N998U2bNmpXcd++994pu0wD9xRdfyIQJE+Tmm2+WDz/8MHmMd0Gn/bjyyivtpu+++04uv/xyu/zkk0/K+eef7z2UZQQQQAABBBBAAAGPAAHYg+FdHCwA//nnn3LuueeK9uxOnjxZNMAef/zx8scff8jrr78u7rjhF198UU4//XR7ah0msXDhQvn5559tT+1HH30ko8y8yT/++KPdrgdpSD7jjDPs8fqAnk4kfcstt8hnn30m//rXv+Spp56y+3QKNneohfZA639aLrjgAnniiSfsMn8ggAACCCCAAAIIZAoQgDNN7JbBArBO7qxhVHtsdZiCd+iBBl3t+dU58GbOnCkrV65MXuX3339Pzou3dOlS28u7YMEC2bJlS87wOtgY4N9++81er7OzU5599lkbxJMXZAEBBBBAAAEEEEAgRYAAnMIxsDJYANaAqxMwX3PNNXa87sA3E0s6993ixYvtig6VcHtrdcPbb78td999t92nU5tpgNaxvZ9//rmMHTvWbvf+MVgA1mPdF3mEPG/h856DZQQQQAABBBBAAIGEAAE4x50wWAA+8sgjk9/USZ7Ty6+//io//PCD3axDHaZMmZI8RMPqtddeKxqS3fLGG2/IKaec4q6mfBYSgFO+wAoCCCCAAAIIIIBATgECcA6afAG4ra1NTjjhhBzfzNz86quvyrx581J2bN68WXTog5Zjjz1W3n///ZT93hUCsFeDZQQQQAABBBBAYGgCBOAcfvkCsI7xbWlpsd/U3l998Cxb0SnPotGoHHXUURlDG2699daU0PvKK6/Y6dOynYcAnE2FbQgggAACCCCAQGkCBOAcbvkCsH5l0aJF8u2334o+yHb77bfnOEv2zfpO7Ouvv97u1JkddIYHHQP86aefyvjx4zO+RADOIGEDAggggAACCCBQsgABOAfdYAH4scceE53iTIPrmjVrZOLEiSln0pkZ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AQgggAACCCCAAAIFESAAF+RGcBkIIIAAAggggAAC9REgANfHmbMggAACCCCAAAIIFESAAFyQG8FlIIAAAggggAACCNRHgABcH2fOggACCCCAAAIIIFAQAQJwQW4El4EAAggggAACCCBQHwECcH2cOQsCCCCAAAIIIIBAQQQIwAW5EVwGAggggAACCCCAQH0ECMD1ceYsCCCAAAIIIIAAAgURIAAX5EZwGQgggAACCCCAAAL1ESAA18eZsyCAAAIIIIAAAggURIAAXJAbwWUggAACCCCAAAII1EeAAFwfZ86CAAIIIIAAAgggUBABAnBBbgSXgQACCCCAAAIIIFAfAQJwHzpv2LAhLF++PAwfPrwPz0LXCCCAAAIIIIAAArUIEIBTWgqtM2fODP/4xz/CG2+8EXbcccew5557hve+971h2223Te29afHEE0+M+1511VXhE5/4RFy5cuXKcPTRR4d58+aFG264IXzqU5/KPDZr5YwZM8IJJ5wQNz355JNhhx12yNqtkOtef/318Oc//znMmjUrDB06NIwfPz4cccQRYdCgQYW8Xi4KAQQQQAABBLY+AQKwu+cKveecc04MrW510rzsssvC2WefHZqampJ1ahx++OEx8F199dXhtNNOi9teeeWVcNJJJ8X2McccEyZPnhzb3fn2z3/+Mxx33HFx1+eeey6MGjWqO4c1dJ9ly5aFr371q+H3v//9ZtehAH/NNdcEOVAQQAABBBBAAIFGCxCAO+/AY489Fj73uc8l92PXXXcNEydODAsXLgwKs1Y+/vGPh5tuuskWY50VgDWSfPHFF4fp06eHyy+/POy///5djqm2ULYArNHuM844I478Vvu5brnlljBp0qRqu7ANAQQQQAABBBDocwECcCexRienTZsWRo8eHW6++ebwwQ9+MMFfsmRJ+PrXv56Mbv7sZz8L++67b7I9KwAnG3vQKFsA/t73vtflLwWa8nDyySeHqVOnhjvuuCP85z//iQqaQvLMM8+EYcOG9UCFQxBAAAEEEEAAgXwECMAdjpqvqhCrovBr0w/iis5va9asCR/+8IfDokWLwplnnhmuvPLKZHNvAnB7e3vsU+HQ5sl2NwDr2KVLl8bj2trakuvpTkMj1O+8804YMWJEGDhwYHcOydxnxYoVYZ999km2HXrooeGee+5Jlv1UEK38yle+Ei644IJk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">
```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnModal :open="True" :show_close_button="True" :background_close="True">
    <PnCol>
      <PnTextInput name="Text:" />
      <PnIntSlider name="Slider" />
    </PnCol>
  </PnModal>
</template>
<script lang='py'>
from vuepy import ref
</script>

```


## API

### 属性

| 属性名            | 说明                                 | 类型      | 默认值 |
| ---------------- | ------------------------------------ | --------- | ------ |
| open             | Whether to open the modal            | bool      | False  |
| show_close_button| Show close button                    | bool      | True   |
| background_close | Click outside to close               | bool      | True   |

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |
|       |                      |                                        |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | Custom content     |

### 方法

| 方法名         | 说明                                                                 | 返回值类型  |
|---------------|--------------------------------------------------------------------|------------|
| show          | 显示模态框                                                           | ^[None]    |
| hide          | 隐藏模态框                                                           | ^[None]    |
| toggle        | 切换模态框显示状态（显示↔隐藏）                                         | ^[None]    |
| create_button | 创建控制按钮（可配置为show/hide/toggle功能）                           | ^[Button]  |




# Tabs 标签页

标签页组件，允许用户通过点击标签头在多个对象之间切换。标签页的标题可以显式定义，也可以从内容对象的 `name` 参数中推断。`PnTabs` 提供了类似列表的 API，支持 `append`、`extend`、`clear`、`insert`、`pop` 和 `remove` 等方法，可以动态更新和修改标签页。

底层实现为`panel.Tabs`，参数基本一致，参考文档：https://panel.holoviz.org/reference/layouts/Tabs.html


## 基本用法


```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnTabs v-model="active.value" @change='on_change'>
    <PnTabPane name="Scatter Plot">
      <PnDisplay :obj="p1" />
    </PnTabPane>
    <PnTabPane name="Line Plot">
      <PnDisplay :obj="p2" />
    </PnTabPane>
    <PnTabPane name="Square Plot">
      <PnDisplay :obj="p3" />
    </PnTabPane>
  </PnTabs>
  <p>active: {{ active.value }} </p>
</template>
<script lang='py'>
from vuepy import ref
from bokeh.plotting import figure

# Create sample figures
p1 = figure(width=300, height=300, margin=5)
p1.scatter([0, 1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 2, 1, 0])

p2 = figure(width=300, height=300, margin=5)
p2.line([0, 1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 2, 1, 0])

p3 = figure(width=300, height=300, margin=5)
p3.scatter([0, 1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 2, 1, 0], marker='square', size=10)

# Define active panels (can be multiple when toggle is False)
active = ref(0)

def on_change(event):
    print(event.new) # 1
</script>

```

## 动态添加标签页

==Todo==
## 动态渲染

启用 dynamic 选项后，仅当前活动的标签页会被渲染，只有当切换到新标签页时才会加载其内容。这对于服务器环境或笔记本环境中显示大量标签页，或当单个组件渲染体量极大/渲染成本极高时尤为有用。但需注意：在没有实时服务器的情况下，非活动标签页的内容将不会被加载。
```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnTabs dynamic>
    <PnTabPane name="Scatter Plot">
      <PnDisplay :obj="p1" />
    </PnTabPane>
    <PnTabPane name="Line Plot">
      <PnDisplay :obj="p2" />
    </PnTabPane>
  </PnTabs>
</template>
<script lang='py'>
from vuepy import ref
from bokeh.plotting import figure

# Create sample figures
p1 = figure(width=300, height=300, margin=5)
p1.scatter([0, 1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 2, 1, 0])

p2 = figure(width=300, height=300, margin=5)
p2.line([0, 1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 2, 1, 0])
</script>

```

## 可关闭标签页

设置 closable 为 True 后，标签页会显示关闭按钮：
```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnTabs closable>
    <PnTabPane name="Red">
      <PnSpacer style="background: red; width: 100px; height: 100px" />
    </PnTabPane>
    <PnTabPane name="Blue">
      <PnSpacer style="background: blue; width: 100px; height: 100px" />
    </PnTabPane>
  </PnTabs>
</template>

```

## 标签位置

通过 tabs_location 参数可以调整标签头的位置：
```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnTabs tabs_location="above">
    <PnTabPane name="Above1">
      <PnButton name='xxx' />
    </PnTabPane>
    <PnTabPane name="Above2">
      <PnButton name='yyy' />
    </PnTabPane>
  </PnTabs>
  <PnDivider/>
  <PnTabs tabs_location="right">
    <PnTabPane name="Right1">
      <PnButton name='xxx' />
    </PnTabPane>
    <PnTabPane name="Right2">
      <PnButton name='yyy' />
    </PnTabPane>
  </PnTabs>
</template>

```

## Tabs API

### 属性

| 属性名         | 说明                                                                 | 类型                          | 默认值        |
|--------------|--------------------------------------------------------------------|-----------------------------|--------------|
| active       | 当前选中标签页的索引（可通过选择标签页或编程方式更新）                     | ^[int]                      | 0            |
| dynamic      | 是否仅动态加载当前活动标签页的内容                                       | ^[bool]                     | False        |
| closable     | 是否允许通过界面关闭标签页（关闭后将从对象列表中删除）                      | ^[bool]                     | False        |
| objects      | 标签页内显示的对象列表（通常应整体替换而非直接修改）                       | ^[list]                     | []           |
| tabs_location| 标签位置（'left'-左侧, 'right'-右侧, 'below'-下方, 'above'-上方）       | ^[str]                      | 'above'      |

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |
|       |                      |                                        |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | Tab panels         |

### 方法

| 属性名 | 说明 | 类型 |
| --- | --- | --- |

## TabPane API

### 属性

| 属性名        | 说明                 | 类型                                                           | 默认值 |
| --------     | ------------------- | ---------------------------------------------------------------| ------- |
| name | 面板标题 | ^[str]                                                       | —       |

### Slots

| 插槽名   | 说明               | 
| ---     | ---               |
| default | 自定义默认内容      |



# Card 卡片

卡片组件提供了一个可折叠的容器，带有标题栏，用于组织和展示内容。

底层实现为`panel.layout.Card`，参数基本一致，参考文档：https://panel.holoviz.org/reference/layouts/Card.html


## 基本用法

卡片可以包含任意内容，并可以设置标题。

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnCard title="Card" style="background: WhiteSmoke">
    <PnTextInput name="Text:" />
    <PnFloatSlider name="Slider" />
  </PnCard>
</template>
<script lang='py'>
from vuepy import ref
</script>

```


## 折叠控制

卡片可以通过`collapsible`和`collapsed`属性来控制是否可折叠以及初始状态是否折叠。

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnCol>
    <PnCard title="Collapsible (Default)" >
      <PnTextInput placeholder="This card can be collapsed" />
    </PnCard>
    
    <PnCard title='Initially Collapsed' 
            collapsible collapsed >
      <PnTextInput placeholder="This card is initially collapsed" />
    </PnCard>
    
    <PnCard title="Not Collapsible" :collapsible="False">
      <PnTextInput placeholder="This card cannot be collapsed" />
    </PnCard>
  </PnCol>
</template>
<script lang='py'>
from vuepy import ref
</script>

```


## 自定义头部

卡片可以使用自定义的头部，而不仅仅是标题文本。

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnCard header_background="#2f2f2f" header_color="white" :width="300">
    <template #header>
      <PnButton name='header' :height="50" />
    </template>
    <PnButton name='content1' :height="50" />
    <PnButton name='content2' :height="50" />
  </PnCard>
</template>
<script lang='py'>
from vuepy import ref

</script>

```


## 隐藏头部

可以通过`hide_header`属性完全隐藏卡片的头部。

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnCard hide_header :width="160" style="background: lightgray">
    <PnNumber :value="42" :default_color="'white'" name="Completion" format="{value}%" />
  </PnCard>
</template>

```


## 布局控制

可以设置卡片的固定尺寸，或者让它根据内容自适应。

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnCol>
    <!-- fixed size -->
    <PnCard title="Fixed Size" :height="300" :width="200">
      <PnButton name='fixed' sizing_mode="stretch_both" />
    </PnCard>
    
    <!-- Responsive -->
    <PnCard title='Responsive' sizing_mode='stretch_width'>
      <!--<PnDisplay :obj="p1" />-->
      <PnButton name='responsive' sizing_mode="stretch_both" />
      <PnDivider />
      <!--<PnDisplay :obj="p2" />-->
    </PnCard>
  </PnCol>
</template>
<script lang='py'>
from vuepy import ref
from bokeh.plotting import figure

p1 = figure(height=250, sizing_mode='stretch_width', margin=5)
p2 = figure(height=250, sizing_mode='stretch_width', margin=5)

p1.line([1, 2, 3], [1, 2, 3])
p2.scatter([1, 2, 3], [1, 2, 3])
</script>

```


## API

### 属性

| 属性名                   | 说明                                    | 类型                | 默认值  |
|------------------------|----------------------------------------|---------------------|--------|
| title                  | 卡片标题                                 | ^[String]           | —      |
| collapsed              | 是否折叠                                 | ^[Boolean]          | False  |
| collapsible            | 是否可折叠                               | ^[Boolean]          | False  |
| hide_header            | 是否隐藏头部                             | ^[Boolean]          | False  |
| active_header_background | 展开卡片时的标题背景颜色                 | ^[String]           | —      |
| header_background      | 标题背景颜色                             | ^[String]           | —      |
| header_color           | 标题文本颜色                             | ^[String]           | —      |
| background             | 内容区域背景颜色                         | ^[String]           | —      |
| button_css_classes     | 应用于折叠按钮的CSS类列表                 | ^[Array]            | —      |
| css_classes            | 应用于主区域的CSS类列表                   | ^[Array]            | —      |
| header_css_classes     | 应用于头部的CSS类列表                     | ^[Array]            | —      |

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |
| change | 当卡片折叠状态改变时触发  | ^[Callable]`(event: dict) -> None` |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | 卡片内容            |
| header  | 自定义卡片头部       |
| footer  | 自定义卡片底部       |




# GridSpec 网格规格

GridSpec布局是一种类似数组的布局，允许使用简单的API将多个Panel对象排列在网格中，可以将对象分配到单个网格单元或网格跨度。

底层实现为`panel.layout.GridSpec`，参数基本一致，参考文档：https://panel.holoviz.org/reference/layouts/GridSpec.html


## 基本用法

GridSpec可以创建固定大小的网格布局，并通过GridSpecItem放置组件：

```vue
<!-- --plugins vpanel --show-code -->
<template>
<PnGridSpec :width="400" :height="300">
  <PnGridSpecItem :row_start="0" :row_end="3" :col_start="0" :col_end="1">
    <PnSpacer style="background: red" />
  </PnGridSpecItem>
  
  <PnGridSpecItem :row_start="0" :row_end="1" :col_start="1" :col_end="3">
    <PnSpacer style="background: green" />
  </PnGridSpecItem>
  
  <PnGridSpecItem :row_start="1" :row_end="2" :col_start="2" :col_end="4">
    <PnSpacer style="background: orange" />
  </PnGridSpecItem>
  
  <PnGridSpecItem :row_start="2" :row_end="3" :col_start="1" :col_end="4">
    <PnSpacer style="background: blue" />
  </PnGridSpecItem>
  
  <PnGridSpecItem :row_start="0" :row_end="1" :col_start="3" :col_end="4">
    <PnSpacer style="background: purple" />
  </PnGridSpecItem>
</PnGridSpec>
</template>

```


## 响应式网格

除了固定大小的网格外，GridSpec还支持响应式尺寸，可以在浏览器窗口调整大小时动态调整：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnGridSpec sizing_mode="stretch_both" :max_height="800">
    <PnGridSpecItem :row_start="0" :row_end="1" :col_start="0" :col_end="3">
      <PnSpacer style="background: #FF0000" />
    </PnGridSpecItem>
    
    <PnGridSpecItem :row_start="1" :row_end="3" :col_start="0" :col_end="1">
      <PnSpacer style="background: #0000FF" />
    </PnGridSpecItem>
    
    <PnGridSpecItem :row_start="1" :row_end="3" :col_start="1" :col_end="3">
      <!--<PnDisplay :obj="fig" />-->
      <PnButton name='xxx' />
    </PnGridSpecItem>
    
    <PnGridSpecItem :row_start="3" :row_end="5" :col_start="0" :col_end="1">
      <!--<PnDisplay :obj="curve" />-->
      <PnButton name='yyy' />
    </PnGridSpecItem>
    
    <PnGridSpecItem :row_start="3" :row_end="5" :col_start="1" :col_end="2">
      <PnImage :object="image_url" />
    </PnGridSpecItem>
    
    <PnGridSpecItem :row_start="4" :row_end="5" :col_start="2" :col_end="3">
      <PnColumn>
        <PnFloatSlider />
        <PnColorPicker />
        <PnToggle name="Toggle Me!" />
      </PnColumn>
    </PnGridSpecItem>
  </PnGridSpec>
</template>
<script lang='py'>
from vuepy import ref
import holoviews as hv
from bokeh.plotting import figure
import requests
from io import BytesIO

# 创建Bokeh图表
fig = figure()
fig.scatter([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 1, 2, 3, 2, 1, 0, -1, -2, -3])

# 创建HoloViews曲线
curve = hv.Curve([1, 2, 3])

# 图片URL
image_url = "https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png"
</script>

```


## 复杂布局示例

使用GridSpec可以创建复杂的仪表板布局：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnGridSpec sizing_mode="stretch_both" :height="600">
    <!-- 标题区 -->
    <PnGridSpecItem :row_start="0" :row_end="1" :col_start="0" :col_end="6">
      <PnMarkdown style="background: #e0e0e0; padding: 10px; text-align: center">
        # Dashboard Title
      </PnMarkdown>
    </PnGridSpecItem>
    
    <!-- 左侧控制面板 -->
    <PnGridSpecItem :row_start="1" :row_end="4" :col_start="0" :col_end="1">
      <PnCard title="Controls">
        <PnSelect :options="['Option 1', 'Option 2', 'Option 3']" name="Select" />
        <PnIntSlider name="Value" :value="50" />
        <PnDatePicker name="Date" />
        <PnButton name="Update" />
      </PnCard>
    </PnGridSpecItem>
    
    <!-- 主图表区域 -->
    <PnGridSpecItem :row_start="1" :row_end="3" :col_start="1" :col_end="5">
      <PnCard title="Main Chart">
        <PnDisplay :obj="main_fig" />
      </PnCard>
    </PnGridSpecItem>
    
    <!-- 右侧信息区 -->
    <PnGridSpecItem :row_start="1" :row_end="2" :col_start="5" :col_end="6">
      <PnCard title="Statistics">
        <PnMarkdown>
          - Value 1: 42
          - Value 2: 73
          - Average: 57.5
        </PnMarkdown>
      </PnCard>
    </PnGridSpecItem>
    
    <!-- 右下角信息区 -->
    <PnGridSpecItem :row_start="2" :row_end="4" :col_start="5" :col_end="6">
      <PnCard title="Information">
        <PnMarkdown>
          This is additional information about the dashboard.
          You can include any relevant details here.
        </PnMarkdown>
      </PnCard>
    </PnGridSpecItem>
    
    <!-- 底部小图表区域 -->
    <PnGridSpecItem :row_start="3" :row_end="4" :col_start="1" :col_end="3">
      <PnCard title="Chart 1">
        <PnDisplay :obj="sub_fig1" />
      </PnCard>
    </PnGridSpecItem>
    
    <PnGridSpecItem :row_start="3" :row_end="4" :col_start="3" :col_end="5">
      <PnCard title="Chart 2">
        <PnDisplay :obj="sub_fig2" />
      </PnCard>
    </PnGridSpecItem>
  </PnGridSpec>
</template>
<script lang='py'>
from vuepy import ref
from bokeh.plotting import figure
import numpy as np

# 创建主图表
main_fig = figure(height=300)
x = np.linspace(0, 10, 100)
y = np.sin(x)
main_fig.line(x, y, line_width=2)

# 创建子图表1
sub_fig1 = figure(height=150)
x = np.linspace(0, 10, 50)
y = np.cos(x)
sub_fig1.line(x, y, line_color="orange", line_width=2)

# 创建子图表2
sub_fig2 = figure(height=150)
x = np.random.rand(50)
y = np.random.rand(50)
sub_fig2.scatter(x, y, color="green", size=8)
</script>

```


## GridSpec API

### 属性

| 属性名   | 说明                                       | 类型                | 默认值  |
|---------|-------------------------------------------|---------------------|--------|
| ncols   | 限制可分配的列数                           | ^[Number]           | 3      |
| nrows   | 限制可分配的行数                           | ^[Number]           | 3      |
| mode    | 重叠分配时的行为模式（warn、error、override） | ^[String]           | warn   |

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |
| change | 当网格内容改变时触发   | ^[Callable]`(event: dict) -> None` |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | GridSpec的内容，应该是PnGridSpecItem组件 |

## GridSpecItem API

### 属性

| 属性名        | 说明                             | 类型    | 默认值  |
|--------------|-------------------------------------------|---------------------|--------|
| row_start    | 开始行的索引                      | ^[Number]           | 0 |
| row_end      | 结束行的索引，开区间               | ^[Number]           | `row_start+1` |
| col_start    | 开始列的索引                      | ^[Number]           | 0 |
| col_end      | 结束列的索引，开区间               | ^[Number]           | `col_start+1` |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | 默认内容 |








# VTK 三维可视化

`PnVTK` 组件可以在 Panel 应用程序中渲染 VTK 场景，使得可以与复杂的 3D 几何体进行交互。
它允许在 Python 端定义的 `vtkRenderWindow` 与通过 vtk-js 在组件中显示的窗口之间保持状态同步。
在这种情况下，Python 充当服务器，向客户端发送有关场景的信息。
同步只在一个方向进行：Python => JavaScript。在 JavaScript 端所做的修改不会反映回 Python 的 `vtkRenderWindow`。

底层实现为`panel.pane.VTK`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/VTK.html


## 基本用法

与直接使用 `VTK` 相比，在 Panel 中使用它有一些区别。由于 VTK 面板处理对象的渲染和与视图的交互，我们不需要调用 `vtkRenderWindow` 的 `Render` 方法（这会弹出传统的 VTK 窗口），也不需要指定 `vtkRenderWindowInteractor`。

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnVTK :object="ren_win" :width="500" :height="500" />
</template>
<script lang='py'>
import vtk
from vtk.util.colors import tomato

# 创建一个具有八个周向面的多边形圆柱体模型
cylinder = vtk.vtkCylinderSource()
cylinder.SetResolution(8)

# 映射器负责将几何体推送到图形库中
# 它还可以进行颜色映射（如果定义了标量或其他属性）
cylinder_mapper = vtk.vtkPolyDataMapper()
cylinder_mapper.SetInputConnection(cylinder.GetOutputPort())

# actor 是一种分组机制：除了几何体（映射器），它还有属性、变换矩阵和/或纹理映射
# 这里我们设置它的颜色并旋转 -22.5 度
cylinder_actor = vtk.vtkActor()
cylinder_actor.SetMapper(cylinder_mapper)
cylinder_actor.GetProperty().SetColor(tomato)
# 我们必须将 ScalarVisibilty 设置为 0 以使用 tomato 颜色
cylinder_mapper.SetScalarVisibility(0)
cylinder_actor.RotateX(30.0)
cylinder_actor.RotateY(-45.0)

# 创建图形结构。渲染器渲染到渲染窗口中
ren = vtk.vtkRenderer()
ren_win = vtk.vtkRenderWindow()
ren_win.AddRenderer(ren)

# 将 actor 添加到渲染器，设置背景和大小
ren.AddActor(cylinder_actor)
ren.SetBackground(0.1, 0.2, 0.4)
</script>

```


我们还可以向场景添加其他 actor，然后调用 `synchronize` 方法来更新组件：
```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnVTK :object="ren_win" :width="500" :height="500" ref="vtk_pane_ref" />
  <PnButton @click="add_sphere()">添加球体</PnButton>
</template>
<script lang='py'>
from vuepy import ref
import vtk
from vtk.util.colors import tomato

vtk_pane_ref = ref(None)

# 创建一个具有八个周向面的多边形圆柱体模型
cylinder = vtk.vtkCylinderSource()
cylinder.SetResolution(8)

# 映射器负责将几何体推送到图形库中
cylinder_mapper = vtk.vtkPolyDataMapper()
cylinder_mapper.SetInputConnection(cylinder.GetOutputPort())

# actor 是一种分组机制
cylinder_actor = vtk.vtkActor()
cylinder_actor.SetMapper(cylinder_mapper)
cylinder_actor.GetProperty().SetColor(tomato)
cylinder_mapper.SetScalarVisibility(0)
cylinder_actor.RotateX(30.0)
cylinder_actor.RotateY(-45.0)

# 创建图形结构
ren = vtk.vtkRenderer()
ren_win = vtk.vtkRenderWindow()
ren_win.AddRenderer(ren)

# 将 actor 添加到渲染器，设置背景
ren.AddActor(cylinder_actor)
ren.SetBackground(0.1, 0.2, 0.4)

def add_sphere():
    sphere = vtk.vtkSphereSource()
    
    sphere_mapper = vtk.vtkPolyDataMapper()
    sphere_mapper.SetInputConnection(sphere.GetOutputPort())
    
    sphere_actor = vtk.vtkActor()
    sphere_actor.SetMapper(sphere_mapper)
    sphere_actor.GetProperty().SetColor(tomato)
    sphere_mapper.SetScalarVisibility(0)
    sphere_actor.SetPosition(0.5, 0.5, 0.5)
    
    ren.AddActor(sphere_actor)
    vtk_pane = vtk_pane_ref.value.unwrap()
    vtk_pane.reset_camera()
    vtk_pane.synchronize()
</script>

```


## 与 PyVista 集成

这些示例大多使用 [PyVista](https://docs.pyvista.org/) 库作为 VTK 的便捷接口。

虽然这些示例通常可以重写为仅依赖于 VTK 本身，但 `pyvista` 支持简洁的 Python 语法，用于处理 VTK 对象所需的主要功能。

例如，上面的 VTK 示例可以使用 PyVista 重写如下：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnVTK :object="plotter.ren_win" :width="500" :height="500" />
</template>
<script lang='py'>
import pyvista as pv
from vtk.util.colors import tomato

# 创建 PyVista plotter
plotter = pv.Plotter()
plotter.background_color = (0.1, 0.2, 0.4)

# 创建并添加对象到 PyVista plotter
pvcylinder = pv.Cylinder(resolution=10, direction=(0, 1, 0))
cylinder_actor = plotter.add_mesh(pvcylinder, color=tomato, smooth_shading=True)
cylinder_actor.RotateX(30.0)
cylinder_actor.RotateY(-45.0)
</script>

```


## 导出场景

场景可以导出，生成的文件可以由官方的 vtk-js 场景导入器加载：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnVTK :object="plotter.ren_win" :width="500" :height="500" ref="vtk_pane_ref" />
  <PnButton @click="export_scene()">导出场景</PnButton>
  <div v-if="filename.value">导出的文件：{{ filename.value }}</div>
</template>
<script lang='py'>
import os
import pyvista as pv
from vuepy import ref
from vtk.util.colors import tomato

filename = ref("")
vtk_pane_ref = ref(None)

# 创建 PyVista plotter
plotter = pv.Plotter()
plotter.background_color = (0.1, 0.2, 0.4)

# 创建并添加对象到 PyVista plotter
pvcylinder = pv.Cylinder(resolution=8, direction=(0, 1, 0))
cylinder_actor = plotter.add_mesh(pvcylinder, color=tomato, smooth_shading=True)
cylinder_actor.RotateX(30.0)
cylinder_actor.RotateY(-45.0)

def export_scene():
    vtk_pane = vtk_pane_ref.value.unwrap()
    exported_filename = vtk_pane.export_scene(filename='vtk_example')
    filename.value = os.path.join(os.getcwd(), exported_filename)
</script>

```


## 高级用法和交互性

### 键盘绑定和方向部件

`PnVTK` 组件支持键盘绑定和方向部件，以增强用户交互体验：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnVTK 
    :object="plotter.ren_win" 
    :width="500" 
    :height="500" 
    :enable_keybindings="True"
    :orientation_widget="True" />
</template>
<script lang='py'>
import pyvista as pv
from vtk.util.colors import tomato

# 创建 PyVista plotter
plotter = pv.Plotter()
plotter.background_color = (0.1, 0.2, 0.4)

# 创建并添加对象到 PyVista plotter
pvcylinder = pv.Cylinder(resolution=8, direction=(0, 1, 0))
cylinder_actor = plotter.add_mesh(pvcylinder, color=tomato, smooth_shading=True)
cylinder_actor.RotateX(30.0)
cylinder_actor.RotateY(-45.0)
</script>

```


键盘绑定允许用户使用以下键:
- s: 将所有 actor 表示设置为*表面*
- w: 将所有 actor 表示设置为*线框*
- v: 将所有 actor 表示设置为*顶点*
- r: 居中 actor 并移动相机，使所有 actor 可见

## 添加坐标轴

使用 `axes` 参数可以在 3D 视图中显示坐标轴：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnVTK 
    :object="plotter.ren_win" 
    :width="500" 
    :height="500" 
    :axes="axes" />
</template>
<script lang='py'>
import numpy as np
import pyvista as pv
from vtk.util.colors import tomato

# 创建 PyVista plotter
plotter = pv.Plotter()
plotter.background_color = (0.1, 0.2, 0.4)

# 创建并添加对象到 PyVista plotter
pvcylinder = pv.Cylinder(resolution=8, direction=(0, 1, 0))
cylinder_actor = plotter.add_mesh(pvcylinder, color=tomato, smooth_shading=True)
cylinder_actor.RotateX(30.0)
cylinder_actor.RotateY(-45.0)

# 定义坐标轴
axes = {
    'origin': [-5, 5, -2],
    'xticker': {'ticks': np.linspace(-5, 5, 5).tolist()},
    'yticker': {'ticks': np.linspace(-5, 5, 5).tolist()},
    'zticker': {'ticks': np.linspace(-2, 2, 5).tolist(), 
                'labels': [''] + [str(int(item)) for item in np.linspace(-2, 2, 5)[1:]]},
    'fontsize': 12,
    'digits': 1,
    'show_grid': True,
    'grid_opacity': 0.5,
    'axes_opacity': 1.0
}
</script>

```


## API

### 属性

| 属性名                      | 说明                          | 类型                                                           | 默认值 |
| -------------------------- | ----------------------------- | ---------------------------------------------------------------| ------- |
| object                        | `vtkRenderWindow` 实例        | ^[vtkRenderWindow]                                             | None |
| axes                       | 在 3D 视图中构造的坐标轴的参数字典。必须至少包含 `xticker`、`yticker` 和 `zticker` | ^[dict]    | None |
| camera                     | 反映 VTK 相机当前状态的字典      | ^[dict]                                                       | None |
| enable_keybindings         | 激活/禁用键盘绑定的布尔值。绑定的键有：s（将所有 actor 表示设置为*表面*）、w（将所有 actor 表示设置为*线框*）、v（将所有 actor 表示设置为*顶点*）、r（居中 actor 并移动相机，使所有 actor 可见） | ^[boolean] | False |
| orientation_widget         | 激活/禁用 3D 面板中的方向部件的布尔值 | ^[boolean]                                                  | False |
| interactive_orientation_widget | 如果为 True，则方向部件可点击并允许将场景旋转到正交投影之一 | ^[boolean]                | False |
| sizing_mode                | 尺寸调整模式                   | ^[str]                                                         | 'fixed'  |
| width                      | 宽度                          | ^[int, str]                                                    | None    |
| height                     | 高度                          | ^[int, str]                                                    | None    |
| min_width                  | 最小宽度                      | ^[int]                                                         | None    |
| min_height                 | 最小高度                      | ^[int]                                                         | None    |
| max_width                  | 最大宽度                      | ^[int]                                                         | None    |
| max_height                 | 最大高度                      | ^[int]                                                         | None    |
| margin                     | 外边距                        | ^[int, tuple]                                                  | 5       |
| css_classes                | CSS类名列表                   | ^[list]                                                        | []      |

### 属性值

* **`actors`**：返回场景中的 vtkActors 列表
* **`vtk_camera`**：返回组件持有的渲染器的 vtkCamera

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | 自定义默认内容      |

### 方法

| 方法名 | 说明 | 参数 |
| --- | --- | --- |
| set_background | 设置场景背景颜色为 RGB 颜色 | r: float, g: float, b: float |
| synchronize | 同步 Python 端 `vtkRenderWindow` 对象状态与 JavaScript | 无 |
| unlink_camera | 创建一个新的 vtkCamera 对象，允许面板拥有自己的相机 | 无 |
| link_camera | 设置两个面板共享相同的相机 | other: VTK |
| export_scene | 导出场景并生成可以被官方 vtk-js 场景导入器加载的文件 | filename: str |




# VTKVolume 3D体积数据组件

`VTKVolume`组件可渲染定义在规则网格上的3D体积数据。它可以从3D NumPy数组或`vtkVolume`构建。该组件提供了许多交互控制，可以通过Python回调或JavaScript回调设置。

底层实现为`panel.pane.VTKVolume`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/VTKVolume.html


## 基本用法

最简单的创建`PnVTKVolume`组件的方法是使用3D NumPy数组。通过设置spacing参数可以产生一个长方体而不是立方体。

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnVTKVolume :object="data_matrix" 
               :width="800" 
               :height="600" 
               :spacing="(3, 2, 1)" 
               interpolation="nearest"
               :edge_gradient="0"
               :sampling="0" />
</template>

<script lang='py'>
import numpy as np

# Create a 3D volume data
data_matrix = np.zeros([75, 75, 75], dtype=np.uint8)
data_matrix[0:35, 0:35, 0:35] = 50
data_matrix[25:55, 25:55, 25:55] = 100
data_matrix[45:74, 45:74, 45:74] = 150
</script>

```


或者，该组件也可以从`vtkImageData`对象构建。这种类型的对象可以直接使用vtk或pyvista模块构建：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnVTKVolume :object="vol" 
               :height="600" 
               sizing_mode="stretch_width"
               :display_slices="True" />
</template>

<script lang='py'>
import pyvista as pv
from pyvista import examples

# Download a volumetric dataset
vol = examples.download_head()
</script>

```


## 交互控制

`PnVTKVolume`组件公开了许多选项，可以从Python和JavaScript更改。尝试交互式地测试这些参数的效果：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnRow>
    <PnCol>
      <PnVTKVolume :object="vol" 
                   :height="600" 
                   :display_slices="display_slices.value"
                   :slice_i="slice_i.value"
                   :slice_j="slice_j.value"
                   :slice_k="slice_k.value"
                   :ambient="ambient.value"
                   :diffuse="diffuse.value"
                   :specular="specular.value"
                   :display_slices="display_slices.value" />
    </PnCol>
    <PnCol>
      <PnCheckbox v-model="display_slices.value" name="Display Slices" />
      <PnIntSlider v-model="slice_i.value" 
                name="Slice I" 
                :start="0" 
                :end="vol.dimensions[0]-1" 
                :step="1" />
      <PnIntSlider v-model="slice_j.value" 
                name="Slice J" 
                :start="0" 
                :end="vol.dimensions[1]-1" 
                :step="1" />
      <PnIntSlider v-model="slice_k.value" 
                name="Slice K" 
                :start="0" 
                :end="vol.dimensions[2]-1" 
                :step="1" />
      <PnFloatSlider v-model="ambient.value" 
                name="Ambient" 
                :start="0" 
                :end="1" 
                :step="0.1" />
      <PnFloatSlider v-model="diffuse.value" 
                name="Diffuse" 
                :start="0" 
                :end="1" 
                :step="0.1" />
      <PnFloatSlider v-model="specular.value" 
                name="Specular" 
                :start="0" 
                :end="1" 
                :step="0.1" />
    </PnCol>
  </PnRow>
</template>

<script lang='py'>
import pyvista as pv
from pyvista import examples
from vuepy import ref

# Download a volumetric dataset
vol = examples.download_head()

# Control parameters
display_slices = ref(True)
slice_i = ref(vol.dimensions[0]//2)
slice_j = ref(vol.dimensions[1]//2)
slice_k = ref(vol.dimensions[2]//2)
ambient = ref(0.2)
diffuse = ref(0.7)
specular = ref(0.3)

</script>

```


## API

### 属性

| 属性名               | 说明                                                                | 类型                 | 默认值 |
| ------------------- | ------------------------------------------------------------------- | ------------------- | ------ |
| object              | 可以是3D numpy数组或`vtkImageData`类的实例                            | ^[ndarray\|object]  | —      |
| origin              | 场景中体积的原点                                                      | ^[tuple]            | (0,0,0) |
| spacing             | 定义3个维度中2个相邻体素之间的距离                                      | ^[tuple]            | (1,1,1) |
| render_background   | 定义3D渲染的背景颜色                                                  | ^[str]              | '#52576e' |
| camera              | 反映VTK相机当前状态的字典                                              | ^[dict]             | —      |
| controller_expanded | 展开/折叠视图中的体积控制器面板的布尔值                                 | ^[bool]             | —      |
| orientation_widget  | 在3D窗格中激活/停用方向小部件的布尔值                                   | ^[bool]             | —      |
| colormap            | 用于将像素值转换为颜色的colormap名称                                   | ^[str]              | 'erdc_rainbow_bright' |
| rescale             | 如果设置为True，则colormap在非透明像素的最小值和最大值之间重新缩放        | ^[bool]             | True   |
| display_volume      | 如果设置为True，则使用光线投射显示体积的3D表示                           | ^[bool]             | True   |
| display_slices      | 如果设置为true，则显示三个(X, Y, Z)方向的正交切片                       | ^[bool]             | False  |
| mapper              | 存储有关通过3d视图中的javascript小部件设置的颜色映射器的信息的参数        | ^[dict]             | —      |
| sampling            | 调整用于渲染的样本之间距离的参数                                        | ^[Number]           | 0.4    |
| edge_gradient       | 基于体素之间的梯度调整体积不透明度的参数                                 | ^[Number]           | 0.4    |
| interpolation       | 用于采样体积的插值类型                                                 | ^[str]              | 'fast_linear' |
| shadow              | 如果设置为false，则体积的映射器将不执行阴影计算                          | ^[bool]             | True   |
| ambient             | 控制环境光照的值                                                      | ^[Number]           | 0.2    |
| diffuse             | 控制漫反射光照的值                                                    | ^[Number]           | 0.7    |
| specular            | 控制镜面光照的值                                                      | ^[Number]           | 0.3    |
| specular_power      | 镜面功率指的是光线像镜子一样反射的程度                                  | ^[Number]           | 8.0    |
| slice_i             | 控制垂直于X方向的切片位置的参数                                         | ^[int]              | —      |
| slice_j             | 控制垂直于Y方向的切片位置的参数                                         | ^[int]              | —      |
| slice_k             | 控制垂直于Z方向的切片位置的参数                                         | ^[int]              | —      |
| nan_opacity         | 控制切片中NaN值的不透明度的参数                                         | ^[Number]           | 1      |

### 方法

| 方法名    | 说明                  | 类型                  |
| --------- | --------------------- | --------------------- |
| controls  | 返回控制面板组件       | ^[Callable]`(jslink=bool) -> Panel` |




# Audio 音频

音频组件用于展示音频播放器，可以显示本地或远程音频文件、NumPy ndarray 或 Torch Tensor。

该组件还允许访问和控制播放器状态，包括切换播放/暂停和循环状态、当前播放时间和音量。

音频播放器支持 `ogg`、`mp3` 和 `wav` 文件格式。

如果安装了 SciPy，还支持 1 维 NumPy ndarray 和 1 维 Torch Tensor。数据类型必须是以下之一：
- numpy: np.int16, np.uint16, np.float32, np.float64
- torch: torch.short, torch.int16, torch.half, torch.float16, torch.float, torch.float32, torch.double, torch.float64

数组或张量输入将被 SciPy 降采样到 16bit 并转换为 wav 文件。

底层实现为`panel.pane.Audio`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/Audio.html


## 基本用法

`PnAudio` 组件可以通过指向远程音频文件的 URL 或本地音频文件构建（在这种情况下，数据被嵌入）：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnAudio name="Audio" :object="url" />
</template>
<script lang='py'>
url = 'https://ccrma.stanford.edu/~jos/mp3/pno-cs.mp3'
</script>

```


## 控制播放

播放器可以使用其自身的控件控制，也可以通过 Python 代码控制。要在代码中暂停或取消暂停，请使用 `paused` 属性：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnAudio name="Audio" :object="url" ref="audio_ref" />
  <PnRow>
    <PnButton @click="play()">播放</PnButton>
    <PnButton @click="pause()">暂停</PnButton>
    <PnButton @click="set_time()">跳至5秒</PnButton>
    <PnButton @click="set_volume()">设置音量50%</PnButton>
  </PnRow>
</template>
<script lang='py'>
from vuepy import ref

url = 'https://ccrma.stanford.edu/~jos/mp3/pno-cs.mp3'

audio_ref = ref(None)

def play():
    audio = audio_ref.value.unwrap()
    audio.paused = False

def pause():
    audio = audio_ref.value.unwrap()
    audio.paused = True
    
def set_time():
    audio = audio_ref.value.unwrap()
    audio.time = 5.0
    
def set_volume():
    audio = audio_ref.value.unwrap()
    audio.volume = 50
</script>

```


## NumPy 数组输入

当提供 NumPy 数组或 Torch 张量时，应指定 `sample_rate`。

在此示例中，我们绘制了一个频率调制信号：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnAudio :object="waveform_quiet" :sample_rate="sps" />
</template>
<script lang='py'>
import numpy as np

# Samples per second
sps = 44100
# Duration in seconds
duration = 10

modulator_frequency = 2.0
carrier_frequency = 120.0
modulation_index = 2.0

time = np.arange(sps*duration) / sps
modulator = np.sin(2.0 * np.pi * modulator_frequency * time) * modulation_index
carrier = np.sin(2.0 * np.pi * carrier_frequency * time)
waveform = np.sin(2. * np.pi * (carrier_frequency * time + modulator))
    
waveform_quiet = waveform * 0.3
</script>

```


## API

### 属性

| 属性名      | 说明                 | 类型                                                           | 默认值 |
| ---------- | ------------------- | ---------------------------------------------------------------| ------- |
| object     | 本地文件路径、指向音频文件的远程URL、1维numpy数组或1维torch张量 | ^[string, numpy.ndarray, torch.Tensor] | None |
| autoplay   | 当为True时，指定输出将自动播放。在Chromium浏览器中，这需要用户点击一次播放 | ^[boolean] | False |
| loop       | 是否在播放结束时循环    | ^[boolean]                                                    | False |
| muted      | 当为True时，指定输出应该被静音 | ^[boolean]                                                | False |
| name       | 面板的标题            | ^[str]                                                         | None |
| paused     | 播放器是否暂停         | ^[boolean]                                                    | True |
| sample_rate | 给定NumPy数组或Torch张量时的采样率 | ^[int]                                            | 44100 |
| throttle   | 以毫秒为单位的当前播放采样频率 | ^[int]                                                  | 500 |
| time       | 当前播放时间（秒）      | ^[float]                                                      | 0 |
| volume     | 音量范围为0-100        | ^[int]                                                        | 100 |
| sizing_mode | 尺寸调整模式         | ^[str]                                                         | 'fixed'  |
| width      | 宽度                 | ^[int, str]                                                    | None    |
| height     | 高度                 | ^[int, str]                                                    | None    |




# Video 视频组件

`PnVideo` 组件允许在 Panel 应用程序中显示视频播放器，可以用于显示本地或远程视频文件。该组件还提供对播放器状态的访问和控制，包括切换播放/暂停状态、循环状态、当前时间和音量。根据浏览器的不同，视频播放器支持 `mp4`、`webm` 和 `ogg` 容器以及多种编解码器。

底层实现为`panel.pane.Video`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/Video.html


## 基本用法

`PnVideo` 组件可以通过 URL 指向远程视频文件或本地视频文件（在这种情况下，数据将被嵌入）：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnVideo 
    object="https://assets.holoviz.org/panel/samples/video_sample.mp4" 
    :width="640" 
    :loop="True" />
</template>

```


## 控制视频播放

可以通过播放器自身的控件以及使用组件属性来控制视频播放。例如，通过修改 `paused` 属性来暂停或恢复播放：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnVideo 
    :object="video_url" 
    :width="640" 
    :loop="True"
    :paused="is_paused.value" 
  />
  <PnButton @click="toggle_play()">{{ play_button_text.value }}</PnButton>
</template>
<script lang='py'>
from vuepy import ref, computed

video_url = "https://assets.holoviz.org/panel/samples/video_sample.mp4"
is_paused = ref(True)

def toggle_play():
    is_paused.value = not is_paused.value

play_button_text = computed(lambda: "播放" if is_paused.value else "暂停")
</script>

```


## 音量控制

可以通过设置 `volume` 属性来控制视频的音量：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnVideo 
    object="https://assets.holoviz.org/panel/samples/video_sample.mp4" 
    :width="640" 
    :volume="volume.value" 
  />
  <PnRow>
    <PnMD>音量：</PnMD>
    <PnIntSlider v-model="volume.value" :start="0" :end="100" />
  </PnRow>
</template>
<script lang='py'>
from vuepy import ref

volume = ref(50)
</script>

```


## 访问当前播放时间

可以通过 `time` 属性读取和设置当前播放时间（以秒为单位）：

```vue
<!-- --plugins vpanel --show-code -->
<template>
<PnCol>
  <PnVideo 
    v-model:time='current_time.value'
    object="https://assets.holoviz.org/panel/samples/video_sample.mp4" 
    :width="640" 
  />
  <PnRow>
    <PnMD>当前时间：{{ current_time.value }} 秒</PnMD>
    <PnButton @click="jump_to_middle()">跳转到中间</PnButton>
  </PnRow>
</PnCol>
</template>
<script lang='py'>
from vuepy import ref

current_time = ref(0)

def jump_to_middle():
    # 获取视频总时长（这里假设为30秒）
    current_time.value = 15
</script>

```


## API

### 属性

| 属性名      | 说明                          | 类型                                                           | 默认值 |
| ---------- | ----------------------------- | ---------------------------------------------------------------| ------- |
| object     | 指向视频文件的本地文件路径或远程 URL | ^[str]                                                    | None |
| loop       | 是否在播放结束时循环            | ^[boolean]                                                     | False |
| paused     | 播放器是否暂停                 | ^[boolean]                                                     | True |
| autoplay   | 当为 True 时，指定输出将自动播放。在 Chromium 浏览器中，这需要用户点击一次播放 | ^[boolean]   | False |
| muted      | 当为 True 时，指定输出应该静音  | ^[boolean]                                                     | False |
| throttle   | 以毫秒为单位，多久采样一次当前播放时间 | ^[int]                                                   | 250 |
| time       | 当前播放时间（以秒为单位）      | ^[float]                                                       | 0.0 |
| volume     | 音量范围从 0 到 100            | ^[int]                                                         | 100 |
| sizing_mode| 尺寸调整模式                   | ^[str]                                                         | 'fixed'  |
| width      | 宽度                          | ^[int, str]                                                    | None    |
| height     | 高度                          | ^[int, str]                                                    | None    |
| min_width  | 最小宽度                      | ^[int]                                                         | None    |
| min_height | 最小高度                      | ^[int]                                                         | None    |
| max_width  | 最大宽度                      | ^[int]                                                         | None    |
| max_height | 最大高度                      | ^[int]                                                         | None    |
| margin     | 外边距                        | ^[int, tuple]                                                  | 5       |
| css_classes| CSS类名列表                   | ^[list]                                                        | []      |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | 自定义默认内容      |




# Folium 地图

`PnFolium` 组件渲染 [folium](http://python-visualization.github.io/folium/) 交互式地图。

底层实现为`panel.pane.plot.Folium`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/Folium.html


## 基本用法

`PnFolium` 组件使用 `folium` 提供的内置 HTML 表示来渲染地图：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnFolium :object="m" :width='400' :height="400" />
</template>
<script lang='py'>
import folium

m = folium.Map(location=[52.51, 13.39], zoom_start=12)
</script>

```


## 更新地图

与任何其他组件一样，可以通过设置 `object` 参数来更新 `PnFolium` 组件的视图：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnFolium :object="m" :width='400' :height="400" ref="folium_pane" />
  <PnButton @click="add_marker()">添加标记</PnButton>
</template>
<script lang='py'>
from vuepy import ref
import folium

folium_pane = ref(None)
m = folium.Map(location=[52.51, 13.39], zoom_start=12)

def add_marker():
    # Add a marker to the map
    folium.Marker(
        [52.516, 13.381], popup="<i>Brandenburg Gate</i>", tooltip="Click me!"
    ).add_to(m)
    
    # Update the Folium pane
    folium_pane.value.unwrap().object = m
</script>

```


## API

### 属性

| 属性名      | 说明                 | 类型                                                           | 默认值 |
| ---------- | ------------------- | ---------------------------------------------------------------| ------- |
| object     | 要显示的 Folium 对象  | ^[object]                                                      | None |
| sizing_mode | 尺寸调整模式         | ^[str]                                                         | 'fixed'  |
| width      | 宽度                 | ^[int, str]                                                    | None    |
| height     | 高度                 | ^[int, str]                                                    | None    |
| min_width  | 最小宽度             | ^[int]                                                         | None    |
| min_height | 最小高度             | ^[int]                                                         | None    |
| max_width  | 最大宽度             | ^[int]                                                         | None    |
| max_height | 最大高度             | ^[int]                                                         | None    |
| margin     | 外边距               | ^[int, tuple]                                                  | 5       |
| css_classes | CSS类名列表          | ^[list]                                                        | []      |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | 自定义默认内容      |



# SVG 矢量图

`PnSVG` 组件如果提供本地路径，则将 `.svg` 矢量图文件嵌入到面板中，或者如果提供 URL，则会链接到远程图像。

底层实现为`panel.pane.SVG`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/SVG.html


## 基本用法

`PnSVG` 组件可以指向任何本地或远程 `.svg` 文件。如果给定以 `http` 或 `https` 开头的 URL，则 `embed` 参数决定图像是嵌入还是链接到：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnSVG 
    object="https://panel.holoviz.org/_static/logo_stacked.svg" 
    link_url="https://panel.holoviz.org" 
    :width="300" />
</template>

```


## 调整大小

我们可以通过设置特定的固定 `width` 或 `height` 来调整图像的大小：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnSVG 
    object="https://panel.holoviz.org/_static/logo_stacked.svg" 
    :width="150" />
</template>

```


与任何其他组件一样，`PnSVG` 组件可以通过设置 `object` 参数来更新：

```vue
<!-- --plugins vpanel --show-code -->
<template>
<PnCol>
  <PnSVG 
    :object="svg_url.value" 
    :width="150" 
  />
  <PnButton @click="update_svg()">更新 SVG</PnButton>
</PnCol>
</template>
<script lang='py'>
from vuepy import ref
svg_url = ref("https://panel.holoviz.org/_static/logo_stacked.svg")

def update_svg():
    svg_url.value = "https://panel.holoviz.org/_static/jupyterlite.svg"
</script>

```


## 响应式 SVG

您也可以使用 *响应式* `sizing_mode`，如 `'stretch_width'`：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnSVG 
    object="https://assets.holoviz.org/panel/samples/svg_sample2.svg" 
    sizing_mode="stretch_width" />
</template>

```


请注意，默认情况下图像的宽高比是固定的，要覆盖此行为，请设置 `fixed_aspect=false` 或提供固定的 `width` 和 `height` 值。

## 编码选项

SVG 图像可以使用 base64 编码进行嵌入。使用 `encode` 参数可以控制是否对 SVG 进行编码：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnRow>
    <PnColumn>
      <PnMD>## encode=true（默认）</PnMD>
      <PnSVG 
        object="https://panel.holoviz.org/_static/logo_stacked.svg" 
        :encode="True"
        :width="200" />
    </PnColumn>
    <PnColumn>
      <PnMD>## encode=false</PnMD>
      <PnSVG 
        object="https://panel.holoviz.org/_static/logo_stacked.svg" 
        :encode="False"
        :width="200" />
    </PnColumn>
  </PnRow>
</template>

```


当启用编码时，SVG 链接可能无法工作，而禁用编码会阻止图像缩放正常工作。

## API

### 属性

| 属性名          | 说明                          | 类型                                                           | 默认值 |
| -------------- | ----------------------------- | ---------------------------------------------------------------| ------- |
| object         | 要显示的 SVG 文件。可以是指向本地或远程文件的字符串，或具有 `_repr_svg_` 方法的对象 | ^[str, object] | None |
| alt_text       | 添加到图像标签的替代文本。当用户无法加载或显示图像时显示替代文本 | ^[str]                   | None |
| embed          | 如果给定图像 URL，这决定图像是否将被嵌入为 base64 或仅链接到 | ^[boolean]                  | False |
| encode         | 是否将 SVG 编码为 base64。启用时 SVG 链接可能无法工作，而禁用编码会阻止图像缩放正常工作 | ^[boolean] | True |
| fixed_aspect   | 是否强制图像的宽高比相等       | ^[boolean]                                                     | True |
| link_url       | 使图像可点击并链接到其他网站的链接 URL | ^[str]                                                  | None |
| styles         | 指定 CSS 样式的字典           | ^[dict]                                                        | {} |
| sizing_mode    | 尺寸调整模式                   | ^[str]                                                         | 'fixed'  |
| width          | 宽度                          | ^[int, str]                                                    | None    |
| height         | 高度                          | ^[int, str]                                                    | None    |
| min_width      | 最小宽度                      | ^[int]                                                         | None    |
| min_height     | 最小高度                      | ^[int]                                                         | None    |
| max_width      | 最大宽度                      | ^[int]                                                         | None    |
| max_height     | 最大高度                      | ^[int]                                                         | None    |
| margin         | 外边距                        | ^[int, tuple]                                                  | 5       |
| css_classes    | CSS类名列表                   | ^[list]                                                        | []      |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | 自定义默认内容      |




# HoloViews 可视化

[HoloViews](https://holoviews.org/) 是一个流行且功能强大的数据可视化库，支持多种数据和绘图后端。

[hvPlot](https://hvplot.holoviz.org/index.html)（快速可视化）和 [GeoViews](https://holoviz.org/assets/geoviews.png)（空间可视化）都是基于 HoloViews 构建的，并产生 `HoloViews` 对象。

**Panel、HoloViews、hvPlot 和 GeoViews 都是 [HoloViz](https://holoviz.org) 生态系统的成员，它们可以完美地协同工作**。

`PnHoloViews` 组件使用 HoloViews 支持的绘图后端之一渲染 [HoloViews](https://holoviews.org/) 对象。这包括 [hvPlot](https://hvplot.holoviz.org/index.html) 和 [GeoViews](https://holoviz.org/assets/geoviews.png) 生成的对象。

`PnHoloViews` 组件支持显示包含小部件的交互式 [`HoloMap`](https://holoviews.org/reference/containers/bokeh/HoloMap.html) 和 [`DynamicMap`](https://holoviews.org/reference/containers/bokeh/DynamicMap.html) 对象。`PnHoloViews` 组件甚至允许自定义小部件类型及其相对于图表的位置。

底层实现为`panel.pane.HoloViews`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/HoloViews.html


## 基本用法

`PnHoloViews` 组件将任何 `HoloViews` 对象自动转换为可显示的面板，同时保持其所有交互功能：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnHoloViews :object="box" :height="300" :width="500" />
</template>
<script lang='py'>
import numpy as np
import holoviews as hv

data = {"group": np.random.randint(0, 10, 100), "value": np.random.randn(100)}
box = hv.Scatter(data, kdims="group", vdims="value").sort().opts()
</script>

```


通过设置组件的 `object` 可以像所有其他组件对象一样更新图表：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnHoloViews :object="plot" :height="300" :width="500" ref='hv_pane' />
  <PnButton @click="update_plot()">更新为小提琴图</PnButton>
</template>
<script lang='py'>
import numpy as np
import holoviews as hv
from vuepy import ref

hv_pane = ref(None)

data = {"group": np.random.randint(0, 10, 100), "value": np.random.randn(100)}
box = hv.Scatter(data, kdims="group", vdims="value").sort().opts()
plot = box

def update_plot():
    nonlocal plot
    plot = hv.Violin(box).opts(violin_color='Group', responsive=True, height=300)
    hv_pane.value.unwrap().object = plot
</script>

```


您也可以显示 [hvPlot](https://hvplot.holoviz.org/)（和 [GeoViews](https://geoviews.org/)）对象，因为它们是 `HoloViews` 对象：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnHoloViews :object="plot" :height="300" :width="500" />
</template>
<script lang='py'>
import numpy as np
import pandas as pd
import hvplot.pandas

data = {"group": np.random.randint(0, 10, 100), "value": np.random.randn(100)}
df = pd.DataFrame(data)
plot = df.hvplot.box(by="group", y="value", responsive=True, height=300)
</script>

```


您还可以显示 [`HoloMap`](https://holoviews.org/reference/containers/bokeh/HoloMap.html) 和 [`DynamicMap`](https://holoviews.org/reference/containers/bokeh/DynamicMap.html) 对象。

[HoloViews](https://holoviews.org/)（框架）如果 [`HoloMap`](https://holoviews.org/reference/containers/bokeh/HoloMap.html) 或 [DynamicMap](https://holoviews.org/reference/containers/bokeh/DynamicMap.html) 声明了任何键维度，它原生渲染带有小部件的图表。这种方法高效地仅更新图表内的数据，而不是完全替换图表。

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnHoloViews :object="dmap" :width='300' :height='300'/>
</template>
<script lang='py'>
import numpy as np
import pandas as pd
import hvplot.pandas
import holoviews as hv
import holoviews.plotting.bokeh

def sine(frequency=1.0, amplitude=1.0, function='sin'):
    xs = np.arange(200)/200*20.0
    ys = amplitude*getattr(np, function)(frequency*xs)
    return pd.DataFrame(dict(y=ys), index=xs).hvplot(height=250, responsive=True)

# todo have no controls
dmap = hv.DynamicMap(sine, kdims=['frequency', 'amplitude', 'function']).redim.range(
    frequency=(0.1, 10), amplitude=(1, 10)).redim.values(function=['sin', 'cos', 'tan'])
</script>

```


## 后端选择

`PnHoloViews` 组件默认使用 'bokeh' 绘图后端（如果没有通过 `holoviews` 加载后端），但您可以根据需要将后端更改为 'bokeh'、'matplotlib' 和 'plotly' 中的任何一个。

### Bokeh

Bokeh 是默认的绘图后端，所以通常您不必指定它。但让我们在这里展示它是如何工作的：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnHoloViews :object="plot" backend='bokeh' sizing_mode='stretch_width' :height="300" />
</template>
<script lang='py'>
import numpy as np
import pandas as pd
import hvplot.pandas

data = {"group": np.random.randint(0, 10, 100), "value": np.random.randn(100)}
df = pd.DataFrame(data)
plot = df.hvplot.scatter(x="group", y="value")
</script>

```


### Matplotlib

Matplotlib 后端允许生成用于打印和出版的图形。如果你想允许响应式大小调整，你可以设置 `format='svg'`，然后使用标准的响应式 `sizing_mode` 设置：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnHoloViews :object="plot" backend='matplotlib' format='svg'
               sizing_mode='stretch_both' :center="False" />
</template>
<script lang='py'>
import numpy as np
import pandas as pd
import hvplot.pandas
hvplot.extension("matplotlib")

data = {"group": np.random.randint(0, 10, 100), "value": np.random.randn(100)}
df = pd.DataFrame(data)
plot = df.hvplot.scatter(x="group", y="value")
</script>

```


### Plotly

要使用 'plotly' 绘图后端，您需要运行 `hv.extension("plotly")` 来配置 'plotly' 后端。

如果您使用的是 `hvPlot`，您可以使用 `hvplot.extension("plotly")` 来代替：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnHoloViews :object="plot" backend='plotly' :height="300" />
</template>
<script lang='py'>
import numpy as np
import pandas as pd
import hvplot.pandas
hvplot.extension("plotly")

data = {"group": np.random.randint(0, 10, 100), "value": np.random.randn(100)}
df = pd.DataFrame(data)
plot = df.hvplot.scatter(x="group", y="value", height=300, responsive=True)
</script>

```


### 动态后端切换

您还可以通过小部件动态更改绘图后端：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnColumn>
    <PnRadioButtonGroup v-model="backend.value" 
                        :options="['bokeh', 'matplotlib', 'plotly']" 
                        button_type="primary" button_style="outline" />
    <PnHoloViews :object="plot" :backend="backend.value" 
                 sizing_mode="stretch_width" :height="300" />
  </PnColumn>
</template>
<script lang='py'>
import numpy as np
import pandas as pd
import hvplot.pandas
from vuepy import ref
import holoviews as hv
hv.extension("bokeh", "matplotlib", "plotly")

data = {
    "group": np.random.randint(0, 10, 100),
    "value": np.random.randn(100),
}
df = pd.DataFrame(data)
plot = df.hvplot.scatter(x="group", y="value", height=300, 
                         responsive=True, 
                         title="Try changing the backend")
backend = ref('bokeh')
</script>

```


## 链接坐标轴

默认情况下，具有共享键或值维度的图表的坐标轴是链接的。您可以通过将 `linked_axes` 参数设置为 `False` 来删除链接：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnColumn>
    <PnHoloViews :object="not_linked_plot" backend='bokeh' 
                 sizing_mode='stretch_width' :height="200" :linked_axes="False" />
    <PnHoloViews :object="linked_plot" backend='bokeh' 
                 sizing_mode='stretch_width' :height="200" />
    <PnHoloViews :object="linked_plot" backend='bokeh' 
                 sizing_mode='stretch_width' :height="200" />
  </PnColumn>
</template>
<script lang='py'>
import numpy as np
import pandas as pd
import hvplot.pandas
import holoviews as hv
hv.extension("bokeh")

data = {"group": np.random.randint(0, 10, 100), "value": np.random.randn(100)}
df = pd.DataFrame(data)
not_linked_plot = df.hvplot.scatter(x="group", y="value", responsive=True, title="Not Linked Axes")\
    .opts(active_tools=['box_zoom'])
linked_plot = df.hvplot.scatter(x="group", y="value", responsive=True, title="Linked Axes")\
    .opts(active_tools=['box_zoom'])
</script>

```


## 主题

您可以更改 `theme`：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnHoloViews :object="plot" :height="300" theme="night_sky" />
</template>
<script lang='py'>
import numpy as np
import pandas as pd
import hvplot.pandas

data = {"group": np.random.randint(0, 10, 100), "value": np.random.randn(100)}
df = pd.DataFrame(data)
plot = df.hvplot.scatter(x="group", y="value", height=300, responsive=True)
</script>

```


## 布局和小部件参数

`PnHoloViews` 组件提供了 `layout` 属性，其中包含 `HoloViews` 组件和 `widget_box`。

### 居中

您可以通过 `center` 参数将图表居中：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
    <PnHoloViews :object='plot' :center="True" sizing_mode="fixed" />
<!--
  <PnCol>
    <PnMarkdown>center=True, sizing_mode='fixed'</PnMarkdown>

    <PnMarkdown>center=True, sizing_mode='stretch_width'</PnMarkdown>
    <PnHoloViews :object="plot" :center="True" sizing_mode="stretch_width" />

    <PnMarkdown>center=False, sizing_mode='fixed'</PnMarkdown>
    <PnHoloViews :object="plot" :center="False" sizing_mode="fixed" />

    <PnMarkdown>center=False, sizing_mode='stretch_width'</PnMarkdown>
    <PnHoloViews :object="plot" :center="False" sizing_mode="stretch_width" />
  </PnCol>
-->
</template>
<script lang='py'>
import pandas as pd
import hvplot.pandas

df = pd.DataFrame({
    "group": [1, 2, 3, 4, 5],
    "value": [10, 20, 30, 20, 10]
})
# todo center
plot = df.hvplot.scatter(x="group", y="value", height=100, width=400)
</script>

```


## API

### 属性

| 属性名           | 说明                   | 类型                                                           | 默认值 |
| --------------- | --------------------- | ---------------------------------------------------------------| ------- |
| object          | 要显示的 HoloViews 对象 | ^[object]                                                      | None |
| backend         | 任何支持的 HoloViews 后端（'bokeh'，'matplotlib' 或 'plotly'）。如果未指定，默认为活动的 holoviews 渲染器。默认为 'bokeh'。 | ^[str] | None |
| linked_axes     | 是否在面板布局中链接各图的坐标轴 | ^[boolean]                                            | True |
| format          | 绘制 Matplotlib 图时使用的输出格式 | ^[str]                                              | 'png' |
| renderer        | 用于渲染 HoloViews 图的明确的 HoloViews 渲染器实例。覆盖 `backend` 参数。 | ^[object]    | None |
| theme           | 应用于 HoloViews 图的 Bokeh 主题 | ^[str, object]                                       | None |
| layout          | 包含图表窗格和（可选）`widget_box` 布局的布局 | ^[pn.layout.Panel]                       | None |
| widget_box      | 包含小部件的布局       | ^[ListPanel]                                                    | None |
| center          | 是否居中显示图表       | ^[boolean]                                                      | False |
| widgets         | 从维度名称到小部件类、实例或覆盖字典的映射，用于修改默认小部件 | ^[dict]                | None |
| widget_location | 相对于图表放置小部件的位置 | ^[str]                                                      | None |
| widget_layout   | 放置小部件的对象，可以是 `Row`、`Column` 或 `WidgetBox` | ^[ListPanel]                  | None |
| widget_type     | 是否为每个维度生成单独的小部件，或使用具有连接维度的全局线性滑块 | ^[str]                 | None |
| sizing_mode     | 尺寸调整模式           | ^[str]                                                         | 'fixed'  |
| width           | 宽度                   | ^[int, str]                                                    | None    |
| height          | 高度                   | ^[int, str]                                                    | None    |
| min_width       | 最小宽度               | ^[int]                                                         | None    |
| min_height      | 最小高度               | ^[int]                                                         | None    |
| max_width       | 最大宽度               | ^[int]                                                         | None    |
| max_height      | 最大高度               | ^[int]                                                         | None    |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | 自定义默认内容      |




# IPyWidget 组件

`PnIPyWidget` 组件可以在 Panel 应用程序中渲染任何 ipywidgets 模型，不论是在笔记本环境中还是在部署的服务器上。这使得可以直接从 Panel 中利用这个不断发展的生态系统，只需将组件包装在面板中即可。

在笔记本中，这不是必需的，因为 Panel 只是使用常规的笔记本 ipywidget 渲染器。特别是在 JupyterLab 中，以这种方式导入 ipywidgets 扩展可能会干扰 UI 并使 JupyterLab UI 无法使用，因此请谨慎启用扩展。

底层实现为`panel.pane.IPyWidget`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/IPyWidget.html


## 基本用法

`panel_vuepy` 函数会自动将任何 `ipywidgets` 对象转换为可显示的面板，同时保持其所有交互功能：


## 交互性和回调

任何具有 `value` 参数的 ipywidget 也可以在 `pn.depends` 装饰的回调中使用，例如，这里我们声明一个依赖于 `FloatSlider` 值的函数：


如果您想自己编写回调，也可以像通常一样使用 `traitlets` 的 `observe` 方法。要了解更多信息，请参阅 ipywidgets 文档中的 [Widget Events](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20Events.html) 部分。


## 外部小部件库

`PnIPyWidget` 组件不仅限于简单的小部件，ipywidget 库（如 [`ipyvolume`](https://ipyvolume.readthedocs.io/en/latest/index.html) 和 [`ipyleaflet`](https://ipyleaflet.readthedocs.io/en/latest/)）也受支持。



## 限制

ipywidgets 支持有一些限制，因为它整合了两个截然不同的生态系统。特别是，目前还不能在 Panel 和 ipywidget 对象之间设置 JS 链接或支持嵌入。这些限制不是基本的技术限制，可能在未来得到解决。

## API

### 属性

| 属性名            | 说明                          | 类型                                                           | 默认值 |
| ---------------- | ----------------------------- | ---------------------------------------------------------------| ------- |
| object           | 被显示的 ipywidget 对象        | ^[object]                                                      | None |
| default_layout   | 包装图表和小部件的布局        | ^[pn.layout.Panel]                                             | Row |
| sizing_mode      | 尺寸调整模式                  | ^[str]                                                         | 'fixed'  |
| width            | 宽度                          | ^[int, str]                                                    | None    |
| height           | 高度                          | ^[int, str]                                                    | None    |
| min_width        | 最小宽度                      | ^[int]                                                         | None    |
| min_height       | 最小高度                      | ^[int]                                                         | None    |
| max_width        | 最大宽度                      | ^[int]                                                         | None    |
| max_height       | 最大高度                      | ^[int]                                                         | None    |
| margin           | 外边距                        | ^[int, tuple]                                                  | 5       |
| css_classes      | CSS类名列表                   | ^[list]                                                        | []      |

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | 自定义默认内容      |

### 方法

| 属性名 | 说明 | 类型 |
| --- | --- | --- |



# LaTeX 公式

`PnLaTeX` 组件可以使用 [KaTeX](https://katex.org/) 或 [MathJax](https://www.mathjax.org) 渲染器将 LaTeX 方程渲染为 HTML。

您必须手动加载所需的渲染器（例如，`pn.extension('katex')` 或 `pn.extension('mathjax')`）。如果同时加载了两个渲染器，则默认使用 KaTeX。

请注意，[KaTeX](https://katex.org/) 和 [MathJax](https://www.mathjax.org) 都只支持完整 LaTeX 渲染器中可用功能的一个子集。有关支持的功能的详细信息，请参阅它们各自的文档。

底层实现为`panel.pane.LaTeX`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/LaTeX.html


## 基本用法

`PnLaTeX` 组件将渲染任何具有 `_repr_latex_` 方法的对象、[SymPy](https://www.sympy.org/en/index.html) 表达式或包含 LaTeX 的任何字符串。任何 LaTeX 内容都应该包装在 `$...$` 或 `\(...\)` 分隔符中，例如：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnLatex 
    object="supports two delimiters: $\frac{1}{n}$ and \(\frac{1}{n}\)" 
    :styles="{'font-size': '18pt'}" />
</template>

```


为 LaTeX 字符串添加前缀 `r` 很重要，这样可以使字符串成为*原始*字符串，不会转义 `\\` 字符：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnCol>
    <PnLatex :object="rs" :styles="{'font-size': '18pt'}"/>
    <PnLatex :object="s" :styles="{'font-size': '18pt'}"/>  <!-- 不起作用 -->
  </PnCol>
</template>
<script lang='py'>
rs = r'$\frac{1}{n}$'
s = '$\frac{1}{n}$'
</script>

```


与其他组件一样，`PnLaTeX` 组件可以动态更新：

```vue
<!-- --plugins vpanel --show-code -->
<template>
<PnCol>
  <PnLatex :object="latex_formula.value" />
  <PnButton @click="update_formula()">更新公式</PnButton>
</PnCol>
</template>
<script lang='py'>
from vuepy import ref
latex_formula = ref(r'The LaTeX pane supports two delimiters: $LaTeX$ and \(LaTeX\)')

def update_formula():
    latex_formula.value = r'$\sum_{j}{\sum_{i}{a*w_{j, i}}}$'
</script>

```


如果两个渲染器都已加载，我们可以覆盖默认渲染器：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnLaTeX 
    object="The LaTeX pane supports two delimiters: $LaTeX$ and \(LaTeX\)" 
    renderer="mathjax"
    :styles="{'font-size': '18pt'}" />
</template>

```


## 复杂公式示例

`PnLaTeX` 组件可以渲染复杂的数学公式：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnRow>
    <PnLaTeX :object="maxwell" style="font-size: 24pt" />
    <PnSpacer :width="50" />
    <PnLaTeX :object="cross_product" style="font-size: 24pt" />
    <PnSpacer :width="50" />
    <PnLaTeX :object="cauchy_schwarz" style="font-size: 24pt" />
  </PnRow>
</template>
<script lang='py'>
maxwell = r"""
$\begin{aligned}
  \nabla \times \vec{\mathbf{B}} -\, \frac1c\, \frac{\partial\vec{\mathbf{E}}}{\partial t} & = \frac{4\pi}{c}\vec{\mathbf{j}} \\
  \nabla \cdot \vec{\mathbf{E}} & = 4 \pi \rho \\
  \nabla \times \vec{\mathbf{E}}\, +\, \frac1c\, \frac{\partial\vec{\mathbf{B}}}{\partial t} & = \vec{\mathbf{0}} \\
  \nabla \cdot \vec{\mathbf{B}} & = 0
\end{aligned}
$"""

cauchy_schwarz = r"""
$\left( \sum_{k=1}^n a_k b_k \right)^2 \leq \left( \sum_{k=1}^n a_k^2 \right) \left( \sum_{k=1}^n b_k^2 \right)$
"""

cross_product = r"""
$\mathbf{V}_1 \times \mathbf{V}_2 =  \begin{vmatrix}
\mathbf{i} & \mathbf{j} & \mathbf{k} \\
\frac{\partial X}{\partial u} &  \frac{\partial Y}{\partial u} & 0 \\
\frac{\partial X}{\partial v} &  \frac{\partial Y}{\partial v} & 0
\end{vmatrix}
$"""
</script>

```


## SymPy 集成

可以渲染 SymPy 表达式：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnColumn>
    <PnMarkdown>
    # SymPy 表达式渲染：
    </PnMarkdown>
    <PnLaTeX :object="expression" style="font-size: 20px" />
  </PnColumn>
</template>
<script lang='py'>
import sympy as sp

# 使用 SymPy 定义符号和符号表达式
x = sp.symbols('x')
expression = sp.integrate(sp.sin(x)**2, x)
expression_latex = sp.latex(expression) # \frac{x}{2} - ...
</script>

```


## API

### 属性

| 属性名     | 说明                          | 类型                                                           | 默认值 |
| --------- | ----------------------------- | ---------------------------------------------------------------| ------- |
| object    | 包含 LaTeX 代码的字符串，具有 `_repr_latex_` 方法的对象，或 SymPy 表达式 | ^[str, object] | None |
| renderer  | 当前渲染器；必须是可用选项之一  | ^[str]                                                        | 'katex' |
| styles    | 指定 CSS 样式的字典           | ^[dict]                                                        | {} |
| sizing_mode | 尺寸调整模式                | ^[str]                                                         | 'fixed'  |
| width     | 宽度                          | ^[int, str]                                                    | None    |
| height    | 高度                          | ^[int, str]                                                    | None    |
| min_width | 最小宽度                      | ^[int]                                                         | None    |
| min_height| 最小高度                      | ^[int]                                                         | None    |
| max_width | 最大宽度                      | ^[int]                                                         | None    |
| max_height| 最大高度                      | ^[int]                                                         | None    |
| margin    | 外边距                        | ^[int, tuple]                                                  | 5       |
| css_classes| CSS类名列表                  | ^[list]                                                        | []      |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | 自定义默认内容      |




# Matplotlib 图表

`PnMatplotlib` 组件允许在 Panel 应用程序中显示 [Matplotlib](http://matplotlib.org) 图表。这包括由 [Seaborn](https://seaborn.pydata.org/)、[Pandas `.plot`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.plot.html)、[Plotnine](https://plotnine.readthedocs.io/) 和任何其他基于 `Matplotlib` 构建的绘图库创建的图表。

`PnMatplotlib` 组件将以声明的 DPI 将 `object` 渲染为 PNG 或 SVG，然后显示它。

底层实现为`panel.pane.Matplotlib`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/Matplotlib.html


## 基本用法

创建一个简单的 Matplotlib 图表并显示：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnMatplotlib :object="fig" :dpi="144" />
</template>
<script lang='py'>
import numpy as np
from matplotlib.figure import Figure
from matplotlib import cm

Y, X = np.mgrid[-3:3:100j, -3:3:100j]
U = -1 - X**2 + Y
V = 1 + X - Y**2

fig = Figure(figsize=(4, 3))
ax = fig.subplots()

strm = ax.streamplot(X, Y, U, V, color=U, linewidth=2, cmap=cm.autumn)
fig.colorbar(strm.lines)
</script>

```


通过修改图表并使用组件对象的 `param.trigger('object')` 方法，我们可以轻松更新图表：

```vue
<!-- --plugins vpanel --show-code -->
<template>
<PnCol>
  <PnMatplotlib :object="fig" :dpi="144" ref="mpl_pane" />
  <PnButton @click="update_cmap()">更新颜色映射</PnButton>
</PnCol>
</template>
<script lang='py'>
import numpy as np
from matplotlib.figure import Figure
from matplotlib import cm
from vuepy import ref

mpl_pane = ref(None)

Y, X = np.mgrid[-3:3:100j, -3:3:100j]
U = -1 - X**2 + Y
V = 1 + X - Y**2

fig = Figure(figsize=(4, 3))
ax = fig.subplots()

strm = ax.streamplot(X, Y, U, V, color=U, linewidth=2, cmap=cm.autumn)
fig.colorbar(strm.lines)

def update_cmap():
    strm.lines.set_cmap(cm.viridis)
    mpl_pane.value.unwrap().param.trigger('object')
</script>

```


与所有其他模型一样，`PnMatplotlib` 组件也可以通过直接设置 `object` 来更新：

```vue
<!-- --plugins vpanel --show-code -->
<template>
<PnCol>
  <PnMatplotlib :object="fig" :dpi="144" ref="mpl_pane" />
  <PnButton @click="update_fig()">更新为3D图表</PnButton>
</PnCol>
</template>
<script lang='py'>
from vuepy import ref
import numpy as np
from matplotlib.figure import Figure
from matplotlib import cm
from mpl_toolkits.mplot3d import axes3d

mpl_pane = ref(None)

Y, X = np.mgrid[-3:3:100j, -3:3:100j]
U = -1 - X**2 + Y
V = 1 + X - Y**2

fig = Figure(figsize=(4, 3))
ax = fig.subplots()

strm = ax.streamplot(X, Y, U, V, color=U, linewidth=2, cmap=cm.autumn)
fig.colorbar(strm.lines)

def update_fig():
    fig3d = Figure(figsize=(8, 6))
    ax = fig3d.add_subplot(111, projection='3d')
    
    X, Y, Z = axes3d.get_test_data(0.05)
    ax.plot_surface(X, Y, Z, rstride=8, cstride=8, alpha=0.3)
    cset = ax.contourf(X, Y, Z, zdir='z', offset=-100, cmap=cm.coolwarm)
    cset = ax.contourf(X, Y, Z, zdir='x', offset=-40, cmap=cm.coolwarm)
    cset = ax.contourf(X, Y, Z, zdir='y', offset=40, cmap=cm.coolwarm)
    
    ax.set_xlabel('X')
    ax.set_xlim(-40, 40)
    ax.set_ylabel('Y')
    ax.set_ylim(-40, 40)
    ax.set_zlabel('Z')
    ax.set_zlim(-100, 100)
    
    mpl_pane.value.unwrap().object = fig3d
</script>

```


## 使用 Matplotlib pyplot 接口

您可能已经注意到，我们在上面没有使用 `matplotlib.pyplot` API。我们这样做是为了避免需要特意关闭图形。如果图形未关闭，将导致内存泄漏。

**您可以使用 `matplotlib.pyplot` 接口，但随后必须像下面所示特别关闭图形！**

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnMatplotlib :object="create_voltage_figure()" :dpi="144" :tight="True" />
</template>
<script lang='py'>
import matplotlib.pyplot as plt
import numpy as np

def create_voltage_figure(figsize=(4,3)):
    t = np.arange(0.0, 2.0, 0.01)
    s = 1 + np.sin(2 * np.pi * t)
    
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(t, s)
    
    ax.set(xlabel='time (s)', ylabel='voltage (mV)',
          title='Voltage')
    ax.grid()
    
    plt.close(fig)  # 关闭图形！
    return fig
</script>

```


## 修复裁剪问题

如果您发现图形在边缘被裁剪，可以设置 `tight=true`：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnRow>
    <PnMarkdown>
     ## ❌ tight=false
    </PnMarkdown>
    <PnMatplotlib :object="create_voltage_figure()" :dpi="144" :tight="False" />
  </PnRow>
  <PnRow>
    <PnMarkdown>
     ## ✔️ tight=true
    </PnMarkdown>
    <PnMatplotlib :object="create_voltage_figure()" :dpi="144" :tight="True" />
  </PnROw>
</template>
<script lang='py'>
import matplotlib.pyplot as plt
import numpy as np

def create_voltage_figure(figsize=(4,3)):
    t = np.arange(0.0, 2.0, 0.01)
    s = 1 + np.sin(2 * np.pi * t)
    
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(t, s)
    
    ax.set(xlabel='time (s)', ylabel='voltage (mV)',
          title='Voltage')
    ax.grid()
    
    plt.close(fig)  # 关闭图形！
    return fig
</script>

```


## 响应式图表

如果您希望您的图表能够响应式地适应它们所在的任何容器，那么您应该使用适当的 `sizing_mode` 结合：

- `format="svg"`：获得更好看的调整大小后的图表
- `fixed_aspect=true`：允许 'svg' 图像独立调整其高度和宽度 
- `fixed_aspect=false`（默认）：允许 'svg' 图像调整其高度和宽度，同时保持宽高比

让我们先使用默认的 `'png'` 格式和 `sizing_mode="stretch_width"` 显示：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnMatplotlib :object="fig" :tight="True" sizing_mode="stretch_width" 
                style="background: pink" />
</template>
<script lang='py'>
import matplotlib.pyplot as plt
import numpy as np

def create_voltage_figure(figsize=(6,1)):
    t = np.arange(0.0, 2.0, 0.01)
    s = 1 + np.sin(2 * np.pi * t)
    
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(t, s)
    
    ax.set(xlabel='time (s)', ylabel='voltage (mV)',
          title='Voltage')
    ax.grid()
    
    plt.close(fig)
    return fig

fig = create_voltage_figure(figsize=(6,1))
</script>

```


如果您的窗口宽度较大，您会在两侧看到一些大的粉色区域。如果减小窗口宽度，您会看到图表自适应调整大小。

使用 `'svg'` 格式可以使图形占据全宽：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnMatplotlib :object="fig" :tight="True" format="svg" 
                sizing_mode="stretch_width" />
</template>
<script lang='py'>
import matplotlib.pyplot as plt
import numpy as np

def create_voltage_figure(figsize=(6,1)):
    t = np.arange(0.0, 2.0, 0.01)
    s = 1 + np.sin(2 * np.pi * t)
    
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(t, s)
    
    ax.set(xlabel='time (s)', ylabel='voltage (mV)',
          title='Voltage')
    ax.grid()
    
    plt.close(fig)
    return fig

fig = create_voltage_figure(figsize=(6,1))
</script>

```


但这可能会使图形太高。让我们尝试使用固定的 `height`：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnMatplotlib 
    :object="fig" 
    :tight="True" 
    :height="150" 
    format="svg" 
    sizing_mode="stretch_width" 
    style="background: pink" />
</template>
<script lang='py'>
import matplotlib.pyplot as plt
import numpy as np

def create_voltage_figure(figsize=(6,1)):
    t = np.arange(0.0, 2.0, 0.01)
    s = 1 + np.sin(2 * np.pi * t)
    
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(t, s)
    
    ax.set(xlabel='时间 (s)', ylabel='电压 (mV)',
          title='电压')
    ax.grid()
    
    plt.close(fig)
    return fig

fig = create_voltage_figure(figsize=(6,1))
</script>

```


但也许我们希望图形占据全宽。让我们将 `fixed_aspect` 更改为 `false`：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnMatplotlib 
    :object="fig" 
    :tight="True" 
    :height="150" 
    format="svg" 
    :fixed_aspect="False" 
    sizing_mode="stretch_width" />
</template>
<script lang='py'>
import matplotlib.pyplot as plt
import numpy as np

def create_voltage_figure(figsize=(6,1)):
    t = np.arange(0.0, 2.0, 0.01)
    s = 1 + np.sin(2 * np.pi * t)
    
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(t, s)
    
    ax.set(xlabel='time (s)', ylabel='voltage (mV)',
          title='voltage')
    ax.grid()
    
    plt.close(fig)
    return fig

fig = create_voltage_figure(figsize=(6,1))
</script>

```


总之，通过使用适当组合的 `format`、`fixed_aspect` 和 `sizing_mode` 值，您应该能够实现所需的响应式大小调整。

## 使用 Seaborn

我们建议创建一个 Matplotlib `Figure` 并将其提供给 Seaborn：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnMatplotlib :object="fig" :tight="True" />
</template>
<script lang='py'>
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib.figure import Figure

sns.set_theme()

df = pd.DataFrame(np.random.rand(10, 10), columns=[chr(65+i) for i in range(10)], index=[chr(97+i) for i in range(10)])

fig = Figure(figsize=(2, 2))
ax = fig.add_subplot(111)
sns.heatmap(df, ax=ax)
</script>

```


您也可以直接使用 Seaborn，但请记住手动关闭 `Figure` 以避免内存泄漏：


## 使用 Pandas.plot
```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnMatplotlib :object="fig" :height="300" />
</template>
<script lang='py'>
import pandas as pd
from matplotlib.figure import Figure

df = pd.DataFrame({'a': range(10)})
fig = Figure(figsize=(4, 2))
ax = fig.add_subplot(111)
ax = df.plot.barh(ax=ax)
</script>

```


## API

### 属性

| 属性名        | 说明                          | 类型                                                           | 默认值 |
| ------------ | ----------------------------- | ---------------------------------------------------------------| ------- |
| object       | 要显示的 Matplotlib [`Figure`](https://matplotlib.org/stable/api/figure_api.html#matplotlib.figure.Figure) 对象 | ^[object] | None |
| alt_text     | 添加到图像标签的替代文本。当用户无法加载或显示图像时显示替代文本 | ^[str]                   | None |
| dpi          | 导出 png 的每英寸点数         | ^[int]                                                         | 144 |
| encode       | 是否将 'svg' 编码为 base64。默认为 False。'png' 将始终被编码 | ^[boolean]                  | False |
| fixed_aspect | 是否强制图像的宽高比相等       | ^[boolean]                                                     | True |
| format       | 渲染图形的格式：'png' 或 'svg'  | ^[str]                                                         | 'png' |
| high_dpi     | 是否为高 dpi 显示优化输出      | ^[boolean]                                                     | True |
| interactive  | 是否使用交互式 ipympl 后端     | ^[boolean]                                                     | False |
| link_url     | 使图像可点击并链接到其他网站的链接 URL | ^[str]                                                  | None |
| tight        | 自动调整图形大小以适应子图和其他艺术元素 | ^[boolean]                                             | False |
| sizing_mode  | 尺寸调整模式                   | ^[str]                                                         | 'fixed'  |
| width        | 宽度                          | ^[int, str]                                                    | None    |
| height       | 高度                          | ^[int, str]                                                    | None    |
| min_width    | 最小宽度                      | ^[int]                                                         | None    |
| min_height   | 最小高度                      | ^[int]                                                         | None    |
| max_width    | 最大宽度                      | ^[int]                                                         | None    |
| max_height   | 最大高度                      | ^[int]                                                         | None    |
| margin       | 外边距                        | ^[int, tuple]                                                  | 5       |
| css_classes  | CSS类名列表                   | ^[list]                                                        | []      |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | 自定义默认内容      |




# DataFrame 数据框

`PnDataFrame` 组件将 pandas、dask 和 streamz 的 `DataFrame` 和 `Series` 类型渲染为 HTML 表格。该组件支持 `DataFrame.to_html` 函数的所有参数。

如果需要显示更大的 `DataFrame` 或使用高级表格功能和交互性，我们建议使用 `PnTabulator` 组件或 `PnPerspective` 组件。

底层实现为`panel.pane.DataFrame`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/DataFrame.html


## 基本用法

`PnDataFrame` 使用内置的 HTML 表示来渲染底层的 DataFrame：


## 参数控制

与所有其他 Panel 对象一样，更改参数将更新视图，使我们能够控制数据框的样式：


## HTML 标记

通过将 `escape` 设置为 False，您可以在 `DataFrame` 组件中包含 *HTML 标记*：


## 大型数据框

对于较大的数据框，设置 `sizing_mode="stretch_both"` 可以确保它们不会*溢出*很有用。这样做时，可以使用 `max_height` 指定（最大）高度：


## Streamz DataFrames

除了渲染标准的 pandas `DataFrame` 和 `Series` 类型外，`PnDataFrame` 组件还将渲染更新的 `streamz` 类型：
注意：
- 在活动内核中，您应该看到数据框每 0.5 秒更新一次。
- `streamz` 当前在 Pyodide/PyScript 中不起作用。


## API

### 属性

| 属性名      | 说明                 | 类型                                                           | 默认值 |
| ---------- | ------------------- | ---------------------------------------------------------------| ------- |
| object     | 被显示的DataFrame对象 | ^[pandas.DataFrame, dask.DataFrame, streamz.DataFrame]          | None |
| bold_rows  | 在输出中使行标签加粗  | ^[boolean]                                                      | True |
| border     | 在开始的table标签中包含的边框宽度 | ^[int]                                                | 0 |
| classes    | 应用于结果HTML表格的CSS类 | ^[list[str]]                                                | None |
| col_space  | 每列的最小宽度（以CSS长度单位表示）| ^[int, str, dict]                                    | None |
| decimal    | 识别为小数分隔符的字符，例如欧洲的',' | ^[str]                                             | '.' |
| escape     | 将字符 <, >, 和 & 转换为HTML安全序列 | ^[boolean]                                        | True |
| float_format | 如果列元素是浮点数，则应用的格式化函数 | ^[function]                                     | None |
| formatters | 按位置或名称应用于列元素的格式化函数 | ^[dict, list]                                       | None |
| header     | 是否打印列标签        | ^[boolean]                                                     | True |
| index      | 是否打印索引（行）标签 | ^[boolean]                                                     | True |
| index_names | 是否打印索引的名称    | ^[boolean]                                                     | True |
| justify    | 如何对齐列标签        | ^[str]                                                          | None |
| max_rows   | 要显示的最大行数      | ^[int]                                                          | None |
| max_cols   | 要显示的最大列数      | ^[int]                                                          | None |
| na_rep     | NAN的字符串表示      | ^[str]                                                          | 'NaN' |
| render_links | 将URL转换为HTML链接 | ^[boolean]                                                     | False |
| show_dimensions | 显示DataFrame维度（行数乘以列数） | ^[boolean]                                       | False |
| sparsify   | 对于具有分层索引的DataFrame，设置为False以在每行打印每个多索引键 | ^[boolean]            | True |
| text_align | 如何对齐非标题单元格  | ^[str]                                                         | None |
| sizing_mode | 尺寸调整模式         | ^[str]                                                         | 'fixed' |
| width      | 宽度                 | ^[int, str]                                                    | None |
| height     | 高度                 | ^[int, str]                                                    | None |
| max_height | 最大高度             | ^[int]                                                         | None |

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | 自定义默认内容      |

### 方法

| 属性名 | 说明 | 类型 |
| --- | --- | --- |



# Plotly 图表

`PnPlotly` 组件允许在 Panel 应用程序中显示 [Plotly 图表](https://plotly.com/python/)。它通过对 Plotly 对象中包含的数组数据使用二进制序列化来提高图表更新速度。

请注意，要在 Jupyter 笔记本中使用 Plotly 组件，必须激活 Panel 扩展并包含 `"plotly"` 作为参数。这一步确保正确设置 plotly.js。

底层实现为`panel.pane.Plotly`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/Plotly.html


## 基本用法

让我们创建一个基本示例：

创建后，`PnPlotly` 组件可以通过分配新的图形对象来更新：
```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnButton @click="update_fig()">Update</PnButton>
  <PnPlotly :object="fig.value"/>
</template>
<script lang='py'>
from vuepy import ref
import numpy as np
import plotly.graph_objs as go

xx = np.linspace(-3.5, 3.5, 100)
yy = np.linspace(-3.5, 3.5, 100)
x, y = np.meshgrid(xx, yy)
z = np.exp(-((x - 1) ** 2) - y**2) - (x**3 + y**4 - x / 5) * np.exp(-(x**2 + y**2))

surface = go.Surface(z=z)
fig = go.Figure(data=[surface])

fig.update_layout(
    title="Plotly 3D",
    width=500,
    height=500,
    margin=dict(t=50, b=50, r=50, l=50),
)
fig = ref(fig)

def update_fig():
    new_fig = go.Figure(data=[go.Surface(z=np.sin(z+1))])
    new_fig.update_layout(
        title="Update Plotly 3D",
        width=500,
        height=500,
        margin=dict(t=50, b=50, r=50, l=50),
    )
    fig.value = new_fig
</script>

```


## 布局示例

`PnPlotly` 组件支持任意复杂度的布局和子图，允许显示即使是深度嵌套的 Plotly 图形：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnPlotly :object="fig_layout" />
</template>
<script lang='py'>
import numpy as np
import plotly.graph_objs as go
from plotly import subplots

heatmap = go.Heatmap(
    z=[[1, 20, 30],
       [20, 1, 60],
       [30, 60, 1]],
    showscale=False)

y0 = np.random.randn(50)
y1 = np.random.randn(50)+1

box_1 = go.Box(y=y0)
box_2 = go.Box(y=y1)
data = [heatmap, box_1, box_2]

fig_layout = subplots.make_subplots(
    rows=2, cols=2, specs=[[{}, {}], [{'colspan': 2}, None]],
    subplot_titles=('first subplot','second subplot', 'third subplot')
)

fig_layout.append_trace(box_1, 1, 1)
fig_layout.append_trace(box_2, 1, 2)
fig_layout.append_trace(heatmap, 2, 1)

fig_layout['layout'].update(height=600, width=600, title='i <3 subplots')
</script>

```


## 响应式图表

通过在 Plotly 布局上使用 `autosize` 选项和 `PnPlotly` 组件的响应式 `sizing_mode` 参数，可以使 Plotly 图表具有响应性：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnCol name="## A responsive plot" sizing_mode="stretch_width">
    <PnPlotly :object="fig_responsive" :height="300" sizing_mode="stretch_width" />
  </PnCol>
</template>
<script lang='py'>
import pandas as pd
import plotly.express as px

data = pd.DataFrame([
    ('Monday', 7), ('Tuesday', 4), ('Wednesday', 9), ('Thursday', 4),
    ('Friday', 4), ('Saturday', 4), ('Sunday', 4)], columns=['Day', 'Orders']
)

fig_responsive = px.line(data, x="Day", y="Orders")
fig_responsive.update_traces(mode="lines+markers", marker=dict(size=10), line=dict(width=4))
fig_responsive.layout.autosize = True
</script>

```


## 图表配置

您可以通过 `config` 参数设置 [Plotly 配置选项](https://plotly.com/javascript/configuration-options/)。让我们尝试配置 `scrollZoom`：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnCol name="## A responsive and scroll zoomable plot" 
         sizing_mode="stretch_width">
    <PnPlotly 
      :object="fig_responsive" 
      :config="{'scrollZoom': True}" 
      :height="300" 
      sizing_mode="stretch_width" />
  </PnCol>
</template>
<script lang='py'>
import pandas as pd
import plotly.express as px

data = pd.DataFrame([
    ('Monday', 7), ('Tuesday', 4), ('Wednesday', 9), ('Thursday', 4),
    ('Friday', 4), ('Saturday', 4), ('Sunday', 4)], columns=['Day', 'Orders']
)

fig_responsive = px.line(data, x="Day", y="Orders")
fig_responsive.update_traces(mode="lines+markers", marker=dict(size=10), line=dict(width=4))
fig_responsive.layout.autosize = True
</script>

```


尝试在图表上用鼠标滚动！

## 增量更新

您可以通过使用字典而不是 Plotly Figure 对象来高效地增量更新轨迹或布局，而不是更新整个 Figure。

请注意，增量更新只有在将 `Figure` 定义为字典时才会高效，因为 Plotly 会复制轨迹，这意味着原地修改它们没有效果。修改数组将仅发送该数组（使用二进制协议），从而实现快速高效的更新。

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnPlotly :object="fig_patch" ref="plotly_pane_patch" />
  <PnRow>
    <PnButton @click="update_z()">更新数据</PnButton>
    <PnButton @click="update_layout()">更新布局</PnButton>
    <PnButton @click="reset()">重置</PnButton>
  </PnRow>
</template>
<script lang='py'>
import numpy as np
import plotly.graph_objs as go
from vuepy import ref

xx = np.linspace(-3.5, 3.5, 100)
yy = np.linspace(-3.5, 3.5, 100)
x, y = np.meshgrid(xx, yy)
z = np.exp(-((x - 1) ** 2) - y**2) - (x**3 + y**4 - x / 5) * np.exp(-(x**2 + y**2))

surface = go.Surface(z=z)
layout = go.Layout(
    title='Plotly 3D 图表',
    autosize=False,
    width=500,
    height=500,
    margin=dict(t=50, b=50, r=50, l=50)
)

fig_patch = dict(data=[surface], layout=layout)
plotly_pane_patch = ref(None)

def update_z():
    surface.z = np.sin(z+1)
    plotly_pane_patch.value.unwrap().object = fig_patch
    
def update_layout():
    fig_patch['layout']['width'] = 800
    plotly_pane_patch.value.unwrap().object = fig_patch
    
def reset():
    surface.z = z
    fig_patch['layout']['width'] = 500
    plotly_pane_patch.value.unwrap().object = fig_patch
</script>

```


## 事件处理

`PnPlotly` 组件提供对 [Plotly 事件](https://plotly.com/javascript/plotlyjs-events/)的访问，如点击、悬停和选择(使用`Box Select`、`Lasso Select`工具)等：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnPlotly :object="fig" ref="plotly_ref" 
            @click='on_click'
            @selected='on_selected'
  />
</template>
<script lang='py'>
import numpy as np
import plotly.express as px
from vuepy import ref, onMounted

# 创建一些示例数据
df = px.data.iris()

# 创建散点图
fig = px.scatter(
    df, x="sepal_width", y="sepal_length", 
    color="species", size="petal_length",
    hover_data=["petal_width"]
)

# 事件数据引用
click_data = ref({})
hover_data = ref({})
plotly_ref = ref(None)

def on_click(event):
    if not event:
        return
    print(event.new['points']) # [{'curveNumber': 2, 'pointNumber': 31, 
                               #   'pointIndex': 31, 'x': 3.8, 'y': 7.9, 
                               #   'marker.size': 6.4, 'customdata': [2]}]
    click_data.value = event.new['points']
    
def on_selected(event):
    if not event:
        return
    print(event.new['points']) # [{'curveNumber': 2, 'pointNumber': 31, ...
</script>

```


## API

### 属性

| 属性名                      | 说明                          | 类型                                                           | 默认值 |
| -------------------------- | ----------------------------- | ---------------------------------------------------------------| ------- |
| object                     | 正在显示的 Plotly `Figure` 或字典对象 | ^[object]                                              | None |
| config                     | 图表的额外配置。参见 [Plotly 配置选项](https://plotly.com/javascript/configuration-options/) | ^[dict] | {} |
| link_figure                | 当 Plotly `Figure` 原地修改时更新显示的 Plotly 图表 | ^[boolean]                            | True |
| click_data                 | 来自 `plotly_click` 事件的点击事件数据 | ^[dict]                                                | {} |
| clickannotation_data       | 来自 `plotly_clickannotation` 事件的点击注释事件数据 | ^[dict]                           | {} |
| hover_data                 | 来自 `plotly_hover` 和 `plotly_unhover` 事件的悬停事件数据 | ^[dict]                       | {} |
| relayout_data              | 来自 `plotly_relayout` 事件的重新布局事件数据 | ^[dict]                                   | {} |
| restyle_data               | 来自 `plotly_restyle` 事件的重新样式事件数据 | ^[dict]                                    | {} |
| selected_data              | 来自 `plotly_selected` 和 `plotly_deselect` 事件的选择事件数据 | ^[dict]                  | {} |
| viewport                   | 当前视口状态，即显示图表的 x 和 y 轴限制。在 `plotly_relayout`、`plotly_relayouting` 和 `plotly_restyle` 事件时更新 | ^[dict] | {} |
| viewport_update_policy     | 用户交互期间更新视口参数的策略 | ^[str]                                                        | 'mouseup' |
| viewport_update_throttle   | 当 viewport_update_policy 为 "throttle" 时，视口更新同步的时间间隔（毫秒） | ^[int]              | 200 |
| sizing_mode                | 尺寸调整模式                   | ^[str]                                                         | 'fixed'  |
| width                      | 宽度                          | ^[int, str]                                                    | None    |
| height                     | 高度                          | ^[int, str]                                                    | None    |
| min_width                  | 最小宽度                      | ^[int]                                                         | None    |
| min_height                 | 最小高度                      | ^[int]                                                         | None    |
| max_width                  | 最大宽度                      | ^[int]                                                         | None    |
| max_height                 | 最大高度                      | ^[int]                                                         | None    |
| margin                     | 外边距                        | ^[int, tuple]                                                  | 5       |
| css_classes                | CSS类名列表                   | ^[list]                                                        | []      |

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |
| click  | 当元素被点击时触发的事件 | ^[Callable]`(Event) -> None`    |
| hover | 当元素被鼠标覆盖时触发 | ^[Callable]`(Event) -> None`    |
| selected | 当元素被`Box Select`、`Lasso Select`工具选中时触发 | ^[Callable]`(Event) -> None`    |
| doubleclick  | 当元素被双击时触发的事件 | ^[Callable]`(Event) -> None`    |
| clickannotation | 当元素被鼠标覆盖时触发 | ^[Callable]`(Event) -> None`    |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | 自定义默认内容      |




# PDF 文档

`PnPDF` 组件如果提供本地路径，则将 `.pdf` 文档嵌入到面板中，或者如果提供 URL，则会链接到远程文件。

底层实现为`panel.pane.PDF`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/PDF.html


## 基本用法

`PnPDF` 组件可以指向任何本地或远程 `.pdf` 文件。如果给定以 `http` 或 `https` 开头的 URL，则 `embed` 参数决定 PDF 是嵌入还是链接到：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnPDF 
    object="https://assets.holoviz.org/panel/samples/pdf_sample.pdf" 
    :width="700" 
    :height="1000" />
</template>

```


与任何其他组件一样，可以通过设置 `object` 参数来更新 `PnPDF` 组件：

```vue
<!-- --plugins vpanel --show-code -->
<template>
<PnCol>
  <PnPDF 
    :object="pdf_url.value" 
    :width="700" 
    :height="1000" 
  />
  <PnButton @click="update_pdf()">更新 PDF</PnButton>
</PnCol>
</template>
<script lang='py'>
from vuepy import ref
pdf_url = ref("https://assets.holoviz.org/panel/samples/pdf_sample.pdf")

def update_pdf():
    pdf_url.value = "https://assets.holoviz.org/panel/samples/pdf_sample2.pdf"
</script>

```


## 设置起始页

使用 `start_page` 参数，您可以指定加载页面时 PDF 文件的起始页：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnPDF 
    object="https://assets.holoviz.org/panel/samples/pdf_sample2.pdf" 
    :start_page="2"
    :width="700" 
    :height="1000" />
</template>

```


## API

### 属性

| 属性名       | 说明                          | 类型                                                           | 默认值 |
| ----------- | ----------------------------- | ---------------------------------------------------------------| ------- |
| object      | 要显示的 PDF 文件。可以是指向本地或远程文件的字符串，或具有 `_repr_pdf_` 方法的对象 | ^[str, object] | None |
| embed       | 如果给定 URL 到文件，这决定 PDF 是否将被嵌入为 base64 或仅链接到 | ^[boolean]                 | False |
| start_page  | 加载页面时 `.pdf` 文件的起始页 | ^[int]                                                         | None |
| styles      | 指定 CSS 样式的字典           | ^[dict]                                                        | {} |
| sizing_mode | 尺寸调整模式                   | ^[str]                                                         | 'fixed'  |
| width       | 宽度                          | ^[int, str]                                                    | None    |
| height      | 高度                          | ^[int, str]                                                    | None    |
| min_width   | 最小宽度                      | ^[int]                                                         | None    |
| min_height  | 最小高度                      | ^[int]                                                         | None    |
| max_width   | 最大宽度                      | ^[int]                                                         | None    |
| max_height  | 最大高度                      | ^[int]                                                         | None    |
| margin      | 外边距                        | ^[int, tuple]                                                  | 5       |
| css_classes | CSS类名列表                   | ^[list]                                                        | []      |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | 自定义默认内容      |




# ReactiveExpr 响应式表达式

`PnReactiveExpr` 组件可以渲染 [Param `rx` 对象](https://param.holoviz.org/user_guide/Reactive_Expressions.html)，它代表一个响应式表达式，同时显示表达式中包含的小部件和表达式的最终输出。小部件相对于输出的位置可以设置，也可以完全移除小部件。

请注意，当导入 `panel_vuepy as vpanel` 时，可以使用 `vpanel.rx` 代替 [`param.rx`](https://param.holoviz.org/user_guide/Reactive_Expressions.html)。

有关使用 `rx` 的详细信息，请参阅 [`param.rx` 文档](https://param.holoviz.org/user_guide/Reactive_Expressions.html)。

底层实现为`panel.pane.ReactiveExpr`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/ReactiveExpr.html

建议用`vuepy`的`computed` 来代替该功能。

## 基本用法

[`param.rx`](https://param.holoviz.org/user_guide/Reactive_Expressions.html) API 是构建声明式和响应式 UI 的强大工具。

让我们看几个例子：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnReactiveExpr :object="rx_model" />
</template>
<script lang='py'>
import panel as pn

def model(n):
    return f"🤖 {n}x2 等于 {n*2}"

n = pn.widgets.IntSlider(value=2, start=0, end=10)
rx_model = pn.rx(model)(n=n)
</script>

```


在底层，Panel 确保上面的*响应式表达式*被渲染在 `PnReactiveExpr` 组件中。您也可以显式地这样做：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnReactiveExpr :object="rx_model" />
</template>
<script lang='py'>
import panel as pn

def model(n):
    return f"🤖 {n}x2 等于 {n*2}"

n = pn.widgets.IntSlider(value=2, start=0, end=10)
rx_model = pn.rx(model)(n=n)
</script>

```


响应式表达式从不是"死胡同"。您始终可以更新和更改*响应式表达式*。

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnReactiveExpr :object="expr" />
</template>
<script lang='py'>
import panel as pn

def model(n):
    return f"🤖 {n}x2 等于 {n*2}"

n = pn.widgets.IntSlider(value=2, start=0, end=10)
expr = pn.rx(model)(n=n) + "\n\n🧑 谢谢"
</script>

```


您还可以组合*响应式表达式*：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnReactiveExpr :object="expr" />
</template>
<script lang='py'>
import panel as pn

x = pn.widgets.IntSlider(value=2, start=0, end=10, name="x")
y = pn.widgets.IntSlider(value=2, start=0, end=10, name="y")

expr = x.rx()*"⭐" + y.rx()*"⭐"
</script>

```


## 布局选项

您可以更改 `widget_location`：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnReactiveExpr :object="expr" widget_location="top" />
</template>
<script lang='py'>
import panel as pn

x = pn.widgets.IntSlider(value=2, start=0, end=10, name="x")
y = pn.widgets.IntSlider(value=2, start=0, end=10, name="y")

expr = x.rx()*"⭐" + "\n\n" + y.rx()*"❤️"
</script>

```


您可以将 `widget_layout` 更改为 `Row`：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnReactiveExpr :object="expr" :widget_layout="PnRow" />
</template>
<script lang='py'>
import panel as pn

x = pn.widgets.IntSlider(value=2, start=0, end=10, name="x")
y = pn.widgets.IntSlider(value=2, start=0, end=10, name="y")

expr = x.rx()*"⭐" + "\n\n" + y.rx()*"❤️"
PnRow = pn.Row
</script>

```


您可以水平 `center` 输出：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnReactiveExpr :object="expr" :center="True" />
</template>
<script lang='py'>
import panel as pn

x = pn.widgets.IntSlider(value=2, start=0, end=10, name="x")
y = pn.widgets.IntSlider(value=2, start=0, end=10, name="y")

expr = x.rx()*"⭐" + "\n\n" + y.rx()*"❤️"
</script>

```


通过设置 `show_widgets=False` 可以隐藏小部件：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnReactiveExpr :object="expr" :show_widgets="False" />
</template>
<script lang='py'>
import panel as pn

x = pn.widgets.IntSlider(value=2, start=0, end=10, name="x")
y = pn.widgets.IntSlider(value=2, start=0, end=10, name="y")

expr = x.rx()*"⭐" + "\n\n" + y.rx()*"❤️"
</script>

```


## 响应式表达式作为引用

在笔记本中显式或隐式地使用 `PnReactiveExpr` 组件非常适合探索。但这并不是很高效，因为每当响应式表达式重新渲染时，Panel 都必须创建一个新的组件来渲染您的输出。

相反，您可以并且应该将*响应式表达式*作为*引用*传递给特定的 Panel 组件。Panel 组件可以动态解析表达式的值：



> **引用方法通常应该是首选**，因为它更具声明性和明确性，允许 Panel 有效地更新现有视图，而不是完全重新渲染输出。

## 样式化 DataFrame 示例

让我们通过一个稍微复杂一点的例子来展示，构建一个表达式来动态加载一些数据并从中采样 N 行：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnReactiveExpr :object="df_rx" />
</template>
<script lang='py'>
import pandas as pd
import panel as pn

dataset = pn.widgets.Select(name='选择数据集', options={
    'penguins': 'https://datasets.holoviz.org/penguins/v1/penguins.csv',
    'stocks': 'https://datasets.holoviz.org/stocks/v1/stocks.csv'
})
nrows = pn.widgets.IntSlider(value=5, start=0, end=20, name='N 行')

# 加载当前选择的数据集并从中采样 nrows
df_rx = pn.rx(pd.read_csv)(dataset).sample(n=nrows)
</script>

```


现在我们有了一个符合我们需求的表达式，可以将其用作引用来响应式地更新 `Tabulator` 小部件的 `value`：

```vue
<!-- --plugins vpanel --show-code -->
<template>
    <PnCol>
      <PnSelect v-model="dataset.value" name='选择数据集' :options="options" />
      <PnIntSlider v-model="nrows.value" :start="0" :end="20" name="N 行" />
    </PnCol>
    <PnTabulator :value="df_rx.value" :page_size="5" pagination="remote" />
</template>
<script lang='py'>
import pandas as pd
import panel as pn
from vuepy import ref, computed

dataset = ref('https://datasets.holoviz.org/stocks/v1/stocks.csv')
nrows = ref(5)
options = {'penguins': 'https://datasets.holoviz.org/penguins/v1/penguins.csv',
           'stocks': 'https://datasets.holoviz.org/stocks/v1/stocks.csv'}

# 创建响应式表达式
# df_rx = pn.rx(lambda url, n: pd.read_csv(url).sample(n=n))(url=dataset, n=nrows)
@computed
def df_rx():
    return pd.read_csv(dataset.value).sample(n=nrows.value)
</script>

```


## API

### 属性

| 属性名            | 说明                          | 类型                                                           | 默认值 |
| ---------------- | ----------------------------- | ---------------------------------------------------------------| ------- |
| object           | 一个 `param.reactive` 表达式    | ^[param.reactive]                                              | None |
| center           | 是否水平居中输出               | ^[bool]                                                        | False |
| show_widgets     | 是否显示小部件                 | ^[bool]                                                        | True |
| widget_layout    | 用于显示小部件的布局对象。例如 `pn.WidgetBox`（默认），`pn.Column` 或 `pn.Row` | ^[ListPanel] | WidgetBox |
| widget_location  | 小部件相对于响应式表达式输出的位置。可选值包括 'left', 'right', 'top', 'bottom', 'top_left', 'top_right', 'bottom_left', 'bottom_right', 'left_top'（默认）, 'right_top', 'right_bottom' | ^[str] | 'left_top' |
| sizing_mode      | 尺寸调整模式                  | ^[str]                                                         | 'fixed'  |
| width            | 宽度                          | ^[int, str]                                                    | None    |
| height           | 高度                          | ^[int, str]                                                    | None    |
| min_width        | 最小宽度                      | ^[int]                                                         | None    |
| min_height       | 最小高度                      | ^[int]                                                         | None    |
| max_width        | 最大宽度                      | ^[int]                                                         | None    |
| max_height       | 最大高度                      | ^[int]                                                         | None    |
| margin           | 外边距                        | ^[int, tuple]                                                  | 5       |
| css_classes      | CSS类名列表                   | ^[list]                                                        | []      |

### 属性值

* **`widgets`** (ListPanel): 返回位于 `widget_layout` 中的小部件。

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | 自定义默认内容      |



# PNG 图像

`PnPNG` 组件如果提供本地路径，则将 `.png` 图像文件嵌入到面板中，或者如果提供 URL，则会链接到远程图像。

底层实现为`panel.pane.PNG`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/PNG.html


## 基本用法

`PnPNG` 组件可以指向任何本地或远程 `.png` 文件。如果给定以 `http` 或 `https` 开头的 URL，则 `embed` 参数决定图像是嵌入还是链接到：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnPNG object="https://assets.holoviz.org/panel/samples/png_sample.png" />
</template>

```


## 调整大小

我们可以通过设置特定的固定 `width` 或 `height` 来调整图像的大小：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnPNG 
    object="https://assets.holoviz.org/panel/samples/png_sample.png"
    :width="400" />
</template>

```


或者，我们可以使用 `sizing_mode` 来调整宽度和高度：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnPNG 
    object="https://assets.holoviz.org/panel/samples/png_sample2.png"
    sizing_mode="scale_width" />
</template>

```


请注意，默认情况下，图像的宽高比是固定的，因此即使在响应式调整大小模式下，图像旁边或下方也可能有空隙。要覆盖此行为，请设置 `fixed_aspect=false` 或提供固定的 `width` 和 `height` 值。

## 设置链接 URL

使用 `link_url` 参数，您可以使图像可点击并链接到其他网站：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnPNG 
    object="https://assets.holoviz.org/panel/samples/png_sample.png"
    link_url="https://panel.holoviz.org/"
    :width="400" />
</template>

```


## API

### 属性

| 属性名          | 说明                          | 类型                                                           | 默认值 |
| -------------- | ----------------------------- | ---------------------------------------------------------------| ------- |
| object         | 要显示的 PNG 文件。可以是指向本地或远程文件的字符串，或具有 `_repr_png_` 方法的对象 | ^[str, object] | None |
| alt_text       | 添加到图像标签的替代文本。当用户无法加载或显示图像时显示替代文本 | ^[str]                   | None |
| embed          | 如果给定图像 URL，这决定图像是否将被嵌入为 base64 或仅链接到 | ^[boolean]                  | False |
| fixed_aspect   | 是否强制图像的宽高比相等       | ^[boolean]                                                     | True |
| link_url       | 使图像可点击并链接到其他网站的链接 URL | ^[str]                                                  | None |
| styles         | 指定 CSS 样式的字典           | ^[dict]                                                        | {} |
| sizing_mode    | 尺寸调整模式                   | ^[str]                                                         | 'fixed'  |
| width          | 宽度                          | ^[int, str]                                                    | None    |
| height         | 高度                          | ^[int, str]                                                    | None    |
| min_width      | 最小宽度                      | ^[int]                                                         | None    |
| min_height     | 最小高度                      | ^[int]                                                         | None    |
| max_width      | 最大宽度                      | ^[int]                                                         | None    |
| max_height     | 最大高度                      | ^[int]                                                         | None    |
| margin         | 外边距                        | ^[int, tuple]                                                  | 5       |
| css_classes    | CSS类名列表                   | ^[list]                                                        | []      |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | 自定义默认内容      |




# Markdown 文本

`PnMarkdown` 组件允许在面板中渲染任意 [Markdown](https://python-markdown.github.io)。它渲染包含有效 Markdown 的字符串以及具有 `_repr_markdown_` 方法的对象，还可以定义自定义 CSS 样式。

底层实现为`panel.pane.Markdown`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/Markdown.html


## 基本用法

`PnMarkdown`/`PnMD` 组件接受所有*基本* Markdown 语法，包括嵌入式 HTML。它还支持大多数*扩展* Markdown 语法。

要在代码块中启用代码高亮显示，需要安装 `pip install pygments`

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnMarkdown :width="500">
# Markdown 示例

这个示例文本来自 [The Markdown Guide](https://www.markdownguide.org)!

## 基本语法

这些是 John Gruber 原始设计文档中概述的元素。所有 Markdown 应用程序都支持这些元素。

### 标题

# H1
## H2
### H3

### 粗体

**粗体文本**

### 斜体

*斜体文本*

### 引用块

> 引用块

### 有序列表

1. 第一项
2. 第二项
3. 第三项

### 无序列表

- 第一项
- 第二项
- 第三项

### 代码

`代码`

### 水平分割线

---

### 链接

[Markdown 指南](https://www.markdownguide.org)

### 图像

![替代文本](https://www.markdownguide.org/assets/images/tux.png)

## 扩展语法

这些元素通过添加额外的功能来扩展基本语法。并非所有 Markdown 应用程序都支持这些元素。

### 表格

| 语法 | 描述 |
| ----------- | ----------- |
| 标题 | 标题 |
| 段落 | 文本 |

### 围栏代码块

```
{
  "firstName": "John",
  "lastName": "Smith",
  "age": 25
}
```

### 脚注

这里有一个带有脚注的句子。[^1]

[^1]: 这是脚注。

### 定义列表

术语
: 该术语的一些定义

### 删除线

~~地球是平的。~~

### 任务列表

- [x] 写新闻稿
- [ ] 更新网站
- [ ] 联系媒体

### 表情符号

太有趣了！😂

(另见 [复制和粘贴表情符号](https://www.markdownguide.org/extended-syntax/#copying-and-pasting-emoji))
"""
</PnMarkdown>
</template>

```

还可以通过`object`设置内容。
```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnMarkdown :object="markdown_content" :width="500" />
</template>
<script lang='py'>
markdown_content = """
# Markdown 示例

这个示例文本来自 [The Markdown Guide](https://www.markdownguide.org)!
"""
</script>

```

## 动态内容

vuepy 的响应式特性可以与 `Markdown` 组件的无缝集成，`Slider` 调整时，`Markdown` 内容中的值会实时更新，
```vue
<!-- --plugins vpanel --show-code -->
<template>
<PnCol>
  <PnIntSlider v-model='val.value' :end='10'/>
  <PnMD :width="500">

# h1
slider value: {{ val.value }}

  </PnMD>
</PnCol>
</template>
<script lang='py'>
from vuepy import ref

val = ref(1)

</script>

```


## 样式

如果您想控制从 Markdown 源生成的 HTML 的行为，通常可以通过向此组件的 `style` 参数传递参数来实现。例如，您可以在 Markdown 表格周围添加蓝色边框，如下所示：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnMarkdown style="border: 4px solid blue">
| 语法 | 描述 |
| ----------- | ----------- |
| 标题 | 标题 |
| 段落 | 文本 |
  </PnMarkdown>
</template>

```


但是，以这种方式指定的样式只会应用于最外层的 Div，目前没有任何方法以这种方式将样式应用于 HTML 的特定内部元素。在这种情况下，我们无法使用 `style` 参数来控制生成表格的行或标题的样式。

如果我们想更改生成的 HTML 的特定内部元素，我们可以通过提供 HTML/CSS &lt;style&gt; 部分来实现。例如，我们可以按如下方式更改标题和数据的边框厚度，但请注意，更改将应用于后续的 Markdown，包括笔记本上下文中的其他单元格：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnMarkdown :object="styled_table_md" />
</template>
<script lang='py'>
styled_table_md = """
<style>
table, th, td {
  border: 5px solid black;
}
</style>
| 语法 | 描述 |
| ----------- | ----------- |
| 标题 | 标题 |
| 段落 | 文本 |
"""
</script>

```


如果您只想为特定的 Markdown 文本更改样式，您可以通过添加可以用样式表针对的 CSS 类来轻松实现这一点。这里我们添加了 `special_table` 类，然后表格使用红色边框：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnMarkdown :object="special_md" :stylesheets="[css]" />
</template>
<script lang='py'>
css = """
div.special_table + table * {
  border: 1px solid red;
}
"""

special_md = """
<div class="special_table"></div>

| 语法 | 描述 |
| ----------- | ----------- |
| 标题 | 标题 |
| 段落 | 文本 |
"""
</script>

```


## 渲染器

自 1.0 版本以来，Panel 使用 [`markdown-it`](https://markdown-it-py.readthedocs.io/en/latest/) 作为默认的 markdown 渲染器。如果您想恢复之前的默认值 `'markdown'` 或切换到 `MyST` 风格的 Markdown，可以通过 `renderer` 参数设置它。例如，这里我们使用 'markdown-it' 和 'markdown' 渲染一个任务列表：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnRow>
    <PnMarkdown renderer='markdown-it'>
markdown-it  
- [ ] 鸡蛋
- [x] 面粉
- [x] 牛奶
    </PnMarkdown>
    <PnMarkdown renderer='markdown'>
markdown  

- [ ] 鸡蛋
- [x] 面粉
- [x] 牛奶
    </PnMarkdown>
  </PnRow>
</template>

```


## LaTeX 支持

`PnMarkdown` 组件也支持数学渲染，方法是用 `$$` 分隔符封装要渲染的字符串。要启用 LaTeX 渲染，您必须在 `pn.extension` 调用中显式加载 'mathjax' 扩展。

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnMarkdown :object="latex_md" :width="800" />

  <PnMarkdown :width="800">
Markdown 组件支持用双 $ 分隔符封装的字符串的数学渲染：$$\sum_{j}{\sum_{i}{a*w_{j, i}}}$$
  </PnMarkdown>
</template>
<script lang='py'>
import panel as pn
pn.extension('mathjax')

latex_md = r"""
Markdown 组件支持用双 $ 分隔符封装的字符串的数学渲染：$$\sum_{j}{\sum_{i}{a*w_{j, i}}}$$
"""
</script>

```


请注意使用 `r` 前缀创建字符串作为*原始*字符串。Python 原始字符串将反斜杠字符 (\\) 视为文字字符。例如，这不起作用：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <p>without r</p>
  <PnMarkdown :object="bad_latex" />
  <p>with r</p>
  <PnMarkdown :object="good_latex" />
</template>
<script lang='py'>
bad_latex = "$$\frac{1}{n}$$"
good_latex = r"$$\frac{1}{n}$$"
</script>

```


## API

### 属性

| 属性名             | 说明                          | 类型                                                           | 默认值 |
| ----------------- | ----------------------------- | ---------------------------------------------------------------| ------- |
| object            | 包含 Markdown 的字符串，或具有 `_repr_markdown_` 方法的对象 | ^[str, object]               | None |
| dedent            | 是否对所有行去除共同的空白     | ^[boolean]                                                    | True |
| disable_anchors   | 是否禁用自动为标题添加锚点     | ^[boolean]                                                    | False |
| disable_math      | 是否禁用使用 `$$` 分隔符转义的字符串的 MathJax 数学渲染 | ^[boolean]                     | False |
| enable_streaming  | 是否启用文本片段的流式传输。这将在更新时对 `object` 进行差异比较，只发送添加的尾部块 | ^[boolean] | False |
| extensions        | 要使用的 [Python-Markdown 扩展](https://python-markdown.github.io/extensions/) 列表（不适用于 'markdown-it' 和 'myst' 渲染器） | ^[list] | None |
| hard_line_break   | 简单的新行是否渲染为硬换行。默认为 False 以符合原始 Markdown 规范。`'myst'` 渲染器不支持 | ^[boolean] | False |
| plugins           | 要应用的其他 markdown-it-py 插件的列表 | ^[function]                                          | None |
| renderer          | Markdown 渲染器实现           | ^[literal: `'markdown-it'`, `'markdown'`, `'myst'`]          | 'markdown-it' |
| renderer_options  | 传递给 markdown 渲染器的选项   | ^[dict]                                                       | None |
| styles            | 指定 CSS 样式的字典           | ^[dict]                                                        | {} |
| sizing_mode       | 尺寸调整模式                   | ^[str]                                                         | 'fixed'  |
| width             | 宽度                          | ^[int, str]                                                    | None    |
| height            | 高度                          | ^[int, str]                                                    | None    |
| min_width         | 最小宽度                      | ^[int]                                                         | None    |
| min_height        | 最小高度                      | ^[int]                                                         | None    |
| max_width         | 最大宽度                      | ^[int]                                                         | None    |
| max_height        | 最大高度                      | ^[int]                                                         | None    |
| margin            | 外边距                        | ^[int, tuple]                                                  | 5       |
| css_classes       | CSS类名列表                   | ^[list]                                                        | []      |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | markdown内容      |




# Placeholder 占位符组件

占位符组件用于其他Panel组件的占位符。例如，可以在计算运行时显示一条消息。

底层实现为`panel.pane.Placeholder`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/Placeholder.html


## 基本用法

`PnPlaceholder`组件可以接受任何Panel组件作为其参数，包括其他panes。

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnPlaceholder object="Hello" style='color: red'/>
</template>

```


使用`PnPlaceholder`的好处是它允许您替换窗格的内容，而不受特定类型组件的限制。这意味着您可以用任何其他窗格类型替换占位符，包括图表、图像和小部件。

```vue
<!-- --plugins vpanel --show-code -->
<template>
<PnCol>
  <PnPlaceholder :object="message.value" />
  <PnRow>
    <PnButton @click="updateText()">Update Text</PnButton>
    <PnButton @click="updateInput()">Update Input</PnButton>
    <PnButton @click="resetContent()">Reset</PnButton>
  </PnRow>
</PnCol>
</template>

<script lang='py'>
from vuepy import ref

message = ref("Hello")

def updateText():
    # placeholder.value.update("Hello again!")
    message.value = "Hello again!"
    
def updateInput():
    from panel.widgets import TextInput
    # placeholder.value.update(TextInput(value="Type something..."))
    message.value = TextInput(value="Type something...")
    
def resetContent():
    # placeholder.value.object = "Hello"
    message.value = "Hello"
</script>

```


## 临时替换内容

如果你想临时替换内容，可以使用上下文管理器。

```vue
<!-- --plugins vpanel --show-code -->
<template>
<PnCol>
  <PnPlaceholder ref="placeholder_ref" object="⏳ Idle" 
                 :stylesheets="[':host { font-size: 24pt }']" />
  <PnButton @click="runProcess()">Run Process</PnButton>
</PnCol>
</template>

<script lang='py'>
from vuepy import ref
import asyncio
import time

placeholder_ref = ref(None)

async def runProcess():
    placeholder = placeholder_ref.value.unwrap()
    with placeholder:
        placeholder.update("🚀 Starting...")
        # time.sleep(1)
        await asyncio.sleep(1)
        placeholder.update("🏃 Running...")
        # time.sleep(1)
        await asyncio.sleep(1)
        placeholder.update("✅ Complete!")
        # time.sleep(1)
        await asyncio.sleep(1)
</script>

```


## API

### 属性

| 属性名       | 说明                                                     | 类型       | 默认值 |
| ------------ | -------------------------------------------------------- | ---------- | ------ |
| value        | 要显示的Panel对象，如果对象不是Panel对象，将使用`panel(...)`函数转换 | ^[Any]     | —      |
| stylesheets  | 样式表列表                                               | ^[List]    | []     |
| style | css样式 | ^[str]    | ''     |

### 方法

| 方法名 | 说明                   | 类型                    |
| ------ | ---------------------- | ----------------------- |
| update | 更新占位符中显示的内容 | ^[Callable]`(obj) -> None` |




# Textual 终端UI组件

`PnTextual` 组件允许在 Panel 应用程序中渲染 [Textual](https://textual.textualize.io/) 应用程序。它通过补丁方式实现了一个自定义 Panel 驱动程序，并将应用程序渲染到 [`Terminal`](../widgets/Terminal.ipynb) 组件中，完全支持鼠标和键盘事件。

底层实现为`panel.pane.Textual`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/Textual.html


## 基本用法

需要注意以下几点：

- 一旦 `App` 实例被绑定到 `PnTextual` 组件，它就不能在另一个组件中重用，并且每个 App 实例只能绑定到单个会话。
- 应用程序必须在与它将运行的服务器相同的线程上实例化，例如，如果您使用 `pn.serve(..., threaded=True)` 提供应用程序，则必须在函数内部实例化 `App`。

`PnTextual` 组件可以直接接收 Textual `App`，Panel 将处理其余部分，即启动应用程序、处理输入、重新渲染等。换句话说，应用程序将像在常规终端中运行一样工作。

让我们从一个非常简单的例子开始：

<img style="width:500px" src="data:image/png;base64,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Vq1a2cILdrIOQVPplrPOYl999Y19N3Jkon31bZx11pa2Wpcu9seff9g7QcsrV26gQog1V1vFZg4KFd7/cKBNnjy5viSqsj0tAd66dStbafnlrE2bOeyjjz+3H0ePLsleifEnHrwrLFxRAczsrVuHx6u12pY77hnxKilRIkMAAhCAAAQgMEMCVRHg+jB45J5+Ye23aq633/2Asj9y5u3Qwe665eowI1ODtHpsv8cMM0UECEAAAhBomEClAny7rTe3vXfb2WadbVZzvZpVO/75oK/s+EDQKxx+0L622T83jmrQtU315wM+GGhnnnuRVqMgQXjgvnta9026Wps554y2uwWl/fL/XrdL+l5fMIaIxPodN15pc845RxhV8b78arAtu8xSUQssbTvjnAttzTVWC7tFxfth//vJZ+3aG/uFxyalpUHSXn3tTTvy0P1smaWXsvnn7RCmO3rMWBsydKjdePNdJRUOVCLAJZLPPvV4W3GFZQuYyniX714XXGo/jRkT5qehf+rmdexRh4RR7n3gUVtv3bXCQg9tuPLaW+zJZ/9T5/C0+KSVTh0D2QABCEAAAhDwgEBVBHiP7v+0nocfEGZffcnUp6yS8NDdt9icc0z/uGqopqaSc3AsBCAAgeZEoD4BvnjQfejSC3rZux98aL3/1dcO3GcP22n7rUKBpxpwF64NuhgtEcxaURwkBDffTk3Vze69/QZrP1e74ij222+/2dY771Ow/bQTe4aDlRVsTFj5dvgIO+iI46M9yy+7jF3+r3Oi9foWZFdceMfjuffKCssvGzbRj+/TIKCLLLygtWzZMr45Wla6d9/3cKMHLytXgOu9evgh+xbMEhIZEVuQPTff3t8efOSJ2Na6izddc6ktEjRFV/ztd9vf1ltnTTvhmMPDiN+PHGX7HlL3vZ0Wn7TSqZsrtkAAAhCAAASyT6AqAvywoNZj2y03C3P/2ptv27kXXlYRiSv6nB+Nin71Dbfa4089V1F6HAwBCECguROoT4DvuesOttduO5maJW+3637WYe657cRAmA0e+q3dcMsdEbZll1rSdt5xa1s7qFV2fcS187Irb7BnX3gpjKdBv0465gibt8M84bpaMan2++nnXrTXg3dDPPzr3DNslZVXDDdpqsrB3wy1d957336dONE2+MfaJtHmQvGYIvvsvpP9Y+01bbFFF3FRbPRPY2z4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uzAWAhCAAAQgAAEIQAACEIAABHwlgAD31XPYDQEIQAACEIAABCAAAQhAAAJeEUCAe+UujIUABCAAAQhAAAIQgAAEIAABXwkgwH31HHZDAAIQgAAEIAABCEAAAhCAgFcEEOBeuQtjIQABCEAAAhCAAAQgAAEIQMBXAghwXz2H3RCAAAQgAAEIQAACEIAABCDgFQEnwP8fAAD//7pmnuwAACTtSURBVO3dd5hddZkH8DeNJEAoEZYSAkvvVQRkkQVBgQeli1QBQfrSkQdxBZQiEhWQHno19KU3MWQpihTpVSCEEhAJEJJJZfaem70305LJzNx5yUw+93mSe+8pv/ecz33/+c5pPQYOHFgfXgQIECBAgAABAgQIECBAgECnCLz00kvlcXsI4J3ia1ACBAgQIECAAAECBAgQIFAWEMA1AgECBAgQIECAAAECBAgQSBAQwBOQlSBAgAABAgQIECBAgAABAgK4HiBAgAABAgQIECBAgAABAgkCAngCshIECBAgQIAAAQIECBAgQEAA1wMECBAgQIAAAQIECBAgQCBBQABPQFaCAAECBAgQIECAAAECBAgI4HqAAAECBAgQIECAAAECBAgkCAjgCchKECBAgAABAgQIECBAgAABAVwPECBAgAABAgQIECBAgACBBAEBPAFZCQIECBAgQIAAAQIECBAgIIDrAQIECBAgQIAAAQIECBAgkCAggCcgK0GAAAECBAgQIECAAAECBARwPUCAAAECBAgQIECAAAECBBIEBPAEZCUIECBAgAABAgQIECBAgIAArgcIECBAgAABAgQIECBAgECCgACegKwEAQIECBAgQIAAAQIECBAQwPUAAQIECBAgQIAAAQIECBBIEBDAE5CVIECAAAECBAgQIECAAAECArgeIECAAAECBAgQIECAAAECCQICeAKyEgQIECBAgAABAgQIECBAQADXAwQIECBAgAABAgQIECBAIEFAAE9AVoIAAQIECBAgQIAAAQIECAjgeoAAAQIECBAgQIAAAQIECCQICOAJyEoQIECAAAECBAgQIECAAAEBXA8QIECAAAECBAgQIECAAIEEAQE8AVkJAgQIECBAgAABAgQIECAggOsBAgQIECBAgAABAgQIECCQICCAJyArQYAAAQIECBAgQIAAAQIEBHA9QIAAAQIECBAgQIAAAQIEEgQE8ARkJQgQIECAAAECBAgQIECAgACuBwgQIECAAAECBAgQIECAQIKAAJ6ArAQBAgQIECBAgAABAgQIEBDA9QABAgQIECBAgAABAgQIEEgQEMATkJUgQIAAAQIECBAgQIAAAQICuB4gQIAAAQIECBAgQIAAAQIJAgJ4ArISBAgQIECAAAECBAgQIEBAANcDBAgQIECAAAECBAgQIEAgQUAAT0BWggABAgQIECBAgAABAgQICOB6gAABAgQIECBAgAABAgQIJAgI4AnIShAgQIAAAQIECBAgQIAAAQFcDxAgQIAAAQIECBAgQIAAgQQBATwBWQkCBAgQIECAAAECBAgQICCA6wECBAgQIECAAAECBAgQIJAgIIAnICtBgAABAgQIECBAgAABAgQEcD1AgAABAgQIECBAgAABAgQSBATwBGQlCBAgQIAAAQIECBAgQICAAK4HCBAgQIAAAQIECBAgQIBAgoAAnoCsBAECBAgQIECAAAECBAgQEMD1AAECBAgQIECAAAECBAgQSBAQwBOQlSBAgAABAgQIECBAgAABAgK4HiBAgAABAgQIECBAgAABAgkCAngCshIECBAgQIAAAQIECBAgQEAA1wMECBAgQIAAAQIECBAgQCBBQABPQFaCAAECBAgQIECAAAECBAgI4HqAAAECBAgQIECAAAECBAgkCAjgCchKECBAgAABAgQIECBAgAABAVwPECBAgAABAgQIECBAgACBBAEBPAFZCQIECBAgQIAAAQIECBAgIIDrAQIECBAgQIAAAQIECBAgkCAggCcgK0GAAAECBAgQIECAAAECBARwPUCAAAECBAgQIECAAAECBBIEBPAEZCUIECBAgAABAgQIECBAgIAArgcIECBAgAABAgQIECBAgECCgACegKwEAQIECBAgQIAAAQIECBAQwPUAAQIECBAgQIAAAQIECBBIEBDAE5CVIECAAAECBAgQIECAAAECArgeIECAAAECBAgQIECAAAECCQICeAKyEgQIECBAgAABAgQIECBAQADXAwQIECBAgAABAgQIECBAIEFAAE9AVoIAAQIECBAgQIAAAQIECAjgeoAAAQIECBAgQIAAAQIECCQICOAJyEoQIECAAAECBAgQIECAAAEBXA8QIECAAAECBAgQIECAAIEEAQE8AVkJAgQIECBAgAABAgQIECAggOsBAgQIECBAgAABAgQIECCQICCAJyArQYAAAQIECBAgQIAAAQIEBHA9QIAAAQIECBAgQIAAAQIEEgQE8ARkJQgQIECAAAECBAgQIECAgACuBwgQIECAAAECBAgQIECAQIKAAJ6ArAQBAgQIECBAgAABAgQIEBDA9QABAgQIECBAgAABAgQIEEgQEMATkJUgQIAAAQIECBAgQIAAAQICuB4gQIAAAQIECBAgQIAAAQIJAgJ4ArISBAgQIECAAAECBAgQIEBAANcDBAgQIECAAAECBAgQIEAgQUAAT0BWggABAgQIECBAgAABAgQICOB6gAABAgQIECBAgAABAgQIJAgI4AnIShAgQIAAAQIECBAgQIAAAQFcDxAgQIAAAQIECBAgQIAAgQQBATwBWQkCBAgQIECAAAECBAgQICCA6wECBAgQIECAAAECBAgQIJAgIIAnICtBgAABAgQIECBAgAABAgQEcD1AgAABAgQIECBAgAABAgQSBATwBGQlCBAgQIAAAQIECBAgQICAAK4HCBAgQIAAAQIECBAgQIBAgoAAnoCsBAECBAgQIECAAAECBAgQEMD1AAECBAgQIECAAAECBAgQSBAQwBOQlSBAgAABAgQIECBAgAABAgK4HiBAgAABAgQIECBAgAABAgkCAngCshIECBAgQIAAAQIECBAgQEAA1wMECBAgQIAAAQIECBAgQCBBQABPQFaCAAECBAgQIECAAAECBAgI4HqAAAECBAgQIECAAAECBAgkCAjgCchKECBAgAABAgQIECBAgAABAVwPECBAgAABAgQIECBAgACBBAEBPAFZCQIECBAgQIAAAQIECBAgIIDrAQIECBAgQIAAAQIECBAgkCAggCcgK0GAAAECBAgQIECAAAECBARwPUCAAAECBAgQIECAAAECBBIEBPAEZCUIECBAgAABAgQIECBAgIAArgcIECBAgAABAgQIECBAgECCgACegKwEAQIECBAgQIAAAQIECBAQwPUAAQIECBAgQIAAAQIECBBIEBDAE5CVIECAAAECBAgQIECAAAECArgeIECAAAECBAgQIECAAAECCQICeAKyEgQIECBAgAABAgQIECBAQADXAwQIECBAgAABAgQIECBAIEFAAE9AVoIAAQIECBAgQIAAAQIECAjgeoAAAQIECBAgQIAAAQIECCQICOAJyEoQIECAAAECBAgQIECAAAEBXA8QIECAAAECBAgQIECAAIEEAQE8AVkJAgQIECBAgAABAgQIECAggOsBAgQIECBAgAABAgQIECCQICCAJyArQYAAAQIECBAgQIAAAQIEBHA9QIAAAQIECBAgQIAAAQIEEgQE8ARkJQgQIECAAAECBAgQIECAgACuBwgQIECAAAECBAgQIECAQIKAAJ6ArAQBAgQIECBAgAABAgQIEBDA9QABAgQIECBAgAABAgQIEEgQEMATkJUgQIAAAQIECBAgQIAAAQICuB4gQIAAAQIECBAgQIAAAQIJAgJ4ArISBAgQIECAAAECBAgQIEBAANcDBAgQIECAAAECBAgQIEAgQUAAT0BWggABAgQIECBAgAABAgQICOB6gAABAgQIECBAgAABAgQIJAgI4AnIShAgQIAAAQIECBAgQIAAAQFcDxAgQIAAAQIECBAgQIAAgQQBATwBWQkCBAgQIECAAAECBAgQICCA6wECBAgQIECAAAECBAgQIJAgIIAnICtBgAABAgQIECBAgAABAgQEcD1AgAABAgQIECBAgAABAgQSBATwBGQlCBAgQIAAAQIECBAgQICAAK4HCBAgQIAAAQIECBAgQIBAgoAAnoCsBAECBAgQIECAAAECBAgQEMD1AAECBAgQIECAAAECBAgQSBAQwBOQlSBAgAABAgQIECBAgAABAgK4HiBAgAABAgQIECBAgAABAgkCAngCshIECBAgQIAAAQIECBAgQEAA1wMECBAgQIAAAQIECBAgQCBBQABPQFaCAAECBAgQIECAAAECBAgI4HqAAAECBAgQIECAAAECBAgkCAjgCchKECBAgAABAgQIECBAgAABAVwPECBAgAABAgQIECBAgACBBAEBPAFZCQIECBAgQIAAAQIECBAgIIDrAQIECBAgQIAAAQIECBAgkCAggCcgK0GAAAECBAgQIECAAAECBARwPUCAAAECBAgQIECAAAECBBIEBPAEZCUIECBAgAABAgQIECBAgIAArgcIECBAgAABAgQIECBAgECCgACegKwEAQIECBAgQIAAAQIECBAQwPUAAQIECBAgQIAAAQIECBBIEBDAE5CVIECAAAECBAgQIECAAAECArgeIECAAAECBAgQIECAAAECCQICeAKyEgQIECBAgAABAgQIECBAQADXAwQIECBAgAABAgQIECBAIEFAAE9AVoIAAQIECBAgQIAAAQIECAjgeoAAAQIECBAgQIAAAQIECCQICOAJyEoQIECAAAECBAgQIECAAAEBXA8QIECAAAECBAgQIECAAIEEAQE8AVkJAgQIECBAgAABAgQIECAggOsBAgQIECBAgAABAgQIECCQICCAJyArQYAAAQIECBAgQIAAAQIEBHA9QIAAAQIECBAgQIAAAQIEEgQE8ARkJQgQIECAAAECBAgQIECAgACuBwgQIECAAAECBAgQIECAQIKAAJ6ArAQBAgQIECBAgAABAgQIEBDA9QABAgQIECBAgAABAgQIEEgQEMATkJUgQIAAAQIECBAgQIAAAQICuB4gQIAAAQIECBAgQIAAAQIJAgJ4ArISBAgQIECAAAECBAgQIEBAANcDBAgQIECAAAECBAgQIEAgQUAAT0BWggABAgQIECBAgAABAgQICOB6gAABAgQIECBAgAABAgQIJAgI4AnIShAgQIAAAQIECBAgQIAAAQFcDxAgQIAAAQIECBAgQIAAgQQBATwBWQkCBAgQIECAAAECBAgQICCA6wECBAgQIECAAAECBAgQIJAgIIAnICtBgAABAgQIECBAgAABAgQEcD1AgAABAgQIECBAgAABAgQSBATwBGQlCBAgQIAAAQIECBAgQICAAK4HCBAgQIAAAQIECBAgQIBAgoAAnoCsBAECBAgQIECAAAECBAgQEMD1AAECBAgQIECAAAECBAgQSBAQwBOQlSBAgAABAgQIECBAgAABAgK4HiBAgAABAgQIECBAgAABAgkCAngCshIECBAgQIAAAQIECBAgQEAA1wMECBAgQIAAAQIECBAgQCBBQABPQFaCAAECBAgQIECAAAECBAgI4HqAAAECBAgQIECAAAECBAgkCAjgCchKECBAgAABAgQIECBAgAABAVwPECBAgAABAgQIECBAgACBBAEBPAFZCQIECBAgQIAAAQIECBAgIIDrAQIECBAgQIAAAQIECBAgkCAggCcgK0GAAAECBAgQIECAAAECBARwPUCAAAECBAgQIECAAAECBBIEBPAEZCUIECBAgAABAgQIECBAgIAArgcIECBAgAABAgQIECBAgECCgACegKwEAQIECBAgQIAAAQIECBAQwPUAAQIECBAgQIAAAQIECBBIEBDAE5CVIECAAAECBAgQIECAAAECArgeIECAAAECBAgQIECAAAECCQICeAKyEgQIECBAgAABAgQIECBAQADXAwQIECBAgAABAgQIECBAIEFAAE9AVoIAAQIECBAgQIAAAQIECAjgeoAAAQIECBAgQIAAAQIECCQICOAJyEoQIECAAAECBAgQIECAAAEBXA8QIECAAAECBAgQIECAAIEEAQE8AVkJAgQIECBAgAABAgQIECAggOsBAgQIECBAgAABAgQIECCQICCAJyArQYAAAQIECBAgQIAAAQIEBHA9QIAAAQIECBAgQIAAAQIEEgQE8ARkJQgQIECAAAECBAgQIECAgACuBwgQIECAAAECBAgQIECAQIKAAJ6ArAQBAgQIECBAgAABAgQIEBDA9QABAgQIECBAgAABAgQIEEgQEMATkJUgQIAAAQIECBAgQIAAAQICuB4gQIAAAQIECBAgQIAAAQIJAgJ4ArISBAgQIECAAAECBAgQIEBAANcDBAgQIECAAAECBAgQIEAgQUAAT0BWggABAgQIECBAgAABAgQICOB6gAABAgQIECBAgAABAgQIJAgI4AnIShAgQIAAAQIECBAgQIAAAQFcDxAgQIAAAQIECBAgQIAAgQQBATwBWQkCBAgQIECAAAECBAgQICCA6wECBAgQIECAAAECBAgQIJAgIIAnICtBgAABAgQIECBAgAABAgQEcD1AgAABAgQIECBAgAABAgQSBATwBGQlCBAgQIAAAQIECBAgQICAAK4HCBAgQIAAAQIECBAgQIBAgoAAnoCsBAECBAgQIECAAAECBAgQEMD1AAECBAgQIECAAAECBAgQSBAQwBOQlSBAgAABAgQIECBAgAABAgK4HiBAgAABAgQIECBAgAABAgkCAngCshIECBAgQIAAAQIECBAgQEAA1wMECBAgQIAAAQIECBAgQCBBQABPQFaCAAECBAgQIECAAAECBAgI4HqAAAECBAgQIECAAAECBAgkCAjgCchKECBAgAABAgQIECBAgACBagBfcc0N6nEQIECAAAECBAgQIDBnCyy3zNJlgPc++CDq6ibM2Rj2nkCNBR6+77byiD0E8BrLGo4AAQIECBAgQIBAFxQQwLvgj2aTu4yAAN5lfiobSoAAAQIECBAgQKDzBQTwzjdWYc4VEMDn3N/enhMgQIAAAQIECBBoJiCANyMxgUDNBATwmlEaiAABAgQIECBAgEDXFxDAu/5vaA9mXwEBfPb9bWwZAQIE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">
```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnTextual :object="example_app" :width="500" :height="300" />
</template>
<script lang='py'>
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Button, Footer, Header, Static

QUESTION = "Do you want to learn about Textual CSS?"

class ExampleApp(App):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Container(
            Static(QUESTION, classes="question"),
            Horizontal(
                Button("yes", variant="success"),
                Button("no", variant="error"),
                classes="buttons",
            ),
            id="dialog",
        )

example_app = ExampleApp()
</script>

```


这对于简单的应用程序和更复杂的应用程序都适用。作为示例，这里我们嵌入了 Textual 文档中的计算器示例应用程序：

<img style='height:400px' src="data:image/png;base64,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UZt23313c95550UPxZ9r1qwx559/vmpxFne+yifIT+XAdtxxRzN+/HjTqVOnki9y/0i76aabSm6Tlie15QeBCitZCJTQL40T6X777WfOOOMMYY+Ll6+++mpz7733Fn9SQVXbAUxj312bBg4caG677TbjViErubnVx6OOOspMmzatks2D3Yb8VNa6zp07m4cffth06dKloheceeaZ5rnnnqto25A30pYf7QK1ePkq023djiG33Ou+I1ACTo0T6c9+9jNz6KGHZvbYTZDLli1rs/ddu3bNq333u981S5cuzatpeqDtAKax765f55xzjhk1alRe69yEeOutt2ZqxxxzjNl7773znn/yySfNueeem1dL2wPyU1lHx40bZ/baa6+8je+4445MfoYOHZpZmXIf70W32bNnm4MPPjh6mNqf2vKjVaCcOP30itfNpI++MD/ZbWNzxg+GmI4F/5azC9/mt3//yNzzzCwzcrs+5j8PGpLa3ES/GAIVkSj4qXEi3XXXXTPnKLhdveKKK8yf//zngr025vHHHzfrrLNOpj537lzzgx/8oM02mgraDmAa++769Yc//MEMGDAg27pXXnnFnHLKKdnH7o77uHb99dfP1ubMmWN++MMfZh+n8Q75qayrhfmZOXOmOeSQQ7IvdudVupXq3POifvGLX5gXX3wxu00a72jLj1aB+vtLc82Zt7yTjcD3d9nI/PePt8xKlJOn39w/1dzxROu5l/eM28EMG9At+5o03kGghK5qnUijCdJ9c6bw9p3vfCdz7ktU/+tf/5r5l2X0WONPbQcwrX2/77778r488Mgjj2ROBs7t6YQJE8xWW22VLbmM7L///tnHabxDfirr6mOPPWbcx3jRrdh5TnfffbfZaKONok0yQuVOAUjzTVt+tArU1DlLzAEXvJQXhUiiOtjvIlxy3xRz55Mz855/avzXTWP30ufb5b0gwAcIlNA0rROpsLuZsjvBPPfbWWPGjDHvvNP6r4ZSr63Vc9oOYFr77lYcv/KVr2Tb5D6+datLn3/+eabWu3fvzApU7grC66+/bsaOHZt9TRrvkJ/Kuuq+iZt78nixf1zdc889pl+/ftkB3TlQ7lyoNN+05UerQLkMPPXGfHPyjW/nxWH/r29ouqzT0fzpH7Py6jecuLX5xojW1fC8J1P0AIESmql1IhV2N/Ox3aOPPpo9ybip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">
```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnTextual :object="calculator" :height="500" :width="300" />
</template>
<script lang='py'>
from decimal import Decimal

from textual import events, on
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.css.query import NoMatches
from textual.reactive import var
from textual.widgets import Button, Digits

from pathlib import Path
import requests

def _download_file_if_not_exists(url: str, local_path: str) -> Path:
    local_file_path = Path(local_path)

    if not local_file_path.exists():
        response = requests.get(url)
        response.raise_for_status()
        local_file_path.write_bytes(response.content)

    return local_file_path


file_url = "https://raw.githubusercontent.com/holoviz/panel/main/examples/assets/calculator.tcss"
local_file_path = "calculator.tcss"
calculator_tcss = _download_file_if_not_exists(file_url, local_file_path)


class CalculatorApp(App):
    """一个可用的'桌面'计算器。"""

    CSS_PATH = calculator_tcss.absolute()

    numbers = var("0")
    show_ac = var(True)
    left = var(Decimal("0"))
    right = var(Decimal("0"))
    value = var("")
    operator = var("plus")

    NAME_MAP = {
        "asterisk": "multiply",
        "slash": "divide",
        "underscore": "plus-minus",
        "full_stop": "point",
        "plus_minus_sign": "plus-minus",
        "percent_sign": "percent",
        "equals_sign": "equals",
        "minus": "minus",
        "plus": "plus",
    }

    def watch_numbers(self, value: str) -> None:
        """当 numbers 更新时调用。"""
        self.query_one("#numbers", Digits).update(value)

    def compute_show_ac(self) -> bool:
        """计算是显示 AC 还是 C 按钮"""
        return self.value in ("", "0") and self.numbers == "0"

    def watch_show_ac(self, show_ac: bool) -> None:
        """当 show_ac 更改时调用。"""
        self.query_one("#c").display = not show_ac
        self.query_one("#ac").display = show_ac

    def compose(self) -> ComposeResult:
        """添加我们的按钮。"""
        with Container(id="calculator"):
            yield Digits(id="numbers")
            yield Button("AC", id="ac", variant="primary")
            yield Button("C", id="c", variant="primary")
            yield Button("+/-", id="plus-minus", variant="primary")
            yield Button("%", id="percent", variant="primary")
            yield Button("÷", id="divide", variant="warning")
            yield Button("7", id="number-7", classes="number")
            yield Button("8", id="number-8", classes="number")
            yield Button("9", id="number-9", classes="number")
            yield Button("×", id="multiply", variant="warning")
            yield Button("4", id="number-4", classes="number")
            yield Button("5", id="number-5", classes="number")
            yield Button("6", id="number-6", classes="number")
            yield Button("-", id="minus", variant="warning")
            yield Button("1", id="number-1", classes="number")
            yield Button("2", id="number-2", classes="number")
            yield Button("3", id="number-3", classes="number")
            yield Button("+", id="plus", variant="warning")
            yield Button("0", id="number-0", classes="number")
            yield Button(".", id="point")
            yield Button("=", id="equals", variant="warning")

    def on_key(self, event: events.Key) -> None:
        """当用户按下键时调用。"""

        def press(button_id: str) -> None:
            """按下一个按钮，如果它存在的话。"""
            try:
                self.query_one(f"#{button_id}", Button).press()
            except NoMatches:
                pass

        key = event.key
        if key.isdecimal():
            press(f"number-{key}")
        elif key == "c":
            press("c")
            press("ac")
        else:
            button_id = self.NAME_MAP.get(key)
            if button_id is not None:
                press(self.NAME_MAP.get(key, key))

    @on(Button.Pressed, ".number")
    def number_pressed(self, event: Button.Pressed) -> None:
        """按下了数字。"""
        assert event.button.id is not None
        number = event.button.id.partition("-")[-1]
        self.numbers = self.value = self.value.lstrip("0") + number

    @on(Button.Pressed, "#plus-minus")
    def plus_minus_pressed(self) -> None:
        """按下 + / -"""
        self.numbers = self.value = str(Decimal(self.value or "0") * -1)

    @on(Button.Pressed, "#percent")
    def percent_pressed(self) -> None:
        """按下 %"""
        self.numbers = self.value = str(Decimal(self.value or "0") / Decimal(100))

    @on(Button.Pressed, "#point")
    def pressed_point(self) -> None:
        """按下 ."""
        if "." not in self.value:
            self.numbers = self.value = (self.value or "0") + "."

    @on(Button.Pressed, "#ac")
    def pressed_ac(self) -> None:
        """按下 AC"""
        self.value = ""
        self.left = self.right = Decimal(0)
        self.operator = "plus"
        self.numbers = "0"

    @on(Button.Pressed, "#c")
    def pressed_c(self) -> None:
        """按下 C"""
        self.value = ""
        self.numbers = "0"

    def _do_math(self) -> None:
        """执行数学运算：LEFT OPERATOR RIGHT"""
        try:
            if self.operator == "plus":
                self.left += self.right
            elif self.operator == "minus":
                self.left -= self.right
            elif self.operator == "divide":
                self.left /= self.right
            elif self.operator == "multiply":
                self.left *= self.right
            self.numbers = str(self.left)
            self.value = ""
        except Exception:
            self.numbers = "Error"

    @on(Button.Pressed, "#plus,#minus,#divide,#multiply")
    def pressed_op(self, event: Button.Pressed) -> None:
        """按下了算术运算之一。"""
        self.right = Decimal(self.value or "0")
        self._do_math()
        assert event.button.id is not None
        self.operator = event.button.id

    @on(Button.Pressed, "#equals")
    def pressed_equals(self) -> None:
        """按下 ="""
        if self.value:
            self.right = Decimal(self.value)
        self._do_math()


calculator = CalculatorApp()
</script>

```


## API

### 属性

| 属性名            | 说明                          | 类型                                                           | 默认值 |
| ---------------- | ----------------------------- | ---------------------------------------------------------------| ------- |
| object           | 要渲染的 Textual 应用程序      | ^[textual.app.App]                                             | None |
| sizing_mode      | 尺寸调整模式                  | ^[str]                                                         | 'fixed'  |
| width            | 宽度                          | ^[int, str]                                                    | None    |
| height           | 高度                          | ^[int, str]                                                    | None    |
| min_width        | 最小宽度                      | ^[int]                                                         | None    |
| min_height       | 最小高度                      | ^[int]                                                         | None    |
| max_width        | 最大宽度                      | ^[int]                                                         | None    |
| max_height       | 最大高度                      | ^[int]                                                         | None    |
| margin           | 外边距                        | ^[int, tuple]                                                  | 5       |
| css_classes      | CSS类名列表                   | ^[list]                                                        | []      |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | 自定义默认内容      |




# GIF 图片

`PnGif` 组件在提供本地路径时将 `.gif` 图像文件嵌入到面板中，或者在提供 URL 时将链接到远程图像。

底层实现为`panel.pane.GIF`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/GIF.html


## 基本用法

`PnGIF` 组件可以指向任何本地或远程的 `.gif` 文件。如果给定以 `http` 或 `https` 开头的 URL，`embed` 参数决定图像是嵌入还是链接，可以通过设置特定的固定 `width` 或 `height` 来调整图像的大小：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnGif :object="url" :width="100" />
</template>
<script lang='py'>
url = 'https://upload.wikimedia.org/wikipedia/commons/d/de/Ajax-loader.gif'
</script>

```


或者，我们可以使用 `sizing_mode` 来调整宽度和高度：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnGif :object="url" sizing_mode="stretch_width" />
</template>
<script lang='py'>
url = 'https://upload.wikimedia.org/wikipedia/commons/b/b1/Loading_icon.gif'
</script>

```


请注意，默认情况下，图像的宽高比是固定的，因此即使在响应式调整大小模式下，图像旁边或下方也可能有空隙。要覆盖此行为，请设置 `fixed_aspect=False` 或提供固定的 `width` 和 `height` 值。

## API

### 属性

| 属性名       | 说明                 | 类型                                                           | 默认值 |
| ----------- | ------------------- | ---------------------------------------------------------------| ------- |
| object      | 要显示的字符串或对象  | ^[str, object]                                                 | None |
| alt_text    | 添加到图像标签的替代文本。当用户无法加载或显示图像时显示替代文本 | ^[str]              | None |
| embed       | 如果给定图像 URL，这决定图像是否将被嵌入为 base64 或仅链接到 | ^[boolean]            | False |
| fixed_aspect | 是否强制图像的宽高比相等 | ^[boolean]                                                 | True |
| link_url    | 使图像可点击并链接到其他网站的链接 URL | ^[str]                                       | None |
| styles      | 指定 CSS 样式的字典   | ^[dict]                                                        | {} |
| sizing_mode | 尺寸调整模式         | ^[str]                                                         | 'fixed'  |
| width       | 宽度                 | ^[int, str]                                                    | None    |
| height      | 高度                 | ^[int, str]                                                    | None    |
| min_width   | 最小宽度             | ^[int]                                                         | None    |
| min_height  | 最小高度             | ^[int]                                                         | None    |
| max_width   | 最大宽度             | ^[int]                                                         | None    |
| max_height  | 最大高度             | ^[int]                                                         | None    |
| margin      | 外边距               | ^[int, tuple]                                                  | 5       |
| css_classes | CSS类名列表          | ^[list]                                                        | []      |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | 自定义默认内容      |




# JPG 图像

`PnJpg` 组件如果提供本地路径，则将 `.jpg` 或 `.jpeg` 图像文件嵌入到面板中，或者如果提供 URL，则会链接到远程图像。

底层实现为`panel.pane.JPG`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/JPG.html


## 基本用法

`PnJPG` 组件可以指向任何本地或远程 `.jpg` 文件。如果给定以 `http` 或 `https` 开头的 URL，则 `embed` 参数决定图像是嵌入还是链接到：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnJpg 
    object="https://assets.holoviz.org/panel/samples/jpeg_sample.jpg"
    link_url="https://blog.holoviz.org/panel_0.13.0.html"
    :width="800" />
</template>

```


## 调整大小

我们可以通过设置特定的固定 `width` 或 `height` 来调整图像的大小：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnJpg 
    object="https://assets.holoviz.org/panel/samples/jpeg_sample.jpg"
    :width="400" />
</template>

```


或者，我们可以使用 `sizing_mode` 来调整宽度和高度：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnJpg 
    object="https://assets.holoviz.org/panel/samples/jpeg_sample2.jpg"
    link_url="https://blog.holoviz.org/panel_0.14.html"
    sizing_mode="scale_both" />
</template>

```


请注意，默认情况下，图像的宽高比是固定的，因此即使在响应式调整大小模式下，图像旁边或下方也可能有空隙。要覆盖此行为，请设置 `fixed_aspect=false` 或提供固定的 `width` 和 `height` 值。

## API

### 属性

| 属性名          | 说明                          | 类型                                                           | 默认值 |
| -------------- | ----------------------------- | ---------------------------------------------------------------| ------- |
| object         | 要显示的 JPEG 文件。可以是指向本地或远程文件的字符串，或具有 `_repr_jpeg_` 方法的对象 | ^[str, object] | None |
| alt_text       | 添加到图像标签的替代文本。当用户无法加载或显示图像时显示替代文本 | ^[str]                   | None |
| embed          | 如果给定图像 URL，这决定图像是否将被嵌入为 base64 或仅链接到 | ^[boolean]                  | False |
| fixed_aspect   | 是否强制图像的宽高比相等       | ^[boolean]                                                     | True |
| link_url       | 使图像可点击并链接到其他网站的链接 URL | ^[str]                                                  | None |
| styles         | 指定 CSS 样式的字典           | ^[dict]                                                        | {} |
| sizing_mode    | 尺寸调整模式                   | ^[str]                                                         | 'fixed'  |
| width          | 宽度                          | ^[int, str]                                                    | None    |
| height         | 高度                          | ^[int, str]                                                    | None    |
| min_width      | 最小宽度                      | ^[int]                                                         | None    |
| min_height     | 最小高度                      | ^[int]                                                         | None    |
| max_width      | 最大宽度                      | ^[int]                                                         | None    |
| max_height     | 最大高度                      | ^[int]                                                         | None    |
| margin         | 外边距                        | ^[int, tuple]                                                  | 5       |
| css_classes    | CSS类名列表                   | ^[list]                                                        | []      |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | 自定义默认内容      |




# WebP WebP图像组件

`WebP`组件可以在面板中嵌入`.webp`图像文件。如果提供本地路径，则嵌入该文件；如果提供URL，则链接到远程图像。

底层实现为`panel.pane.WebP`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/WebP.html


## 基本用法

`PnWebP`组件可以指向任何本地或远程的`.webp`文件。如果给定的URL以`http`或`https`开头，`embed`参数决定图像是嵌入还是链接：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnWebP object="https://assets.holoviz.org/panel/samples/webp_sample.webp" />
</template>

```


我们可以通过设置特定的固定`width`或`height`来调整图像的大小：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnWebP object="https://assets.holoviz.org/panel/samples/webp_sample.webp" :width="400" />
</template>

```


或者，我们可以使用`sizing_mode`来调整宽度和高度：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnWebP object="https://assets.holoviz.org/panel/samples/webp_sample2.webp" 
          sizing_mode="scale_width" />
</template>

```


请注意，默认情况下，图像的宽高比是固定的，因此即使在响应式尺寸模式下，图像的旁边或下方也可能存在间隙。要覆盖此行为，请设置`fixed_aspect=False`或提供固定的`width`和`height`值。

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnRow>
    <PnWebP object="https://assets.holoviz.org/panel/samples/webp_sample2.webp" 
             :fixed_aspect="False"
             :width="300"
             :height="150" />
    <PnWebP object="https://assets.holoviz.org/panel/samples/webp_sample2.webp" 
             :fixed_aspect="True"
             :width="300"
             :height="150" />
  </PnRow>
</template>

```


## API

### 属性

| 属性名        | 说明                                    | 类型       | 默认值 |
| ------------- | --------------------------------------- | ---------- | ------ |
| value         | 要显示的WebP文件。可以是指向本地或远程文件的字符串 | ^[str\|object] | —      |
| alt_text      | 添加到图像标签的替代文本。当用户无法加载或显示图像时显示 | ^[str] | None   |
| embed         | 如果给定图像URL，这将决定图像是作为base64嵌入还是仅链接 | ^[bool] | False  |
| fixed_aspect  | 是否强制图像的宽高比相等                | ^[bool]    | True   |
| link_url      | 链接URL，使图像可点击并链接到其他网站    | ^[str]     | None   |
| styles        | 指定CSS样式的字典                       | ^[dict]    | {}     |




# Perspective 数据可视化

`PnPerspective` 组件提供了一个强大的可视化工具，用于处理大型实时数据集，基于 [Perspective 项目](https://perspective.finos.org/)。**`PnPerspective` 为您的数据应用程序带来了*类似Excel*的功能**。查看 [Perspective 示例库](https://perspective.finos.org/examples/) 获取灵感。

`PnPerspective` 组件是 [`Tabulator`](../widgets/Tabulator.ipynb) 小部件的一个很好的替代品。

底层实现为`panel.pane.Perspective`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/Perspective.html


## 基本用法

`PnPerspective` 组件将指定为字典列表或数组以及 pandas DataFrame 的数据列呈现为交互式表格：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnPerspective :object="df" :width="600" :height='300'/>
</template>
<script lang='py'>
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# 创建示例数据
data = {
    'int': [random.randint(-10, 10) for _ in range(9)],
    'float': [random.uniform(-10, 10) for _ in range(9)],
    'date': [(datetime.now() + timedelta(days=i)).date() for i in range(9)],
    'datetime': [(datetime.now() + timedelta(hours=i)) for i in range(9)],
    'category': ['类别 A', '类别 B', '类别 C', '类别 A', '类别 B',
             '类别 C', '类别 A', '类别 B', '类别 C',],
    'link': ['https://panel.holoviz.org/', 'https://discourse.holoviz.org/', 'https://github.com/holoviz/panel']*3,
}
df = pd.DataFrame(data)
</script>

```


试着与 `PnPerspective` 组件交互：

- 左上角的三个垂直点会切换*配置菜单*
- 每列顶部的三条垂直线会切换*列配置菜单*
- 顶部菜单提供选项来更改*插件*以及*分组*、*拆分*、*排序*和*过滤*数据
- 底部菜单提供选项来*重置*、*下载*和*复制*以及*更改主题*

默认情况下会显示 `index`。如果您默认不想显示它，可以提供要显示的 `columns` 列表：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnPerspective :object="df" :columns="list(df.columns)" 
                 :width="600" :height='300'/>
</template>
<script lang='py'>
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# 创建示例数据
data = {
    'int': [random.randint(-10, 10) for _ in range(9)],
    'float': [random.uniform(-10, 10) for _ in range(9)],
    'date': [(datetime.now() + timedelta(days=i)).date() for i in range(9)],
    'datetime': [(datetime.now() + timedelta(hours=i)) for i in range(9)],
    'category': ['类别 A', '类别 B', '类别 C', '类别 A', '类别 B',
             '类别 C', '类别 A', '类别 B', '类别 C',],
    'link': [
        'https://panel.holoviz.org/', 
        'https://discourse.holoviz.org/', 
        'https://github.com/holoviz/panel',
    ] * 3,
}
df = pd.DataFrame(data)
</script>

```


您也可以通过 `settings` 参数隐藏*配置菜单*：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnPerspective 
    :object="df" 
    :columns="['float']" 
    :group_by="['category']" 
    plugin="d3_y_bar" 
    :settings="False"
    :width="400" 
    :height="300" />
</template>
<script lang='py'>
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# 创建示例数据
data = {
    'int': [random.randint(-10, 10) for _ in range(9)],
    'float': [random.uniform(-10, 10) for _ in range(9)],
    'date': [(datetime.now() + timedelta(days=i)).date() for i in range(9)],
    'datetime': [(datetime.now() + timedelta(hours=i)) for i in range(9)],
    'category': ['类别 A', '类别 B', '类别 C', '类别 A', '类别 B',
             '类别 C', '类别 A', '类别 B', '类别 C',],
    'link': ['https://panel.holoviz.org/', 'https://discourse.holoviz.org/', 'https://github.com/holoviz/panel']*3,
}
df = pd.DataFrame(data)
</script>

```


通过点击左上角的 3 个垂直点，尝试切换*配置菜单*与 `PnPerspective` 组件交互。

## 插件配置

您可以手动配置活动*插件*，如下所示为*数据网格*

![perspective_edit](https://panel.holoviz.org/assets/perspective_edit.png)

您还可以通过 `columns_config` 参数以编程方式配置*列*配置：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnPerspective 
    :object="df" 
    :columns="list(df.columns)" 
    :width="600"
    :height='300'
    :columns_config="columns_config" />
</template>
<script lang='py'>
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# 创建示例数据
data = {
    'int': [random.randint(-10, 10) for _ in range(9)],
    'float': [random.uniform(-10, 10) for _ in range(9)],
    'date': [(datetime.now() + timedelta(days=i)).date() for i in range(9)],
    'datetime': [(datetime.now() + timedelta(hours=i)) for i in range(9)],
    'category': ['类别 A', '类别 B', '类别 C', '类别 A', '类别 B',
             '类别 C', '类别 A', '类别 B', '类别 C',],
    'link': [
        'https://panel.holoviz.org/', 
        'https://discourse.holoviz.org/', 
        'https://github.com/holoviz/panel'] * 3,
}
df = pd.DataFrame(data)

# 列配置
columns_config = {
    'int': {'number_fg_mode': 'color', 'neg_fg_color': '#880808', 'pos_fg_color': '#008000', "fixed": 0},
    'float': {'number_fg_mode': "bar", 'neg_fg_color': '#880808', 'pos_fg_color': '#008000', 'fg_gradient': 7.93,  },
    'category': {'string_color_mode': 'series', 'format': 'italics'},
    'date': {"dateStyle": "short", "datetime_color_mode": "foreground", "color": "#008000"},
    'datetime': {"timeZone": "Asia/Shanghai", "dateStyle": "full", "timeStyle": "full", "datetime_color_mode": "background", "color": "#880808"},
    'link': {'format': 'link', 'string_color_mode': 'foreground', 'color': '#008000'},
}
</script>

```


请注意：

- 提供 `plugin_config` 时，您也可以使用*命名*颜色，如 'green'。但如果这样做，它们将不会在*列配置菜单*的*颜色选择器*中设置。

有关可用选项的更多详细信息，请参阅下面的[列配置选项部分](#列配置选项)。

## 时区处理

底层的 Perspective Viewer 假设*非时区*感知的日期时间是 UTC 时间。默认情况下，它会在您的本地时区中显示它们。

如果您的数据不是时区感知的，您可以将它们设置为时区感知。我的服务器时区是 'cet'，我可以按如下方式使它们感知时区：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnColumn>
    <PnTabulator :value="df_aware.head(3)" />
    <PnPerspective :object="df_aware" :columns="list(df.columns)" 
                   :width="600" :height='300' />
  </PnColumn>
</template>
<script lang='py'>
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# 创建示例数据
data = {
    'int': [random.randint(-10, 10) for _ in range(9)],
    'float': [random.uniform(-10, 10) for _ in range(9)],
    'date': [(datetime.now() + timedelta(days=i)).date() for i in range(9)],
    'datetime': [(datetime.now() + timedelta(hours=i)) for i in range(9)],
    'category': ['类别 A', '类别 B', '类别 C', '类别 A', '类别 B',
             '类别 C', '类别 A', '类别 B', '类别 C',],
    'link': ['https://panel.holoviz.org/', 'https://discourse.holoviz.org/', 'https://github.com/holoviz/panel']*3,
}
df = pd.DataFrame(data)

# 创建时区感知副本
df_aware = df.copy(deep=True)
df_aware['datetime'] = df_aware['datetime'].dt.tz_localize("cet")
</script>

```


如上节所示，您可以强制日期时间以特定时区显示：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnPerspective 
    :object="df_aware" 
    :width="600"
    :height='300'
    :columns="list(df.columns)" 
    :plugin_config="plugin_config" />
</template>
<script lang='py'>
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# 创建示例数据
data = {
    'int': [random.randint(-10, 10) for _ in range(9)],
    'float': [random.uniform(-10, 10) for _ in range(9)],
    'date': [(datetime.now() + timedelta(days=i)).date() for i in range(9)],
    'datetime': [(datetime.now() + timedelta(hours=i)) for i in range(9)],
    'category': ['类别 A', '类别 B', '类别 C', '类别 A', '类别 B',
             '类别 C', '类别 A', '类别 B', '类别 C',],
    'link': ['https://panel.holoviz.org/', 'https://discourse.holoviz.org/', 'https://github.com/holoviz/panel']*3,
}
df = pd.DataFrame(data)

# 创建时区感知副本
df_aware = df.copy(deep=True)
df_aware['datetime'] = df_aware['datetime'].dt.tz_localize("cet")

# 插件配置
plugin_config = {'columns': {'datetime': {"timeZone": "Europe/London", "timeStyle": "full"}}}
</script>

```


## 流式处理和补丁更新

`PnPerspective` 组件还支持 `stream` 和 `patch` 方法，使我们能够高效地更新数据：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnPerspective 
    ref="stream_perspective"
    :object="df_stream" 
    plugin="d3_y_line" 
    :columns="['A', 'B', 'C', 'D']" 
    sizing_mode="stretch_width" 
    :height="500" 
    :margin="0" />
  <PnCol>
    <PnNumberInput v-model="period.value" name="更新频率(毫秒)" />
    <PnIntInput v-model="rollover.value" name="保留的数据点数量" />
    <PnButton @click='start_stream()'>开始流式处理</PnButton>
    <PnButton @click='stop_stream()'>停止流式处理</PnButton>
  </PnCol>
</template>
<script lang='py'>
import pandas as pd
import numpy as np
from vuepy import ref
import panel as pn

# 创建示例数据
df_stream = pd.DataFrame(np.random.randn(400, 4), columns=list('ABCD')).cumsum()

# 流式处理控制
period = ref(50)
rollover = ref(500)
streaming = ref(False)
callback = None
stream_perspective = ref(None)

def stream():
    print('xxx')
    data = df_stream.iloc[-1] + np.random.randn(4)
    perspective = strestream_perspective.value.unwrap()
    perspective.stream(data, rollover.value)

def start_stream():
    nonlocal callback
    streaming.value = True
    print('xxxxx')
    callback = pn.state.add_periodic_callback(stream, period.value)

def stop_stream():
    nonlocal callback
    streaming.value = False
    if callback and callback.running:
        callback.stop()
</script>

```


或者，我们也可以使用 `patch` 方法更新数据：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnPerspective 
    ref="perspective_ref"
    :object="mixed_df" 
    :columns="list(mixed_df)" 
    :height="500" />
  <PnButton @click="patch_data()">修补数据</PnButton>
</template>
<script lang='py'>
import pandas as pd
import numpy as np
from vuepy import ref

perspective_ref = ref(None)

# 创建混合类型数据
mixed_df = pd.DataFrame({'A': np.arange(10), 'B': np.random.rand(10), 'C': [f'foo{i}' for i in range(10)]})

def patch_data():
    perspective = perspective_ref.value.unwrap()
    # 修补 'A' 列的第 0 行和 'C' 列的前两行
    perspective.patch({'A': [(0, 3)], 'C': [(slice(0, 1), 'bar')]})
</script>

```


通过流式处理您想要可见的数据并将 rollover 设置为等于新数据的行数，可以实现删除行。通过这种方式，有效地删除旧行。目前不支持以类似于修补的方式按索引删除特定行。

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnPerspective 
    ref="perspective_ref"
    :object="data" 
    :height="500" />
  <PnButton @click="stream_smaller()">流式处理更小的数据集</PnButton>
</template>
<script lang='py'>
import pandas as pd
import numpy as np
from vuepy import ref

perspective_ref = ref(None)

# 创建简单数据
data = {'A': np.arange(2)}

def stream_smaller():
    perspective = perspective_ref.value.unwrap()
    smaller_data = {'A': np.arange(5)}
    perspective.stream(smaller_data, rollover=5)
</script>

```


## 列配置选项

底层 FinOS Perspective viewer 的*插件和列配置选项*没有很好的文档记录。找到它们的最佳方法是：

- 通过上面的*Controls*小部件交互式探索
- 探索 [Perspective 示例库](https://perspective.finos.org/examples/)
- 从 [Perspective GitHub 仓库](https://github.com/finos/perspective)进行逆向工程
  - 例如，对于 `Datagrid` 插件，配置*数字*列的选项定义在 [number_column_style.rs](https://github.com/finos/perspective/blob/master/rust/perspective-viewer/src/rust/config/number_column_style.rs)中

以下列出了我们能够找到并且看到有效的一些最有用的选项。

> **注意**：下面的一些选项是*驼峰式*的，如 `timeZone`。我们预计这是一个错误，FinOS Perspective 某天会修复。如果一个*驼峰式*选项停止工作，请尝试将其*蛇形式*化。例如，改为 `time_zone`。请在 [Github](https://github.com/holoviz/panel/issues) 上报告更改。

## API

### 属性

| 属性名            | 说明                          | 类型                                                           | 默认值 |
| ---------------- | ----------------------------- | ---------------------------------------------------------------| ------- |
| object           | 作为字典数组或DataFrame声明的绘图数据 | ^[dict, pd.DataFrame]                                       | None |
| aggregates       | 聚合规范，例如 {x: "distinct count"} | ^[dict]                                                    | None |
| columns          | 要显示的列名列表或带有列配置选项的字典 | ^[list, dict]                                               | None |
| columns_config   | 列配置，允许为每列指定格式化器、着色和各种其他属性 | ^[dict]                                           | None |
| editable         | 项目是否可编辑                | ^[bool]                                                         | True |
| expressions      | 表达式列表，例如 `['"x"+"y"']` | ^[list]                                                        | None |
| filters          | 过滤器列表，例如 `[["x", "<", 3], ["y", "contains", "abc"]]` | ^[list]                           | None |
| group_by         | 要分组的列列表，例如 `["x", "y"]` | ^[list]                                                      | None |
| plugin           | 用于显示数据的插件名称。例如 'datagrid' 或 'd3_xy_scatter' | ^[str]                              | None |
| plugin_config    | PerspectiveViewerPlugin 的配置 | ^[dict]                                                        | None |
| selectable       | 行是否可选择                  | ^[bool]                                                         | True |
| settings         | 是否显示设置面板              | ^[bool]                                                         | True |
| sort             | 排序规范列表，例如 `[["x", "desc"]]` | ^[list]                                                   | None |
| split_by         | 要透视的列列表。例如 `["x", "y"]` | ^[list]                                                     | None |
| theme            | 查看器的主题，可用选项包括 'pro'、'pro-dark'、'monokai'、'solarized'、'solarized-dark' 和 'vaporwave' | ^[str] | None |
| title            | Perspective Viewer 的标题     | ^[str]                                                          | None |
| sizing_mode      | 尺寸调整模式                  | ^[str]                                                         | 'fixed'  |
| width            | 宽度                          | ^[int, str]                                                    | None    |
| height           | 高度                          | ^[int, str]                                                    | None    |
| min_width        | 最小宽度                      | ^[int]                                                         | None    |
| min_height       | 最小高度                      | ^[int]                                                         | None    |
| max_width        | 最大宽度                      | ^[int]                                                         | None    |
| max_height       | 最大高度                      | ^[int]                                                         | None    |
| margin           | 外边距                        | ^[int, tuple]                                                  | 5       |
| css_classes      | CSS类名列表                   | ^[list]                                                        | []      |

### 回调

* **`on_click`**: 允许注册回调，这些回调接收包含被点击项的 `config`、`column_names` 和 `row` 的 `PerspectiveClickEvent` 对象。

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | 自定义默认内容      |

### 方法

| 属性名 | 说明 | 类型 |
| --- | --- | --- |
| patch | 更新特定行和列的数据 | dict, rollover=None |
| stream | 将新数据附加到现有数据上 | obj, rollover=None |




# Image 图像

`PnImage` 组件如果提供本地路径，则将任何已知图像格式文件嵌入到面板中，或者如果提供 URL，则会链接到远程图像。

`PnImage` 组件作为一种宏组件，它会选择一种更具体的图像组件来显示图像（首先识别特定图像格式的组件）。

底层实现为`panel.pane.Image`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/Image.html


## 基本用法

`PnImage` 组件可以指向任何本地或远程图像文件。如果给定以 `http` 或 `https` 开头的 URL，则 `embed` 参数决定图像是嵌入还是链接到：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnRow>
    <PnCol>
      <PnImage object="https://assets.holoviz.org/panel/samples/jpeg_sample.jpeg" />
    </PnCol>
    <PnCol>
      <PnImage object="https://assets.holoviz.org/panel/samples/png_sample.png" />
    </PnCol>
    <PnCol>
      <PnImage object="https://assets.holoviz.org/panel/samples/webp_sample.webp" />
    </PnCol>
  </PnRow>
</template>

```


## 调整大小

我们可以通过设置特定的固定 `width` 或 `height` 来调整图像的大小：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnImage object="https://assets.holoviz.org/panel/samples/png_sample.png" :width="400" />
</template>

```


或者，我们可以使用 `sizing_mode` 来调整宽度和高度：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnImage object="https://assets.holoviz.org/panel/samples/png_sample2.png" 
           sizing_mode="scale_width" />
</template>

```


您可以通过使用 `caption` 为图像添加标题：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnImage 
    object="https://assets.holoviz.org/panel/samples/png_sample2.png" 
    sizing_mode="scale_width" 
    caption="世界地图" />
</template>

```


请注意，默认情况下，图像的宽高比是固定的，因此即使在响应式调整大小模式下，图像旁边或下方也可能有空隙。要覆盖此行为，请设置 `fixed_aspect=false` 或提供固定的 `width` 和 `height` 值。

## PIL 图像支持

Image 组件将渲染任何定义了 `_repr_[png | jpeg | svg]_` 方法的组件，包括 PIL 图像：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnImage :object="pil_image" />
</template>
<script lang='py'>
from PIL import Image, ImageDraw

im = Image.new(mode='RGB', size=(256, 256))

draw = ImageDraw.Draw(im)
draw.line((0, 0) + im.size, fill=128, width=5)
draw.line((0, im.size[1], im.size[0], 0), fill=128, width=5)
draw.rectangle([(96, 96), (160, 160)], fill=(0, 0, 128), width=10)

pil_image = im
</script>

```


## API

### 属性

| 属性名          | 说明                          | 类型                                                           | 默认值 |
| -------------- | ----------------------------- | ---------------------------------------------------------------| ------- |
| object         | 要显示的图像文件。可以是指向本地或远程文件的字符串，或具有 `_repr_extension_` 方法的对象，其中扩展名是图像文件扩展名 | ^[str, object] | None |
| alt_text       | 添加到图像标签的替代文本。当用户无法加载或显示图像时显示替代文本 | ^[str]                   | None |
| embed          | 如果给定图像 URL，这决定图像是否将被嵌入为 base64 或仅链接到 | ^[boolean]                  | False |
| fixed_aspect   | 是否强制图像的宽高比相等       | ^[boolean]                                                     | True |
| link_url       | 使图像可点击并链接到其他网站的链接 URL | ^[str]                                                  | None |
| styles         | 指定 CSS 样式的字典           | ^[dict]                                                        | {} |
| sizing_mode    | 尺寸调整模式                   | ^[str]                                                         | 'fixed'  |
| width          | 宽度                          | ^[int, str]                                                    | None    |
| height         | 高度                          | ^[int, str]                                                    | None    |
| min_width      | 最小宽度                      | ^[int]                                                         | None    |
| min_height     | 最小高度                      | ^[int]                                                         | None    |
| max_width      | 最大宽度                      | ^[int]                                                         | None    |
| max_height     | 最大高度                      | ^[int]                                                         | None    |
| margin         | 外边距                        | ^[int, tuple]                                                  | 5       |
| css_classes    | CSS类名列表                   | ^[list]                                                        | []      |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | 自定义默认内容      |




# DeckGL 可视化

[Deck.gl](https://deck.gl/#/) 是一个功能强大的基于 WebGL 的框架，用于大型数据集的可视化探索性数据分析。`PnDeckGL` 组件可以渲染 Deck.gl JSON 规范以及 `PyDeck` 图表。如果数据被编码在 deck.gl 图层中，该组件将提取数据并通过二进制格式的 websocket 发送，加速渲染。

[`PyDeck`](https://deckgl.readthedocs.io/en/latest/) 软件包提供 Python 绑定。请严格按照[安装说明](https://github.com/uber/deck.gl/blob/master/bindings/pydeck/README.md)进行操作，以便在 Jupyter Notebook 中使用它。

底层实现为`panel.pane.DeckGL`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/DeckGL.html


## 基本用法

要使用 Deck.gl，您需要一个 MAP BOX 密钥，可以在 [mapbox.com](https://account.mapbox.com/access-tokens/) 上免费获取（有限使用）。

现在我们可以定义一个 JSON 规范并将其与 Mapbox 密钥（如果有）一起传递给 DeckGL 组件：


如果您没有 Mapbox API 密钥，可以使用 [Carto basemaps](https://deck.gl/docs/api-reference/carto/basemap#supported-basemaps) 之一。

与其他组件一样，DeckGL 对象可以被替换或更新。在此示例中，我们将更改 HexagonLayer 的 `colorRange` 然后触发更新：


## 工具提示

默认情况下，可以通过设置 `tooltips=True/False` 禁用和启用工具提示。为了更多的自定义，可以传入定义格式的字典。让我们首先声明具有两个图层的图：


## PyDeck

除了编写原始的类 JSON 字典外，`PnDeckGL` 组件还可以接收 PyDeck 对象进行渲染：


注意，使用 pydeck 指定工具提示时，还必须使用 `{properties.<DATA_FIELD_NAME>}` 语法引用任何数据字段。

## API

### 属性

| 属性名           | 说明                          | 类型                                                           | 默认值 |
| --------------- | ----------------------------- | --------------------------------------------------------------| ------- |
| object          | 要显示的 deck.GL JSON 或 PyDeck 对象 | ^[object, dict, string]                                 | None |
| mapbox_api_key  | 如果 PyDeck 对象未提供，则为 MapBox API 密钥 | ^[string]                                     | None |
| tooltips        | 是否启用工具提示或自定义工具提示格式化程序 | ^[bool, dict]                                    | True |
| throttle        | 视图状态和悬停事件的节流超时（以毫秒为单位） | ^[dict]                                         | {'view': 200, 'hover': 200} |
| click_state     | 包含 DeckGL 图上最后一次点击事件的信息 | ^[dict]                                               | {} |
| hover_state     | 包含有关 DeckGL 图上当前悬停位置的信息 | ^[dict]                                              | {} |
| view_state      | 包含有关 DeckGL 图当前视口的信息 | ^[dict]                                                     | {} |
| sizing_mode     | 尺寸调整模式                   | ^[str]                                                        | 'fixed'  |
| width           | 宽度                         | ^[int, str]                                                    | None    |
| height          | 高度                         | ^[int, str]                                                    | None    |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | 自定义默认内容      |



# Param 参数组件

`PnParam` 组件允许自定义 `param.Parameterized` 类参数的小部件、布局和样式。通过该组件，可以轻松地为参数化模型创建交互式界面。

底层实现为`panel.pane.Param`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/Param.html


## 基本用法

`PnParam` 组件可以用来查看和编辑参数化模型。下面我们构建一个骑行运动员及其功率曲线的模型作为示例：


## 自定义小部件

我们可以为特定参数自定义小部件类型：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnParam :object="athlete.param" :widgets="widgets"/>
  <hr/>
  <PnParam :object="athlete.param">
    <template #weight>
      <PnLiteralInput name='Weight' />
    </template>
    <template #birthday>
      <PnDatePicker name='Birthday' />
    </template>
  </PnParam>
</template>
<script lang='py'>
import param
import datetime
import panel as pn

DATE_BOUNDS = (datetime.date(1900, 1, 1), datetime.datetime.now().date())


class Athlete(param.Parameterized):
    name_ = param.String(default="P.A. Nelson")
    birthday = param.Date(default=datetime.date(1976, 9, 17), bounds=DATE_BOUNDS)
    weight = param.Number(default=82, bounds=(20, 300))

athlete = Athlete()

import ipywidgets as iw
# 自定义小部件
widgets = {
    "birthday": pn.widgets.DatePicker, 
    "weight": pn.widgets.LiteralInput(),
}
</script>

```


## 展开子对象

我们可以通过 `expand` 参数默认展开子对象：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnParam 
    :object="athlete.param" 
    :expand="True" />
</template>
<script lang='py'>
import param
import datetime
import panel as pn

DATE_BOUNDS = (datetime.date(1900, 1, 1), datetime.datetime.now().date())

class PowerCurve(param.Parameterized):
    one_hour_date = param.Date(default=datetime.date(2017, 8, 6), bounds=DATE_BOUNDS)

class Athlete(param.Parameterized):
    weight = param.Number(default=82, bounds=(20, 300))
    power_curve = param.ClassSelector(class_=PowerCurve, default=PowerCurve())

athlete = Athlete()
</script>

```


## 选择特定参数和自定义布局

我们可以选择只显示特定参数，并自定义布局：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnParam 
    :object="athlete.param"
    :widgets="widgets"
    :parameters="['name_', 'birthday', 'weight']"
    :show_name="False"
    :default_layout="PnRow"
    :width="600" />
  <hr/>
  <PnParam 
    :object="athlete.param"
    :parameters="['name_', 'birthday', 'weight']"
    :show_name="False"
    :default_layout="PnRow"
    :width="600">
    <template #weight>
      <PnLiteralInput name='Weight' :width=100 />
    </template>
    <template #birthday>
      <PnDatePicker name='Birthday' />
    </template>
  </PnParam>
</template>
<script lang='py'>
import param
import datetime
import panel as pn

DATE_BOUNDS = (datetime.date(1900, 1, 1), datetime.datetime.now().date())

class Athlete(param.Parameterized):
    name_ = param.String(default="P.A. Nelson")
    birthday = param.Date(default=datetime.date(1976, 9, 17), bounds=DATE_BOUNDS)
    weight = param.Number(default=82, bounds=(20, 300))

athlete = Athlete()

# 自定义小部件
widgets = {
    "birthday": pn.widgets.DatePicker,
    "weight": {"type": pn.widgets.LiteralInput, "width": 100}
}

# 导入布局组件
PnRow = pn.Column
</script>

```


## 滑块控件的连续更新禁用

当函数运行时间较长并且依赖于某个参数时，实时反馈可能成为负担，而不是有帮助。因此，如果参数使用的是滑块控件，可以通过设置 `throttled` 关键字为 `True` 来仅在释放鼠标按钮后才执行函数。

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnParam :object="model.param" :widgets="widgets" />
</template>
<script lang='py'>
import param
import panel as pn

class Model(param.Parameterized):
    without_throttled_enabled = param.Range(
        default=(100, 250),
        bounds=(0, 250),
    )

    with_throttled_enabled = param.Range(
        default=(100, 250),
        bounds=(0, 250),
    )

    @param.depends("without_throttled_enabled", "with_throttled_enabled")
    def result(self):
        return f"无节流: {self.without_throttled_enabled}, 有节流: {self.with_throttled_enabled}"

model = Model()

widgets = {
    "without_throttled_enabled": pn.widgets.IntRangeSlider,
    "with_throttled_enabled": {
        "type": pn.widgets.IntRangeSlider,
        "throttled": True,
    },
}
</script>

```


## 组合参数控件与结果显示

可以组合参数控件与计算结果显示：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnCol>
    <PnMarkdown>### 运动员</PnMarkdown>
    <PnParam 
      :object="athlete.param"
      :widgets="athlete_widgets"
      :parameters="['name_', 'birthday', 'weight']"
      :show_name="False"
      :default_layout="PnRow"
      :width="600" />
    
    <PnMarkdown>#### 功率曲线</PnMarkdown>
    <PnRow>
      <PnParam 
        :object="athlete.power_curve.param"
        :default_layout="grid_layout"
        :show_name="False"
        :widgets="power_curve_widgets" />
    </PnRow>
    <PnDisplay :obj="athlete.power_curve.plot()" />
  </PnCol>
</template>
<script lang='py'>
import param
import datetime
import pandas as pd
import hvplot.pandas
import panel as pn

DATE_BOUNDS = (datetime.date(1900, 1, 1), datetime.datetime.now().date())

class PowerCurve(param.Parameterized):
    ten_sec = param.Number(default=1079)
    ten_sec_date = param.Date(default=datetime.date(2018, 8, 21), bounds=DATE_BOUNDS)
    one_min = param.Number(default=684)
    one_min_date = param.Date(default=datetime.date(2017, 8, 31), bounds=DATE_BOUNDS)
    ten_min = param.Number(default=419)
    ten_min_date = param.Date(default=datetime.date(2017, 9, 22), bounds=DATE_BOUNDS)
    twenty_min = param.Number(default=398)
    twenty_min_date = param.Date(default=datetime.date(2017, 9, 22), bounds=DATE_BOUNDS)
    one_hour = param.Number(default=319)
    one_hour_date = param.Date(default=datetime.date(2017, 8, 6), bounds=DATE_BOUNDS)
    
    @param.depends("ten_sec", "one_min", "ten_min", "twenty_min", "one_hour")
    def plot(self):
        data = {
            "duration": [10 / 60, 1, 10, 20, 60],
            "power": [self.ten_sec, self.one_min, self.ten_min, self.twenty_min, self.one_hour],
        }
        dataframe = pd.DataFrame(data)
        line_plot = dataframe.hvplot.line(
            x="duration", y="power", line_color="#007BFF", line_width=3, responsive=True,
        )
        scatter_plot = dataframe.hvplot.scatter(
            x="duration", y="power", marker="o", size=6, color="#007BFF", responsive=True
        )
        fig = line_plot * scatter_plot
        gridstyle = {"grid_line_color": "black", "grid_line_width": 0.1}
        fig = fig.opts(
            min_height=400,
            toolbar=None,
            yticks=list(range(0, 1600, 200)),
            ylim=(0, 1500),
            gridstyle=gridstyle,
            show_grid=True,
        )
        return fig

class Athlete(param.Parameterized):
    name_ = param.String(default="P.A. Nelson")
    birthday = param.Date(default=datetime.date(1976, 9, 17), bounds=DATE_BOUNDS)
    weight = param.Number(default=82, bounds=(20, 300))
    power_curve = param.ClassSelector(class_=PowerCurve, default=PowerCurve())

athlete = Athlete()

# 自定义小部件
athlete_widgets = {
    "birthday": pn.widgets.DatePicker,
    "weight": {"type": pn.widgets.LiteralInput, "width": 100}
}

power_curve_widgets = {
    "ten_sec_date": pn.widgets.DatePicker, 
    "one_min_date": pn.widgets.DatePicker, 
    "ten_min_date": pn.widgets.DatePicker,
    "twenty_min_date": pn.widgets.DatePicker, 
    "one_hour_date": pn.widgets.DatePicker
}

# 导入布局组件
PnRow = pn.Row
PnColumn = pn.Column

# 创建一个新的网格布局类
def new_class(cls, **kwargs):
    "创建一个覆盖参数默认值的新类。"
    return type(type(cls).__name__, (cls,), kwargs)

grid_layout = new_class(pn.GridBox, ncols=2)
</script>

```


## API

### 属性

| 属性名            | 说明                          | 类型                                                           | 默认值 |
| ---------------- | ----------------------------- | ---------------------------------------------------------------| ------- |
| object           | `param.Parameterized` 类的 `param` 属性 | ^[param.parameterized.Parameters]                     | None |
| parameters       | 标识要包含在窗格中的参数子集的列表 | ^[List[str]]                                                | [] |
| widgets          | 指定特定参数使用哪些小部件的字典。还可以指定小部件属性 | ^[Dict]                               | {} |
| default_layout   | 布局，如 Column、Row 等，或自定义 GridBox | ^[ClassSelector]                                    | Column |
| display_threshold | 优先级低于此值的参数不会显示 | ^[float]                                                        | 0 |
| expand           | 参数化子对象在实例化时是否展开或折叠 | ^[bool]                                                   | False |
| expand_button    | 是否添加展开和折叠子对象的按钮 | ^[bool]                                                        | True |
| expand_layout    | 展开子对象的布局 | ^[layout]                                                                   | Column |
| name             | 窗格的标题 | ^[str]                                                                           | '' |
| show_labels      | 是否显示标签 | ^[bool]                                                                        | True |
| show_name        | 是否显示参数化类的名称 | ^[bool]                                                              | True |
| sizing_mode      | 尺寸调整模式 | ^[str]                                                                         | 'fixed'  |
| width            | 宽度 | ^[int, str]                                                                           | None    |
| height           | 高度 | ^[int, str]                                                                           | None    |
| min_width        | 最小宽度 | ^[int]                                                                            | None    |
| min_height       | 最小高度 | ^[int]                                                                            | None    |
| max_width        | 最大宽度 | ^[int]                                                                            | None    |
| max_height       | 最大高度 | ^[int]                                                                            | None    |
| margin           | 外边距 | ^[int, tuple]                                                                       | 5       |
| css_classes      | CSS类名列表 | ^[list]                                                                        | []      |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| Param的字段 | 自定义widget      |




# JSON 数据

`PnJson` 组件允许在面板中渲染任意 JSON 字符串、字典和其他 JSON 可序列化对象。

底层实现为`panel.pane.JSON`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/JSON.html


## 基本用法

`PnJSON` 组件可用于渲染任意 JSON 对象的树视图，这些对象可以定义为字符串或 JSON 可序列化的 Python 对象。

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnJson :object="json_obj" name="JSON" />
</template>
<script lang='py'>
json_obj = {
    'boolean': False,
    'dict': {'a': 1, 'b': 2, 'c': 3},
    'int': 1,
    'float': 3.1,
    'list': [1, 2, 3],
    'null': None,
    'string': '一个字符串',
}
</script>

```


## 控制选项

`PnJson` 组件公开了许多可以从 Python 和 Javascript 更改的选项。尝试交互式地体验这些参数的效果：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnRow>
    <PnCol>
      <PnCheckbox v-model="hover_preview.value" name="悬停预览" />
      <PnIntSlider v-model="depth.value" name='展开深度' :start="-1" :end="5" />
      <PnRadioButtonGroup v-model="theme.value" :options="['light', 'dark']" name="主题" />
    </PnCol>
    <PnCol>
      <PnJson 
        :object="json_obj" 
        :hover_preview="hover_preview.value" 
        :depth="depth.value"
        :theme="theme.value" />
    </PnCol>
  </PnRow>
</template>
<script lang='py'>
from vuepy import ref

json_obj = {
    'boolean': False,
    'dict': {
        'a': 1, 
        'b': 2, 
        'c': 3,
        'nested': {
            'd': 4,
            'e': 5,
            'f': {
                'g': 6,
                'h': 7
            }
        }
    },
    'int': 1,
    'float': 3.1,
    'list': [1, 2, 3],
    'null': None,
    'string': '一个字符串',
}

hover_preview = ref(True)
depth = ref(1)
theme = ref('light')
</script>

```


## API

### 属性

| 属性名         | 说明                          | 类型                                                           | 默认值 |
| ------------- | ----------------------------- | ---------------------------------------------------------------| ------- |
| object        | JSON 字符串或 JSON 可序列化对象 | ^[str, object]                                                | None |
| depth         | 初始化时 JSON 结构展开的深度（`depth=-1` 表示完全展开） | ^[int]                              | 1 |
| hover_preview | 是否为折叠节点启用悬停预览      | ^[boolean]                                                    | True |
| theme         | 如果未提供值，则默认为由 pn.config.theme 设置的当前主题，如 JSON.THEME_CONFIGURATION 字典中所指定。如果未在那里定义，则回退到默认参数值（'light'）。 | ^[string] | 'light' |
| sizing_mode   | 尺寸调整模式                   | ^[str]                                                         | 'fixed'  |
| width         | 宽度                          | ^[int, str]                                                    | None    |
| height        | 高度                          | ^[int, str]                                                    | None    |
| min_width     | 最小宽度                      | ^[int]                                                         | None    |
| min_height    | 最小高度                      | ^[int]                                                         | None    |
| max_width     | 最大宽度                      | ^[int]                                                         | None    |
| max_height    | 最大高度                      | ^[int]                                                         | None    |
| margin        | 外边距                        | ^[int, tuple]                                                  | 5       |
| css_classes   | CSS类名列表                   | ^[list]                                                        | []      |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | 自定义默认内容      |




# ECharts 图表

`PnECharts` 组件在 Panel 中渲染 [Apache ECharts](https://echarts.apache.org/en/index.html) 和 [pyecharts](https://pyecharts.org/#/) 图表。请注意，要在 notebook 中使用 `PnECharts` 组件，必须以 'echarts' 作为参数加载 Panel 扩展，以确保初始化 echarts.js。

底层实现为`panel.pane.ECharts`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/ECharts.html


## 基本用法

让我们尝试 `PnECharts` 组件对 ECharts 规范的原始形式（即字典）的支持，例如，这里我们声明一个柱状图：

```vue
<!-- --plugins vpanel --show-code --codege-backend='panel' -->
<template>
  <PnECharts :object="echart_bar" :height="480" :width="640" />
</template>
<script lang='py'>
echart_bar = {
    'title': {
        'text': 'ECharts entry example'
    },
    'tooltip': {},
    'legend': {
        'data': ['Sales']
    },
    'xAxis': {
        'data': ["shirt", "cardign", "chiffon shirt", "pants", "heels", "socks"]
    },
    'yAxis': {},
    'series': [{
        'name': 'Sales',
        'type': 'bar',
        'data': [5, 20, 36, 10, 10, 20]
    }],
}
</script>

```


与所有其他组件一样，`PnECharts` 组件的 `object` 可以更新，要么是就地更新并触发更新：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnECharts :object="echart_bar" :height="480" :width="640" ref="echart_pane_ref" />
  <PnButton @click="change_to_line()">更改为折线图</PnButton>
  <PnButton @click="change_to_bar()">更改为柱状图</PnButton>
</template>
<script lang='py'>
from vuepy import ref

echart_pane_ref = ref(None)

echart_bar = {
    'title': {
        'text': 'ECharts entry example'
    },
    'tooltip': {},
    'legend': {
        'data': ['Sales']
    },
    'xAxis': {
        'data': ["shirt", "cardign", "chiffon shirt", "pants", "heels", "socks"]
    },
    'yAxis': {},
    'series': [{
        'name': 'Sales',
        'type': 'bar',
        'data': [5, 20, 36, 10, 10, 20]
    }],
}

def change_to_line():
    echart_bar['series'] = [dict(echart_bar['series'][0], type='line')]
    echart_pane_ref.value.unwrap().param.trigger('object')
    
def change_to_bar():
    echart_bar['series'] = [dict(echart_bar['series'][0], type='bar')]
    echart_pane_ref.value.unwrap().param.trigger('object')
</script>

```


ECharts 规范也可以通过声明宽度或高度以匹配容器来进行响应式调整大小：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnECharts :object="responsive_spec" :width='600' :height="400" />
</template>
<script lang='py'>
echart_bar = {
    'title': {
        'text': 'ECharts entry example'
    },
    'tooltip': {},
    'legend': {
        'data': ['Sales']
    },
    'xAxis': {
        'data': ["shirt", "cardign", "chiffon shirt", "pants", "heels", "socks"]
    },
    'yAxis': {},
    'series': [{
        'name': 'Sales',
        'type': 'bar',
        'data': [5, 20, 36, 10, 10, 20]
    }],
}

# todo 没有显示
responsive_spec = dict(echart_bar, responsive=True)
</script>

```


## PyECharts 支持

ECharts 组件还支持 pyecharts。例如，我们可以直接将 `pyecharts.charts.Bar` 图表传递给 `PnECharts` 组件：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnCol>
    <PnIntSlider v-model="bar1.value" name='Bar 1' :start="1" :end="100" />
    <PnIntSlider v-model="bar2.value" name='Bar 2' :start="1" :end="100" />
  </PnCol>
  <PnECharts :object="plot.value" :width="500" :height="250" />
</template>
<script lang='py'>
from vuepy import ref, computed
from pyecharts.charts import Bar

bar1 = ref(50)
bar2 = ref(50)

@computed
def plot():
    my_plot = (Bar()
               .add_xaxis(['Helicoptors', 'Planes'])
               .add_yaxis('Total In Flight', [bar1.value, bar2.value])
               )
    return my_plot
</script>

```


## 仪表盘示例

ECharts 库支持各种图表类型，由于图表使用 JSON 数据结构表示，我们可以轻松更新数据，然后发出更改事件以更新图表：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnColumn>
    <PnIntSlider v-model='value.value' name='Value' 
                 :start="0" :end="100" ref='slider_ref'/>
    <PnECharts :object="gauge" :width="400" :height="400" 
               ref="gauge_pane_ref" />
  </PnColumn>
</template>
<script lang='py'>
from vuepy import ref, watch, onMounted

value = ref(50)
gauge_pane_ref = ref(None)
slider_ref = ref(None)

gauge = {
    'tooltip': {
        'formatter': '{a} <br/>{b} : {c}%'
    },
    'series': [
        {
            'name': 'Gauge',
            'type': 'gauge',
            'detail': {'formatter': '{value}%'},
            'data': [{'value': 50, 'name': 'Value'}]
        }
    ]
}

@onMounted
def update_gauge():
    gauge_pane = gauge_pane_ref.value.unwrap()
    slider = slider_ref.value.unwrap()
    slider.jscallback(
        args={'gauge': gauge_pane}, 
        value="""
            gauge.data.series[0].data[0].value = cb_obj.value
            gauge.properties.data.change.emit()
        """
    )
</script>

```


## 事件处理

`PnECharts` 组件允许您监听 JavaScript API 中定义的任何事件，方法是使用 `on_event` 方法在 Python 中监听事件，或者使用 `js_on_event` 方法触发 JavaScript 回调。

有关可以监听的事件的详细信息，请参阅 [ECharts 事件文档](https://echarts.apache.org/handbook/en/concepts/event)。

### Python 事件处理

让我们从一个简单的点击事件开始，我们想从 Python 监听这个事件。要添加事件监听器，只需使用事件类型（在本例中为 'click'）和 Python 处理程序调用 `on_event` 方法：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
<PnRow>
  <PnECharts :object="echart_bar" :height="480" :width="640" 
             @click='on_click' />
  <PnJson :object="event_data.value" name="JSON" />
</PnRow>
</template>
<script lang='py'>
from vuepy import shallowRef


echart_bar = {
    'title': {
        'text': 'ECharts entry example'
    },
    'tooltip': {},
    'legend': {
        'data': ['Sales']
    },
    'xAxis': {
        'data': ["shirt", "cardign", "chiffon shirt", "pants", "heels", "socks"]
    },
    'yAxis': {},
    'series': [{
        'name': 'Sales',
        'type': 'line',
        'data': [5, 20, 36, 10, 10, 20]
    }],
}

event_data = shallowRef({})

def on_click(event):
    event_data.value = event.data
</script>

```


尝试单击折线上的点。点击后检查 `event_data.value` 时，您应该看到类似以下内容的数据。

要限制特定事件适用的对象类型，还可以向 `on_event` 方法提供 `query` 参数。`query` 的格式应该是 `mainType` 或 `mainType.subType`，例如：

- `'series'`：单击数据系列时触发事件
- `'series.line'`：仅当单击折线数据系列时才触发事件
- `'dataZoom'`：单击缩放时触发事件
- `'xAxis.category'`：单击 x 轴上的类别时触发事件

### JavaScript 事件处理

相同的概念适用于 JavaScript，但这里我们传入 JavaScript 代码片段。命名空间允许您访问事件数据 `cb_data` 和 ECharts 图表本身作为 `cb_obj`。这样，您可以访问事件并自己操作图表：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnECharts :object="echart_bar" :height="480" :width="640" 
             @jsclick='on_jsclick()' />
</template>
<script lang='py'>
from vuepy import ref, onMounted

echart_pane_ref = ref(None)
echart_bar = {
    'title': {
        'text': 'ECharts entry example'
    },
    'tooltip': {},
    'legend': {
        'data': ['Sales']
    },
    'xAxis': {
        'data': ["shirt", "cardign", "chiffon shirt", "pants", "heels", "socks"]
    },
    'yAxis': {},
    'series': [{
        'name': 'Sales',
        'type': 'line',
        'data': [5, 20, 36, 10, 10, 20]
    }],
}

def on_jsclick():
    return "alert(`Clicked on point: ${cb_data.dataIndex + 1}`)"

</script>

```


## API

### 属性

| 属性名      | 说明                 | 类型                                                           | 默认值 |
| ---------- | ------------------- | ---------------------------------------------------------------| ------- |
| object     | 以 Python 字典表示的 ECharts 图表规范，然后转换为 JSON。或者是像 `pyecharts.charts.Bar` 这样的 pyecharts 图表。 | ^[dict, object] | None |
| options    | 传递给 [`Echarts.setOption`](https://echarts.apache.org/en/api.html#echartsInstance.setOption) 的可选字典选项。允许微调渲染行为。 | ^[dict] | None |
| renderer   | 是否使用 HTML 'canvas'（默认）或 'svg' 渲染 | ^[str] | 'canvas' |
| theme      | 应用于图表的主题（'default'、'dark'、'light' 之一） | ^[str] | 'default' |
| sizing_mode | 尺寸调整模式         | ^[str]                                                         | 'fixed'  |
| width      | 宽度                 | ^[int, str]                                                    | None    |
| height     | 高度                 | ^[int, str]                                                    | None    |
| min_width  | 最小宽度             | ^[int]                                                         | None    |
| min_height | 最小高度             | ^[int]                                                         | None    |
| max_width  | 最大宽度             | ^[int]                                                         | None    |
| max_height | 最大高度             | ^[int]                                                         | None    |

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |
| click  | 当元素被点击时触发的事件 | ^[Callable]`(Event) -> None`    |
| jsclick  | 当元素被点击时触发的js事件 | ^[Callable]`() -> Str`    |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | 自定义默认内容      |

### 方法

| 属性名 | 说明 | 类型 |
| --- | --- | --- |
| on_event | 添加事件监听器 | ^[function] `(event_type: str, callback: Callable, query: str = None) -> None` |
| js_on_event | 添加 JavaScript 事件监听器 | ^[function] `(event_type: str, code: str, **args) -> None` |




# HTML 文本

`PnHTML` 组件允许在面板中渲染任意 HTML。它可以渲染包含有效 HTML 的字符串以及具有 `_repr_html_` 方法的对象，还可以定义自定义 CSS 样式。

底层实现为`panel.pane.HTML`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/HTML.html


## 基本用法

`PnHTML` 组件接受整个 HTML5 规范，包括任何嵌入的脚本标签（这些标签将被执行）。它还支持 `styles` 字典来控制渲染 HTML 内容的 `<div>` 标签的样式。

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnHTML :object="html_content" :styles="styles" />
  <PnHTML :object="html_content" style="border: 2px solid red" />
</template>
<script lang='py'>
styles = {
    'background-color': '#F6F6F6', 
    'border': '2px solid black',
    'border-radius': '5px', 
    'padding': '10px'
}

html_content = """
<h1>这是一个 HTML 面板</h1>

<code>
x = 5;<br>
y = 6;<br>
z = x + y;
</code>

<br>
<br>

<table>
  <tr>
    <th>名字</th>
    <th>姓氏</th> 
    <th>年龄</th>
  </tr>
  <tr>
    <td>张</td>
    <td>三</td> 
    <td>50</td>
  </tr>
  <tr>
    <td>李</td>
    <td>四</td> 
    <td>94</td>
  </tr>
</table>
"""
</script>

```


要更新 `object` 或 `styles`，我们可以直接设置它：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnHTML :object="html_content" :styles="dict(styles.value)"/>
  <PnButton @click="update_style()">更新样式</PnButton>
</template>
<script lang='py'>
from vuepy import ref

styles = ref({
    'background-color': '#F6F6F6', 
    'border': '2px solid black',
    'border-radius': '5px', 
    'padding': '10px'
})

html_content = """
<h1>这是一个 HTML 面板</h1>

<code>
x = 5;<br>
y = 6;<br>
z = x + y;
</code>

<br>
<br>

<table>
  <tr>
    <th>名字</th>
    <th>姓氏</th> 
    <th>年龄</th>
  </tr>
  <tr>
    <td>张</td>
    <td>三</td> 
    <td>50</td>
  </tr>
  <tr>
    <td>李</td>
    <td>四</td> 
    <td>94</td>
  </tr>
</table>
"""

def update_style():
    styles.value['border'] = '2px solid red'
</script>

```


## HTML 文档

`PnHTML` 组件设计用于显示*基本* HTML 内容。它不适合渲染包含 JavaScript 或其他动态元素的完整 HTML 文档。

要显示完整的 HTML 文档，您可以转义 HTML 内容并将其嵌入在 [`iframe`](https://www.w3schools.com/html/html_iframe.asp) 中。以下是实现方式：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnHTML :object="iframe_html" :height="350" sizing_mode="stretch_width" />
</template>
<script lang='py'>
import html
import numpy as np
import pandas as pd
import hvplot.pandas
from io import StringIO

# 设置随机种子以便结果可重现
np.random.seed(1)

# 创建时间序列数据框
idx = pd.date_range("1/1/2000", periods=1000)
df = pd.DataFrame(np.random.randn(1000, 4), index=idx, columns=list("ABCD")).cumsum()

# 使用 hvplot 绘制数据
plot = df.hvplot()

# 保存图表。这里使用 StringIO 对象而不是保存到磁盘
plot_file = StringIO()
hvplot.save(plot, plot_file)
plot_file.seek(0)  # 移动到 StringIO 对象的开头

# 读取 HTML 内容并转义
html_content = plot_file.read()
escaped_html = html.escape(html_content)

# 创建嵌入转义 HTML 的 iframe 并显示它
iframe_html = f'<iframe srcdoc="{escaped_html}" style="height:100%; width:100%" frameborder="0"></iframe>'
</script>

```


这种方法确保嵌入的 HTML 安全地隔离在 iframe 中，防止任何脚本直接在 Panel 环境中执行。这种方法特别适用于嵌入需要自己独立 HTML 结构的丰富内容，如交互式可视化。

## API

### 属性

| 属性名             | 说明                          | 类型                                                           | 默认值 |
| ----------------- | ----------------------------- | ---------------------------------------------------------------| ------- |
| object            | 要显示的字符串或具有 `_repr_html_` 方法的对象 | ^[str, object]                                  | None |
| disable_math      | 是否禁用使用 `$$` 分隔符转义的字符串的 MathJax 数学渲染 | ^[boolean]                          | True |
| enable_streaming  | 是否启用文本片段的流式传输。这将在更新时对 `object` 进行差异比较，只发送添加的尾部块 | ^[boolean] | False |
| sanitize_html     | 是否对发送到前端的 HTML 进行净化 | ^[boolean]                                                    | False |
| sanitize_hook     | 如果 `sanitize_html=True`，应用的净化回调 | ^[Callable]                                        | bleach.clean |
| styles            | 指定 CSS 样式的字典           | ^[dict]                                                        | {} |
| style            | 指定 CSS 样式           | ^[]                                                        | '' |
| sizing_mode       | 尺寸调整模式                   | ^[str]                                                         | 'fixed'  |
| width             | 宽度                          | ^[int, str]                                                    | None    |
| height            | 高度                          | ^[int, str]                                                    | None    |
| min_width         | 最小宽度                      | ^[int]                                                         | None    |
| min_height        | 最小高度                      | ^[int]                                                         | None    |
| max_width         | 最大宽度                      | ^[int]                                                         | None    |
| max_height        | 最大高度                      | ^[int]                                                         | None    |
| margin            | 外边距                        | ^[int, tuple]                                                  | 5       |
| css_classes       | CSS类名列表                   | ^[list]                                                        | []      |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | 自定义默认内容      |




# Vega 图表

`PnVega` 组件可以渲染基于 Vega 的图表（包括来自 Altair 的图表）。它通过对 Vega/Altair 对象中的数组数据使用二进制序列化来优化图表渲染，与 Vega 原生使用的标准 JSON 序列化相比，提供了显著的加速。请注意，要在 Jupyter 笔记本中使用 `PnVega` 组件，必须使用 'vega' 作为参数加载 Panel 扩展，以确保正确初始化 vega.js。

底层实现为`panel.pane.Vega`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/Vega.html


## 基本用法

`PnVega` 组件支持 [`vega`](https://vega.github.io/vega/docs/specification/) 和 [`vega-lite`](https://vega.github.io/vega-lite/docs/spec.html) 规范，可以以原始形式（即字典）提供，或者通过定义一个 `altair` 图表。

### Vega 和 Vega-lite

要显示 `vega` 和 `vega-lite` 规范，只需直接构造一个 `PnVega` 组件：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnVega :object="vegalite" :height="240" />
</template>
<script lang='py'>
vegalite = {
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "data": {"url": "https://raw.githubusercontent.com/vega/vega/master/docs/data/barley.json"},
  "mark": "bar",
  "encoding": {
    "x": {"aggregate": "sum", "field": "yield", "type": "quantitative"},
    "y": {"field": "variety", "type": "nominal"},
    "color": {"field": "site", "type": "nominal"}
  }
}
</script>

```


与所有其他组件一样，`PnVega` 组件的 `object` 可以更新：

```vue
<!-- --plugins vpanel --show-code -->
<template>
<PnCol>
  <PnVega :object="dict(chart.value)" />
  <PnButton @click="update_chart()">更新图表</PnButton>
</PnCol>
</template>
<script lang='py'>
from vuepy import ref

chart = ref({
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "data": {"url": "https://raw.githubusercontent.com/vega/vega/master/docs/data/barley.json"},
  "mark": "bar",
  "encoding": {
    "x": {"aggregate": "sum", "field": "yield", "type": "quantitative"},
    "y": {"field": "variety", "type": "nominal"},
    "color": {"field": "site", "type": "nominal"}
  }
})

def update_chart():
    chart.value.mark = 'area'
</script>

```


### 响应式大小调整

`vega-lite` 规范还可以通过将宽度或高度声明为匹配容器来进行响应式大小调整：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnVega :object="responsive_spec" />
</template>
<script lang='py'>
responsive_spec = {
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "data": {
    "url": "https://raw.githubusercontent.com/vega/vega/master/docs/data/disasters.csv"
  },
  "width": "container",
  "title": "响应式图表",
  "transform": [
    {"filter": "datum.Entity !== 'All natural disasters'"}
  ],
  "mark": {
    "type": "circle",
    "opacity": 0.8,
    "stroke": "black",
    "strokeWidth": 1
  },
  "encoding": {
    "x": {
        "field": "Year",
        "type": "quantitative",
        "axis": {"labelAngle": 90},
        "scale": {"zero": False}
    },
    "y": {
        "field": "Entity",
        "type": "nominal",
        "axis": {"title": ""}
    },
    "size": {
      "field": "Deaths",
      "type": "quantitative",
      "legend": {"title": "全球年度死亡人数", "clipHeight": 30},
      "scale": {"range": [0, 5000]}
    },
    "color": {"field": "Entity", "type": "nominal", "legend": None}
  }
}
</script>

```


请注意，`vega` 规范不支持将 `width` 和 `height` 设置为 `container`。

### DataFrame 数据值

为了方便起见，我们支持将 Pandas DataFrame 作为 `data` 的 `values`：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnVega :object="dataframe_spec" />
</template>
<script lang='py'>
import pandas as pd

dataframe_spec = {
    "title": "从 Pandas DataFrame 创建的简单条形图",
    'config': {
        'mark': {'tooltip': None},
        'view': {'height': 200, 'width': 500}
    },
    'data': {'values': pd.DataFrame({'x': ['A', 'B', 'C', 'D', 'E'], 'y': [5, 3, 6, 7, 2]})},
    'mark': 'bar',
    'encoding': {'x': {'type': 'ordinal', 'field': 'x'},
                 'y': {'type': 'quantitative', 'field': 'y'}},
    '$schema': 'https://vega.github.io/schema/vega-lite/v3.2.1.json'
}
</script>

```


## Altair

定义 Vega 图表的一种更便捷的方式是使用 [altair](https://altair-viz.github.io)，它在 vega-lite 之上提供了声明式 API。`PnVega` 组件在传入 Altair 图表时会自动渲染 Vega-Lite 规范：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnVega :object="chart" />
</template>
<script lang='py'>
import altair as alt
from vega_datasets import data

cars = data.cars()

chart = alt.Chart(cars).mark_circle(size=60).encode(
    x='Horsepower',
    y='Miles_per_Gallon',
    color='Origin',
    tooltip=['Name', 'Origin', 'Horsepower', 'Miles_per_Gallon']
).interactive()
</script>

```


Altair 图表也可以通过更新组件的 `object` 来更新：

```vue
<!-- --plugins vpanel --show-code -->
<template>
<PnCol>
  <PnVega :object="chart.value" />
  <PnButton @click="update_chart()">更新图表</PnButton>
</PnCol>
</template>
<script lang='py'>
import altair as alt
from vega_datasets import data
from vuepy import ref

cars = data.cars()

chart = ref(alt.Chart(cars).mark_circle(size=60).encode(
    x='Horsepower',
    y='Miles_per_Gallon',
    color='Origin',
    tooltip=['Name', 'Origin', 'Horsepower', 'Miles_per_Gallon']
).interactive())

def update_chart():
    # refs['altair_pane'].object = chart.mark_circle(size=100)
    chart.value = chart.value.mark_circle(size=200)
</script>

```


Altair 支持的所有常规布局和组合操作符也可以渲染：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnVega :object="combined_chart" />
</template>
<script lang='py'>
import altair as alt

penguins_url = "https://raw.githubusercontent.com/vega/vega/master/docs/data/penguins.json"

chart1 = alt.Chart(penguins_url).mark_point().encode(
    x=alt.X('Beak Length (mm):Q', scale=alt.Scale(zero=False)),
    y=alt.Y('Beak Depth (mm):Q', scale=alt.Scale(zero=False)),
    color='Species:N'
).properties(
    height=300,
    width=300,
)

chart2 = alt.Chart(penguins_url).mark_bar().encode(
    x='count()',
    y=alt.Y('Beak Depth (mm):Q', bin=alt.Bin(maxbins=30)),
    color='Species:N'
).properties(
    height=300,
    width=100
)

combined_chart = chart1 | chart2
</script>

```


## 选择

`PnVega` 组件自动同步在 Vega/Altair 图表上表达的任何选择。目前支持三种类型的选择：

- `selection_interval`：允许使用框选工具选择区间，以 `{<x轴名称>: [x最小值, x最大值], <y轴名称>: [y最小值, y最大值]}` 的形式返回数据
- `selection_single`：允许使用点击选择单个点，返回整数索引列表
- `selection_multi`：允许使用（shift+）点击选择多个点，返回整数索引列表

### 区间选择

作为一个例子，我们可以在图表中添加一个 Altair `selection_interval` 选择：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnVega :object="chart" :debounce="10" ref='vega'/>
  <PnColumn>
    <h3>选择数据：</h3>
    <PnJSON :object="selection_data.value" />
  </PnColumn>
</template>
<script lang='py'>
import altair as alt
from vuepy import ref, onMounted

penguins_url = "https://raw.githubusercontent.com/vega/vega/master/docs/data/penguins.json"

brush = alt.selection_interval(name='brush')  # 区间类型的选择

chart = alt.Chart(penguins_url).mark_point().encode(
    x=alt.X('Beak Length (mm):Q', scale=alt.Scale(zero=False)),
    y=alt.Y('Beak Depth (mm):Q', scale=alt.Scale(zero=False)),
    color=alt.condition(brush, 'Species:N', alt.value('lightgray'))
).properties(
    width=250,
    height=250
).add_params(
    brush
)

selection_data = ref(None)
vega = ref(None)


@onMounted
def on_render():
    vega_pane = vega.value.unwrap()
    
    def on_selection_change(event):
        print(event)
        selection_data.value = event.new
        
    # todo
    vega_pane.param.watch(on_selection_change, 'selection')
    
</script>

```


请注意，我们指定了一个单一的 `debounce` 值，如果我们声明多个选择，可以通过将其指定为字典来为每个命名事件声明一个去抖动值，例如 `debounce={'brush': 10, ...}`。

## 主题

可以使用 `theme` 参数为图表应用主题：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnVega :object="chart" theme="dark" />
</template>
<script lang='py'>
import altair as alt
from vega_datasets import data

cars = data.cars()

chart = alt.Chart(cars).mark_circle(size=60).encode(
    x='Horsepower',
    y='Miles_per_Gallon',
    color='Origin',
    tooltip=['Name', 'Origin', 'Horsepower', 'Miles_per_Gallon']
).interactive()
</script>

```


## API

### 属性

| 属性名        | 说明                          | 类型                                                           | 默认值 |
| ------------ | ----------------------------- | ---------------------------------------------------------------| ------- |
| object       | 包含 Vega 或 Vega-Lite 图表规范的字典，或者是 Altair 图表 | ^[dict, object]                  | None |
| debounce     | 应用于选择事件的去抖延迟时间，可以指定为单个整数值（以毫秒为单位）或声明每个事件的去抖值的字典 | ^[int, dict] | None |
| theme        | 应用于图表的主题。必须是 'excel'、'ggplot2'、'quartz'、'vox'、'fivethirtyeight'、'dark'、'latimes'、'urbaninstitute' 或 'googlecharts' 之一 | ^[str] | None |
| show_actions | 是否显示图表操作菜单，如保存、编辑等 | ^[boolean]                                               | True |
| selection    | Selection 对象公开反映图表上声明的选择到 Python 中的参数 | ^[object]                         | None |
| sizing_mode  | 尺寸调整模式                   | ^[str]                                                         | 'fixed'  |
| width        | 宽度                          | ^[int, str]                                                    | None    |
| height       | 高度                          | ^[int, str]                                                    | None    |
| min_width    | 最小宽度                      | ^[int]                                                         | None    |
| min_height   | 最小高度                      | ^[int]                                                         | None    |
| max_width    | 最大宽度                      | ^[int]                                                         | None    |
| max_height   | 最大高度                      | ^[int]                                                         | None    |
| margin       | 外边距                        | ^[int, tuple]                                                  | 5       |
| css_classes  | CSS类名列表                   | ^[list]                                                        | []      |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | 自定义默认内容      |




# Streamz 数据流组件

`PnStreamz` 组件可以渲染 [Streamz](https://streamz.readthedocs.io/en/latest/) Stream 对象发出的任意对象，与专门处理 streamz DataFrame 和 Series 对象并公开各种格式化选项的 `DataFrame` 组件不同。

底层实现为`panel.pane.Streamz`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/Streamz.html


## 基本用法

> **注意**：如果您尚未使用 Streamz 库，我们建议使用 Param 和 Panel 生态系统中的功能，例如[反应式表达式](https://param.holoviz.org/user_guide/Reactive_Expressions.html)、[生成器函数](https://param.holoviz.org/user_guide/Generators.html)和/或*周期性回调*。我们发现这些功能得到更加可靠的支持。

`PnStreamz` 组件使用默认的 Panel 解析方式来确定如何渲染 Stream 返回的对象。默认情况下，该组件只有在显示时才会监视 `Stream`，我们可以通过设置 `always_watch=True` 让它在创建后立即开始监视流：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnStreamz :object="stream_map.value" :always_watch="True"/>
</template>
<script lang='py'>
from vuepy import ref, onMounted
from streamz import Stream

def increment(x):
    return x + 1

source = Stream()
stream_map = ref(source.map(increment))

# 注意：为了确保流的静态渲染显示内容
# 我们设置 always_watch=True 并在显示前发出一个事件
@onMounted
def emit():
    source.emit(1)
</script>

```


现在我们可以定义一个周期性回调，它在 `Stream` 上发出递增的计数：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnStreamz :object="stream_map" :always_watch="True" ref="streamz_pane" />
  <PnButton @click="start_emit()">开始发送数据</PnButton>
  <PnButton @click="stop_emit()">停止发送数据</PnButton>
</template>
<script lang='py'>
from vuepy import ref, onMounted
from streamz import Stream
import panel as pn

def increment(x):
    return x + 1

source = Stream()
stream_map = source.map(increment)
streamz_pane = ref(None)

# 为了确保流的静态渲染显示内容
@onMounted
def emit():
    source.emit(1)

count = 1
callback = None

def emit_count():
    nonlocal count
    count += 1
    source.emit(count)

def start_emit():
    nonlocal callback
    if callback is None or not callback.running:
        callback = pn.state.add_periodic_callback(emit_count, period=100)

def stop_emit():
    nonlocal callback
    if callback and callback.running:
        callback.stop()
</script>

```


## 复杂数据流

`PnStreamz` 组件可以用于流式传输任何类型的数据。例如，我们可以创建一个 streamz DataFrame，将数据累积到滑动窗口中，然后将其映射到 Altair `line_plot` 函数：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnStreamz 
    :object="altair_stream" 
    :height="350" 
    :sizing_mode="'stretch_width'" 
    :always_watch="True" 
    ref="altair_pane" />
  <PnButton @click="start_emit()">开始发送数据</PnButton>
  <PnButton @click="stop_emit()">停止发送数据</PnButton>
</template>
<script lang='py'>
from vuepy import ref
import numpy as np
import altair as alt
import pandas as pd
from datetime import datetime
from streamz.dataframe import DataFrame as sDataFrame
import panel as pn

altair_pane = ref(None)

# 创建一个 streamz DataFrame
df = sDataFrame(example=pd.DataFrame({'y': []}, index=pd.DatetimeIndex([])))

def line_plot(data):
    return alt.Chart(pd.concat(data).reset_index()).mark_line().encode(
        x='index',
        y='y',
    ).properties(width="container")

# 创建累积数据的流，使用滑动窗口，并映射到图表函数
altair_stream = df.cumsum().stream.sliding_window(50).map(line_plot)

# 初始数据
for i in range(20):
    df.emit(pd.DataFrame({'y': [np.random.randn()]}, index=pd.DatetimeIndex([datetime.now()])))

callback = None

def emit():
    df.emit(pd.DataFrame({'y': [np.random.randn()]}, index=pd.DatetimeIndex([datetime.now()])))

def start_emit():
    nonlocal callback
    if callback is None or not callback.running:
        callback = pn.state.add_periodic_callback(emit, period=500)

def stop_emit():
    nonlocal callback
    if callback and callback.running:
        callback.stop()
</script>

```


## API

### 属性

| 属性名            | 说明                          | 类型                                                           | 默认值 |
| ---------------- | ----------------------------- | ---------------------------------------------------------------| ------- |
| object           | 被监视的 streamz.Stream 对象    | ^[streamz.Stream]                                              | None |
| always_watch     | 是否在未显示时也监视流         | ^[bool]                                                        | False |
| rate_limit       | 事件之间的最小间隔（秒）       | ^[float]                                                       | 0.1 |
| sizing_mode      | 尺寸调整模式                  | ^[str]                                                         | 'fixed'  |
| width            | 宽度                          | ^[int, str]                                                    | None    |
| height           | 高度                          | ^[int, str]                                                    | None    |
| min_width        | 最小宽度                      | ^[int]                                                         | None    |
| min_height       | 最小高度                      | ^[int]                                                         | None    |
| max_width        | 最大宽度                      | ^[int]                                                         | None    |
| max_height       | 最大高度                      | ^[int]                                                         | None    |
| margin           | 外边距                        | ^[int, tuple]                                                  | 5       |
| css_classes      | CSS类名列表                   | ^[list]                                                        | []      |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | 自定义默认内容      |




# Alert 警告

警告组件用于提供针对典型用户操作的上下文反馈消息，具有多种可用且灵活的警告消息样式。

底层实现为`panel.pane.Alert`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/Alert.html


## 基本用法

`PnAlert` 支持 Markdown 和 HTML 语法：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnAlert>
## Alert
This is a warning!
  </PnAlert>
</template>

```

## 不同类型

`PnAlert` 组件有多种 `alert_type` 选项，用于控制警告消息的颜色：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnCol sizing_mode='stretch_width' >
    <PnAlert :alert_type='alert_type' v-for='alert_type in alert_types'>
    {{ message.replace('{alert_type}', alert_type) }}
    </PnAlert>
  </PnCol>
</template>
<script lang='py'>
alert_types = ['primary', 'secondary', 'success', 'danger', 'warning', 'info', 'light', 'dark']
message = "This is a **{alert_type}** alert with [an example link](https://panel.holoviz.org/). Give it a click if you like."
</script>

```


## 长文本消息

它也可以用于较长的消息：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnAlert alert_type="success">{{ long_text }}</PnAlert>
</template>
<script lang='py'>
long_text = """
### Well done!

Aww yeah, you successfully read this important alert message. 
This example text is going to run a bit longer so that you 
can see how spacing within an alert works with this kind of content.

---

Did you notice the use of the divider?
"""
</script>

```


## API

### 属性

| 属性名      | 说明                 | 类型                                                           | 默认值 |
| ---------- | ------------------- | ---------------------------------------------------------------| ------- |
| alert_type | 警告类型             | ^[str] `'primary'`, `'secondary'`, `'success'`, `'danger'`, `'warning'`, `'info'`, `'light'`, `'dark'` | 'primary' |
| sizing_mode | 尺寸调整模式         | ^[str]                                                         | 'fixed'  |
| width      | 宽度                 | ^[int, str]                                                    | None    |
| height     | 高度                 | ^[int, str]                                                    | None    |
| min_width  | 最小宽度             | ^[int]                                                         | None    |
| min_height | 最小高度             | ^[int]                                                         | None    |
| max_width  | 最大宽度             | ^[int]                                                         | None    |
| max_height | 最大高度             | ^[int]                                                         | None    |
| margin     | 外边距               | ^[int, tuple]                                                  | 5       |
| css_classes | CSS类名列表          | ^[list]                                                        | []      |




# Reacton 组件

`PnReacton` 组件可以在 Panel 应用程序中渲染 [Reacton](https://reacton.solara.dev/en/latest/) 组件，无论是在笔记本中还是在部署的服务器上。Reacton 提供了一种以类似 React 的方式编写可重用组件的方法，用于使用 ipywidgets 生态系统（ipywidgets、ipyvolume、bqplot、threejs、leaflet、ipyvuetify 等）构建基于 Python 的 UI。请注意，Reacton 主要是一种编写应用程序的方法。

在笔记本中，这不是必需的，因为 Panel 只是使用常规的笔记本 ipywidget 渲染器。特别是在 JupyterLab 中，以这种方式导入 ipywidgets 扩展可能会干扰 UI 并使 JupyterLab UI 无法使用，因此请谨慎启用扩展。

底层实现为`panel.pane.Reacton`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/Reacton.html


## 基本用法

`panel_vuepy` 函数会自动将任何 Reacton 组件转换为可显示的面板，同时保持其所有交互功能：


## 结合 Reacton 和 Panel 组件

Reacton 可以与 Panel 组件结合使用，但我们需要做两个修改：

1. Panel 组件必须使用 `pn.ipywidget` 包装器包装为 ipywidget（这需要 `jupyter_bokeh`）。
2. 包装后的 Panel 组件必须添加到 reacton 布局组件中。

在下面的示例中，我们将 `reacton.ipywidgets.Button` 替换为 `PnButton`，然后用 `pn.ipywidget` 和 `reacton.ipywidgets.VBox` 包装它：


## 复杂示例

可以在 Reacton 中构建更复杂的应用程序并在 Panel 中显示。以下是 Reacton 文档中的计算器示例。

### 逻辑


## 使用 ipyvuetify

Reacton 也可以与 ipyvuetify 结合使用，创建更美观的界面：


## API

### 属性

| 属性名           | 说明                          | 类型                                                           | 默认值 |
| --------------- | ----------------------------- | ---------------------------------------------------------------| ------- |
| object          | 被显示的 Reacton 组件对象      | ^[object]                                                      | None |
| default_layout  | 包装图表和小部件的布局        | ^[pn.layout.Panel]                                             | Row |
| sizing_mode     | 尺寸调整模式                  | ^[str]                                                         | 'fixed'  |
| width           | 宽度                          | ^[int, str]                                                    | None    |
| height          | 高度                          | ^[int, str]                                                    | None    |
| min_width       | 最小宽度                      | ^[int]                                                         | None    |
| min_height      | 最小高度                      | ^[int]                                                         | None    |
| max_width       | 最大宽度                      | ^[int]                                                         | None    |
| max_height      | 最大高度                      | ^[int]                                                         | None    |
| margin          | 外边距                        | ^[int, tuple]                                                  | 5       |
| css_classes     | CSS类名列表                   | ^[list]                                                        | []      |

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | 自定义默认内容      |

### 方法

| 属性名 | 说明 | 类型 |
| --- | --- | --- |



# VTKJS 三维模型

`PnVTK` 组件可以在 Panel 应用程序中渲染 vtk.js 文件，使得可以加载和交互复杂的 3D 几何体。

底层实现为`panel.pane.VTK`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/VTKJS.html


## 基本用法

构造 `PnVTKJS` 组件最简单的方法是给它一个 vtk.js 文件，它将序列化并嵌入到图表中。`PnVTKJS` 组件还支持 Bokeh 提供的常规尺寸选项，包括响应式尺寸模式：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnVTK 
    object="https://raw.githubusercontent.com/Kitware/vtk-js/master/Data/StanfordDragon.vtkjs"
    sizing_mode="stretch_width" 
    :height="400" 
    :enable_keybindings="True" 
    :orientation_widget="True" />
</template>

```


与所有其他组件一样，`PnVTKJS` 组件可以通过替换 `object` 来更新：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnVTK
    :object="vtkjs_url.value" 
    sizing_mode="stretch_width" 
    :height="400" 
    :enable_keybindings="True" 
    :orientation_widget="True"
  />
  <PnButton @click="update_object()">更换 3D 模型</PnButton>
</template>
<script lang='py'>
from vuepy import ref

vtkjs_url = ref("https://raw.githubusercontent.com/Kitware/vtk-js/master/Data/StanfordDragon.vtkjs")

def update_object():
    vtkjs_url.value = "https://raw.githubusercontent.com/Kitware/vtk-js-datasets/master/data/vtkjs/TBarAssembly.vtkjs"
</script>

```


## 相机控制

一旦显示了 VTKJS 组件，它将自动将相机状态与组件对象同步。相机参数仅在交互结束时更新。我们可以在相应的参数上读取相机状态：

```vue
<!-- --plugins vpanel --show-code --codegen-backend='panel' -->
<template>
  <PnVTK 
    object="https://raw.githubusercontent.com/Kitware/vtk-js/master/Data/StanfordDragon.vtkjs"
    :sizing_mode="'stretch_width'" 
    :height="400" 
    :enable_keybindings="True" 
    :orientation_widget="True"
    ref="vtk_pane_ref" />
  <PnButton @click="read_camera()">读取相机状态</PnButton>
  <PnJSON v-if="camera_state.value" :object="camera_state.value" :depth="1" />
</template>
<script lang='py'>
from vuepy import ref

vtk_pane_ref = ref(None)
camera_state = ref(None)

def read_camera():
    vtk_pane = vtk_pane_ref.value.unwrap()
    if vtk_pane.camera:
        camera_state.value = vtk_pane.camera
</script>

```


这种技术也使得可以将两个或多个 VTKJS 组件的相机链接在一起：

还可以在 Python 中修改相机状态并触发更新：
```vue
<!-- --plugins vpanel --show-code --codegen-backend='panel' -->
<template>
  <PnRow>
    <PnVTK 
      object="https://raw.githubusercontent.com/Kitware/vtk-js/master/Data/StanfordDragon.vtkjs"
      :height="400" 
      :sizing_mode="'stretch_width'"
      ref="dragon1_ref" />
    <PnVTK 
      object="https://raw.githubusercontent.com/Kitware/vtk-js/master/Data/StanfordDragon.vtkjs"
      :height="400" 
      :sizing_mode="'stretch_width'"
      ref="dragon2_ref" />
  </PnRow>
  <PnButton @click="change_view_angle()">改变视角</PnButton>
</template>
<script lang='py'>
from vuepy import ref, onMounted

dragon1_ref = ref(None)
dragon2_ref = ref(None)

@onMounted
def on_render():
    dragon1 = dragon1_ref.value.unwrap()
    dragon2 = dragon2_ref.value.unwrap()
    # 双向链接两个组件的相机
    dragon1.jslink(dragon2, camera='camera', bidirectional=True)
    
def change_view_angle():
    dragon1 = dragon1_ref.value.unwrap()
    if dragon1.camera:
        dragon1.camera['viewAngle'] = 50
        dragon1.param.trigger('camera')
</script>

```


## API

### 属性

| 属性名                      | 说明                          | 类型                                                           | 默认值 |
| -------------------------- | ----------------------------- | ---------------------------------------------------------------| ------- |
| object                     | 可以是指向本地或远程的带有 `.vtkjs` 扩展名的文件的字符串 | ^[str, object]                  | None |
| axes                       | 在 3D 视图中构造的坐标轴的参数字典。必须至少包含 `xticker`、`yticker` 和 `zticker` | ^[dict]    | None |
| camera                     | 反映 VTK 相机当前状态的字典      | ^[dict]                                                       | None |
| enable_keybindings         | 激活/禁用键盘绑定的布尔值。绑定的键有：s（将所有 actor 表示设置为*表面*）、w（将所有 actor 表示设置为*线框*）、v（将所有 actor 表示设置为*顶点*）、r（居中 actor 并移动相机，使所有 actor 可见） | ^[boolean] | False |
| orientation_widget         | 激活/禁用 3D 面板中的方向部件的布尔值 | ^[boolean]                                                  | False |
| interactive_orientation_widget | 如果为 True，则方向部件可点击并允许将场景旋转到正交投影之一 | ^[boolean]                | False |
| sizing_mode                | 尺寸调整模式                   | ^[str]                                                         | 'fixed'  |
| width                      | 宽度                          | ^[int, str]                                                    | None    |
| height                     | 高度                          | ^[int, str]                                                    | None    |
| min_width                  | 最小宽度                      | ^[int]                                                         | None    |
| min_height                 | 最小高度                      | ^[int]                                                         | None    |
| max_width                  | 最大宽度                      | ^[int]                                                         | None    |
| max_height                 | 最大高度                      | ^[int]                                                         | None    |
| margin                     | 外边距                        | ^[int, tuple]                                                  | 5       |
| css_classes                | CSS类名列表                   | ^[list]                                                        | []      |
### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | 自定义默认内容      |

### 方法

| 方法名 | 说明 | 参数 |
| --- | --- | --- |
| export_scene | 导出场景并生成可以被官方 vtk-js 场景导入器加载的文件 | filename: str |




# Str 原始字符串组件

`Str`组件允许在面板中呈现任意文本。

与`PnMarkdown`和`PnHTML`组件不同，`PnStr`组件将文本解释为原始字符串，不应用任何标记，并默认以等宽字体显示。

这个组件将渲染任何文本，如果给定一个`object`，将显示该`object`的Python `repr`。

底层实现为`panel.pane.Str`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/Str.html


## 基本用法

`PnStr`组件可以显示任何文本字符串，并保持其原始格式。

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnStr object="This is a raw string which will not be formatted in any way except for the applied style." 
         :styles="{'font-size': '12pt'}" />
</template>

```


与其他组件一样，`PnStr`组件可以通过设置其`object`参数进行更新。如前所述，非字符串类型会自动转换为字符串：

```vue
<!-- --plugins vpanel --show-code -->
<template>
<PnCol>
  <PnStr :object="content.value" :styles="{'font-size': '14pt'}" />
  <PnRow>
    <PnButton @click="updateToString()">Display String</PnButton>
    <PnButton @click="updateToNumber()">Display Number</PnButton>
    <PnButton @click="updateToObject()">Display Object</PnButton>
  </PnRow>
</PnCol>
</template>

<script lang='py'>
from vuepy import ref

content = ref('This is a raw string which will not be formatted in any way except for the applied style.')

def updateToString():
    content.value = 'Updated raw string content'
    
def updateToNumber():
    content.value = 1.3234232
    
def updateToObject():
    class TestObject:
        def __repr__(self):
            return "TestObject(custom_repr)"
    content.value = TestObject()
</script>

```


## API

### 属性

| 属性名    | 说明                                     | 类型                | 默认值 |
| --------- | ---------------------------------------- | ------------------- | ------ |
| value     | 要显示的字符串。如果提供非字符串类型，将显示该对象的`repr` | ^[str\|object]     | —      |
| styles    | 指定CSS样式的字典                       | ^[dict]             | {}     |
| style    | 指定CSS样式的                      | ^[str]             | ''     |




# Vizzu 可视化图表组件

`Vizzu`组件在Panel中渲染[Vizzu](https://lib.vizzuhq.com/)图表。注意，要在notebook中使用`Vizzu`组件，必须在加载Panel扩展时将'vizzu'作为参数传递，以确保初始化vizzu.js。

底层实现为`panel.pane.Vizzu`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/Vizzu.html


## 基本用法

`PnVizzu`组件可以根据`config`定义如何绘制数据（以列字典或DataFrame的形式定义）：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnVizzu :object="data" 
           :config="{'geometry': 'rectangle', 'x': 'Name', 
                     'y': 'Weight', 'title': 'Weight by person'}"
           :duration="400" 
           :height="400" 
           sizing_mode="stretch_width" 
           :tooltip="True" />
</template>

<script lang='py'>
import numpy as np

# Create sample data
data = {
    'Name': ['Alice', 'Bob', 'Ted', 'Patrick', 'Jason', 'Teresa', 'John'],
    'Weight': 50+np.random.randint(0, 10, 7)*10
}
</script>

```


Vizzu的主要卖点之一是在数据或`config`更新时的动态动画。例如，如果我们更改"geometry"，可以看到动画在两种状态之间平滑过渡。

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnVizzu ref="vizzu_ref" 
           :object="data" 
           :config="config.value"
           :duration="400" 
           :height="400" 
           sizing_mode="stretch_width" 
           :tooltip="True" />
  <PnRow>
    <PnButton @click="changeToCircle()">Change to Circle</PnButton>
    <PnButton @click="changeToArea()">Change to Area</PnButton>
    <PnButton @click="changeToRectangle()">Change to Rectangle</PnButton>
  </PnRow>
</template>

<script lang='py'>
import numpy as np
from vuepy import ref

# Create sample data
data = {
    'Name': ['Alice', 'Bob', 'Ted', 'Patrick', 'Jason', 'Teresa', 'John'],
    'Weight': 50+np.random.randint(0, 10, 7)*10
}

config = ref({'geometry': 'rectangle', 'x': 'Name', 'y': 'Weight', 
              'title': 'Weight by person'})
vizzu_ref = ref(None)

def changeToCircle():
    config.value = {**config.value, 'geometry': 'circle'}
    
def changeToArea():
    config.value = {**config.value, 'geometry': 'area'}
    
def changeToRectangle():
    vizzu = vizzu_ref.value.unwrap()
    vizzu.animate({'geometry': 'rectangle'})
    config.value = vizzu.config
</script>

```


## 列类型

`PnVizzu`支持两种列类型：

- `'dimension'`：通常用于非数值数据和/或图表的独立维度（例如x轴）
- `'measure'`：数值通常用于图表的因变量（例如y轴值）

`PnVizzu`组件会根据数据的dtypes自动推断类型，但在某些情况下，可能需要使用`column_types`参数显式覆盖列的类型。一个常见的例子是在x轴上绘制整数时，通常会被视为"measure"，但在折线图或条形图的情况下应该被视为独立维度。

下面的示例演示了这种情况，这里我们希望将"index"视为独立变量，并使用`column_types={'index': 'dimension'}`覆盖默认推断的类型：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnVizzu :object="df" 
           :column_types="{'index': 'dimension'}" 
           :config="{'x': 'index', 'y': 'Y', 'geometry': 'line'}"
           :height="300" 
           sizing_mode="stretch_width" />
</template>

<script lang='py'>
import numpy as np
import pandas as pd

# Create sample data
df = pd.DataFrame(np.random.randn(50), columns=list('Y')).cumsum()
</script>

```


## 预设

Vizzu提供了各种[预设图表类型](https://lib.vizzuhq.com/latest/examples/presets/)。在`PnVizzu`组件中，您可以通过在`config`中提供`'preset'`作为键来使用这些预设。在下面的示例中，我们动态创建一个`config`，根据`RadioButtonGroup`切换`preset`：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnRow>
    <PnRadioButtonGroup 
        v-model="chart_type.value" 
        :options="{'Stream': 'stream', 'Bar': 'stackedColumn'}" 
        align="center" />
  </PnRow>
  <PnVizzu :object="agg"
           :config="getConfig()"
           :column_types="{'p_year': 'dimension'}"
           :height="500"
           sizing_mode="stretch_width"
           :style="{
             'plot': {
               'xAxis': {
                 'label': {
                   'angle': '-45deg'
                 }
               }
             }
           }" />
</template>

<script lang='py'>
import pandas as pd
from vuepy import ref

# Load data
windturbines = pd.read_csv('https://datasets.holoviz.org/windturbines/v1/windturbines.csv')
agg = windturbines.groupby(['p_year', 't_manu'])[['p_cap']]\
      .sum().sort_index(level=0).reset_index()

# Chart type selection
chart_type = ref('stream')

def getConfig():
    return {
        'preset': chart_type.value, 
        'x': 'p_year', 
        'y': 'p_cap', 
        'stackedBy': 't_manu'
    }
</script>

```


## 交互控制

`PnVizzu`组件公开了许多选项，可以从Python和JavaScript更改。尝试交互式地测试这些参数的效果：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnVizzu ref="vizzu_ref" 
           :object="data" 
           :config="dict(config.value)"
           :duration="duration.value" 
           :height="400" 
           sizing_mode="stretch_width" 
           :tooltip="tooltip.value" />
  <PnRow>
    <PnCol>
      <PnCheckbox v-model="tooltip.value" name="Show Tooltip" />
      <PnIntSlider v-model="duration.value" 
                   name="Animation Duration" 
                   :start="100" 
                   :end="2000" 
                   :step="100" />
    </PnCol>
    <PnCol>
      <PnButton @click="changeToCircle()">Change to Circle</PnButton>
      <PnButton @click="changeToArea()">Change to Area</PnButton>
      <PnButton @click="changeToRectangle()">Change to Rectangle</PnButton>
    </PnCol>
  </PnRow>
</template>

<script lang='py'>
import numpy as np
from vuepy import ref

# Create sample data
data = {
    'Name': ['Alice', 'Bob', 'Ted', 'Patrick', 'Jason', 'Teresa', 'John'],
    'Weight': 50+np.random.randint(0, 10, 7)*10
}

# Control parameters
tooltip = ref(True)
duration = ref(400)
vizzu_ref = ref(None)
config = ref({
    'geometry': 'rectangle', 'x': 'Name', 'y': 
    'Weight', 'title': 'Weight by person'
})

def changeToCircle():
    config.value.geometry = 'circle'
    
def changeToArea():
    config.value.geometry = 'area'
    
def changeToRectangle():
    config.value.geometry = 'rectangle'
</script>

```


## API

### 属性

| 属性名        | 说明                                     | 类型                | 默认值 |
| ------------- | ---------------------------------------- | ------------------- | ------ |
| value         | 以Python数组字典或DataFrame表示的数据     | ^[dict\|pd.DataFrame] | —      |
| animation     | 动画设置                                 | ^[dict]             | {}     |
| config        | 包含渲染特定静态图表或动画图表状态所需的所有参数 | ^[dict]        | {}     |
| columns       | 可选的列定义。如果未定义，将从数据中推断   | ^[list]             | None   |
| column_types  | 列类型定义，覆盖自动推断的类型            | ^[dict]             | {}     |
| tooltip       | 是否在图表上启用工具提示                  | ^[bool]             | False  |
| duration      | 动画持续时间（毫秒）                      | ^[int]              | 500    |
| style         | 图表样式配置                             | ^[dict]             | {}     |

### 方法

| 方法名    | 说明                            | 类型                         |
| --------- | ------------------------------- | ---------------------------- |
| animate   | 接受一个新的'data'、'config'和'style'值的字典，用于更新图表 | ^[Callable]`(obj: dict) -> None` |
| stream    | 向图表流式传输新数据            | ^[Callable]`(data: dict) -> None` |
| patch     | 修补数据中的一行或多行          | ^[Callable]`(data: dict) -> None` |
| controls  | 返回控制面板组件                | ^[Callable]`(jslink=bool) -> Panel` |




# Bokeh 图表

`PnBokeh` 组件允许在 Panel 应用程序中显示任何可显示的 [Bokeh](http://bokeh.org) 模型。由于 Panel 内部基于 Bokeh 构建，Bokeh 模型只是简单地插入到图表中。由于 Bokeh 模型通常只显示一次，某些与 Panel 相关的功能（如同步同一模型的多个视图）可能无法工作。尽管如此，这种组件类型对于将原始 Bokeh 代码与高级 Panel API 结合起来非常有用。

在 notebook 中工作时，对 Bokeh 对象的任何更改可能不会自动同步，需要显式调用包含 Bokeh 对象的 Panel 组件的 `pn.state.push_notebook`。

底层实现为`panel.pane.Bokeh`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/Bokeh.html


## 基本用法

下面是一个使用 Bokeh 创建饼图并将其显示在 Panel 中的示例：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnBokeh :object="p" theme="dark_minimal" />
</template>
<script lang='py'>
import pandas as pd
from math import pi
from bokeh.palettes import Category20c
from bokeh.plotting import figure
from bokeh.transform import cumsum

x = {
    'United States': 157,
    'United Kingdom': 93,
    'Japan': 89,
    'China': 63,
    'Germany': 44,
    'India': 42,
    'Italy': 40,
    'Australia': 35,
    'Brazil': 32,
    'France': 31,
    'Taiwan': 31,
    'Spain': 29
}

data = pd.Series(x).reset_index(name='value').rename(columns={'index':'country'})
data['angle'] = data['value']/data['value'].sum() * 2*pi
data['color'] = Category20c[len(x)]

p = figure(height=350, title="Pie Chart", toolbar_location=None,
           tools="hover", tooltips="@country: @value", x_range=(-0.5, 1.0))

r = p.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='country', source=data)

p.axis.axis_label=None
p.axis.visible=False
p.grid.grid_line_color = None
</script>

```


## 更新 Bokeh 对象

要使用实时服务器更新图表，我们可以简单地修改底层模型。如果我们在 Jupyter notebook 中工作，我们还必须在组件上调用 `pn.io.push_notebook` 辅助函数，或者明确使用 `bokeh_pane.param.trigger('object')` 触发事件：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnBokeh :object="p" ref="bokeh_pane_ref" />
  <PnButton @click="update_colors()">更新颜色</PnButton>
  <PnButton @click="replace_with_div()">替换为文本</PnButton>
</template>
<script lang='py'>
import pandas as pd
from math import pi
from bokeh.palettes import Category20c, Category20
from bokeh.plotting import figure
from bokeh.transform import cumsum
from bokeh.models import Div

from vuepy import ref

bokeh_pane_ref = ref(None)

x = {
    'United States': 157,
    'United Kingdom': 93,
    'Japan': 89,
    'China': 63,
    'Germany': 44
}

data = pd.Series(x).reset_index(name='value').rename(columns={'index':'country'})
data['angle'] = data['value']/data['value'].sum() * 2*pi
data['color'] = Category20c[len(x)]

p = figure(height=350, title="Pie Chart", toolbar_location=None,
           tools="hover", tooltips="@country: @value", x_range=(-0.5, 1.0))

r = p.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='country', source=data)

p.axis.axis_label=None
p.axis.visible=False
p.grid.grid_line_color = None

def update_colors():
    bokeh_pane = bokeh_pane_ref.value.unwrap()
    r.data_source.data['color'] = Category20[len(x)]
    bokeh_pane.param.trigger('object')

# in a live server
def replace_with_div():
    bokeh_pane = bokeh_pane_ref.value.unwrap()
    bokeh_pane.object = Div(text='<h2>This text replaced the pie chart</h2>')
</script>

```


## 交互式 Bokeh 应用

使用 Panel 渲染 Bokeh 对象的另一个很好的特性是回调将像在服务器上一样工作。因此，您可以简单地将现有的 Bokeh 应用程序包装在 Panel 中，它将可以渲染并开箱即用，无论是在 notebook 中还是作为独立应用程序提供服务：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnBokeh :object="app" />
</template>
<script lang='py'>
import numpy as np
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider, TextInput
from bokeh.plotting import figure

# Set up data
N = 200
x = np.linspace(0, 4*np.pi, N)
y = np.sin(x)
source = ColumnDataSource(data=dict(x=x, y=y))

# Set up plot
plot = figure(height=400, width=400, title="my sine wave",
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_range=[0, 4*np.pi], y_range=[-2.5, 2.5])

plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)

# todo to vuepy component
# Set up widgets
text = TextInput(title="title", value='my sine wave')
offset = Slider(title="offset", value=0.0, start=-5.0, end=5.0, step=0.1)
amplitude = Slider(title="amplitude", value=1.0, start=-5.0, end=5.0, step=0.1)
phase = Slider(title="phase", value=0.0, start=0.0, end=2*np.pi)
freq = Slider(title="frequency", value=1.0, start=0.1, end=5.1, step=0.1)

# Set up callbacks
def update_title(attrname, old, new):
    plot.title.text = text.value

text.on_change('value', update_title)

def update_data(attrname, old, new):
    # Get the current slider values
    a = amplitude.value
    b = offset.value
    w = phase.value
    k = freq.value

    # Generate the new curve
    x = np.linspace(0, 4*np.pi, N)
    y = a*np.sin(k*x + w) + b

    source.data = dict(x=x, y=y)

for w in [offset, amplitude, phase, freq]:
    w.on_change('value', update_data)

# Set up layouts and add to document
inputs = column(text, offset, amplitude, phase, freq)
app = row(inputs, plot, width=800)
</script>

```


## API

### 属性

| 属性名      | 说明                 | 类型                                                           | 默认值 |
| ---------- | ------------------- | ---------------------------------------------------------------| ------- |
| object     | 要显示的 Bokeh 模型    | ^[bokeh.layouts.LayoutDOM]                                     | None |
| theme      | 要应用的 Bokeh 主题    | ^[bokeh.themes.Theme]                                          | None |
| sizing_mode | 尺寸调整模式         | ^[str]                                                         | 'fixed'  |
| width      | 宽度                 | ^[int, str]                                                    | None    |
| height     | 高度                 | ^[int, str]                                                    | None    |
| min_width  | 最小宽度             | ^[int]                                                         | None    |
| min_height | 最小高度             | ^[int]                                                         | None    |
| max_width  | 最大宽度             | ^[int]                                                         | None    |
| max_height | 最大高度             | ^[int]                                                         | None    |
| margin     | 外边距               | ^[int, tuple]                                                  | 5       |
| css_classes | CSS类名列表          | ^[list]                                                        | []      |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | 自定义默认内容      |




# StaticText 静态文本

StaticText组件显示文本值但不允许编辑它，适用于展示只读信息。

底层实现为`panel.widgets.StaticText`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/StaticText.html


## 基本用法

静态文本组件提供了一种简单的方式来显示不可编辑的文本内容。

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnStaticText 
    name="静态文本" 
    value="这是一个不可编辑的文本内容"
  />
</template>

```


## 动态内容

静态文本组件可以与响应式数据结合使用，以显示动态更新的内容。

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnCol>
    <PnStaticText 
      name="计数器值" 
      :value="f'当前计数: {counter.value}'"
    />
    <PnButton 
      name="增加计数" 
      button_type="primary" 
      @click="increment()"
    />
  </PnCol>
</template>
<script lang='py'>
import panel as pn
from vuepy import ref

counter = ref(0)

def increment():
    counter.value += 1
</script>

```


## 样式自定义

可以通过样式参数自定义静态文本的外观。

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnCol>
    <PnStaticText 
      name="标准样式" 
      value="默认样式的静态文本"
    />
    
    <PnStaticText 
      name="自定义颜色" 
      value="红色文本内容"
      style="color: red"
    />
    
    <PnStaticText 
      value="无标题但有背景色的文本"
      style="background: #e8f4f8; padding: 10px; border-radius: 5px"
    />
    
    <PnStaticText 
      name="大字体" 
      value="这是一个字体较大的文本"
      style="font-size: 24px; font-weight: bold"
    />
  </PnCol>
</template>
<script lang='py'>
import panel as pn
from vuepy import ref

pn.extension()
</script>

```


## API

### 属性

| 属性名 | 说明 | 类型 | 默认值 |
| -------- | ------------------- | ---------------------------------------------------------------| ------- |
| name | 组件标题 | ^[string] | — |
| value | 文本内容 | ^[string] | — |




# ButtonIcon 图标按钮

此小部件最初显示一个默认 `icon` 。点击后，会在指定的 `toggle_duration` 时间内显示 `active_icon`。

例如，可以有效利用 `ButtonIcon` 来实现类似于 `ChatGPT` 的复制到剪贴板按钮的功能。

底层实现为`panel.widgets.ButtonIcon`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/ButtonIcon.html


## 基本用法

基本的图标按钮使用：[tabler-icons.io](https://tabler-icons.io/) 图标
```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnColumn>
    <!-- Basic icons -->
    <PnButtonIcon icon="heart" name="favorite" :toggle_duration='1000' />
    <PnButtonIcon icon="heart" size='20px' />
    <PnButtonIcon icon="clipboard" active_icon='check'>copy</PnButtonIcon>
    <PnButtonIcon icon="download" v-model:clicks='count.value'>
     + {{ count.value }}
    </PnButtonIcon>
    
    <!-- With events -->
    <PnButtonIcon icon="refresh" active_icon="check" @click="handle_refresh" />
  </PnColumn>
</template>

<script lang="py">
import asyncio
from vuepy import ref

count = ref(0)

def handle_refresh(event):
    print("Refreshing...")
</script>

```


## 使用SVG图标

可以使用SVG字符串作为图标：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnButtonIcon name='svg icon' :toggle_duration='1000' size='25px'>
    <template #icon>
      <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-ad-off" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
      <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
      <path d="M9 5h10a2 2 0 0 1 2 2v10m-2 2h-14a2 2 0 0 1 -2 -2v-10a2 2 0 0 1 2 -2" />
      <path d="M7 15v-4a2 2 0 0 1 2 -2m2 2v4" />
      <path d="M7 13h4" />
      <path d="M17 9v4" />
      <path d="M16.115 12.131c.33 .149 .595 .412 .747 .74" />
      <path d="M3 3l18 18" />
      </svg>
    </template>
    <template #active-icon>
     <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-ad-filled" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
     <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
     <path d="M19 4h-14a3 3 0 0 0 -3 3v10a3 3 0 0 0 3 3h14a3 3 0 0 0 3 -3v-10a3 3 0 0 0 -3 -3zm-10 4a3 3 0 0 1 2.995 2.824l.005 .176v4a1 1 0 0 1 -1.993 .117l-.007 -.117v-1h-2v1a1 1 0 0 1 -1.993 .117l-.007 -.117v-4a3 3 0 0 1 3 -3zm0 2a1 1 0 0 0 -.993 .883l-.007 .117v1h2v-1a1 1 0 0 0 -1 -1zm8 -2a1 1 0 0 1 .993 .883l.007 .117v6a1 1 0 0 1 -.883 .993l-.117 .007h-1.5a2.5 2.5 0 1 1 .326 -4.979l.174 .029v-2.05a1 1 0 0 1 .883 -.993l.117 -.007zm-1.41 5.008l-.09 -.008a.5 .5 0 0 0 -.09 .992l.09 .008h.5v-.5l-.008 -.09a.5 .5 0 0 0 -.318 -.379l-.084 -.023z" stroke-width="0" fill="currentColor" />
     </svg>
    </template>
  </PnButtonIcon>
</template>

```

## 自定义 css style

通过`style`设置组件外层DOM节点(意味着无法设置某些组件内的样式，如background-color，font-size等)的CSS样式:
* `width`、`height` 设置组件的高和宽
* `border` 设置组件的边框
* `size`  设置大小
* ...
```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnButtonIcon name="height 60px" :height="60" />
  <PnButtonIcon name="width 30px" :width="30" />
  <PnButtonIcon name='border: 5px solid red;' style='border: 5px solid #FAEBD7;'/>
  <PnButtonIcon :icon="custom_icon" size="2.5em" />
</template>
<script lang='py'>
from vuepy import ref

custom_icon = """
<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-bulb" 
     width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" 
     fill="none" stroke-linecap="round" stroke-linejoin="round">
   <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
   <path d="M3 12h1m8 -9v1m8 8h1m-15.4 -6.4l.7 .7m12.1 -.7l-.7 .7"></path>
   <path d="M9 16a5 5 0 1 1 6 0a3.5 3.5 0 0 0 -1 3a2 2 0 0 1 -4 0a3.5 3.5 0 0 0 -1 -3"></path>
   <path d="M9.7 17l4.6 0"></path>
</svg>
"""
</script>

```


## API

### 属性

| 属性名        | 说明                 | 类型                                                | 默认值 |
| ------------ | ------------------- | -------------------------------------------------- | ------- |
| icon         | 正常显示的图标（tabler-icons.io图标名称或SVG字符串） | ^[str]            | None    |
| active_icon  | 切换时显示的图标（tabler-icons.io图标名称或SVG字符串） | ^[str]            | None    |
| clicks       | 图标被点击的次数       | ^[int]                                            | 0       |
| toggle_duration | active_icon显示的毫秒数及按钮禁用时间 | ^[int]                            | -       |
| value        | 处理事件时从False切换到True | ^[bool]                                       | False   |
| name         | 小部件的标题           | ^[str]                                            | ""      |
| description  | 悬停时显示的描述        | ^[str]                                            | ""      |
| disabled     | 是否可编辑            | ^[bool]                                           | False   |
| size         | 大小（支持css font-size格式如`1em`, `20px`等） | ^[str]                            | -       |

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |
| click | 当按钮被点击时触发的事件 | ^[Callable]`(event: dict) -> None` |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
|    default     |          按钮文字        |
|    icon |          svg 图标 |




# IntRangeSlider 整数范围滑块

整数范围滑块组件允许使用带有两个手柄的滑块选择整数范围，与RangeSlider类似，但专门用于整数值。

底层实现为`panel.widgets.IntRangeSlider`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/IntRangeSlider.html


## 基本用法

基本的整数范围滑块使用：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnIntRangeSlider name="整数范围滑块" 
                   :start="0" 
                   :end="10" 
                   :value="(2, 8)"
                   :step="1"
                   @change="update_value" />
</template>
<script lang='py'>
from vuepy import ref

value = ref((2, 8))

def update_value(event):
    print(event.new) # (3, 9)
</script>

```


## 自定义步长

可以设置`step`参数来控制值的间隔：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnIntRangeSlider name="步长为2" 
                   :start="0" 
                   :end="20" 
                   :value="(4, 12)"
                   :step="2" />
</template>
<script lang='py'>
from vuepy import ref

value = ref((4, 12))
</script>

```


## 垂直方向

滑块可以设置为垂直方向显示：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnRow>
    <PnIntRangeSlider name="垂直范围滑块" 
                     orientation="vertical"
                     :value="(30, 70)"
                     :height="300" />
  </PnRow>
</template>
<script lang='py'>
from vuepy import ref
</script>

```


## 滑块颜色和方向

可以自定义滑块条的颜色和方向：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnIntRangeSlider name="蓝色范围滑块" 
                   bar_color="#3498db"
                   :start="0" 
                   :end="100" 
                   :value="(20, 80)"
                   :step="10" />
  <PnIntRangeSlider name="从右到左" 
                   direction="rtl"
                   :start="0" 
                   :end="100" 
                   :value="(20, 80)" 
                   :step="10" />
</template>
<script lang='py'>
from vuepy import ref
</script>

```


## API

### 属性

| 属性名          | 说明                           | 类型                                | 默认值     |
| -------------- | ------------------------------ | ---------------------------------- | --------- |
| start          | 范围的下限                     | ^[int]                             | 0         |
| end            | 范围的上限                     | ^[int]                             | 1         |
| step           | 值之间的间隔                   | ^[int]                             | 1         |
| value          | 所选范围的上下界元组            | ^[(int, int)]                      | (0, 1)    |
| value_throttled| 鼠标释放前阻止的所选范围的上下界元组 | ^[(int, int)]                 | (0, 1)    |
| bar_color      | 滑块条的颜色，十六进制RGB值      | ^[str]                             | None      |
| direction      | 滑块方向，从左到右('ltr')或从右到左('rtl') | ^[str]                    | 'ltr'     |
| disabled       | 是否禁用                       | ^[bool]                            | False     |
| name           | 组件标题                       | ^[str]                             | ""        |
| orientation    | 滑块的显示方向，'horizontal'或'vertical' | ^[str]                    | 'horizontal' |
| tooltips       | 是否在滑块手柄上显示工具提示      | ^[bool]                           | True      |

### Events

| 事件名         | 说明                       | 类型                                   |
| ------------- | -------------------------- | -------------------------------------- |
| change        | 当值更改时触发的事件         | ^[Callable]`(value) -> None`          |




# Player 播放器

播放器组件是一个用于循环播放数值范围的工具，可用于动画或步进通过数据。它提供了播放、暂停、步进和循环控制。

底层实现为`panel.widgets.Player`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/Player.html


## 基本用法

基本的播放器使用：

```vue
<!-- --plugins vpanel --show-code -->
<template>
 <PnCol :height='150'>
  <PnPlayer name="Player" 
           :start="0" 
           :end="10" 
           :step="1"
           v-model='current_value.value'/>
 </PnCol>
 <p>value: {{ current_value.value }}</p>
</template>
<script lang='py'>
from vuepy import ref

current_value = ref(0)

</script>

```


## 设置循环和间隔

可以设置播放器是否循环以及播放间隔：

```vue
<!-- --plugins vpanel --show-code -->
<template>
 <PnCol :height=150>
  <PnPlayer name="Player" 
           :start="0" 
           :end="10" 
           :step="1"
           loop_policy='loop'
           :interval="1000" />
  </PnCol>
</template>

```


## 设置显示模式

可以设置播放器的显示模式，如只显示按钮或者同时显示值等：

```vue
<!-- --plugins vpanel --show-code -->
<template>
 <PnCol style='height:140px;'>
  <PnPlayer name="Player" 
           :start="0" 
           :end="10" 
           :step="1"
           show_value
           :visible_buttons="['previous', 'play', 'pause', 'next']" />
 </PnCol>
</template>

```


## API

### 属性

| 属性名               | 说明                                                                 | 类型                          | 默认值      |
|---------------------|--------------------------------------------------------------------|-----------------------------|------------|
| value/v-model               | 当前整数值                                                          | ^[int]                      | 0          |
| direction           | 当前播放方向 (-1: 倒放, 0: 暂停, 1: 正放)                           | ^[int]                      | 0          |
| interval            | 更新间隔时间（毫秒）                                                 | ^[int]                      | 500        |
| loop_policy         | 循环策略 ('once': 一次, 'loop': 循环, 'reflect': 反射)              | ^[str]                      | 'once'     |
| start               | 数值范围下限                                                        | ^[int]                      | 0          |
| end                 | 数值范围上限                                                        | ^[int]                      | 100        |
| step                | 数值变化步长                                                        | ^[int]                      | 1          |
| value_throttled     | 鼠标释放前的节流当前值（使用滑块选择时）                              | ^[int]                      | 0          |
| disabled            | 是否禁用控件                                                        | ^[bool]                     | False      |
| name                | 控件标题                                                           | ^[str]                      | ""         |
| scale_buttons       | 按钮缩放比例                                                        | ^[float]                    | 1.0        |
| show_loop_controls  | 是否显示循环策略切换选项                                             | ^[bool]                     | True       |
| show_value          | 是否显示当前值                                                      | ^[bool]                     | True       |
| value_align         | 数值显示位置 ('start': 左, 'center': 中, 'end': 右)                 | ^[str]                      | 'center'   |
| visible_buttons     | 可见按钮列表 ('slower','first','previous',...,'faster')             | ^[list[str]]                | all        |
| visible_loop_options| 可见循环选项 ('once', 'loop', 'reflect')                            | ^[list[str]]                | all        |

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |
| change | 当当前值变化时触发的事件 | ^[Callable]`(event: dict) -> None` |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |
| pause | 暂停播放 | ^[Callable]`() -> None` |
| play  | 开始播放 | ^[Callable]`() -> None` |
| reverse | 反向播放 | ^[Callable]`() -> None` |




# Checkbox 复选框

复选框组件允许通过勾选框在`True`/`False`状态之间切换单一条件。Checkbox、Toggle和Switch组件功能类似，可互相替换。

底层实现为`panel.widgets.Checkbox`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/Checkbox.html


## 基本用法

基本的复选框使用：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnCheckbox name="复选框" @change="update_value" />
  <div>当前状态: {{ is_checked.value }}</div>
</template>
<script lang='py'>
from vuepy import ref

is_checked = ref(False)

def update_value(event):
    is_checked.value = event.new
</script>

```


## 默认选中状态

可以通过设置`value`参数为`True`使复选框默认处于选中状态：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnCheckbox name="默认选中" :value="True" v-model='is_checked.value' />
  <div>当前状态: {{ is_checked.value }}</div>
</template>
<script lang='py'>
from vuepy import ref

is_checked = ref(True)
</script>

```


## 禁用状态

可以通过设置`disabled`参数为`True`使复选框处于禁用状态：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnRow>
    <PnCheckbox name="禁用状态" @change="update_value" disabled />
  </PnRow>
  <div>禁用复选框状态: {{ is_checked.value }}</div>
</template>
<script lang='py'>
from vuepy import ref

is_checked = ref(False)


def update_value(event):
    is_checked2.value = event.new
</script>

```


## 结合其他组件使用

复选框通常用于控制其他组件的显示或行为：

```vue
<!-- --plugins vpanel --show-code --backend='panel' --app app -->
<template>
  <PnCheckbox name="显示内容" v-model="is_checked.value" />
  <PnRow v-if="is_checked.value">
    <PnTextInput placeholder="input..." />
  </PnRow>
</template>
<script lang='py'>
from vuepy import ref

is_checked = ref(True)

def update_value(value):
    is_checked.value = value
</script>

```


## API

### 属性

| 属性名       | 说明                 | 类型      | 默认值    |
| ----------- | ------------------- | --------- | --------- |
| value       | 复选框是否选中        | ^[bool]   | False     |
| disabled    | 是否禁用组件          | ^[bool]   | False     |
| name        | 组件标题             | ^[str]    | ""        |
| description | 鼠标悬停时显示的描述   | ^[str]    | ""        |

### Events

| 事件名  | 说明                | 类型                          |
| ------ | ------------------ | ----------------------------- |
| change | 当状态改变时触发的事件 | ^[Callable]`(value) -> None` |




# Tabulator 表格

Tabulator组件提供了一个功能丰富的交互式表格，可用于显示、编辑和操作`Pandas DataFrame`数据。

底层实现为`panel.widgets.Tabulator`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/Tabulator.html

## 基本用法
在编辑单元格时，Tabulator 的 value 数据会实时更新，你可以通过常规的 `@change` 监听变化。但如果需要精确获取被修改的单元格信息，还可以绑定 `@edit`，该回调会接收一个 TableEditEvent 对象，其中包含以下字段：
* column：被编辑列的名称
* row：被编辑行在 DataFrame 中的整数索引
* old：单元格的旧值
* value：单元格的新值
```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnTabulator :value="df.value" 
               @change='on_change'
               @edit='on_edit' 
               @click='on_click' />
</template>
<script lang='py'>
import pandas as pd
from vuepy import ref

df = ref(pd.DataFrame({
    'int': [1, 2, 3],
    'float': [3.14, 6.28, 9.42],
    'str': ['A', 'B', 'C'],
    'bool': [True, False, True],
    'date': ['2019-01-01', '2020-01-01', '2020-01-10']
}))

def on_change(event):
    print('on change')
    print(event.new) #    int  float str   bool        date
                     # 0    1   3.14   A  False  2019-01-01
                     # 1    2   6.28   B  False  2020-01-01
                     # 2    3   9.42   C   True  2020-01-10

def on_edit(event):
    print('on edit')
    print(event) # TableEditEvent(column=bool, row=0, value=False, old=True)
    print(df.value) #    int  float str   bool        date
                    # 0    1   3.14   A  False  2019-01-01
                    # 1    2   6.28   B  False  2020-01-01
                    # 2    3   9.42   C   True  2020-01-10

def on_click(event):
    print(event) # CellClickEvent(column=int, row=0, value=1)

</script>

```

## Formatter 格式化器

### 使用 Bokeh Formatter


默认情况下，该组件会根据列的数据类型自动选择适合的Bokeh `CellFormatter`（单元格格式化器）和`CellEditor`（单元格编辑器）类型。用户也可以通过显式指定字典来覆盖默认设置，将列名映射到特定的编辑器或格式化器实例。例如在下面的示例中，我们创建了一个`NumberFormatter`来定制`float`列的数字格式，并使用`BooleanFormatter`实例以勾选/叉号形式显示`bool`列的值。

有效的 Bokeh 格式化程序列表包括：
* [BooleanFormatter](https://docs.bokeh.org/en/latest/docs/reference/models/widgets/tables.html#bokeh.models.BooleanFormatter)
* [DateFormatter](https://docs.bokeh.org/en/latest/docs/reference/models/widgets/tables.html#bokeh.models.DateFormatter)
* [NumberFormatter](https://docs.bokeh.org/en/latest/docs/reference/models/widgets/tables.html#bokeh.models.NumberFormatter)
* [HTMLTemplateFormatter](https://docs.bokeh.org/en/latest/docs/reference/models/widgets/tables.html#bokeh.models.HTMLTemplateFormatter)
* [StringFormatter](https://docs.bokeh.org/en/latest/docs/reference/models/widgets/tables.html#bokeh.models.StringFormatter)
* [ScientificFormatter](https://docs.bokeh.org/en/latest/docs/reference/models/widgets/tables.html#bokeh.models.ScientificFormatter)
```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnTabulator :value="df.value" :formatters="formatters" />
</template>
<script lang='py'>
import pandas as pd
from vuepy import ref
from bokeh.models.widgets.tables import NumberFormatter, BooleanFormatter

df = ref(pd.DataFrame({
    'float': [3.14, 6.28, 9.42],
    'bool': [True, False, True]
}))

formatters = {
    'float': NumberFormatter(format='0.00000'),
    'bool': BooleanFormatter(),
}
</script>

```

### 使用 Tabulator Formatter

除了使用 Bokeh 提供的格式化器之外，还可以使用 Tabulator 库内置的有效格式化器。这些格式化器可以定义为字符串，或者以字典形式声明类型及其他参数（作为 `formatterParams` 传递给 Tabulator）。  

可用的 Tabulator 格式化器列表可在 [Tabulator 文档](https://tabulator.info/docs/6.3.1/format#format-builtin)中查阅。  

需要注意的是，类似的规则也可通过 `title_formatters` 参数应用于列标题（但不支持 Bokeh 的 `CellFormatter` 类型）。
```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnTabulator :value="df.value" :formatters="formatters" />
</template>
<script lang='py'>
import pandas as pd
from vuepy import ref

df = ref(pd.DataFrame({
    'float': [3.14, 6.28, 9.42],
    'bool': [True, False, True]
}))

formatters = {
    'float': {'type': 'progress', 'max': 10},
    'bool': {'type': 'tickCross'}
}
</script>

```

## Editors 编辑器

与格式化器类似，Tabulator 能够原生支持 Bokeh 的编辑器类型，但在底层实现中，它会将大部分 Bokeh 编辑器替换为 Tabulator 库原生支持的等效编辑器。

因此，通常更推荐直接使用 Tabulator 的原生编辑器。将某列的编辑器设为 None 会使该列不可编辑。需要注意的是，除了标准的 Tabulator 编辑器外，Tabulator 组件还额外支持 'date'（日期）和 'datetime'（日期时间）编辑器。
```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnTabulator :value="df.value" :editors="bokeh_editors" />
  <PnTabulator :value="df.value" :editors="tabulator_editors" />
</template>
<script lang='py'>
import pandas as pd
import datetime as dt
from bokeh.models.widgets.tables import CheckboxEditor, NumberEditor, SelectEditor
from vuepy import ref

df = ref(pd.DataFrame({
    'int': [1, 2, 3],
    'float': [3.14, 6.28, 9.42],
    'str': ['A', 'B', 'C'],
    'bool': [True, False, True],
    'date': [dt.date(2019, 1, 1), dt.date(2020, 1, 1), dt.date(2020, 1, 10)],
    'datetime': [dt.datetime(2019, 1, 1, 10), dt.datetime(2020, 1, 1, 12), dt.datetime(2020, 1, 10, 13)]
}, index=[1, 2, 3]))

bokeh_editors = {
    'float': NumberEditor(),
    'bool': CheckboxEditor(),
    'str': SelectEditor(options=['A', 'B', 'C', 'D']),
}

tabulator_editors = {
    'int': None,
    'float': {'type': 'number', 'max': 10, 'step': 0.1},
    'bool': {'type': 'tickCross', 'tristate': True, 'indeterminateValue': None},
    'str': {'type': 'list', 'valuesLookup': True},
    'date': 'date',
    'datetime': 'datetime'
}
</script>

```

### 嵌套编辑器

假设你需要让某个单元格的编辑器依赖于另一个单元格的值，可以使用 `nested type`。嵌套类型需要两个参数：`options` 和 `lookup_order`，其中 `lookup_order` 用于指定选项的查找顺序。

我们创建一个包含三列的简单 DataFrame，其中第 `2` 列的选项取决于第 `0` 列和第 `1` 列的值：
* 如果第 `0` 列的值为 `A`，则第 `2` 列的选项范围固定为 `1` 到 `5`。
* 如果第 `0` 列的值为 `B`，则第 `2` 列的选项还会进一步取决于第 `1` 列的值。

关于嵌套编辑器，需要注意以下几点：
* `options` 字典的键只能是字符串。
* 必须确保 `nested` 编辑器始终有可用的有效选项。
* 无法保证当前显示的值一定是有效选项（可能存在依赖关系变化导致的值失效）。

针对最后一点，你可以使用 `@edit`来修正或清空无效值。以下是一个清空无效值的示例：
```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnTabulator :value="nested_df.value" 
               :editors="tabulator_editors" 
               show_index
               @change='on_change'
               @edit='on_edit'
  />
</template>
<script lang='py'>
import pandas as pd
import datetime as dt
from bokeh.models.widgets.tables import CheckboxEditor, NumberEditor, SelectEditor
from vuepy import ref

options = {
    "A": ["A.1", "A.2", "A.3", "A.4", "A.5"],
    "B": {
        "1": ["B1.1", "B1.2", "B1.3"],
        "2": ["B2.1", "B2.2", "B2.3"],
        "3": ["B3.1", "B3.2", "B3.3"],
    },
}
tabulator_editors = {
    "0": {"type": "list", "values": ["A", "B"]},
    "1": {"type": "list", "values": [1, 2, 3]},
    "Nested Selection": {
        "type": "nested", 
        "options": options,
        "lookup_order": ["0", "1"],
    },
}

nested_df = ref(pd.DataFrame({
    "0": ["A", "B", "A"], 
    "1": [1, 2, 3], 
    "Nested Selection": [None, None, None],
}))

def on_change(event):
    print(event.new) #    0  1 Nested Selection
                     # 0  A  1              A.5
                     # 1  B  2             None
                     # 2  A  3             None

def on_edit(event):
    if event.column in ["0", "1"]:
        nested_table.patch({"2": [(event.row, None)]})
</script>

```

## 列布局

默认情况下，DataFrame 组件会根据内容自动调整列宽和表格大小，这对应参数 `layout="fit_data_table"` 的默认行为。此外，还支持其他布局模式，例如手动指定列宽、均分列宽或仅调整列尺寸。

### 手动设置列宽

如需手动设置列宽，只需为每列显式指定宽度：
```vue
<!-- --plugins vpanel --show-code -->
<template>
  <p> widths = {{  widths }}</p>
  <PnTabulator :value="df.value" :widths="widths" />

  <!-- declare a single width for all columns this way: -->
  <p> widths = {{ 130 }}</p>
  <PnTabulator :value="df.value" :widths="130" />

  <!-- use percentage widths: -->
  <p> widths = {{ percent_widths }}</p>
  <PnTabulator :value="df.value" :widths="percent_widths" 
               sizing_mode='stretch_width' />
</template>
<script lang='py'>
import pandas as pd
from vuepy import ref

df = ref(pd.DataFrame({
    'int': [1, 2, 3],
    'float': [3.14, 6.28, 9.42],
    'str': ['A', 'B', 'C']
}))

widths = {'int': 70, 'float': 100, 'str': 50}
percent_widths = {'index': '15%', 'int': '25%', 'float': '25%', 'str': '35%'}
</script>

```

### 自动调整列宽

通过 `layout` 参数自动调整列宽:
* fit_data_table（默认模式）：自动调整列宽并优化表格整体尺寸（最常用且推荐）：
* fit_data：根据列内容自动调整列宽（不拉伸表格整体宽度）。
* fit_data_stretch：在适应内容的同时，拉伸最后一列以填满可用空间。
* fit_data_fill：适应内容并填充空间，但不拉伸最后一列（其余列均分剩余宽度）。
* fit_columns：每列相同大小
```vue
<!-- --plugins vpanel --show-code -->
<template>
  <p>layout='fit_data_table'</p>
  <PnTabulator :value="df.value" layout='fit_data_table' />

  <p>layout='fit_data'</p>
  <PnTabulator :value="df.value" layout='fit_data' :width="400" />

  <p>layout='fit_data_stretch'</p>
  <PnTabulator :value="df.value" layout='fit_data_stretch' :width="400" />

  <p>layout='fit_data_fill'</p>
  <PnTabulator :value="df.value" layout='fit_data_fill' :width="400" />

  <p>layout='fit_columns'</p>
  <PnTabulator :value="df.value" layout='fit_columns' :width="350" />
</template>
<script lang='py'>
import pandas as pd
from vuepy import ref

df = ref(pd.DataFrame({
    'int': [1, 2, 3],
    'float': [3.14, 6.28, 9.42],
    'str': ['A', 'B', 'C']
}))
</script>

```

## 对齐方式
```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnTabulator 
    :value="df.value" 
    :header_align="'center'" 
    :text_align="{'int': 'center', 'float': 'left'}" 
    :widths="150" 
  />
</template>
<script lang='py'>
import pandas as pd
from vuepy import ref

df = ref(pd.DataFrame({
    'int': [1, 2, 3],
    'float': [3.14, 6.28, 9.42]
}))
</script>

```

## 样式设置

### 基本样式设置

根据表格内容或其他条件进行样式定制是一项非常重要的功能。幸运的是，`pandas` 提供了一个强大的 [styling APIiiii](https://pandas.pydata.org/pandas-docs/stable/user_guide/style.html)，可与 `Tabulator` 组件配合使用。具体来说，`Tabulator` 组件暴露了与 `pandas.DataFrame` 类似的 `.style` 属性，允许用户通过 `.apply` 和 `.applymap` 等方法应用自定义样式。详细指南可参考 [Pandas 官方文档](https://pandas.pydata.org/pandas-docs/stable/user_guide/style.html)。

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnTabulator :value="df.value" ref='styled' />
</template>
<script lang='py'>
import pandas as pd
import numpy as np
from vuepy import ref, onMounted

df = ref(pd.DataFrame(np.random.randn(4, 5), columns=list('ABCDE')))
styled = ref(None)

def color_negative_red(val):
    color = 'red' if val < 0 else 'black'
    return f'color: {color}'

def highlight_max(s):
    is_max = s == s.max()
    return ['background-color: yellow' if v else '' for v in is_max]

@onMounted
def set_style():
    tab = styled.value.unwrap()
    tab.style.map(color_negative_red).apply(highlight_max)
    # tab.value.iloc[0, 0] = 1
</script>

```

### 渐变样式设置

通过 `.text_gradient`（文本渐变）或 `.background_gradient`（背景渐变）方法，配合 [Matplotlib 配色方案](https://matplotlib.org/stable/gallery/color/colormap_reference.html)，可以为表格添加渐变效果：
```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnTabulator :value="df.value" ref='styled'/>
</template>
<script lang='py'>
import pandas as pd
import numpy as np
from vuepy import ref, onMounted

df = ref(pd.DataFrame(np.random.randn(4, 5), columns=list('ABCDE')))
styled = ref(None)

@onMounted
def set_style():
    tab = styled.value.unwrap()
    tab.style.text_gradient(cmap="RdYlGn", subset=["B", "C"])
    tab.style.background_gradient(cmap="RdYlGn", subset=["D", "E"])
    # tab.value.iloc[0, 0] = 1
</script>

```

## 主题

Tabulator 库内置了多种主题，这些主题以 CSS 样式表的形式定义。因此，更改一个表格的主题会影响页面上的所有表格。通常建议在类级别统一设置主题，例如：

完整的主题列表请参阅 [Tabulator 文档](http://tabulator.info/docs/4.9/theme)，默认提供的主题包括：

* 'simple'
* 'default'
* 'midnight'
* 'site'
* 'modern'
* 'bootstrap'
* 'bootstrap4'
* 'materialize'
* 'semantic-ui'
* 'bulma'


此外，您还可以按照 [官方说明](https://tabulator.info/docs/6.2/theme#framework) 添加自定义主题类。

```vue
<!-- --plugins vpanel --show-code -->
<template>
 <PnCol>
  <PnSelect :options='themes' v-model='theme.value' />
  <PnTabulator :value='df.value' :theme='theme.value'
               :theme_classes="['thead-dark', 'table-sm']" />
 </PnCol>
</template>
<script lang='py'>
import pandas as pd
from vuepy import ref

df = ref(pd.DataFrame({
    'int': [1, 2, 3],
    'float': [3.14, 6.28, 9.42]
}))

themes = [
    'simple',
    'default',
    'midnight',
    'site',
    'modern',
    'bootstrap',
    'bootstrap4',
    'materialize',
    'semantic-ui',
    'bulma',
]

theme = ref('simple')
</script>

```

### 更改字体大小

不同主题的字体大小可能有所不同。例如，“bootstrap”主题的字体大小为 13px，而“bootstrap5”主题的字体大小为 16px。以下是将主题“bootstrap5”的字体大小值覆盖为 10px 的一种方法。

```python
 <PnTabulator :stylesheets='[":host .tabulator {font-size: 10px;}"]' ...
```
## 选择/点击
```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnTabulator :value="df.value" :selection="[0, 2]" selectable="checkbox" />
</template>
<script lang='py'>
import pandas as pd
from vuepy import ref

df = ref(pd.DataFrame({
    'int': [1, 2, 3],
    'float': [3.14, 6.28, 9.42]
}))
</script>

```

## 冻结行列
### 冻结列
```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnTabulator :value="df.value" :frozen_columns="['int']" :width="200" />
</template>
<script lang='py'>
import pandas as pd
from vuepy import ref

df = ref(pd.DataFrame({
    'int': [1, 2, 3],
    'float': [3.14, 6.28, 9.42],
    'str': ['A', 'B', 'C']
}))
</script>

```

### 冻结行

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnTabulator :value="agg_df" :frozen_rows="[-2, -1]" :height="150" />
</template>
<script lang='py'>
import pandas as pd
from vuepy import ref

date_df = pd.DataFrame({
    'int': [1, 2, 3],
    'float': [3.14, 6.28, 9.42]
})
agg_df = pd.concat([
    date_df, 
    date_df.median().to_frame('Median').T, 
    date_df.mean().to_frame('Mean').T,
])
agg_df.index= agg_df.index.map(str)
</script>

```

## Row Content 行内容扩展
```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnTabulator :value="periodic_df" :height=350 
               layout='fit_columns' sizing_mode='stretch_width'
               :row_content='content_fn' :embed_content='True' />
</template>
<script lang='py'>
from vuepy import ref
import panel as pn
from bokeh.sampledata.periodic_table import elements

periodic_df = elements[['atomic number', 'name', 'atomic mass', 'metal', 'year discovered']].set_index('atomic number')
content_fn = lambda row: pn.pane.HTML(
    f'<p>{row["name"]}</p>',
    sizing_mode='stretch_width'
)

# periodic_table = pn.widgets.Tabulator(
#     periodic_df, height=350, layout='fit_columns', sizing_mode='stretch_width',
#     row_content=content_fn, embed_content=True
# )

# periodic_table
</script>

```

## Groupby 分组

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnTabulator :value="df.value" :groups="{'Group 1': ['A', 'B'], 'Group 2': ['C', 'D']}" />
</template>
<script lang='py'>
import pandas as pd
from vuepy import ref

df = ref(pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6],
    'C': [7, 8, 9],
    'D': [10, 11, 12]
}))
</script>

```

### 分层多级索引

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnTabulator :value="autompg_df" hierarchical  :height='200'
               :aggregators='{"origin": "mean", "yr": "mean"}'/>
</template>
<script lang='py'>
import pandas as pd
from bokeh.sampledata.autompg import autompg_clean as autompg_df

autompg_df = autompg_df.set_index(["origin", "yr", "mfr"])
</script>

```

## 分页

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnTabulator :value="df.value" pagination='remote' :page_size="3" />
</template>
<script lang='py'>
import pandas as pd
import numpy as np
from vuepy import ref

df = ref(pd.DataFrame({'A': np.random.rand(10000)}))
</script>

```

## 过滤

### 客户端过滤
```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnTabulator 
    :value="df.value" 
    :header_filters="{
      'int': {'type': 'number', 'placeholder': 'Enter number'},
      'str': {'type': 'input', 'placeholder': 'Enter string'}
    }" 
    :height="140" 
    :width="400" 
    layout="fit_columns" 
  />
</template>
<script lang='py'>
import pandas as pd
from vuepy import ref

df = ref(pd.DataFrame({
    'int': [1, 2, 3],
    'str': ['A', 'B', 'C']
}))
</script>

```

## 下载


```vue
<!-- --plugins vpanel --show-code -->
<template>
 <PnCol>
  <PnButton name='download' @click='on_click()'/>
  <PnTabulator :value="df.value" ref='tab'/>
 </PnCol>
</template>
<script lang='py'>
import pandas as pd
from vuepy import ref

df = ref(pd.DataFrame({
    'int': [1, 2, 3],
    'float': [3.14, 6.28, 9.42]
}))
tab = ref(None)

def on_click():
    if tab.value:
        tab.value.unwrap().download()
    
</script>

```

## 按钮

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnTabulator :value="df.value" :buttons="buttons" />
</template>
<script lang='py'>
import pandas as pd
from vuepy import ref

buttons = {
    'print': '<i class=\"fa fa-print\"></i>', 
    'check': '<i class=\"fa fa-check\"></i>',
}

df = ref(pd.DataFrame({
    'int': [1, 2, 3],
    'float': [3.14, 6.28, 9.42]
}))
</script>

```

## 流式数据

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnTabulator :value="df.value" layout='fit_columns' 
               :width='450' :height="200" ref='stream_tab' />
</template>
<script lang='py'>
import pandas as pd
import numpy as np
from vuepy import ref
import panel as pn

df = ref(pd.DataFrame(np.full((1, 5), 0), columns=list('ABCDE')))
stream_tab = ref(None)

count = 0

# In a real app, you would call this method periodically
def stream_data(follow=True):
    nonlocal count
    count += 1
    new_data = pd.DataFrame(np.full((1, 5), count), columns=list('ABCDE'))
    stream_tab.value.unwrap().stream(new_data, follow=follow)

pn.state.add_periodic_callback(stream_data, period=1000, count=4);
</script>

```

## 数据补丁

```vue
<!-- --plugins vpanel --show-code -->
<template>
 <PnCol>
  <PnButton name='Patch' @click='on_click()'/>
  <PnTabulator :value="df.value" ref='tab_ref'/>
 </PnCol>
</template>
<script lang='py'>
import pandas as pd
from vuepy import ref

df = ref(pd.DataFrame({
    'int': [1, 2, 3],
    'float': [3.14, 6.28, 9.42],
    'bool': [True, False, True]
}))

tab_ref = ref(None)

def patch_data():
    tab = tab_ref.value
    if not tab:
        return
    tab.unwrap().patch({
        'bool': [(0, False), (2, False)],
        'int': [(slice(0, 2), [3, 2])]
    })

def on_click():
    patch_data()
</script>

```

## 静态配置

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnTabulator 
    :value="df.value" 
    :configuration="{
      'clipboard': True,
      'rowHeight': 50,
      'columnDefaults': {
        'headerSort': False
      }
    }" 
  />
</template>
<script lang='py'>
import pandas as pd
from vuepy import ref

df = ref(pd.DataFrame({
    'int': [1, 2, 3],
    'float': [3.14, 6.28, 9.42]
}))
</script>

```

## API

### 属性
| 属性名               | 说明                                                                 | 类型                                                | 默认值            |
|----------------------|--------------------------------------------------------------------|---------------------------------------------------|------------------|
| aggregators          | 多级索引聚合配置（支持'min','max','mean','sum'）                      | ^[dict]                                           | {}               |
| buttons              | 表格按钮配置（列名到HTML内容的映射）                                   | ^[dict]                                           | {}               |
| configuration        | Tabulator原生配置选项                                                | ^[dict]                                           | {}               |
| editors              | 列编辑器配置（列名到编辑器实例的映射）                                  | ^[dict]                                           | {}               |
| embed_content        | 是否嵌入展开行内容                                                    | ^[bool]                                           | False            |
| expanded             | 当前展开的行索引列表                                                  | ^[list]                                           | []               |
| filters              | 客户端过滤器配置列表                                                  | ^[list]                                           | []               |
| formatters           | 列格式化器配置（列名到格式化器的映射）                                  | ^[dict]                                           | {}               |
| frozen_columns       | 固定列配置（列表或字典形式）                                            | ^[list\|dict]                                     | []               |
| frozen_rows          | 固定行索引列表                                                        | ^[list]                                           | []               |
| groupby              | 分组依据列名列表                                                      | ^[list]                                           | []               |
| header_align         | 表头对齐方式（'left','center','right'）                               | ^[dict\|str]                                      | 'left'           |
| header_filters       | 表头过滤器配置（布尔值或列配置字典）                                     | ^[bool\|dict]                                     | False            |
| header_tooltips      | 表头提示文本映射                                                      | ^[dict]                                           | {}               |
| hidden_columns       | 隐藏列名列表                                                          | ^[list]                                           | []               |
| hierarchical         | 是否启用多级索引分层显示                                                | ^[bool]                                           | False            |
| initial_page_size    | 初始每页行数（分页启用时）                                              | ^[int]                                            | 20               |
| layout               | 列布局模式（'fit_columns','fit_data'等）                              | ^[str]                                            | 'fit_data_table' |
| page                 | 当前页码（分页启用时）                                                 | ^[int]                                            | 1                |
| page_size            | 每页行数（None时自动计算）                                             | ^[int\|None]                                      | None             |
| pagination           | 分页模式（'local','remote'或None禁用）                                 | ^[str\|None]                                      | None             |
| row_content          | 行展开内容生成函数                                                     | ^[callable]                                       | None             |
| selection            | 当前选中行索引列表                                                     | ^[list]                                           | []               |
| selectable           | 选择模式配置（布尔/字符串/整数）                                         | ^[bool\|str\|int]                                 | True             |
| selectable_rows      | 可选行过滤函数                                                         | ^[callable]                                       | None             |
| show_index           | 是否显示索引列                                                         | ^[bool]                                           | True             |
| sortable             | 是否可排序（全局或按列配置）                                             | ^[bool\|dict]                                     | True             |
| sorters              | 排序器配置列表                                                         | ^[list]                                           | []               |
| text_align           | 文本对齐方式（'left','center','right'）                                | ^[dict\|str]                                      | 'left'           |
| theme                | CSS主题（'simple','bootstrap'等）                                     | ^[str]                                            | 'simple'         |
| theme_classes        | 额外CSS类列表                                                         | ^[list[str]]                                      | []               |
| title_formatters     | 标题格式化器配置                                                       | ^[dict]                                           | {}               |
| titles               | 列标题重写映射                                                         | ^[dict]                                           | {}               |
| value                | 显示的DataFrame数据                                                   | ^[pd.DataFrame]                                   | None             |
| widths               | 列宽度配置映射                                                         | ^[dict]                                           | {}               |
| disabled             | 是否禁用单元格编辑                                                     | ^[bool]                                           | False            |

### 计算属性

| 属性名            | 说明                                  | 类型                |
|-------------------|-------------------------------------|--------------------|
| | | |

### 事件

| 事件名    | 说明                          | 类型                     |
|----------|-----------------------------|------------------------|
| click | 单元格点击事件（含行列值信息）   | ^[CellClickEvent]      |
| edit  | 单元格编辑事件（含新旧值信息）    | ^[TableEditEvent]      |
| change | 数据更新事件   | ^[Event]      |

### 方法

| 方法名       | 说明                | 返回值类型  |
|-------------|-------------------|------------|
| download | 下载表格数据 | ^[Callable]`(filename: str, filetype: str) -> None` |
| patch | 更新数据表格 | ^[Callable]`(...) -> None` |



# DiscreteSlider 离散滑块

离散滑块组件允许使用滑块从离散列表或字典中选择值，提供了类似Select组件的选择功能，但使用滑块作为交互界面。

底层实现为`panel.widgets.DiscreteSlider`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/DiscreteSlider.html


## 基本用法

基本的离散滑块使用列表作为选项：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnDiscreteSlider name="数值列表" 
                   :options="[2, 4, 8, 16, 32, 64, 128]"
                   v-model="value.value"/>
  <p>当前值: {{ value.value }}</p>
</template>
<script lang='py'>
from vuepy import ref

value = ref(32)
</script>

```


## 使用字典作为选项

`options`参数也接受一个字典，其键将作为滑块上显示的文本标签：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnDiscreteSlider name="选择速度" 
                   :options="{'慢': 'slow', '中': 'medium', '快': 'fast'}"
                   :value="'medium'"
                   @change="update_value" />
  <p>当前速度: {{ value.value }}</p>
</template>
<script lang='py'>
from vuepy import ref

value = ref('medium')

def update_value(new_value):
    value.value = new_value.new
</script>

```


## 垂直方向

滑块可以设置为垂直方向显示：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnRow>
    <PnDiscreteSlider name="垂直滑块" 
                     orientation="vertical"
                     :options="[1, 2, 3, 4, 5]"
                     :value="3"
                     :height="200"
                     @change="update_value" />
  </PnRow>
  <div>当前值: {{ value.value }}</div>
</template>
<script lang='py'>
from vuepy import ref

value = ref(3)

def update_value(new_value):
    value.value = new_value
</script>

```


## 自定义样式

可以自定义滑块条的颜色和方向：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnDiscreteSlider name="蓝色滑块" 
                   bar_color="#3498db"
                   :options="['A', 'B', 'C', 'D', 'E']"
                   v-model="value1.value"/>
  <PnDiscreteSlider name="从右到左" 
                   direction="rtl"
                   :options="['A', 'B', 'C', 'D', 'E']"
                   v-model="value2.value"/>
  <div>蓝色滑块值: {{ value1.value }}</div>
  <div>从右到左滑块值: {{ value2.value }}</div>
</template>
<script lang='py'>
from vuepy import ref

value1 = ref('C')
value2 = ref('C')

</script>

```


## API

### 属性

| 属性名          | 说明                           | 类型                                | 默认值        |
| -------------- | ------------------------------ | ---------------------------------- | ------------ |
| options        | 选项列表或字典                  | ^[list\|dict]                      | []           |
| value          | 当前选中的值                    | ^[Any]                             | None         |
| value_throttled| 鼠标释放前阻止的值              | ^[Any]                             | None         |
| bar_color      | 滑块条的颜色，十六进制RGB值      | ^[str]                             | None         |
| direction      | 滑块方向，从左到右('ltr')或从右到左('rtl') | ^[str]               | 'ltr'        |
| disabled       | 是否禁用                       | ^[bool]                            | False        |
| name           | 组件标题                       | ^[str]                             | ""           |
| orientation    | 滑块的显示方向，'horizontal'或'vertical' | ^[str]                 | 'horizontal' |
| tooltips       | 是否在滑块手柄上显示工具提示     | ^[bool]                            | True         |

### Events

| 事件名         | 说明                       | 类型                                   |
| ------------- | -------------------------- | -------------------------------------- |
| change        | 当值更改时触发的事件         | ^[Callable]`(value) -> None`          |




# PasswordInput 密码输入框

密码输入框组件是一个专用于输入密码的文本输入框，会将输入的字符显示为掩码以保护隐私。

底层实现为`panel.widgets.PasswordInput`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/PasswordInput.html


## 基本用法

基本的密码输入框使用： 可以通过设置`v-mode`/`value`参数为密码输入框设置默认值：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnPasswordInput name="password" 
                  placeholder="input password"
                  description="tooltip"
                  v-model="pw.value" />
</template>
<script lang='py'>
from vuepy import ref

pw = ref('')
</script>

```


## API

### 属性

| 属性名            | 说明                    | 类型        | 默认值    |
| ---------------- | ---------------------- | ----------- | --------- |
| value            | 当前输入的密码           | ^[str]      | ""        |
| placeholder      | 输入框占位文本           | ^[str]      | ""        |
| name             | 组件标题                | ^[str]      | ""        |
| description      | 鼠标悬停时显示的描述      | ^[str]      | ""        |

### Events

| 事件名  | 说明                | 类型                          |
| ------ | ------------------ | ----------------------------- |
| change | 当密码更改时触发的事件 | ^[Callable]`(value) -> None` |




# TextEditor 文本编辑器

文本编辑器组件允许用户编辑和显示格式化文本，支持多种格式，包括Markdown和HTML。

底层实现为`panel.widgets.TextEditor`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/TextEditor.html



## 基本用法

基本的文本编辑器使用：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnTextEditor name="基本编辑器" 
               v-model="content.value"/>
  <p>当前内容: {{ content.value }}</p>
</template>
<script lang='py'>
from vuepy import ref

content = ref("这是一个文本编辑器示例")
</script>

```


## 工具栏布局

可以设置工具栏的位置和是否显示：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnRow>
    <PnTextEditor name="基础文本格式" 
                 value="Flat list of options" 
                 :toolbar="['bold', 'italic', 'underline']" />
    
    <PnTextEditor name="分组工具栏" 
                 value="Grouped options" 
                 :toolbar="[['bold', 'italic'], ['link', 'image']]" />
    
    <PnTextEditor name="字体大小" 
                 value="Dropdown of options" 
                 :toolbar="[{'size': ['small', False, 'large', 'huge']}]" />
  </PnRow>
  
  <PnTextEditor name="完整功能编辑器" 
               value="Full configuration" 
               :toolbar="[
                 ['bold', 'italic', 'underline', 'strike'],
                 ['blockquote', 'code-block'],
                 [{ 'header': 1 }, { 'header': 2 }],
                 [{ 'list': 'ordered'}, { 'list': 'bullet' }],
                 [{ 'script': 'sub'}, { 'script': 'super' }],
                 [{ 'indent': '-1'}, { 'indent': '+1' }],
                 [{ 'direction': 'rtl' }],
                 [{ 'size': ['small', False, 'large', 'huge'] }],
                 [{ 'header': [1, 2, 3, 4, 5, 6, False] }],
                 [{ 'color': [] }, { 'background': [] }],
                 [{ 'font': [] }],
                 [{ 'align': [] }],
                 ['clean']
               ]" />
</template>
<script lang='py'>
import panel as pn

pn.config.sizing_mode = 'stretch_width'
</script>

```


## API

### 属性

| 属性名        | 说明                                                                 | 类型                          | 默认值      |
|-------------|--------------------------------------------------------------------|-----------------------------|------------|
| disabled    | 是否禁用编辑器                                                      | ^[bool]                     | False      |
| mode        | 菜单显示模式（'toolbar'-工具栏模式 / 'bubble'-气泡模式）              | ^[str]                      | 'toolbar'  |
| placeholder | 编辑器为空时显示的占位内容                                           | ^[str]                      | ""         |
| toolbar     | 工具栏配置（true/false 开关或详细配置列表）                           | ^[bool] or ^[list]          | True       |
| value       | 组件当前的HTML输出内容                                               | ^[str]                      | ""         |

* 'toolbar'模式下显示顶部工具栏菜单
* 'bubble'模式下显示浮动上下文菜单

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |
| change | 当文本内容变化时触发的事件 | ^[Callable]`(event: dict) -> None` |




# MultiSelect 多选框

多选框组件允许从下拉菜单中选择多个选项。它与Select组件类似，但支持多选功能。

底层实现为`panel.widgets.MultiSelect`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/MultiSelect.html


## 基本用法

基本的多选框使用：


```vue
<!-- --plugins vpanel --show-code -->
<template>
 <PnCol :height='150'>
  <PnMultiSelect name="Fruit" 
                :options="['Apple', 'Orange', 'Pear']"
                v-model="selected.value" />
 </PnCol>
 <p>value: {{ selected.value }}</p>
</template>
<script lang='py'>
from vuepy import ref

selected = ref([])
</script>

```


## 使用字典作为选项

`options`参数也接受一个字典，其键将作为下拉菜单的标签：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnMultiSelect name="Code" 
                :options="{'Python': 'py', 'JavaScript': 'js', 'Java': 'java', 'C++': 'cpp'}"
                :value="['py', 'js']"
                @change="update_value" />
  <div>value: {{ selected.value }}</div>
</template>
<script lang='py'>
from vuepy import ref

selected = ref(['py', 'js'])

def update_value(new_value):
    selected.value = new_value
</script>

```


## 选择区域大小

可以通过`size`参数控制选择区域显示的选项数量：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnMultiSelect name="3 items" 
                :options="['opt1', 'opt2', 'opt3', 'opt4']"
                :size="3"
                @change="update_value" />
  <PnMultiSelect name="all" 
                :options="['opt1', 'opt2', 'opt3', 'opt4', 'opt5']"
                :size="6"
                @change="update_value2" />
</template>
<script lang='py'>
from vuepy import ref

selected1 = ref([])
selected2 = ref([])

def update_value(new_value):
    selected1.value = new_value.new
    
def update_value2(new_value):
    selected2.value = new_value.new
</script>

```


## API

### 属性

| 属性名            | 说明                   | 类型                  | 默认值    |
| ---------------- | --------------------- | -------------------- | --------- |
| options          | 选项列表或字典          | ^[list, dict]        | []        |
| size             | 同时显示的选项数量      | ^[int]               | 4         |
| value            | 当前选择的值列表        | ^[list]              | []        |
| disabled         | 是否禁用组件           | ^[bool]              | False     |
| name             | 组件标题              | ^[str]               | ""        |
| description      | 鼠标悬停时显示的描述    | ^[str]               | ""        |

### Events

| 事件名  | 说明                | 类型                           |
| ------ | ------------------ | ------------------------------ |
| change | 当选择改变时触发的事件 | ^[Callable]`(value) -> None`  |




# LiteralInput 字面量输入框

字面量输入框组件允许用户输入任意Python字面量（包括int、float、list、dict等）并将其解析为相应的Python对象。

底层实现为`panel.widgets.LiteralInput`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/LiteralInput.html


## 基本用法

基本的字面量输入框使用：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnLiteralInput name="字符串输入" 
                 v-model="input_value.value"/>
  <p>value: {{ input_value.value }}</p>
</template>
<script lang='py'>
from vuepy import ref

input_value = ref("Hello, World!")
</script>

```


## 不同类型的值

字面量输入框可以处理各种Python数据类型：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnLiteralInput name="int" 
                 :value="42" />
  <PnLiteralInput name="float" 
                 :value="3.14159" />
  <PnLiteralInput name="list" 
                 :value="[1, 2, 3, 4]" />
  <PnLiteralInput name="dict" 
                 :value="{'name': 'far', 'age': 30}" />
</template>
<script lang='py'>
from vuepy import ref
</script>

```


## 指定类型

可以使用type参数指定输入的数据类型：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnLiteralInput name="type int" 
                 :value="42"
                 :type="int" />
  <PnLiteralInput name="type list" 
                 :value="[1, 2, 3]"
                 :type="list" />
</template>
<script lang='py'>
from vuepy import ref
</script>

```


## 自定义高度

可以设置输入框的高度，特别是对于复杂类型很有用：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnLiteralInput name="多行输入" 
                 :value="nested_dict"
                 :height="150" />
</template>
<script lang='py'>
from vuepy import ref

nested_dict = {
    "users": {
        "user1": {
            "name": "far",
            "age": 30,
            "hobbies": ["xx", "yy"]
        },
    }
}
</script>

```


## API

### 属性

| 属性名    | 说明                 | 类型                                             | 默认值 |
| -------- | ------------------- | ------------------------------------------------ | ------- |
| value    | 指示类型的解析值 | ^[object]                                        | None    |
| type     | 限制数据类型         | ^[type\|None] 如int、float、str、list、dict等    | None    |
| height   | 输入框高度           | ^[int\|str]                                      | None    |
| width    | 输入框宽度           | ^[int\|str]                                      | None    |
| disabled | 是否禁用组件         | ^[bool]                                          | False   |
| name     | 组件标题             | ^[str]                                           | ""      |

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |
| change | 当输入值变化时触发的事件 | ^[Callable]`(event: dict) -> None` |




# Button 按钮

常用的操作按钮。

按钮组件可以在被点击时触发事件。除了在处理点击事件期间会从`False`切换到`True`的`value`参数外，还有一个额外的`clicks`参数，可以被监听以订阅点击事件。

底层实现为`panel.widgets.Button`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/Button.html


## 基本用法

基本的按钮使用，点击时触发事件：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnButton button_type="primary" @click="update_clicks()">
    click: {{ clicks.value }} 
  </PnButton>
</template>
<script lang='py'>
from vuepy import ref

clicks = ref(0)

def update_clicks():
    clicks.value += 1
</script>

```

## 按钮样式

按钮的颜色可以通过设置`button_type`来改变，而`button_style`可以是`'solid'`或`'outline'`：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnRow>
    <PnCol v-for="style in ['solid', 'outline']">
      <PnButton v-for="type in button_types" 
                :name="type" 
                :button_type="type" 
                :button_style="style" 
                style="margin: 5px" />
    </PnCol>
  </PnRow>
</template>
<script lang='py'>
from vuepy import ref

button_types = ['default', 'primary', 'success', 'warning', 'danger', 'light']
</script>

```


## 图标按钮

Button 组件可以添加图标，支持 Unicode、Emoji 字符，以及 [tabler-icons.io](https://tabler-icons.io) 的命名图标或自定义 SVG：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <!-- emoji -->
  <PnButton name="🔍" :width="100" />
  <PnButton :width="100">💾 Save</PnButton>
  <PnButton name="Copy ✂️" :width="100" />
  
  <!-- tabler-icons -->
  <PnButton icon="alert-triangle" />
  <PnButton icon="bug" />

  <!-- svg -->
  <PnButton name='svg icon'>
    <template #icon>
      <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-cash" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
        <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
        <path d="M7 9m0 2a2 2 0 0 1 2 -2h10a2 2 0 0 1 2 2v6a2 2 0 0 1 -2 2h-10a2 2 0 0 1 -2 -2z" />
        <path d="M14 14m-2 0a2 2 0 1 0 4 0a2 2 0 1 0 -4 0" />
        <path d="M17 9v-2a2 2 0 0 0 -2 -2h-10a2 2 0 0 0 -2 2v6a2 2 0 0 0 2 2h2" />
      </svg>
    </template>
  </PnButton>
</template>
<script lang='py'>
from vuepy import ref

cash_icon = """
<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-cash" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
  <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
  <path d="M7 9m0 2a2 2 0 0 1 2 -2h10a2 2 0 0 1 2 2v6a2 2 0 0 1 -2 2h-10a2 2 0 0 1 -2 -2z" />
  <path d="M14 14m-2 0a2 2 0 1 0 4 0a2 2 0 1 0 -4 0" />
  <path d="M17 9v-2a2 2 0 0 0 -2 -2h-10a2 2 0 0 0 -2 2v6a2 2 0 0 0 2 2h2" />
</svg>
"""
</script>

```

## 加载状态按钮

通过设置 loading 属性为 true 来显示加载中状态。  
```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnButton loading>Loading</PnButton>
  <PnButton @click="click1">Click to Loading</PnButton>
</template>
<script lang="py">
from vuepy import ref

def click1(ev):
    btn = ev.obj
    btn.loading = not btn.loading
</script>

```

## 自定义 css style

通过`style`设置组件外层DOM节点(意味着无法设置某些组件内的样式，如background-color，font-size等)的CSS样式:
* `width`、`height` 设置组件的高和宽
* `border` 设置组件的边框
* ...
```vue
<!-- --plugins vpanel --show-code -->
<template>
  <HBox>
    <PnButton name="height 60px" style="height: 60px" />
    <PnButton name="width 90px" style="width: 90px" />
    <PnButton name="border: 5px solid red;" style="border: 5px solid #FAEBD7;" />
  </HBox>
</template>

```


## API

### 属性

| 属性名         | 说明                    | 类型                                | 默认值     |
| ------------- | ----------------------- | ---------------------------------- | --------- |
| button_style  | 按钮样式                | ^[str]`'solid','outline'`          | 'solid'   |
| button_type   | 按钮主题                | ^[str]`'default'、'primary'、'success'、'info'、'light'、'danger'` | 'default' |
| clicks        | 点击次数                | ^[int]                             | 0         |
| disabled      | 是否禁用                | ^[bool]                            | False     |
| icon          | 按钮图标(SVG字符串或tabler-icons.io图标名称)               | ^[str] | None     |
| icon_size     | 图标大小(如"12px"或"1em")                | ^[str]              | None      |
| name          | 按钮标题/文本           | ^[str]                             | ""        |
| value         | 按钮值，处理点击事件时切换 | ^[bool]                          | False     |
| description   | 鼠标悬停时显示的描述     | ^[str]                             | ""        |

### Events

| 事件名  | 说明                | 类型                        |
| ------ | ------------------ | --------------------------- |
| click  | 当按钮被点击时触发的事件 | ^[Callable]`(Event) -> None`    |

### Slots

| 插槽名   | 说明               |
| ------- | ----------------- |
|    default     |          按钮文字        |
|    icon |          svg 图标 |




# SpeechToText 语音转文本

SpeechToText组件通过封装[HTML5 `SpeechRecognition` API](https://developer.mozilla.org/en-US/docs/Web/API/SpeechRecognition)控制浏览器的语音识别服务。

底层实现为`panel.widgets.SpeechToText`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/SpeechToText.html


## 基本用法

语音转文本组件提供了一个简单的界面来启动和停止语音识别服务，将用户的语音转换为文本。

> **注意**：此功能是**实验性的**，**只有Chrome和少数其他浏览器支持**。有关支持SpeechRecognition API的浏览器的最新列表，请参见[caniuse.com](https://caniuse.com/speech-recognition)或[MDN文档](https://developer.mozilla.org/en-US/docs/Web/API/SpeechRecognition#Browser_compatibility)。在某些浏览器（如Chrome）中，即使支持此功能，`grammars`、`interim_results`和`max_alternatives`参数也可能尚未实现。
> 
> 在像Chrome这样的浏览器上，在网页上使用语音识别涉及基于服务器的识别引擎。**您的音频会被发送到网络服务进行识别处理，因此它无法离线工作**。这对您的用例来说是否足够安全和保密，需要您自行评估。

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnSpeechToText 
    button_type="light"
    v-model="speech_text.value"
  />
  <PnStaticText :value="f'result: {speech_text.value}'" />
</template>
<script lang='py'>
import panel as pn
from vuepy import ref

speech_text = ref("")
</script>

```


## 自定义按钮

可以通过设置`button_type`、`button_not_started`和`button_started`参数来自定义按钮的外观。

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnRow>
    <PnSpeechToText 
      button_type="success" 
      button_not_started="点击开始识别" 
      button_started="点击停止识别"
      v-model="custom_text.value"
    />
    <PnStaticText :value="f'识别结果: {custom_text.value}'" />
  </PnRow>
</template>
<script lang='py'>
import panel as pn
from vuepy import ref

custom_text = ref("")
</script>

```


## 连续识别

通过设置`continuous=True`，语音识别服务会保持打开状态，允许您连续说多个语句。

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnSpeechToText 
    button_type="warning" 
    :continuous="True"
    v-model="continuous_text.value"
  />
  <PnStaticText :value="f'连续识别结果: {continuous_text.value}'" />
</template>
<script lang='py'>
import panel as pn
from vuepy import ref

continuous_text = ref("")
</script>

```


## 使用语法列表

可以使用`GrammarList`限制识别服务识别的单词或单词模式。

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnCol>
    <PnStaticText value="尝试说出一种颜色（英文）如red, blue, green等" />
    <PnSpeechToText 
      button_type="primary" 
      :grammars="grammar_list"
      v-model="grammar_text.value"
    />
    <PnStaticText :value="f'识别结果: {grammar_text.value}'" />
  </PnCol>
</template>
<script lang='py'>
import panel as pn
from panel.widgets import GrammarList
from vuepy import ref

# 创建语法列表
grammar_list = GrammarList()
color_grammar = "#JSGF V1.0; grammar colors; public <color> = red | green | blue | yellow | purple | orange | black | white | pink | brown;"
grammar_list.add_from_string(color_grammar, 1)

grammar_text = ref("")
</script>

```


## 显示详细结果

可以通过`results`属性获取更详细的结果，包括置信度级别。

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnCol>
    <PnSpeechToText 
      button_type="danger" 
      v-model="detailed_text.value"
      @change="update_results"
    />
  </PnCol>
  <PnHTML :object="results_html.value" />
</template>
<script lang='py'>
import panel as pn
from vuepy import ref

detailed_text = ref("")
results_html = ref("")

def update_results(event):
    # 通过引用获取SpeechToText组件实例
    speech_component = event.owner
    # 获取格式化的HTML结果
    results_html.value = speech_component.results_as_html
</script>

```


## API

### 属性

| 属性名 | 说明 | 类型 | 默认值 |
| -------- | ------------------- | ---------------------------------------------------------------| ------- |
| results | 识别的结果，字典列表 | ^[List[Dict]] | [] |
| value | 最近的语音识别结果字符串 | ^[str] | "" |
| lang | 当前语音识别服务的语言（BCP 47格式） | ^[str] | 'en-US' |
| continuous | 是否返回每次识别的连续结果，或仅返回单个结果 | ^[boolean] | false |
| interim_results | 是否应返回临时结果 | ^[boolean] | false |
| max_alternatives | 每个结果提供的最大识别替代方案数量 | ^[int] | 1 |
| service_uri | 指定当前语音识别服务使用的语音识别服务位置 | ^[str] | — |
| grammars | 表示当前语音识别服务将理解的语法的GrammarList对象 | ^[GrammarList] | None |
| started | 语音识别服务是否已启动 | ^[boolean] | false |
| audio_started | 音频是否已启动 | ^[boolean] | false |
| sound_started | 声音是否已启动 | ^[boolean] | false |
| speech_started | 用户是否已开始说话 | ^[boolean] | false |
| button_hide | 是否隐藏切换开始/停止按钮 | ^[boolean] | false |
| button_type | 按钮类型 | ^[str] | 'default' |
| button_not_started | 语音识别服务未启动时按钮上显示的文本 | ^[str] | '' |
| button_started | 语音识别服务启动时按钮上显示的文本 | ^[str] | '' |

### Events

| 事件名 | 说明 | 类型 |
| --- | --- | --- |
| change | 当识别结果改变时触发 | ^[Callable]`(event: dict) -> None` |

### 方法

| 属性名 | 说明 | 类型 |
| --- | --- | --- |
| results_deserialized | 获取识别的结果，RecognitionResult对象列表 | ^[property] |
| results_as_html | 获取格式化为HTML的结果 | ^[property] |




# DatetimeRangeSlider 日期时间范围滑块

DatetimeRangeSlider组件允许用户通过带有两个手柄的滑块选择日期时间范围。

底层实现为`panel.widgets.DatetimeRangeSlider`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/DatetimeRangeSlider.html


## 基本用法

日期时间范围滑块提供了一种交互式方式来选择日期时间范围。用户可以通过拖动手柄调整范围的起始和结束时间，也可以通过拖动已选择的范围整体移动。

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnDatetimeRangeSlider 
    name="日期时间范围滑块" 
    :start="dt.datetime(2017, 1, 1)" 
    :end="dt.datetime(2019, 1, 1)" 
    :step="10000"
    v-model="selected_range.value"
  />
</template>
<script lang='py'>
import datetime as dt
from vuepy import ref

selected_range = ref((dt.datetime(2017, 1, 1), dt.datetime(2018, 1, 10)))
</script>

```


## 自定义格式

可以通过format参数自定义日期时间的显示格式。

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnDatetimeRangeSlider 
    name="自定义格式" 
    :start="dt.datetime(2017, 1, 1)" 
    :end="dt.datetime(2019, 1, 1)" 
    :step="10000"
    format="%Y-%m-%dT%H:%M:%S"
    v-model="custom_format_range.value"
  />
</template>
<script lang='py'>
import datetime as dt
from vuepy import ref

custom_format_range = ref((dt.datetime(2017, 1, 1), dt.datetime(2018, 1, 10)))
</script>

```


## 自定义样式

通过设置bar_color和orientation等属性可以自定义滑块样式。

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnDatetimeRangeSlider 
    name="水平滑块" 
    :start="dt.datetime(2017, 1, 1)" 
    :end="dt.datetime(2019, 1, 1)" 
    bar_color="#ff5722"
    tooltips
    v-model="horizontal_range.value"
  />
  
  <PnDatetimeRangeSlider 
    name="垂直滑块" 
    :start="dt.datetime(2017, 1, 1)" 
    :end="dt.datetime(2019, 1, 1)" 
    orientation="vertical"
    bar_color="#2196f3"
    tooltips
    v-model="vertical_range.value"
  />
</template>
<script lang='py'>
import datetime as dt
from vuepy import ref

horizontal_range = ref((dt.datetime(2017, 1, 1), dt.datetime(2018, 1, 10)))
vertical_range = ref((dt.datetime(2017, 3, 15), dt.datetime(2018, 6, 10)))
</script>

```


## API

### 属性

| 属性名 | 说明 | 类型 | 默认值 |
| -------- | ------------------- | ---------------------------------------------------------------| ------- |
| start | 日期时间范围的下限 | ^[datetime] | — |
| end | 日期时间范围的上限 | ^[datetime] | — |
| step | 步长，以毫秒为单位，默认为1分钟(60,000毫秒) | ^[int] | 60000 |
| value | 所选范围的上下限，表示为日期时间类型的元组 | ^[tuple] | — |
| bar_color | 滑块条的颜色，十六进制RGB值 | ^[string] | — |
| direction | 滑块方向，从左到右('ltr')或从右到左('rtl') | ^[string] | 'ltr' |
| disabled | 是否禁用 | ^[boolean] | false |
| format | 应用于滑块值的格式化字符串 | ^[string] | — |
| name | 组件标题 | ^[string] | — |
| orientation | 滑块方向，水平('horizontal')或垂直('vertical') | ^[string] | 'horizontal' |
| tooltips | 是否在滑块手柄上显示提示 | ^[boolean] | false |

### Events

| 事件名 | 说明 | 类型 |
| --- | --- | --- |
| change | 当选择改变时触发 | ^[Callable]`(event: dict) -> None` |




# ColorMap 色彩映射选择器

ColorMap组件允许从包含色彩映射的字典中选择一个值。该组件类似于Select选择器，但只允许选择有效的色彩映射，即十六进制值列表、命名颜色或matplotlib色彩映射。

底层实现为`panel.widgets.ColorMap`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/ColorMap.html


## 基本用法

色彩映射选择器可以提供色彩映射选项让用户进行选择，选项必须是一个包含色彩列表的字典。

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <p>选择的色彩映射: {{selected_map.value}}</p>
  <PnRow :height='200'>
    <PnColorMap 
      :options="cmaps" 
      value_name="Reds" 
      style="width: 200px;"
      v-model="selected_map.value"
      @change="on_change"
    />
  </PnRow>
</template>
<script lang='py'>
from vuepy import ref

cmaps = {
    'Reds': ['lightpink', 'red', 'darkred'],
    'Blues': ['rgba(0, 0, 255, 1)', 'rgba(0, 0, 170, 1)', 'rgba(0, 0, 85, 1)'],
    'Greens': ['#00ff00', '#00aa00', '#004400'],
}

selected_map = ref(['lightpink', 'red', 'darkred'])

def on_change(event):
    print(f"{event.new}") # ['#00ff00', '#00aa00', '#004400']
</script>

```

## 自定义布局

可以通过设置`ncols`参数以及`swatch_width`和`swatch_height`选项来控制色彩映射的显示方式。

```vue
<!-- --plugins vpanel --show-code -->
<template>
 <PnCol :height='300'>
  <PnColorMap 
    :options="cc_palette" 
    :ncols="3" 
    :swatch_width="100"
    v-model="selected_palette.value"
  />
 </PnCol>
</template>
<script lang='py'>
from vuepy import ref
import colorcet as cc

cc_palette = cc.palette
selected_palette = ref(cc.b_circle_mgbm_67_c31)
</script>

```


## Matplotlib支持

组件也支持matplotlib色彩映射：

```vue
<!-- --plugins vpanel --show-code -->
<template>
 <PnCol :height='200'>
  <PnColorMap 
    :options="mpl_maps" 
    v-model="selected_mpl.value"
  />
</PnCol>
</template>
<script lang='py'>
from vuepy import ref
from matplotlib.cm import Reds, Blues, Greens

mpl_maps = {'Reds': Reds, 'Blues': Blues, 'Greens': Greens}
selected_mpl = ref(Reds)
</script>

```


## API

### 属性

| 属性名 | 说明 | 类型 | 默认值 |
| -------- | ------------------- | ---------------------------------------------------------------| ------- |
| options | 色彩映射选项，必须是一个包含色彩列表的字典 | ^[dict] | — |
| ncols | 列数 | ^[int] | 1 |
| swatch_height | 色彩样本高度 | ^[int] | 20 |
| swatch_width | 色彩样本宽度 | ^[int] | 100 |
| value | 当前选中的值 | ^[list[str]] | — |
| value_name | 选定的色彩映射名称 | ^[str] | — |
| disabled | 是否禁用 | ^[boolean] | false |
| name | 组件标题 | ^[str] | — |

### Events

| 事件名 | 说明 | 类型 |
| --- | --- | --- |
| change | 当选择改变时触发 | ^[Callable]`(event: dict) -> None` |



# JSONEditor JSON编辑器

JSONEditor组件提供了一个可视化编辑器，用于编辑JSON可序列化的数据结构，如Python字典和列表，具有不同编辑模式、插入对象和使用JSON Schema进行验证的功能。

底层实现为`panel.widgets.JSONEditor`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/JSONEditor.html


## 基本用法

JSON编辑器提供了一个直观的界面来查看和编辑JSON数据。

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnJSONEditor 
    :width="400"
    v-model="json_data.value"
    @change="on_change"
    ref='e'
  />
  <p> {{ json_data.value }} </p>
</template>
<script lang='py'>
# import panel as pn
# pn.extension('ace', 'jsoneditor')
from vuepy import ref, onMounted
import os

e = ref(None)
# os.environ['PANEL_NPM_CDN'] = 'https://cdn.jsdelivr.net/npm'
# print('cdn', os.environ.get('PANEL_NPM_CDN'))

json_data = ref({
    'dict'  : {'key': 'value'},
    'float' : 3.14,
    'int'   : 1,
    'list'  : [1, 2, 3],
    'string': 'A string',
})

@onMounted
def on():
    # print(type(e.value.unwrap()._widget_type))
    pass

def on_change(event):
    print(event.new)
</script>

```


## 编辑模式

JSON编辑器有多种模式，提供不同的查看和编辑`JSONEditor.value`的方式。注意，要启用对`mode='code'`的支持，必须使用`pn.extension('ace')`加载ace编辑器。

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnCol>
    <PnStaticText value="tree 树形模式" />
    <PnJSONEditor :value="json_data" mode='tree' :width='300' />
  </PnCol>
  
  <PnCol>
    <PnStaticText value="form 表单模式" />
    <PnJSONEditor :value="json_data" mode='form' :width="300" />
  </PnCol>
 
  <PnCol>
    <PnStaticText value="text 文本模式" />
    <PnJSONEditor :value="json_data" mode='text' :width="300" />
  </PnCol>
  
  <PnCol>
    <PnStaticText value="preview 预览模式" />
    <PnJSONEditor :value="json_data" mode='preview' :width="300" />
  </PnCol>
  
  <PnCol>
    <PnStaticText value="view 查看模式" />
    <PnJSONEditor :value="json_data" mode='view' :width="300" />
  </PnCol>
</template>
<script lang='py'>
import panel as pn
from vuepy import ref

json_data = {
    'dict'  : {'key': 'value'},
    'float' : 3.14,
    'int'   : 1,
    'list'  : [1, 2, 3],
    'string': 'A string',
}
</script>

```


## 验证

JSONEditor通过提供JSON Schema可以对`value`进行验证。JSON Schema描述了JSON对象必须具有的结构，如必需的属性或值必须具有的类型。更多信息请参见 http://json-schema.org/。

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnJSONEditor 
    :schema="schema" 
    :value="person_data"
    :height="500"
    :width="400"
  />
</template>
<script lang='py'>
import panel as pn
from vuepy import ref

# 需要初始化jsoneditor扩展
pn.extension('ace', 'jsoneditor')

schema = {
    "title": "Person",
    "type": "object",
    "properties": {
        "firstName": {
            "type": "string",
            "description": "The person's first name."
        },
        "lastName": {
            "type": "string",
            "description": "The person's last name."
        },
        "age": {
            "description": "Age in years which must be equal to or greater than zero.",
            "type": "integer",
            "minimum": 0
        }
    }
}

person_data = {
    'firstName': 2,  # 这将引发验证错误，因为应该是字符串
    'lastName': 'Smith',
    'age': 13.5  # 这将引发验证错误，因为应该是整数
}
</script>

```


## API

### 属性

| 属性名        | 说明                                                                 | 类型                          | 默认值  |
|-------------|--------------------------------------------------------------------|-----------------------------|--------|
| disabled    | 是否禁用编辑器（等同于设置 mode='view'）                               | ^[bool]                     | False  |
| menu        | 是否显示主菜单栏（包含格式、排序、转换、搜索等功能）                        | ^[bool]                     | True   |
| mode        | 编辑器模式：'view'(只读)、'form'(仅值可修改)、'tree'(树)、'text'(纯文本)、'preview'(预览大文件) | ^[str]                      | 'tree' |
| search      | 是否在右上角显示搜索框（仅在 tree/view/form 模式下可用）                   | ^[bool]                     | True   |
| schema      | 用于验证JSON数据的JSON模式（定义必需属性和值类型等）                       | ^[dict]                     | None   |
| value       | 当前可编辑的JSON数据结构                                               | ^[str]                      | ""     |

### Events

| 事件名 | 说明 | 类型 |
| --- | --- | --- |
| change | 当JSON数据改变时触发 | ^[Callable]`(event: dict) -> None` |




# Debugger 调试器

Debugger是一个不可编辑的Card布局组件，可以在前端显示仪表板运行时可能触发的日志和错误。

底层实现为`panel.widgets.Debugger`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/Debugger.html


## 基本用法

调试器可以在应用程序运行时显示日志和错误信息，对于在前端跟踪和调试问题非常有用。如果未指定logger_names，则必须使用`panel`记录器或自定义子记录器（例如`panel.myapp`）记录事件。

注意：调试器基于terminal组件，需要调用`pn.extension('terminal')`。

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnRow>
    <PnDebugger name="我的调试器" />
  </PnRow>
</template>
<script lang='py'>
import panel as pn
# 需要初始化terminal扩展
pn.extension('terminal', console_output='disable')
</script>

```


## 错误捕获

调试器可以捕获和显示应用程序中发生的错误，帮助用户了解交互过程中遇到的问题。

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnCol>
    <PnRadioButtonGroup 
      name="触发错误" 
      value="no error" 
      :options="['ZeroDivision', 'no error', 'Custom error']" 
      button_type="danger" 
      v-model="error_type.value"
      @change="throw_error"
    />
    <PnDebugger name="错误调试器" />
  </PnCol>
</template>
<script lang='py'>
import panel as pn
from vuepy import ref

# 需要初始化terminal扩展
pn.extension('terminal', console_output='disable')

error_type = ref('no error')

def throw_error(event):
    if event['new'] == 'ZeroDivision':
        try:
            1/0
        except Exception as e:
            raise e
    elif event['new'] == 'Custom error':
        raise Exception('自定义错误示例')
</script>

```


## 日志级别

通过设置不同的日志级别，可以控制显示哪些级别的日志信息。

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnCol sizing_mode="stretch_both">
    <PnRadioButtonGroup 
      name="显示信息" 
      :options="['debug', 'info', 'warning']" 
      v-model="info_type.value"
      @change="log_message"
    />
    <PnDebugger 
      name="信息级别调试器" 
      :level="logging.INFO" 
      sizing_mode="stretch_both"
      :logger_names="['panel.myapp']"
    />
  </PnCol>
</template>
<script lang='py'>
import panel as pn
import logging
from vuepy import ref

# 需要初始化terminal扩展
pn.extension('terminal', console_output='disable')

logger = logging.getLogger('panel.myapp')
info_type = ref('info')

def log_message(event):
    msg = (event['new'] + ' 通过按钮发送').capitalize()
    if event['new'] == 'info':
        logger.info(msg)
    elif event['new'] == 'debug':
        logger.debug(msg)
    elif event['new'] == 'warning':
        logger.warning(msg)
</script>

```


## API

### 属性

| 属性名 | 说明 | 类型 | 默认值 |
| -------- | ------------------- | ---------------------------------------------------------------| ------- |
| only_last | 记录异常时，指示是否仅提示堆栈中的最后一个跟踪 | ^[boolean] | false |
| level | 要在前端提示的日志级别 | ^[int] | logging.ERROR |
| formatter_args | 传递给格式化程序对象的参数 | ^[dict] | `{'fmt':"%(asctime)s [%(name)s - %(levelname)s]: %(message)s"}` |
| logger_names | 将提示到终端的记录器名称列表 | ^[list] | ['panel'] |
| name | 组件标题 | ^[string] | — |

### 方法

| 属性名 | 说明 | 类型 |
| --- | --- | --- |
| btns | 获取调试器控制按钮 | ^[function] |



# EditableIntSlider 可编辑整数滑块

EditableIntSlider组件允许用户在设定范围内通过滑块选择整数值，并提供一个可编辑的数字输入框以进行更精确的控制。

底层实现为`panel.widgets.EditableIntSlider`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/EditableIntSlider.html


## 基本用法

可编辑整数滑块提供了滑块和输入框两种方式来选择和输入整数值。

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnEditableIntSlider 
    name="整数滑块" 
    :start="0" 
    :end="8" 
    :step="2" 
    :value="4"
    v-model="int_value.value"
    @change="on_change"
  />
  <PnStaticText :value="f'选择的值: {int_value.value}'" />
</template>
<script lang='py'>
from vuepy import ref

int_value = ref(4)

def on_change(event):
    print(f"值改变: {event}")
</script>

```


## 固定范围

通过设置`fixed_start`和`fixed_end`参数，可以限制value的范围，使其不能超出这个范围。

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnEditableIntSlider 
    name="固定范围滑块" 
    :start="0" 
    :end="10" 
    :step="1" 
    :value="5"
    :fixed_start="-2"
    :fixed_end="12"
    v-model="fixed_value.value"
  />
  <PnStaticText :value="f'尝试输入超出范围的值（-2~12）: {fixed_value.value}'" />
</template>
<script lang='py'>
from vuepy import ref

fixed_value = ref(5)
</script>

```


## 自定义格式

可以通过format参数自定义整数的显示格式。

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnCol>
    <PnEditableIntSlider 
      name="八进制" 
      format="0o" 
      :start="0" 
      :end="100"
      :value="10"
      v-model="octal_value.value"
    />
    
    <PnEditableIntSlider 
      name="带单位" 
      :format="formatter" 
      :start="0" 
      :end="100"
      :value="42"
      v-model="duck_value.value"
    />
  </PnCol>
</template>
<script lang='py'>
from vuepy import ref
from bokeh.models.formatters import PrintfTickFormatter

octal_value = ref(10)
duck_value = ref(42)
formatter = PrintfTickFormatter(format='%d 只鸭子')
</script>

```


## 自定义样式

通过设置bar_color和orientation等属性可以自定义滑块样式。

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnEditableIntSlider 
    name="水平自定义滑块" 
    :start="0" 
    :end="10" 
    :step="1" 
    :value="5"
    bar_color="#ff5722"
    tooltips
    v-model="horizontal_value.value"
  />
  
  <PnEditableIntSlider 
    name="垂直自定义滑块" 
    :start="0" 
    :end="10" 
    :step="1" 
    :value="7"
    orientation="vertical"
    bar_color="#2196f3"
    tooltips
    v-model="vertical_value.value"
  />
</template>
<script lang='py'>
from vuepy import ref

horizontal_value = ref(5)
vertical_value = ref(7)
</script>

```


## API

### 属性

| 属性名 | 说明 | 类型 | 默认值 |
| -------- | ------------------- | ---------------------------------------------------------------| ------- |
| start | 滑块的下限，可以被较低的`value`覆盖 | ^[float] | — |
| end | 滑块的上限，可以被较高的`value`覆盖 | ^[float] | — |
| fixed_start | 滑块和输入框的固定下限，`value`不能低于此值 | ^[float]^[None] | None |
| fixed_end | 滑块和输入框的固定上限，`value`不能高于此值 | ^[float]^[None] | None |
| step | 值之间的间隔 | ^[int] | 1 |
| value | 当前选中的整数值 | ^[int] | — |
| bar_color | 滑块条的颜色，十六进制RGB值 | ^[string] | — |
| direction | 滑块方向，从左到右('ltr')或从右到左('rtl') | ^[string] | 'ltr' |
| disabled | 是否禁用 | ^[boolean] | false |
| format | 应用于滑块值的格式化字符串或bokeh TickFormatter | ^[string]^[bokeh.models.TickFormatter] | — |
| name | 组件标题 | ^[string] | — |
| orientation | 滑块方向，水平('horizontal')或垂直('vertical') | ^[string] | 'horizontal' |
| tooltips | 是否在滑块手柄上显示提示 | ^[boolean] | false |

### Events

| 事件名 | 说明 | 类型 |
| --- | --- | --- |
| change | 当值改变时触发 | ^[Callable]`(event: dict) -> None` |




# DateSlider 日期滑块

DateSlider组件允许用户在设定的日期范围内通过滑块选择一个日期值。

底层实现为`panel.widgets.DateSlider`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/DateSlider.html


## 基本用法

日期滑块组件提供了一种交互式方式来选择日期范围内的特定日期。

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnDateSlider 
    name="日期滑块" 
    :start="dt.datetime(2019, 1, 1)" 
    :end="dt.datetime(2019, 6, 1)" 
    :value="dt.datetime(2019, 2, 8)"
    v-model="selected_date.value"
    @change="on_change"
  />
  <PnStaticText :value="f'选择的日期: {selected_date.value}'" />
</template>
<script lang='py'>
import datetime as dt
from vuepy import ref

selected_date = ref(dt.datetime(2019, 2, 8))

def on_change(event):
    print(f"Date changed: {event}") # Date changed: Event(what='value'
</script>

```

## 自定义样式

通过设置bar_color和orientation等属性可以自定义滑块样式。

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnDateSlider 
    name="水平滑块" 
    :start="dt.datetime(2019, 1, 1)" 
    :end="dt.datetime(2019, 6, 1)" 
    :value="dt.datetime(2019, 2, 8)"
    bar_color="#ff5722"
    tooltips
    v-model="date_horizontal.value"
  />
  
 <PnColumn style='height:400px;'>
  <PnDateSlider 
    name="垂直滑块" 
    :start="dt.datetime(2019, 1, 1)" 
    :end="dt.datetime(2019, 6, 1)" 
    :value="dt.datetime(2019, 3, 15)"
    orientation="vertical"
    bar_color="#2196f3"
    tooltips
    v-model="date_vertical.value"
  />
 </PnColumn>
</template>
<script lang='py'>
import datetime as dt
from vuepy import ref

date_horizontal = ref(dt.datetime(2019, 2, 8))
date_vertical = ref(dt.datetime(2019, 3, 15))
</script>

```


## 步长设置

通过step参数可以设置日期滑块的步长（以天为单位）。

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnDateSlider 
    name="7天步长" 
    :start="dt.datetime(2019, 1, 1)" 
    :end="dt.datetime(2019, 6, 1)" 
    :value="dt.datetime(2019, 2, 8)"
    :step="7"
    tooltips
    v-model="date_step.value"
  />
  <PnStaticText :value="f'选择的日期: {date_step.value}'" />
</template>
<script lang='py'>
import datetime as dt
from vuepy import ref

date_step = ref(dt.datetime(2019, 2, 8))
</script>

```


## 日期格式

可以通过format参数自定义日期的显示格式。

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnDateSlider 
    name="自定义格式" 
    :start="dt.datetime(2019, 1, 1)" 
    :end="dt.datetime(2019, 6, 1)" 
    :value="dt.datetime(2019, 2, 8)"
    format="%Y年%m月%d日"
    tooltips
    v-model="date_format.value"
  />
</template>
<script lang='py'>
import datetime as dt
from vuepy import ref

date_format = ref(dt.datetime(2019, 2, 8))
</script>

```


## API

### 属性

| 属性名 | 说明 | 类型 | 默认值 |
| -------- | ------------------- | ---------------------------------------------------------------| ------- |
| as_datetime | 是否以datetime类型返回值（否则为date类型） | ^[boolean] | false |
| start | 日期范围的下限 | ^[date]^[datetime] | — |
| end | 日期范围的上限 | ^[date]^[datetime] | — |
| value | 当前选中的日期值 | ^[date]^[datetime] | — |
| step | 滑块步长（以天为单位） | ^[integer] | 1 |
| bar_color | 滑块条的颜色，十六进制RGB值 | ^[string] | — |
| direction | 滑块方向，从左到右('ltr')或从右到左('rtl') | ^[string] | 'ltr' |
| disabled | 是否禁用 | ^[boolean] | false |
| name | 组件标题 | ^[string] | — |
| orientation | 滑块方向，水平('horizontal')或垂直('vertical') | ^[string] | 'horizontal' |
| tooltips | 是否在滑块手柄上显示提示 | ^[boolean] | false |
| format | 日期格式 | ^[string] | — |

### Events

| 事件名 | 说明 | 类型 |
| --- | --- | --- |
| change | 当选择改变时触发 | ^[Callable]`(event: dict) -> None` |




# FileInput 文件输入框

文件输入框组件允许用户上传一个或多个文件，支持拖放或点击选择文件。上传的文件可以作为字节字符串获取，也可以自动转换为其他格式。

底层实现为`panel.widgets.FileInput`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/FileInput.html


## 基本用法

基本的文件输入框使用：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnFileInput name="上传文件" @change="on_change" />
</template>
<script lang='py'>
from vuepy import ref

def on_change(event):
    print(event) # Event(what='value', name='value', 
                 #  obj=FileInput(name='上传文件', value=b'hello\n'), 
                 #  cls=FileInput(name='上传文件', value=b'hello\n'), 
                 #  old=None, new=b'hello\n', type='changed')
</script>

```


## 多文件上传

可以通过设置`multiple=True`支持多文件上传：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnFileInput name="上传多个文件" :multiple="True" @change="on_change" />
</template>
<script lang='py'>
from vuepy import ref

def on_change(event):
    print(event) # Event(what='value', name='value', 
                 #  obj=FileInput(filename=['a.txt'], mime_type=['text/plain'], multiple=True, name='上传多个文件', value=[b'hello\n', b'hello\n']),
                 #  cls=FileInput(filename=['a.txt'], mime_type=['text/plain'], multiple=True, name='上传多个文件', value=[b'hello\n', b'hello\n']), 
                 #  old=None, new=[b'hello\n', b'hello\n'], type='changed')
</script>

```

## 接受特定文件类型

可以通过`accept`参数限制可接受的文件类型：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnFileInput name="上传图片" 
              accept=".jpg,.jpeg,.png,.gif" 
              @change="on_change" />
  <PnFileInput name="上传PDF" 
              accept=".pdf" 
              @change="on_change_pdf" />
</template>
<script lang='py'>
from vuepy import ref

def on_change(event):
    print(event)
        
def on_change_pdf(event):
    print(event)
</script>

```


## API

### 属性

| 属性名       | 说明                  | 类型      | 默认值    |
| ----------- | -------------------- | --------- | --------- |
| accept      | 接受的文件MIME类型或扩展名 | ^[str]     | ""       |
| multiple    | 是否允许多文件上传     | ^[bool]   | False     |
| filename    | 上传文件的文件名       | ^[str]    | ""        |
| value       | 上传文件的内容         | ^[bytes\|str] | b""    |
| mime_type   | 上传文件的MIME类型     | ^[str]    | ""        |
| decode      | 是否自动解码为文本     | ^[bool]   | False     |
| disabled    | 是否禁用组件          | ^[bool]   | False     |
| name        | 组件标题             | ^[str]    | ""        |
| description | 鼠标悬停时显示的描述   | ^[str]    | ""        |

### Events

| 事件名  | 说明                | 类型                          |
| ------ | ------------------ | ----------------------------- |
| change | 当文件上传时触发的事件 | ^[Callable]`(event) -> None` |




# TextToSpeech 文本转语音

TextToSpeech组件为Panel带来文本转语音功能，它封装了[HTML5 SpeechSynthesis API](https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesis)和[HTML SpeechSynthesisUtterance API](https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesisUtterance)。

底层实现为`panel.widgets.TextToSpeech`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/TextToSpeech.html


## 基本用法

文本转语音组件可以将文本转换为语音并播放出来。请注意，该组件本身在视觉上不显示任何内容，但仍需添加到应用程序中才能使用。

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnCol>
    <PnTextToSpeech 
      name="语音合成" 
      value="你好，欢迎使用Panel的文本转语音组件。"
      @change="on_change"
    />
    <PnButton 
      name="点击播放" 
      button_type="primary" 
      @click="speak()"
    />
  </PnCol>
</template>
<script lang='py'>
import panel as pn
from vuepy import ref

text_to_speech_ref = ref(None)

def speak():
    text_to_speech_ref.value.speak = True
    
def on_change(event):
    text_to_speech_ref.value = event['owner']
    print(f"语音状态变化: {event}")
</script>

```


## 自动播放

当`auto_speak`设置为true时（默认值），每当`value`更改时，都会自动播放语音。

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnCol>
    <PnTextToSpeech 
      name="自动播放" 
      :value="text.value"
      :auto_speak="True"
      ref="tts"
    />
    <PnTextAreaInput 
      v-model="text.value"
      rows="3"
      placeholder="输入文本，修改后会自动播放"
    />
    <PnRow>
      <PnButton label="暂停" @click="pause()" />
      <PnButton label="恢复" @click="resume()" />
      <PnButton label="取消" @click="cancel()" />
    </PnRow>
  </PnCol>
</template>
<script lang='py'>
import panel as pn
from vuepy import ref

text = ref("输入文本，修改后会自动播放")

def pause():
    tts = pn.state.curdoc.select_one({'name': '自动播放'})
    if tts:
        tts.pause = True

def resume():
    tts = pn.state.curdoc.select_one({'name': '自动播放'})
    if tts:
        tts.resume = True
        
def cancel():
    tts = pn.state.curdoc.select_one({'name': '自动播放'})
    if tts:
        tts.cancel = True
</script>

```


## 语音参数调整

可以通过设置`lang`、`pitch`、`rate`和`volume`参数来调整语音的特性。


## 长文本示例

TextToSpeech组件可以处理较长的文本内容。


## API

### 属性

| 属性名 | 说明 | 类型 | 默认值 |
| -------- | ------------------- | ---------------------------------------------------------------| ------- |
| value | 将在发声时合成的文本 | ^[string] | — |
| auto_speak | 值更改时是否自动发声 | ^[boolean] | true |
| lang | 语音的语言 | ^[string] | — |
| voice | 用于发声的语音 | ^[SpeechSynthesisVoice] | — |
| pitch | 语音的音调，0到2之间的数字 | ^[float] | 1 |
| rate | 语音的速度，0.1到10之间的数字 | ^[float] | 1 |
| volume | 语音的音量，0到1之间的数字 | ^[float] | 1 |
| speak | 发声动作 | ^[boolean] | false |
| cancel | 取消所有待发声的语音 | ^[boolean] | false |
| pause | 暂停语音合成 | ^[boolean] | false |
| resume | 恢复语音合成 | ^[boolean] | false |
| voices | 当前设备上可用的所有语音列表 | ^[List[Voice]] | [] |
| paused | 语音合成是否处于暂停状态 | ^[boolean] | false |
| pending | 语音队列中是否有尚未发声的语音 | ^[boolean] | false |
| speaking | 当前是否正在发声 | ^[boolean] | false |
| name | 组件标题 | ^[string] | — |

### Events

| 事件名 | 说明 | 类型 |
| --- | --- | --- |
| change | 当组件状态改变时触发 | ^[Callable]`(event: dict) -> None` |



# FileDropper 文件拖放上传器

FileDropper组件允许用户将一个或多个文件上传到服务器。它基于[FilePond](https://pqina.nl/filepond/)库构建，如果您广泛使用此组件，请考虑向他们捐款。FileDropper类似于FileInput组件，但增加了对分块上传的支持，使上传大文件成为可能。UI还支持图像文件的预览。与FileInput不同，上传的文件存储为以文件名为索引的字节对象字典。

底层实现为`panel.widgets.FileDropper`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/FileDropper.html


## 基本用法

FileDropper提供了一个拖放区域，允许用户通过拖放或点击选择上传文件。

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnFileDropper 
    v-model="uploaded_files.value"
    @change="on_change"
  />
  <PnStaticText :value="f'上传的文件: {list(uploaded_files.value.keys())}'" />
</template>
<script lang='py'>
from vuepy import ref

uploaded_files = ref({})

def on_change(event):
    print(f"{event}") # Event(what='value', name='value', 
                      #  obj=FileDropper(mime_type={'a.txt': 'text/plain'}, value={'a.txt': 'hello\n'}), 
                      #  cls=FileDropper(mime_type={'a.txt': 'text/plain'}, value={'a.txt': 'hello\n'}), 
                      #  old={'a.txt': 'hello\n'}, new={'a.txt': 'hello\n'},
</script>

```


## 文件类型限制

通过`accepted_filetypes`参数可以限制用户可以选择的文件类型。这包括一个也允许通配符的mime类型列表。

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnCol>
    <PnStaticText value="只允许上传PNG和JPEG图片" />
    <PnFileDropper 
      :accepted_filetypes="['.png', 'image/jpeg']"
    />
    
    <PnStaticText value="允许上传所有图片" />
    <PnFileDropper 
      :accepted_filetypes="['image/*']"
    />
  </PnCol>
</template>

```


## 多文件上传

通过设置`multiple=True`可以允许上传多个文件。

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnFileDropper 
    multiple
    v-model="multiple_files.value"
  />
  <PnStaticText :value="f'上传的文件数量: {len(multiple_files.value)}'" />
</template>
<script lang='py'>
from vuepy import ref

multiple_files = ref({})
</script>

```


## 布局选项

FileDropper支持几种不同的布局选项：
- `"compact"`: 移除边距
- `"integrated"`: 移除背景和其他样式，当组件嵌入到更大的组件中时很有用
- `"circle"`: 圆形上传区域，适用于个人资料图片上传

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnCol>
    <PnFileDropper layout="compact" />
    <PnFileDropper 
      layout="integrated" 
      style="background-color: black; border-radius: 1em; color: white" 
    />
    <PnFileDropper layout="circle" />
  </PnCol>
</template>

```


## 上传大小限制

与FileInput组件不同，FileDropper组件通过分块上传绕过了网络浏览器、Bokeh、Tornado、笔记本等对最大文件大小的限制。这使得上传比以前可能的大得多的文件变得可行。默认的`chunk_size`是10MB（表示为10000000字节）。您可以配置`max_file_size`、`max_total_file_size`（如果设置了`multiple=True`，则限制总上传大小）和`max_files`，以提供对可上传数据量的上限。

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnCol>
    <PnStaticText value="限制单个文件大小为1MB" />
    <PnFileDropper 
      max_file_size="1MB"
      v-model="limited_size.value"
    />
    
    <PnStaticText value="限制最多上传3个文件，总大小不超过5MB" />
    <PnFileDropper 
      :multiple="True"
      :max_files="3"
      max_total_file_size="5MB"
      v-model="limited_total.value"
    />
  </PnCol>
</template>
<script lang='py'>
from vuepy import ref

limited_size = ref({})
limited_total = ref({})
</script>

```


## API

### 属性

| 属性名 | 说明 | 类型 | 默认值 |
| -------- | ------------------- | ---------------------------------------------------------------| ------- |
| accepted_filetypes | 接受的文件类型列表 | ^[list] | [] |
| chunk_size | 每个分块通过WebSocket传输的大小（以字节为单位） | ^[int] | 10000000 |
| layout | 布局模式 | ^[string] | None |
| max_file_size | 文件的最大大小（以KB或MB为单位的字符串表示） | ^[string] | — |
| max_files | 如果`multiple=True`，可以上传的最大文件数 | ^[int] | — |
| max_total_file_size | 所有上传文件的最大大小（以KB或MB为单位的字符串表示） | ^[string] | — |
| mime_type | 包含上传文件的mime类型的字典，以文件名为索引 | ^[dict[str, str]] | — |
| multiple | 是否允许上传多个文件 | ^[boolean] | false |
| value | 包含上传文件的字典，以文件名为索引 | ^[dict[str, str \| bytes]] | {} |

### Events

| 事件名 | 说明 | 类型 |
| --- | --- | --- |
| change | 当上传文件改变时触发 | ^[Callable]`(event: dict) -> None` |




# MultiChoice 多项选择器

多项选择器组件允许用户从可用选项列表中选择多个项目，并支持搜索过滤选项。

底层实现为`panel.widgets.MultiChoice`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/MultiChoice.html


## 基本用法

基本的多项选择器使用：

```vue
<!-- --plugins vpanel --show-code -->
<template>
 <PnCol :height='400'>
  <PnMultiChoice name="Fruit" 
                :options="['Apple', 'Orange', 'Pear']"
                v-model="selected.value" />
 </PnCol>
 <p>value: {{ selected.value }}</p>
</template>
<script lang='py'>
from vuepy import ref

selected = ref(['Apple'])
</script>

```


## 使用字典选项

可以使用字典作为选项，其中键是显示的标签，值是实际的数据值：

```vue
<!-- --plugins vpanel --show-code -->
<template>
 <PnCol :height='400'>
  <PnMultiChoice name="City" 
                :options="city_options"
                v-model="selected.value" />
 </PnCol>
 <p>value: {{ selected.value }}</p>
</template>
<script lang='py'>
from vuepy import ref

city_options = {'Beijing': 'BJ', 'shanghai': 'SH', 'guangzhou': 'GZ'}
selected = ref(['BJ', 'SZ'])

</script>

```


## API

### 属性

| 属性名       | 说明                 | 类型                                             | 默认值 |
| ----------- | ------------------- | ------------------------------------------------ | ------- |
| options     | 可选择的选项列表      | ^[list\|dict]                                    | []      |
| value       | 当前选中的值列表      | ^[list]                                          | []      |
| max_items   | 最多可选择的项目数    | ^[int\|None]                                     | None    |
| placeholder | 选择框的占位符文本    | ^[str]                                           | "Select option(s)" |
| delete_button | 是否显示删除按钮    | ^[bool]                                          | True    |
| solid       | 是否使用实体填充样式  | ^[bool]                                          | True    |
| disabled    | 是否禁用组件          | ^[bool]                                          | False   |
| name        | 组件标题              | ^[str]                                           | ""      |

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |
| change | 当选择变化时触发的事件 | ^[Callable]`(event: dict) -> None` |




# VideoStream 视频流

VideoStream组件可以显示来自本地流（例如网络摄像头）的视频，并允许从Python访问流式视频数据。

底层实现为`panel.widgets.VideoStream`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/VideoStream.html


## 基本用法

视频流组件默认情况下会显示视频流，可用于如网络摄像头实时视频的展示。

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnVideoStream name="视频流" />
</template>

```


## 截图功能

可以调用`snapshot`方法触发组件的`value`更新，以获取当前视频帧的图像。


```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnCol>
    <PnVideoStream 
      name="video stream" 
      @change="update_snapshot"
      v-model="snapshot_img.value"
      ref="video_stream_ref"
    />
    <PnButton 
      name="Snapshot" 
      button_type="primary" 
      @click="take_snapshot()"
    />
  </PnCol>
  <img alt='snap' :src="snapshot_img.value" />
  <PnHTML :object="snapshot_html.value" :width='320' :height='240' />
</template>
<script lang='py'>
import panel as pn
from vuepy import ref

snapshot_html = ref("")
video_stream_ref = ref(None)
snapshot_img = ref('')

def take_snapshot():
    if video_stream_ref.value:
        print('img', video_stream_ref.value.unwrap().value)
        video_stream_ref.value.unwrap().snapshot()

def update_snapshot(event):
    print(event.new)
    if event.new:
        snapshot_html.value = f'<img src="{event.new}" width=320 height=240 />'
        # video_stream_ref.value = event['owner']
</script>

```


## 定时截图

通过设置`timeout`参数，可以指定视频流将以多大频率更新。

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnCol>
    <PnToggle name="暂停" v-model="paused.value" />
    <PnRow>
      <PnVideoStream 
        :timeout="1000" 
        :paused="paused.value"
        @change="update_timed_snapshot"
      />
    </PnRow>
  <PnHTML :object="timed_html.value" />
  </PnCol>
</template>
<script lang='py'>
import panel as pn
from vuepy import ref

pn.extension()

paused = ref(False)
timed_html = ref("")

def update_timed_snapshot(event):
    if 'value' in event and event.new:
        timed_html.value = f'<img src="{event.new}" width=320 height=240 />'
</script>

```


## 图像格式

可以通过`format`参数指定捕获的图像格式，如果需要高频率的截图，可以选择'jpeg'格式，因为图像尺寸要小得多。

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnCol>
    <PnRow>
      <PnVideoStream 
        name="PNG格式" 
        format="png"
        :timeout="500"
        :width="320"
        :height="240"
      />
      <PnVideoStream 
        name="JPEG格式" 
        format="jpeg"
        :timeout="500"
        :width="320"
        :height="240"
      />
    </PnRow>
    <PnStaticText value="JPEG格式适合高频率截图，因为图像尺寸更小" />
  </PnCol>
</template>
<script lang='py'>
import panel as pn
from vuepy import ref

pn.extension()
</script>

```


## API

### 属性

| 属性名 | 说明 | 类型 | 默认值 |
| -------- | ------------------- | ---------------------------------------------------------------| ------- |
| format | 捕获图像的格式，'png'或'jpeg' | ^[string] | 'png' |
| paused | 视频流是否暂停 | ^[boolean] | false |
| timeout | 截图之间的间隔（毫秒），如果为None则仅在调用snapshot方法时才拍摄截图 | ^[int]^[None] | None |
| value | 当前截图的字符串表示 | ^[string] | — |
| snapshot | 触发截图的动作 | ^[boolean] | false |
| name | 组件标题 | ^[string] | — |

### Events

| 事件名 | 说明 | 类型 |
| --- | --- | --- |
| change | 当组件状态（特别是value）改变时触发 | ^[Callable]`(event: dict) -> None` |




# Select 选择器

选择器组件允许用户从下拉菜单或选择区域中选择一个值。它属于单值选择类组件，提供兼容的API，包括RadioBoxGroup、AutocompleteInput和DiscreteSlider等组件。

底层实现为`panel.widgets.Select`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/Select.html


## 基本用法

基本的选择器使用：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnSelect :options="['Apple', 'Orange', 'Banana']" 
            v-model='selection.value' />
  <p>value: {{ selection.value }}</p>
</template>
<script lang='py'>
from vuepy import ref

selection = ref('Apple')
</script>

```


## 使用字典作为选项

`options`参数也接受一个字典，其键将作为下拉菜单的标签：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnSelect :options="{'Apple': 1, 'Orange': 2, 'Banana': 3}"
            v-model='selection.value' />
  <p>value: {{ selection.value }}</p>
</template>
<script lang='py'>
from vuepy import ref

selection = ref(1)
</script>

```


## 禁用选项

可以使用`disabled_options`参数禁用部分选项：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnSelect :options="['Apple', 'Orange', 'xxx', 'Banana']" 
            :disabled_options="['xxx']"
            v-model='selection.value' />
  <p>value: {{ selection.value }}</p>
</template>
<script lang='py'>
from vuepy import ref

selection = ref('Apple')
</script>

```


## 分组选项

可以使用`groups`参数对选项进行分组显示（也称为*optgroup*）：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnSelect 
    :groups="{'Europe': ['Greece', 'France'], 'Asia': ['China', 'Japan']}"
    v-model='selection.value' />
  />
  <p>value: {{ selection.value }}</p>
</template>
<script lang='py'>
from vuepy import ref

selection = ref('France')
</script>

```


## 列表选择区域

通过设置`size`参数大于1，可以从列表中选择一个选项，而不是使用下拉菜单：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnSelect 
    :options="['Apple', 'Orange', 'xxx', 'Banana']" 
    :size="3"
    v-model='selection.value' />
  <p>value: {{ selection.value }}</p>
</template>
<script lang='py'>
from vuepy import ref

selection = ref('Apple')
</script>

```


## API

### 属性

| 属性名            | 说明                   | 类型                  | 默认值    |
| ---------------- | --------------------- | -------------------- | --------- |
| options          | 选项列表或字典          | ^[list, dict]        | []        |
| disabled_options | 禁用选项列表           | ^[list]              | []        |
| groups           | 分组选项字典            | ^[dict]              | {}        |
| size             | 同时显示的选项数量       | ^[int]               | 1         |
| value            | 当前选择的值            | ^[object]            | None      |
| disabled         | 是否禁用组件            | ^[bool]              | False     |
| name             | 组件标题               | ^[str]               | ""        |
| description      | 鼠标悬停时显示的描述     | ^[str]               | ""        |

### Events

| 事件名  | 说明                | 类型                           |
| ------ | ------------------ | ------------------------------ |
| change | 当选择改变时触发的事件 | ^[Callable]`(value) -> None`  |




# Toggle 切换开关

切换开关组件允许在`True`/`False`状态之间切换单一条件。Toggle、Checkbox和Switch组件功能类似，可互相替换。

底层实现为`panel.widgets.Toggle`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/Toggle.html


## 基本用法

基本的切换开关使用：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnToggle name="切换开关" button_type="success" 
            v-model='is_toggled.value'/>
  <p>value: {{ is_toggled.value }}</p>
</template>
<script lang='py'>
from vuepy import ref

is_toggled = ref(False)
</script>

```


## 样式

按钮的颜色可以通过设置`button_type`来改变，而`button_style`可以是`'solid'`或`'outline'`：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnRow>
    <PnCol v-for="style in ['solid', 'outline']">
      <PnToggle v-for="type in button_types" 
                :name="f'{type}-{style}'"
                :button_type="type"
                :button_style="style" 
                style="margin: 5px" />
    </PnCol>
  </PnRow>
</template>
<script lang='py'>
from vuepy import ref

button_types = ['default', 'primary', 'success', 'warning', 'danger', 'light']
</script>

```


## 图标

Toggle组件可以添加图标，支持Unicode、Emoji字符，以及 [tabler-icons.io](https://tabler-icons.io) 的命名图标或自定义SVG：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnRow>
    <PnToggle :name="u'\u25c0'" :width="50" />
    <PnToggle :name="u'\u25b6'" :width="50" />
    <PnToggle name="🔍" :width="100" />
    <PnToggle name="▶️ 播放" :width="100" />
    <PnToggle name="暂停 ⏸️" :width="100" />
  </PnRow>
  
  <PnRow>
    <PnToggle icon="alert-triangle-filled" button_type="warning" name="警告" />
    <PnToggle icon="2fa" button_type='light' icon_size='2em' />
  </PnRow>
  
  <PnToggle button_type='success' name='随机播放' icon_size='2em'>
    <template #icon>
    <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-arrows-shuffle" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
      <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
      <path d="M18 4l3 3l-3 3" />
      <path d="M18 20l3 -3l-3 -3" />
      <path d="M3 7h3a5 5 0 0 1 5 5a5 5 0 0 0 5 5h5" />
      <path d="M21 7h-5a4.978 4.978 0 0 0 -3 1m-4 8a4.984 4.984 0 0 1 -3 1h-3" />
    </svg>
    </template>
  </PnToggle>
</template>

```


## API

### 属性

| 属性名         | 说明                    | 类型                                | 默认值     |
| ------------- | ----------------------- | ---------------------------------- | --------- |
| button_style  | 按钮样式                | ^[str] 'solid'或'outline'          | 'solid'   |
| button_type   | 按钮主题                | ^[str] 'default'、'primary'、'success'、'info'或'danger' | 'default' |
| icon          | 按钮图标                | ^[str] SVG字符串或tabler-icons.io图标名称 | None     |
| icon_size     | 图标大小                | ^[str] 如"12px"或"1em"             | None      |
| value         | 按钮是否切换            | ^[bool]                            | False     |
| disabled      | 是否禁用                | ^[bool]                            | False     |
| name          | 按钮标题/文本           | ^[str]                             | ""        |
| description   | 鼠标悬停时显示的描述     | ^[str]                             | ""        |

### Events

| 事件名  | 说明                | 类型                          |
| ------ | ------------------ | ----------------------------- |
| change | 当状态改变时触发的事件 | ^[Callable]`(value) -> None` |




# ColorPicker 颜色选择器

颜色选择器组件允许使用浏览器的颜色选择小部件选择颜色。

底层实现为`panel.widgets.ColorPicker`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/ColorPicker.html


## 基本用法

基本的颜色选择器使用：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnColorPicker name="basic" value="#99ef78" @change="update_color" />
  <div>color: {{ color.value }}</div>
</template>
<script lang='py'>
from vuepy import ref

color = ref('#99ef78')

def update_color(value):
    color.value = value
</script>

```


## 默认颜色设置

可以通过设置`value`参数来指定默认颜色：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnRow>
    <PnColorPicker name="red" value="#ff0000" @change="update_red" />
    <PnColorPicker name="green" value="#00ff00" @change="update_green" />
    <PnColorPicker name="blue" value="#0000ff" @change="update_blue" />
  </PnRow>
</template>
<script lang='py'>
from vuepy import ref

red = ref('#ff0000')
green = ref('#00ff00')
blue = ref('#0000ff')

def update_red(value):
    red.value = value

def update_green(value):
    green.value = value

def update_blue(value):
    blue.value = value
</script>

```


## 禁用状态

可以通过设置`disabled`参数为`True`使颜色选择器处于禁用状态：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnRow>
    <PnColorPicker name="可用状态" value="#ff9900" />
    <PnColorPicker name="禁用状态" value='#3399ff' disabled />
  </PnRow>
</template>

```

## 实时应用颜色

颜色选择器可以用于实时更新网页元素的样式：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnRow>
    <PnColorPicker name="背景色" v-model="bg_color.value" />
    <PnColorPicker name="文字色" v-model="text_color.value" />
  </PnRow>
    <p :style="f'background-color: {bg_color.value}; color: {text_color.value};'">
      这是一段示例文本，您可以通过上方的颜色选择器来更改其背景色和文字颜色。
   </p>
</template>
<script lang='py'>
from vuepy import ref

bg_color = ref('#f0f0f0')
text_color = ref('#333333')

def update_bg(value):
    bg_color.value = value

def update_text(value):
    text_color.value = value
</script>

```


## API

### 属性

| 属性名       | 说明                 | 类型      | 默认值    |
| ----------- | ------------------- | --------- | --------- |
| value       | 颜色值（十六进制RGB）  | ^[str]    | "#000000" |
| disabled    | 是否禁用组件          | ^[bool]   | False     |
| name        | 组件标题             | ^[str]    | ""        |
| description | 鼠标悬停时显示的描述   | ^[str]    | ""        |

### Events

| 事件名  | 说明                | 类型                          |
| ------ | ------------------ | ----------------------------- |
| change | 当颜色改变时触发的事件 | ^[Callable]`(value) -> None` |




# Switch 开关

开关组件允许通过滑动开关在`True`/`False`状态之间切换单一条件。Switch、Checkbox和Toggle组件功能类似，可互相替换。

底层实现为`panel.widgets.Switch`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/Switch.html


## 基本用法

基本的开关使用：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnSwitch name="Switch" v-model="is_on.value" />
  <p>value: {{ is_on.value }}</p>
</template>
<script lang='py'>
from vuepy import ref

is_on = ref(False)
</script>

```


## API

### 属性

| 属性名       | 说明                 | 类型      | 默认值    |
| ----------- | ------------------- | --------- | --------- |
| value       | 开关是否打开          | ^[bool]   | False     |
| disabled    | 是否禁用组件          | ^[bool]   | False     |
| name        | 组件标题             | ^[str]    | ""        |
| description | 鼠标悬停时显示的描述   | ^[str]    | ""        |

### Events

| 事件名  | 说明                | 类型                          |
| ------ | ------------------ | ----------------------------- |
| change | 当状态改变时触发的事件 | ^[Callable]`(value) -> None` |




# DatetimePicker 日期时间选择器

日期时间选择器组件允许用户选择日期和时间，可以通过文本输入框和浏览器的日期时间选择工具进行选择。

底层实现为`panel.widgets.DatetimePicker`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/DatetimePicker.html


## 基本用法

基本的日期时间选择器使用：

```vue
<!-- --plugins vpanel --show-code -->
<template>
 <PnCol style='height:420px;'>
  <PnDatetimePicker name="选择日期时间" v-model='datetime.value' />
 </PnCol>
 <p>当前选择: {{ datetime.value }}</p>
</template>
<script lang='py'>
from vuepy import ref
import datetime as dt

datetime = ref(None)
# set default
# datetime = ref(dt.datetime(2023, 7, 15, 14, 30))
</script>

```

## 日期范围限制

可以使用`start`和`end`参数限制可选择的日期范围：

```vue
<!-- --plugins vpanel --show-code -->
<template>
 <PnCol style='height:420px;'>
  <PnDatetimePicker name="7天内选择" 
                   :start="today"
                   :end="week_later"/>
 </PnCol>
 <p>当前选择: {{ datetime.value }}</p>
</template>
<script lang='py'>
from vuepy import ref
import datetime as dt

today = dt.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
week_later = today + dt.timedelta(days=7)

datetime = ref(None)
</script>

```


## 自定义时间选项

可以使用`enable_time`、`enable_seconds`和`military_time`参数自定义时间选择功能：

```vue
<!-- --plugins vpanel --show-code -->
<template>
 <PnCol style='height:420px;'>
  <PnDatetimePicker name="仅日期" 
                   :enable_time="False"/>
 </PnCol>
 <PnCol style='height:420px;'>
  <PnDatetimePicker name="带秒选择" 
                   :enable_seconds="True"/>
 </PnCol>
 <PnColumn style='height:420px;'>
  <PnDatetimePicker name="12小时制" 
                   :military_time="False"/>
 </PnCol>
</template>

```


## 禁用特定日期

可以使用`disabled_dates`和`enabled_dates`参数禁用或启用特定日期，**注意**是`datetime.date`类型。


## API

### 属性

| 属性名           | 说明                         | 类型                            | 默认值      |
| ---------------- | ---------------------------- | -------------------------------- | ----------- |
| value            | 当前选择的日期时间            | ^[datetime.datetime]            | None        |
| start            | 允许选择的最早日期时间        | ^[datetime.datetime\|datetime.date] | None      |
| end              | 允许选择的最晚日期时间        | ^[datetime.datetime\|datetime.date] | None      |
| disabled_dates   | 禁用的日期列表                | ^[list[datetime.date]                         | []          |
| enabled_dates    | 启用的日期列表                | ^[list[datetime.date]                         | []          |
| enable_time      | 是否启用时间选择              | ^[bool]                         | True        |
| enable_seconds   | 是否启用秒选择                | ^[bool]                         | True        |
| military_time    | 是否使用24小时制              | ^[bool]                         | True        |
| allow_input      | 是否允许用户直接在输入框中输入 | ^[bool]                         | False       |
| disabled         | 是否禁用组件                  | ^[bool]                         | False       |
| name             | 组件标题                      | ^[str]                          | ""          |
| description      | 鼠标悬停时显示的描述          | ^[str]                          | ""          |

### Events

| 事件名  | 说明                | 类型                                 |
| ------ | ------------------ | ------------------------------------ |
| change | 当选择更改时触发的事件 | ^[Callable]`(value) -> None`        |




# DiscretePlayer 离散播放器

离散播放器组件是一个用于循环播放一系列离散值的工具，可用于动画或步进通过数据集。与标准`Player`组件不同，它使用离散的选项值，而不是连续的数值范围。

底层实现为`panel.widgets.DiscretePlayer`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/DiscretePlayer.html


## 基本用法

基本的离散播放器使用：

```vue
<!-- --plugins vpanel --show-code -->
<template>
 <PnCol style='height:140px;'>
  <PnDiscretePlayer name="月份播放器" 
                  :options="months" 
                  @change="on_change" />
 </PnCol>
  <p>当前月份: {{ current_month.value }}</p>
</template>
<script lang='py'>
from vuepy import ref

months = ['一月', '二月', '三月', '四月', '五月', '六月', 
         '七月', '八月', '九月', '十月', '十一月', '十二月']
current_month = ref("未选择")

def on_change(event):
    current_month.value = event.new
</script>

```


## 设置循环和间隔

可以设置播放器是否循环以及播放间隔(毫秒）：

```vue
<!-- --plugins vpanel --show-code -->
<template>
 <PnCol style='height:140px;'>
  <PnDiscretePlayer name="慢速播放" 
                  :options="months"
                  :interval="1000" />
 </PnCol>
 <PnCol style='height:140px;'>
  <PnDiscretePlayer name="不循环播放" 
                  :options="months"
                  loop_policy="once" />
 </PnCol>
</template>
<script lang='py'>
from vuepy import ref

months = ['一月', '二月', '三月', '四月', '五月', '六月', 
         '七月', '八月', '九月', '十月', '十一月', '十二月']
</script>

```


## 使用字典选项

可以使用字典作为选项，其中键是显示的标签，值是实际的数据值：

```vue
<!-- --plugins vpanel --show-code -->
<template>
 <p>当前季度代码: {{ current_quarter.value }}</p>
 <PnCol style='height:140px;'>
  <PnDiscretePlayer name="季度播放器" 
                  :options="quarters"
                  @change="on_change" />
 </PnCol>
</template>
<script lang='py'>
from vuepy import ref

quarters = {'第一季度': 'Q1', '第二季度': 'Q2', '第三季度': 'Q3', '第四季度': 'Q4'}
current_quarter = ref("未选择")

def on_change(event):
    current_quarter.value = event.new
</script>

```


## 设置显示模式

可以设置播放器的显示模式，如只显示按钮或者同时显示值等：

```vue
<!-- --plugins vpanel --show-code -->
<template>
 <PnCol style='height:140px;'>
  <PnDiscretePlayer name="只显示按钮" 
                  :options="months"
                  :visible_buttons="['previous', 'play', 'pause', 'next']" />
 </PnCol>
</template>
<script lang='py'>
from vuepy import ref

months = ['一月', '二月', '三月', '四月', '五月', '六月', 
         '七月', '八月', '九月', '十月', '十一月', '十二月']
</script>

```


## API

### 属性

| 属性名                | 说明                                                                 | 类型                                                | 默认值      |
|----------------------|--------------------------------------------------------------------|---------------------------------------------------|------------|
| direction            | 当前播放方向 (-1: 倒放, 0: 暂停, 1: 正放)                           | ^[int]                                            | 0          |
| interval             | 更新间隔时间（毫秒）                                                 | ^[int]                                            | -          |
| loop_policy          | 循环策略 ('once', 'loop', 或 'reflect')                             | ^[str]                                            | 'once'     |
| options              | 可选项列表或字典                                                     | ^[list] or ^[dict]                                | []         |
| value                | 当前值（必须是options中的值之一）                                    | ^[object]                                         | None       |
| value_throttled      | 鼠标抬起前的节流当前值（当使用滑块选择时）                            | ^[object]                                         | None       |
| disabled             | 是否禁用控件                                                        | ^[bool]                                           | False      |
| name                 | 控件标题                                                           | ^[str]                                            | ""         |
| scale_buttons        | 按钮缩放比例                                                        | ^[float]                                          | 1.0        |
| show_loop_controls   | 是否显示循环策略切换的单选按钮                                       | ^[bool]                                           | True       |
| show_value           | 是否显示播放器的当前值                                               | ^[bool]                                           | True       |
| value_align          | 数值显示位置 ('start', 'center', 'end')                             | ^[str]                                            | 'center'   |
| visible_buttons      | 要显示的按钮列表 (‘slower’, ‘first’, ‘previous’, ‘reverse’, ‘pause’, ‘play’, ‘next’, ‘last’, ‘faster’) | ^[list[str]]                                      | all        |
| visible_loop_options | 要显示的循环选项 ('once', 'loop', 'reflect')                        | ^[list[str]]                                      | all        |

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |
| change | 当当前值变化时触发的事件 | ^[Callable]`(event: dict) -> None` |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |
| pause | 暂停播放 | ^[Callable]`() -> None` |
| play  | 开始播放 | ^[Callable]`() -> None` |




# ToggleGroup 开关组

开关组组件允许从多个选项中切换选择，类似于`RadioButtonGroup`或`CheckButtonGroup`，但默认使用简单的切换按钮而不是按钮。

底层实现为`panel.widgets.ToggleGroup`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/ToggleGroup.html


## 基本用法

基本的开关组使用：

* ToggleGroup 作为工厂类，实例化后不可修改 widget_type 和 behavior 参数
* 所有额外参数将传递给最终生成的组件构造函数

| 属性名        | 说明                                                                 | 类型                          | 默认值      |
|-------------|--------------------------------------------------------------------|-----------------------------|------------|
| widget_type | 组件类型（可选：button-按钮型 / box-checkbox型）                           | ^[str]                      | 'button'   |
| behavior    | 交互行为（可选：check-多选模式 / radio-单选模式）                      | ^[str]                      | 'check'    |

<!-- 组件类型组合结果表 -->
| widget_type | behavior | 生成的组件类型          |
|------------|----------|-----------------------|
| button     | check    | CheckButtonGroup      |
| button     | radio    | RadioButtonGroup      |
| box        | check    | CheckBoxGroup         |
| box        | radio    | RadioBoxGroup         |

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnToggleGroup name="ToggleGroup" 
                :options="['opt1', 'opt2', 'opt3']" 
                v-model='selected.value'/>
  <p>value: {{ selected.value }}</p>
</template>
<script lang='py'>
from vuepy import ref

selected = ref([])
</script>

```


## 使用Box接口

可以设置为CheckBox样式：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnToggleGroup name="Checkbox" 
                :options="['Opt1', 'Opt2', 'Opt3']" 
                behavior="check"
                widget_type='box' />
</template>
<script lang='py'>
from vuepy import ref
</script>

```


## 垂直布局

可以设置为垂直布局：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnToggleGroup name="垂直布局" 
                :options="['选项1', '选项2', '选项3']" 
                orientation="vertical" />
</template>

```


## 使用字典选项

可以使用字典作为选项，其中键是显示的标签，值是实际的数据值：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnToggleGroup name="使用字典" 
                :options="city_options"
                v-model='selected_city.value'/>
  <p>value: {{ selected_city.value }}</p>
</template>
<script lang='py'>
from vuepy import ref

city_options = {'北京': 'BJ', '上海': 'SH', '广州': 'GZ', '深圳': 'SZ'}
selected_city = ref(['BJ'])
</script>

```


## API

### 属性

| 属性名        | 说明                 | 类型                                                | 默认值 |
| ------------ | ------------------- | -------------------------------------------------- | ------- |
| widget_type | 组件类型（可选：button-按钮型 / box-Checkbox型）                           | ^[str]                      | 'button'   |
| behavior    | 交互行为（可选：check-多选模式 / radio-单选模式）                      | ^[str]                      | 'check'    |
| options      | 选择选项             | ^[list\|dict]                                      | []      |
| value        | 当前值，多选模式下为列表 | ^[object\|list]                                    | None    |
| behavior     | 用户交互行为          | ^[str] 'radio'、'check'或'button'                   | 'radio' |
| button_style | 按钮样式（行为为button时） | ^[str] 'solid'或'outline'                        | 'solid' |
| button_type  | 按钮主题（行为为button时） | ^[str] 'default'、'primary'、'success'、'info'或'danger' | 'default' |
| disabled     | 是否禁用组件          | ^[bool]                                            | False   |
| name         | 组件标题             | ^[str]                                             | ""      |
| orientation  | 开关组方向           | ^[str] 'horizontal'或'vertical'                     | 'horizontal' |

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |
| change | 当选择变化时触发的事件 | ^[Callable]`(event: dict) -> None` |




# DateRangePicker 日期范围选择器

日期范围选择器组件允许用户使用文本框和浏览器的日期选择工具选择一个日期范围。

底层实现为`panel.widgets.DateRangePicker`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/DateRangePicker.html


## 基本用法

基本的日期范围选择器使用：

```vue
<!-- --plugins vpanel --show-code -->
<template>
 <PnColumn style='height:400px;'>
  <PnDateRangePicker name="日期范围" 
                    :value="(date(2023, 3, 1), date(2023, 3, 15))"
                    @change="on_change" />
 </PnColumn>
 <p>选择的范围: {{ selected_range.value }}</p>
</template>
<script lang='py'>
from vuepy import ref
import datetime

def date(year, month, day):
    return datetime.date(year, month, day)

selected_range = ref("")

def on_change(event):
    selected_range.value = f"{event.new[0]} 至 {event.new[1]}"
</script>

```


## 设置日期范围限制

可以设置可选日期的范围：

```vue
<!-- --plugins vpanel --show-code -->
<template>
 <PnColumn style='height:400px;'>
  <PnDateRangePicker name="范围限制" 
                    :start="date(2023, 12, 5)"
                    :end="date(2023, 12, 31)"
                    :value="(date(2023, 12, 6), date(2023, 12, 15))" />
 </PnColumn>
</template>
<script lang='py'>
import datetime

def date(year, month, day):
    return datetime.date(year, month, day)
</script>

```


## 禁用和启用特定日期

可以设置特定日期不可选或可选：

```vue
<!-- --plugins vpanel --show-code -->
<template>
 <PnColumn style='height:400px;'>
  <PnDateRangePicker name="禁用特定日期" 
                    :disabled_dates="[
                      date(2023, 3, 5),
                      date(2023, 3, 6),
                      date(2023, 3, 12),
                      date(2023, 3, 13)
                    ]"
                    :value="(date(2023, 3, 1), date(2023, 3, 15))" />
 </PnColumn>
 <PnColumn style='height:400px;'>
  <PnDateRangePicker name="启用特定日期" 
                    :enabled_dates="[
                      date(2023, 3, 1),
                      date(2023, 3, 2),
                      date(2023, 3, 3),
                      date(2023, 3, 8),
                      date(2023, 3, 9),
                      date(2023, 3, 10)
                    ]"
                    :value="(date(2023, 3, 1), date(2023, 3, 10))" />
 </PnColumn>
</template>
<script lang='py'>
import datetime

def date(year, month, day):
    return datetime.date(year, month, day)
</script>

```


## API

### 属性

| 属性名          | 说明                 | 类型                                             | 默认值 |
| -------------- | ------------------- | ------------------------------------------------ | ------- |
| value          | 选择的范围           | ^[tuple] 表示为date类型的上下限元组                | None    |
| start          | 允许选择的日期的下限   | ^[date]                                          | None    |
| end            | 允许选择的日期的上限   | ^[date]                                          | None    |
| disabled_dates | 不可选的日期          | ^[list] 日期列表                                 | None    |
| enabled_dates  | 可选的日期            | ^[list] 日期列表                                 | None    |
| allow_input    | 是否允许用户直接在输入字段中输入日期 | ^[bool]                             | False   |
| disabled       | 是否禁用组件          | ^[bool]                                          | False   |
| name           | 组件标题              | ^[str]                                           | ""      |
| visible        | 组件是否可见          | ^[bool]                                          | True    |

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |
| change | 当选择变化时触发的事件 | ^[Callable]`(event: dict) -> None` |




# Display 小组件/Output 展示器

支持 IPython 提供的所有 display tools，如`Video`、`Audio`、`HTML` 等，详情见 [rich output generated by IPython](http://ipython.readthedocs.io/en/stable/api/generated/IPython.display.html#module-IPython.display)

也可以用来集成并展示第三方组件，如 Matplotlib、Pandas、Plotly、Panel、Bokeh 等。

::: tip 
默认使用 `display` 函数（对小组件的兼容性更好）来渲染组件，但是在多进程场景 `display` 的会有[意想不到的行为](https://ipywidgets.readthedocs.io/en/latest/examples/Output%20Widget.html#interacting-with-output-widgets-from-background-threads)。在多进程场景建议使用 `multi_thread` 参数把 `Display` 的渲染函数切换为另一个实现（对小组件的兼容性没有display好）。  
:::

::: warning
当前页面只能展示组件的样式，需要在 `notebook` 才有交互效果。
:::
```vue
<!-- --plugins vpanel --show-code -->
<template>
  <p>{{ time.value }}</p>
  <PnDisplay :obj='audio' />
  <PnButton name='update' @click='on_click()' />
</template>
<script lang='py'>
from vuepy import ref
import panel as pn

audio = pn.pane.Audio('https://ccrma.stanford.edu/~jos/mp3/pno-cs.mp3', name='Audio')

time = ref(0)

def on_click():
    time.value = audio.time
</script>

```

## 展示 Matplotlib

展示 matplotlib 绘制的图，并利用布局组件进行排列。更推荐使用`PnMatplotlib`组件。
```vue
<!-- --plugins vpanel --show-code -->
<template>
  <HBox>
    <PnDisplay :obj="plt1.value"/>
  </HBox>
</template>
<script lang='py'>
import matplotlib.pyplot as plt
import numpy as np

from vuepy import ref


def plt_to_img(title, xlabel, ylabel):
    """
    plt to matplotlib.figure.Figure
    """
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    # plt.show()
    im = plt.gcf()
    plt.close()
    return im


def plt_sin():
    x = np.arange(0, 5 * np.pi, 0.1)
    y = np.sin(x)
    plt.plot(x, y, color='green')
    return plt_to_img('Sine Curve using Matplotlib', 'x', 'sin(x)')

plt1 = ref(plt_sin())
</script>

```

## 展示 PIL 图片
```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnDisplay :obj="pil_img"/>
</template>






<script lang="py">
import numpy as np
from PIL import Image

width, height = 300, 200
gradient = np.linspace(0, 255, width, dtype=np.uint8)
gradient_array = np.tile(gradient, (height, 1))

pil_img = Image.fromarray(gradient_array, 'L')
</script>

```

## 展示 Pandas Dataframe
```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnDisplay :obj="df1"/>
</template>

<script lang="py">
import pandas as pd

df1 = pd.DataFrame(data={
    'col1': ['a', 'b'],
    'col2': ['c', 'd'],
    'col3': ['e', 'f'],
})
</script>

```

## 展示 widget

利用 `Display` 组件集成基于 ipywidgets/Panel 的任意 widget。
```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnDisplay :obj="btn"/>
</template>

<script lang="py">
import panel as pn

btn = pn.widgets.Button(name='btn')
</script>

```

## Display API

### 属性

| 属性名        | 说明                 | 类型                                                           | 默认值 |
| --------     | ------------------- | ---------------------------------------------------------------| ------- |
| obj | 支持 IPython display 的对象 | ^[any]                                                         | —       |

其他属性和[Column](/panel_vuepy/layouts/Column)相同。


# FileSelector 文件选择器

文件选择器组件提供了一个用于在服务器端文件系统中选择文件或目录的界面。

底层实现为`panel.widgets.FileSelector`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/FileSelector.html


## 基本用法

基本的文件选择器使用：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnFileSelector name="选择文件"
                  directory="/Users/test"
                 @change="on_change" />
  <p>当前选择: {{ selected_file.value }}</p>
</template>
<script lang='py'>
from vuepy import ref

selected_file = ref("未选择")

def on_change(event):
    selected_file.value = event.new
</script>

```


## 显示隐藏文件

可以控制是否显示隐藏文件：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnFileSelector name="显示隐藏文件"
                  directory="/Users/test"
                  show_hidden />
</template>

```


## 文件过滤

可以通过正则表达式过滤文件：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnFileSelector name="只显示Python文件"
                  directory="/Users/test"
                  file_pattern="*.txt" />
</template>

```

## 远程文件系统

利用 [fsspec](https://filesystem-spec.readthedocs.io/en/latest/) 的强大功能，我们可以连接到远程文件系统。在下面的示例中，我们使用 s3fs 包连接到远程 S3 服务器。
```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnFileSelector :fs='fs'
                  directory="s3://datasets.holoviz.org" />
</template>
<script lang='py'>
import s3fs

fs = s3fs.S3FileSystem(anon=True)
</script>

```



## API

### 属性

| 属性名                   | 说明                 | 类型                                             | 默认值 |
| ----------------------- | ------------------- | ------------------------------------------------ | ------- |
| directory               | 当前浏览的目录       | ^[str]                                           | None    |
| fs | 文件系统 | ^[AbstractFileSystem]                                           | None    |
| file_pattern            | 用于过滤文件的正则表达式 | ^[str]                                         | None    |
| only_files | 是否只允许选择文件    | ^[bool]                                          | False   |
| root_directory          | 文件选择器的根目录     | ^[str]                                           | None    |
| show_hidden             | 是否显示隐藏文件      | ^[bool]                                          | False   |
| value                   | 当前选中的文件或目录   | ^[str\|list] 多选为list，单选为str              | None    |
| disabled                | 是否禁用组件          | ^[bool]                                          | False   |
| name                    | 组件标题              | ^[str]                                           | ""      |

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |
| change | 当选择变化时触发的事件 | ^[Callable]`(event: dict) -> None` |




# DatetimeRangeInput 日期时间范围输入框

日期时间范围输入框组件允许用户以文本形式输入日期时间范围，并使用预定义的格式解析它。

底层实现为`panel.widgets.DatetimeRangeInput`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/DatetimeRangeInput.html


## 基本用法

基本的日期时间范围输入框使用：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnDatetimeRangeInput name="日期时间范围" 
                       :value="(dt(2023, 3, 1, 8, 0), dt(2023, 3, 15, 18, 0))"
                       @change="on_change" />
  <p>当前值: {{ selected_range.value }}</p>
</template>
<script lang='py'>
from vuepy import ref
import datetime

def dt(year, month, day, hour=0, minute=0, second=0):
    return datetime.datetime(year, month, day, hour, minute, second)

selected_range = ref("未选择")

def on_change(event):
    selected_range.value = f"{event.new[0]} - {event.new[1]}"
</script>

```


## 自定义格式

可以通过format参数自定义日期时间的解析和显示格式：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnDatetimeRangeInput name="标准格式" 
                       :value="(dt(2023, 3, 1), dt(2023, 3, 15))" />
  <PnDatetimeRangeInput name="自定义格式" 
                       :value="(dt(2023, 3, 1), dt(2023, 3, 15))"
                       format="%Y年%m月%d日 %H:%M:%S" />
</template>
<script lang='py'>
import datetime

def dt(year, month, day, hour=0, minute=0, second=0):
    return datetime.datetime(year, month, day, hour, minute, second)
</script>

```


## 设置边界

可以设置日期时间的上下限：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnDatetimeRangeInput name="有范围限制" 
                       :value="(dt(2023, 2, 15), dt(2023, 3, 15))"
                       :start="dt(2023, 1, 1)"
                       :end="dt(2023, 12, 31)" />
</template>
<script lang='py'>
import datetime

def dt(year, month, day, hour=0, minute=0, second=0):
    return datetime.datetime(year, month, day, hour, minute, second)
</script>

```


## API

### 属性

| 属性名    | 说明                 | 类型                                             | 默认值 |
| -------- | ------------------- | ------------------------------------------------ | ------- |
| start    | 日期时间下限          | ^[datetime]                                     | None    |
| end      | 日期时间上限          | ^[datetime]                                     | None    |
| value    | 解析后的日期时间范围值 | ^[tuple] 以datetime类型的(start, end)表示的元组   | None    |
| disabled | 是否禁用组件          | ^[bool]                                         | False   |
| format   | 日期时间格式字符串     | ^[str]                                          | '%Y-%m-%d %H:%M:%S' |
| name     | 组件标题              | ^[str]                                          | ""      |

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |
| change | 当输入值变化时触发的事件 | ^[Callable]`(event: dict) -> None` |




# Terminal 终端

终端组件提供了一个与底层命令行交互的终端界面。它基于xterm.js，并通过WebSocket连接到服务器端的虚拟终端。

底层实现为`panel.widgets.Terminal`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/Terminal.html


## 基本用法

创建一个基本的终端界面：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnTerminal 
    output="Welcome to the Panel Terminal!\nI'm based on xterm.js\n\n"
    :height="300" sizing_mode='stretch_width'/>
</template>
<script lang='py'>
from vuepy import ref
</script>

```


## 自定义参数

可以设置各种终端参数，如字体大小、是否显示光标等：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnTerminal :height='200' :width='300' output='> hello'
              :options="{
               'cursorBlink': True,
               'fontSize': 18,
               'theme': {
                 'background': '#42b883',
                 'foreground': '#f8f8f8'
               }
             }" />
</template>
<script lang='py'>
from vuepy import ref
</script>

```


## 交互处理

终端还可以通过命令随时更新：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnRow>
    <PnButton name="run python" @click="run_py()" />
    <PnButton name="clear" @click="clear_term()" />
  </PnRow>
  <PnTerminal output='>>> Python 3.10.12' ref='terminal'
             :height='300' sizing_mode='stretch_width'/>
</template>
<script lang='py'>
from vuepy import ref, onMounted

terminal = ref(None)

def run_py():
    if terminal.value:
        t = terminal.value.unwrap()
        if t.subprocess.running:
            return
        # t.subprocess.run("python", "-c", 'print(\"Hello from Python!\")')
        t.subprocess.run("python")

def clear_term():
    if terminal.value:
        t = terminal.value.unwrap()
        t.subprocess.kill()
        t.clear()

@onMounted
def run():
    run_py()
</script>

```


## API

### 属性

| 属性名          | 说明                 | 类型                          | 默认值 |
| -------------- | ------------------- | ----------------------------- | ------ |
| output         | 终端目前的输出内容     | ^[str]                        | ""     |
| options        | 传递给终端后端的选项   | ^[dict]                       | None   |
| disabled       | 是否禁用组件          | ^[bool]                       | False  |
| name           | 组件标题              | ^[str]                        | ""     |

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |
| change | 当终端内容变化时触发   | ^[Callable]`(event: dict) -> None` |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |
| clear | 清空终端内容 | ^[Callable]`() -> None` |
| write | 向终端写入内容 | ^[Callable]`(content: str) -> None` |
| subprocess.run | 运行命令子进程 | ^[Callable]`(command: List[str]) -> None` |
| subprocess.kill | 杀死命令子进程 | |




# FloatSlider 浮点滑块

浮点滑块组件允许使用滑块在设定范围内选择浮点数值。

底层实现为`panel.widgets.FloatSlider`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/FloatSlider.html


## 基本用法

基本的浮点滑块使用：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnFloatSlider name="浮点滑块" 
                :start="0" 
                :end="3.141" 
                :step="0.01" 
                v-model="value.value" />
</template>
<script lang='py'>
from vuepy import ref

value = ref(1.57)
</script>

```


## 自定义格式

可以使用自定义格式字符串或Bokeh TickFormatter来格式化滑块值：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnFloatSlider name="距离（字符串格式）" 
                format="1[.]00"
                :start="0" 
                :end="10" 
                v-model="value1.value" />
  <PnFloatSlider name="距离（格式化器）" 
                :format="tick_formatter"
                :start="0" 
                :end="10" 
                v-model="value2.value" />
</template>
<script lang='py'>
from vuepy import ref
from bokeh.models.formatters import PrintfTickFormatter

value1 = ref(5)
value2 = ref(5)
tick_formatter = PrintfTickFormatter(format='%.3f 米')
</script>

```


## 垂直方向

滑块可以设置为垂直方向显示：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnRow>
    <PnFloatSlider name="水平滑块" 
                  orientation="horizontal"
                  :start="0" 
                  :end="10" 
                  :value="5"
                  :width="300" />
    <PnFloatSlider name="垂直滑块" 
                  orientation="vertical"
                  :start="0" 
                  :end="10" 
                  :value="5"
                  :height="300" />
  </PnRow>
</template>
<script lang='py'>
from vuepy import ref
</script>

```


## 滑块颜色和方向

可以自定义滑块条的颜色和方向：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnFloatSlider name="蓝色滑块" 
                bar_color="#3498db"
                :start="0" 
                :end="10" 
                :value="5" />
  <PnFloatSlider name="绿色滑块" 
                bar_color="#2ecc71"
                :start="0" 
                :end="10" 
                :value="5" />
  <PnFloatSlider name="从右到左" 
                direction="rtl"
                :start="0" 
                :end="10" 
                :value="5" />
</template>
<script lang='py'>
from vuepy import ref
</script>

```


## API

### 属性

| 属性名          | 说明                           | 类型                                | 默认值     |
| -------------- | ------------------------------ | ---------------------------------- | --------- |
| start          | 范围的下限                     | ^[float]                           | 0.0       |
| end            | 范围的上限                     | ^[float]                           | 1.0       |
| step           | 值之间的间隔                   | ^[float]                           | 0.1       |
| value          | 所选的值                       | ^[float]                           | 0.0       |
| value_throttled| 鼠标释放前阻止的所选值          | ^[float]                           | 0.0       |
| bar_color      | 滑块条的颜色，十六进制RGB值      | ^[str]                             | None      |
| direction      | 滑块方向，从左到右('ltr')或从右到左('rtl') | ^[str]                    | 'ltr'     |
| disabled       | 是否禁用                       | ^[bool]                            | False     |
| format         | 应用于滑块值的格式化器           | ^[str\|bokeh.models.TickFormatter] | None      |
| name           | 组件标题                       | ^[str]                             | ""        |
| orientation    | 滑块的显示方向，'horizontal'或'vertical' | ^[str]                    | 'horizontal' |
| tooltips       | 是否在滑块手柄上显示工具提示      | ^[bool]                           | True      |

### Events

| 事件名         | 说明                       | 类型                                   |
| ------------- | -------------------------- | -------------------------------------- |
| change        | 当值更改时触发的事件         | ^[Callable]`(value) -> None`          |




# IntInput 整数输入框

整数输入框组件允许输入整数值，可以通过箭头按钮调整或直接输入数值。

底层实现为`panel.widgets.IntInput`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/IntInput.html


## 基本用法

基本的整数输入框使用：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnIntInput name="数量" 
              v-model="i.value" />
</template>
<script lang='py'>
from vuepy import ref

i = ref(0)
</script>

```


## 范围限制

可以使用`start`和`end`参数设定值的范围：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnIntInput name="评分 (1-10)" 
              :start="1"
              :end="10"
              v-model="i.value" />
</template>
<script lang='py'>
from vuepy import ref

i = ref(5)
</script>

```


## 自定义步长

可以使用`step`参数定义上下调整时的步进值：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnIntInput name="调整(步长10)" 
              :value="10"
              :step="10"
              v-model="i.value" />
</template>
<script lang='py'>
from vuepy import ref

i = ref(10)
</script>

```


## API

### 属性

| 属性名          | 说明                           | 类型                                | 默认值     |
| -------------- | ------------------------------ | ---------------------------------- | --------- |
| start          | 最小允许值                     | ^[int\|None]                       | None      |
| end            | 最大允许值                     | ^[int\|None]                       | None      |
| step           | 调整值的步长                   | ^[int]                             | 1         |
| value          | 当前输入的整数值               | ^[int]                             | 0         |
| disabled       | 是否禁用                       | ^[bool]                            | False     |
| name           | 组件标题                       | ^[str]                             | ""        |
| placeholder    | 输入框占位文本                 | ^[str]                             | ""        |
| description    | 鼠标悬停时显示的描述           | ^[str]                             | ""        |

### Events

| 事件名         | 说明                       | 类型                                   |
| ------------- | -------------------------- | -------------------------------------- |
| change        | 当值更改时触发的事件         | ^[Callable]`(value) -> None`          |




# MenuButton 菜单按钮

菜单按钮组件允许指定一个菜单项列表供用户选择，当点击菜单项时触发事件。与其他组件不同，它没有`value`参数，而是有一个`clicked`参数，可以通过监听此参数来触发事件，该参数报告最后点击的菜单项。

底层实现为`panel.widgets.MenuButton`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/MenuButton.html


## 基本用法

基本的菜单按钮使用，定义按钮名称和菜单项列表：菜单项可以是单个字符串或元组，用None分隔为不同组。

```vue
<!-- --plugins vpanel --show-code -->
<template>
 <PnCol :height='200'>
  <PnMenuButton name="Dropdown" 
               :items="menu_items" 
               button_type="primary" 
               @click="on_click" />
 </PnCol>
 <p>value: {{ clicked_item.value }}</p>
</template>
<script lang='py'>
from vuepy import ref

menu_items = [
    ('A', 'a'), 
    ('B', 'b'), 
    ('C', 'c'), 
    None, 
    ('Help', 'help'),
]
clicked_item = ref("")

def on_click(event):
    clicked_item.value = event.new
</script>

```


## 分离式菜单

可以使用`split`选项将下拉指示器移动到单独的区域：

在`split`模式下，如果点击按钮本身，将报告`name`参数的值。
```vue
<!-- --plugins vpanel --show-code -->
<template>
 <PnCol :height='200'>
  <PnMenuButton name="Split Menu" 
               :split="True"
               :items="menu_items" 
               button_type="primary" 
               @click="on_click" />
 </PnCol>
 <p>value: {{ clicked_item.value }}</p>
</template>
<script lang='py'>
from vuepy import ref

menu_items = [
    ('A', 'a'), 
    ('B', 'b'), 
    ('C', 'c'), 
    None, 
    ('Help', 'help'),
]
clicked_item = ref("")

def on_click(event):
    clicked_item.value = event.new # Split Menu, a, b, c
</script>

```


## 按钮样式

可以通过设置`button_type`来改变按钮的颜色：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnCol>
    <PnMenuButton v-for="type in button_types" 
                 :name="type" 
                 :button_type="type"
                 :items="menu_items" />
  </PnCol>
</template>
<script lang='py'>
from vuepy import ref

menu_items = [('A', 'a'), ('B', 'b'), ('C', 'c')]
button_types = ['default', 'primary', 'success', 'warning', 'light', 'danger']
</script>

```


## 图标

菜单按钮的名称和菜单项可以包含Unicode字符和表情符号，为常见的图形按钮提供了一种便捷的方式：

```vue
<!-- --plugins vpanel --show-code -->
<template>
 <PnCol style='height: 200px'>
  <PnRow style="border-bottom: 1px solid black">
    <PnMenuButton name="File" 
                 icon="file" 
                 :items="file_items" 
                 :width="75" 
                 button_type="light" />
    <PnMenuButton name="🧏🏻‍♂️ Help" 
                 :items="help_items" 
                 :width="100" 
                 button_type="light" />
  </PnRow>
 </PnCol>
</template>
<script lang='py'>
from vuepy import ref

file_items = ["\U0001F4BE Save", "🚪 Exit"]
help_items = ["⚖️ License", None, "\U0001F6C8 About"]
</script>

```


对于按钮本身，可以通过提供SVG `icon`值或从[tabler-icons.io](https://tabler-icons.io)加载的命名`icon`来使用更高级的图标：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnRow>
    <PnMenuButton icon="alert-triangle-filled" 
                  button_type="warning" 
                  :items="['Confirm']">Warning</PnMenuButton>
    <PnMenuButton name="Error" 
                  icon="bug" 
                  button_type="danger" 
                  :items="['Retry']" />
    <PnMenuButton name="Payment" 
                  button_type="success" 
                  icon_size="1.5em"
                  :items="['WeChat']">
     <template #icon>
       <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-cash" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
         <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
         <path d="M7 9m0 2a2 2 0 0 1 2 -2h10a2 2 0 0 1 2 2v6a2 2 0 0 1 -2 2h-10a2 2 0 0 1 -2 -2z" />
         <path d="M14 14m-2 0a2 2 0 1 0 4 0a2 2 0 1 0 -4 0" />
         <path d="M17 9v-2a2 2 0 0 0 -2 -2h-10a2 2 0 0 0 -2 2v6a2 2 0 0 0 2 2h2" />
       </svg>
     </template>
    </PnMenuButton>
  </PnRow>
</template>

```


## API

### 属性

| 属性名        | 说明                 | 类型                                                | 默认值 |
| ------------ | ------------------- | -------------------------------------------------- | ------- |
| clicked      | 最后点击的菜单项      | ^[str]                                             | None    |
| items        | 下拉菜单中的菜单项，允许字符串、(标题,值)形式的元组或者None分隔组允许字符串、(标题,值)形式的元组或者None分隔组    | ^[list] | []      |
| split        | 是否为按钮添加单独的下拉区域 | ^[bool]                                      | False   |
| button_style | 按钮样式，'solid'或'outline'  | ^[str]                           | 'solid' |
| button_type  | 按钮主题:'default'、'primary'、'success'、'warning'、'light'或'danger'              | ^[str]  | 'default' |
| icon         | 按钮左侧的图标，SVG字符串或tabler-icons.io图标名称         | ^[str]           | None    |
| icon_size    | 图标大小，如"12px"或"1em"               | ^[str]                            | None    |
| disabled     | 是否禁用组件          | ^[bool]                                            | False   |
| name         | 按钮标题              | ^[str]                                             | ""      |

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |
| click | 当菜单项被点击时触发的事件 | ^[Callable]`(event: dict) -> None` |




# DatetimeRangePicker 日期时间范围选择器

日期时间范围选择器组件允许使用文本框和浏览器的日期时间选择工具选择日期时间范围。

底层实现为`panel.widgets.DatetimeRangePicker`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/DatetimeRangePicker.html


## 基本用法

基本的日期时间范围选择器使用：

```vue
<!-- --plugins vpanel --show-code -->
<template>
 <PnColumn style='height:400px;'>
  <PnDatetimeRangePicker 
    name="日期时间范围" v-model="selected_range.value"/>
 </PnColumn>
 <p>选择的范围: {{ selected_range.value }}</p>
</template>
<script lang='py'>
from vuepy import ref
import datetime

def dt(year, month, day, hour=0, minute=0, second=0):
    return datetime.datetime(year, month, day, hour, minute, second)

selected_range = ref((dt(2023, 3, 2, 12, 10), dt(2023, 3, 2, 12, 22)))

</script>

```


## 设置日期范围限制

可以设置可选日期的范围：

```vue
<!-- --plugins vpanel --show-code -->
<template>
 <PnColumn style='height:400px;'>
  <PnDatetimeRangePicker name="范围限制" 
                        :start="dt(2023, 12, 10)"
                        :end="dt(2023, 12, 31)"
                        :value="(dt(2023, 12, 11), dt(2023, 12, 15))" />
 </PnColumn>
</template>
<script lang='py'>
import datetime

def dt(year, month, day, hour=0, minute=0, second=0):
    return datetime.datetime(year, month, day, hour, minute, second)
</script>

```


## 禁用和启用特定日期

可以设置特定日期不可选或可选：**注意**是`datetime.date`类型。

```vue
<!-- --plugins vpanel --show-code -->
<template>
 <PnColumn style='height:400px;'>
  <PnDatetimeRangePicker name="禁用特定日期" 
                        :value='(date(2023, 3, 8), date(2023, 3, 10))'
                        :disabled_dates="disabled"/>
 </PnColumn>
 <PnColumn style='height:400px;'>
  <PnDatetimeRangePicker name="启用特定日期" 
                        :value='(date(2023, 3, 1), date(2023, 3, 2))'
                        :enabled_dates="enabled" />
 </PnColumn>
</template>
<script lang='py'>
import datetime

def date(year, month, day):
    return datetime.date(year, month, day)
    
disabled = [
  date(2023, 3, 5),
  date(2023, 3, 6),
  date(2023, 3, 12),
  date(2023, 3, 13)
]
enabled = [
  date(2023, 3, 1),
  date(2023, 3, 2),
  date(2023, 3, 10)
]
</script>

```


## 时间格式设置

可以控制时间显示和编辑的方式：

```vue
<!-- --plugins vpanel --show-code -->
<template>
 <PnCol style='height:400px;'>
  <PnDatetimeRangePicker name="不显示时间" 
                        :enable_time="False"
                        :value="(dt(2023, 3, 1), dt(2023, 3, 15))" />
  
 </PnCol>
 <PnCol style='height:400px;'>
  <PnDatetimeRangePicker name="不显示秒" 
                        :enable_seconds="False"
                        :value="(dt(2023, 3, 1, 12, 30), dt(2023, 3, 15, 18, 45))" />
  
 </PnCol>
 <PnColumn style='height:400px;'>
  <PnDatetimeRangePicker name="12小时制" 
                        :military_time="False"
                        :value="(dt(2023, 3, 1, 13, 30), dt(2023, 3, 15, 15, 45))" />
 </PnCol>
</template>
<script lang='py'>
import datetime

def dt(year, month, day, hour=0, minute=0, second=0):
    return datetime.datetime(year, month, day, hour, minute, second)
</script>

```


## API

### 属性

| 属性名          | 说明                 | 类型                                             | 默认值 |
| -------------- | ------------------- | ------------------------------------------------ | ------- |
| value          | 选择的范围           | ^[tuple] 表示为datetime类型的上下限元组           | None    |
| start          | 允许选择的日期的下限   | ^[datetime]                                     | None    |
| end            | 允许选择的日期的上限   | ^[datetime]                                     | None    |
| disabled_dates | 不可选的日期          | ^[list] 日期列表                                 | None    |
| enabled_dates  | 可选的日期            | ^[list] 日期列表                                 | None    |
| enable_time    | 是否启用时间编辑       | ^[bool]                                         | True    |
| enable_seconds | 是否启用秒编辑         | ^[bool]                                         | True    |
| military_time  | 是否使用24小时制显示时间 | ^[bool]                                         | True    |
| allow_input    | 是否允许用户直接在输入字段中输入日期 | ^[bool]                             | False   |
| disabled       | 是否禁用组件          | ^[bool]                                          | False   |
| name           | 组件标题              | ^[str]                                           | ""      |
| visible        | 组件是否可见          | ^[bool]                                          | True    |

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |
| change | 当选择变化时触发的事件 | ^[Callable]`(event: dict) -> None` |




# CheckButtonGroup 多选按钮组

多选按钮组组件允许通过切换相应的按钮来选择多个选项。它属于多选项选择组件的广泛类别，提供兼容的API，包括[``MultiSelect``](MultiSelect.md)、[``CrossSelector``](CrossSelector.md)和[``CheckBoxGroup``](CheckBoxGroup.md)组件。

底层实现为`panel.widgets.CheckButtonGroup`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/CheckButtonGroup.html


## 基本用法

基本的多选按钮组使用：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnCheckButtonGroup name="水果选择" 
                     :value="['苹果', '梨']"
                     :options="['苹果', '香蕉', '梨', '草莓']"
                     @change="on_change" />
  <div>当前选择: {{ selected.value }}</div>
</template>
<script lang='py'>
from vuepy import ref

selected = ref(["苹果", "梨"])

def on_change(event):
    selected.value = event['new']
</script>

```


## 垂直方向

可以将按钮组设置为垂直方向：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnCheckButtonGroup name="水果选择" 
                     :value="['苹果']"
                     :options="['苹果', '香蕉', '梨', '草莓']"
                     button_type="primary"
                     orientation="vertical" />
</template>
<script lang='py'>
from vuepy import ref
</script>

```


## 使用字典选项

可以使用字典作为选项，其中键是显示的标签，值是实际的数据值：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnCheckButtonGroup name="城市选择" 
                     :options="city_options"
                     :value="['BJ', 'SZ']"
                     v-model="selected_cities.value" />
  <div>选中城市代码: {{ selected_cities.value }}</div>
</template>
<script lang='py'>
from vuepy import ref

city_options = {'北京': 'BJ', '上海': 'SH', '广州': 'GZ', '深圳': 'SZ'}
selected_cities = ref(['BJ', 'SZ'])
</script>

```


## 按钮样式

可以通过设置`button_type`和`button_style`来改变按钮的外观：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnRow>
    <PnCol v-for="style in ['solid', 'outline']">
      <PnCheckButtonGroup v-for="type in button_types" 
                         :name="type"
                         :button_type="type"
                         :button_style="style"
                         :options="['选项1', '选项2', '选项3']"
                         :value="['选项2']" />
    </PnCol>
  </PnRow>
</template>
<script lang='py'>
from vuepy import ref

button_types = ['default', 'primary', 'success', 'warning', 'danger', 'light']
</script>

```


## API

### 属性

| 属性名        | 说明                 | 类型                                                | 默认值 |
| ------------ | ------------------- | -------------------------------------------------- | ------- |
| options      | 选择选项             | ^[list\|dict]                                      | []      |
| value        | 当前值，多个选中项的列表 | ^[list]                                            | []      |
| button_style | 按钮样式             | ^[str] 'solid'或'outline'                           | 'solid' |
| button_type  | 按钮主题             | ^[str] 'default'、'primary'、'success'、'info'或'danger' | 'default' |
| description  | 鼠标悬停时显示的描述   | ^[str]                                             | ""      |
| disabled     | 是否禁用组件          | ^[bool]                                            | False   |
| name         | 组件标题             | ^[str]                                             | ""      |
| orientation  | 按钮组方向           | ^[str] 'horizontal'或'vertical'                     | 'horizontal' |

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |
| change | 当选择变化时触发的事件 | ^[Callable]`(event: dict) -> None` |




# RadioButtonGroup 单选按钮组

单选按钮组组件允许使用一组切换按钮从列表或字典中选择一个值。它属于单值选项选择组件的广泛类别，提供兼容的API，包括[``RadioBoxGroup``](RadioBoxGroup.md)、[``Select``](Select.md)和[``DiscreteSlider``](DiscreteSlider.md)组件。

底层实现为`panel.widgets.RadioButtonGroup`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/RadioButtonGroup.html


## 基本用法

基本的单选按钮组使用：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnRadioButtonGroup name="RadioButtonGroup" 
                     :options="['Apple', 'Orange', 'Banana']" 
                     v-model="selected.value"
                     button_type="success"
                     @change="on_change" />
  <p>value: {{ selected.value }}</p>
</template>
<script lang='py'>
from vuepy import ref

selected = ref('Apple')

def on_change(event):
    print(event.new)
</script>

```


## 垂直方向

可以将按钮组设置为垂直方向：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnRadioButtonGroup button_type="primary"
                     :options="['Apple', 'Orange', 'Banana']" 
                     orientation="vertical" />
</template>

```


## 使用字典选项

可以使用字典作为选项，其中键是显示的标签，值是实际的数据值：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnRadioButtonGroup name="RadioButtonGroup" 
                     :options="city_options"
                     button_type="warning"
                     v-model="selected_city.value" />
  <p>value: {{ selected_city.value }}</p>
</template>
<script lang='py'>
from vuepy import ref

city_options = {'Beijing': 'BJ', 'Shanghai': 'SH', 'Guangzhou': 'GZ'}
selected_city = ref('BJ')
</script>

```


## 按钮样式

可以通过设置`button_type`和`button_style`来改变按钮的外观：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnRow>
    <PnCol v-for="style in ['solid', 'outline']">
      <PnRadioButtonGroup v-for="type in button_types" 
                         :name="type"
                         :button_type="type"
                         :button_style="style"
                         :options="['opt1', 'opt2', 'opt3']"
                         value="opt2" />
    </PnCol>
  </PnRow>
</template>
<script lang='py'>
from vuepy import ref

button_types = ['default', 'primary', 'success', 'warning', 'danger', 'light']
</script>

```


## API

### 属性

| 属性名        | 说明                 | 类型                                                | 默认值 |
| ------------ | ------------------- | -------------------------------------------------- | ------- |
| options      | 选择选项             | ^[list\|dict]                                      | []      |
| value        | 当前值，必须是选项值之一 | ^[object]                                          | None    |
| button_style | 按钮样式             | ^[str] 'solid'或'outline'                           | 'solid' |
| button_type  | 按钮主题             | ^[str] 'default'、'primary'、'success'、'info'或'danger' | 'default' |
| description  | 鼠标悬停时显示的描述   | ^[str]                                             | ""      |
| disabled     | 是否禁用组件          | ^[bool]                                            | False   |
| name         | 组件标题             | ^[str]                                             | ""      |
| orientation  | 按钮组方向           | ^[str] 'horizontal'或'vertical'                     | 'horizontal' |

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |
| change | 当选择变化时触发的事件 | ^[Callable]`(event: dict) -> None` |




# RangeSlider 范围滑块

范围滑块组件允许使用带有两个手柄的滑块选择整数范围。

底层实现为`panel.widgets.RangeSlider`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/RangeSlider.html


## 基本用法

基本的范围滑块，通过拖动两个手柄选择一个范围：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnRangeSlider name="RangeSlider" 
                :start="0" 
                :end="100" 
                v-model="value.value"
                :step="1" />
  <p>value: {{ value.value }}</p>
</template>
<script lang='py'>
from vuepy import ref

value = ref((25, 75))

</script>

```


## 自定义格式

可以使用自定义格式字符串或Bokeh TickFormatter来格式化滑块值：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnRangeSlider name="Price" 
                format="$%d"
                :start="0" 
                :end="1000" 
                v-model="value.value"
                :step="100" />
  <p>value: {{ value.value }}</p>
</template>
<script lang='py'>
from vuepy import ref

value = ref((200, 800))
</script>

```


## 垂直方向

滑块可以设置为垂直方向显示：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnRow>
    <PnRangeSlider name="垂直" 
                  orientation="vertical"
                  :start="0" 
                  :end="100" 
                  :value="(30, 70)"
                  :height="300" />
  </PnRow>
</template>

```


## 滑块颜色和方向

可以自定义滑块条的颜色和方向：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnRangeSlider name="Blue RangeSlider" 
                bar_color="#3498db"
                :start="0" 
                :end="100" 
                :value="(20, 80)" />
  <PnRangeSlider name="Right to Left" 
                direction="rtl"
                :start="0" 
                :end="100" 
                :value="(20, 80)" />
</template>
<script lang='py'>
from vuepy import ref
</script>

```


## API

### 属性

| 属性名          | 说明                           | 类型                                | 默认值     |
| -------------- | ------------------------------ | ---------------------------------- | --------- |
| start          | 范围的下限                     | ^[int]                             | 0         |
| end            | 范围的上限                     | ^[int]                             | 1         |
| step           | 值之间的间隔                   | ^[int]                             | 1         |
| value          | 所选范围的上下界元组            | ^[(int, int)]                       | (0, 1)    |
| value_throttled| 鼠标释放前阻止的所选范围的上下界元组 | ^[(int, int)]                    | (0, 1)    |
| bar_color      | 滑块条的颜色，十六进制RGB值      | ^[str]                             | None      |
| direction      | 滑块方向，从左到右('ltr')或从右到左('rtl') | ^[str]                    | 'ltr'     |
| disabled       | 是否禁用                       | ^[bool]                            | False     |
| format         | 应用于滑块值的格式化器           | ^[str\|bokeh.models.TickFormatter] | None      |
| name           | 组件标题                       | ^[str]                             | ""        |
| orientation    | 滑块的显示方向，'horizontal'或'vertical' | ^[str]                    | 'horizontal' |
| tooltips       | 是否在滑块手柄上显示工具提示      | ^[bool]                           | True      |

### Events

| 事件名         | 说明                       | 类型                                   |
| ------------- | -------------------------- | -------------------------------------- |
| change        | 当值更改时触发的事件         | ^[Callable]`(value) -> None`          |




# FloatInput 浮点输入框

浮点输入框组件允许输入浮点数值，可以通过箭头按钮调整或直接输入数值。

底层实现为`panel.widgets.FloatInput`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/FloatInput.html


## 基本用法

基本的浮点数输入框使用：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnFloatInput name="数值" 
               v-model="f.value" />
  <p>当前值: {{ f.value }} </p>
</template>
<script lang='py'>
from vuepy import ref

f = ref(0.0)
</script>

```


## 范围限制

可以使用`start`和`end`参数设定值的范围：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnFloatInput name="温度 (-10.0 到 50.0)" 
               :value="25.5"
               :start="-10.0"
               :end="50.0"
               v-model="f.value" />
  <p>当前温度: {{ f.value }}</p>
</template>
<script lang='py'>
from vuepy import ref

f = ref(25.5)
</script>

```


## 自定义步长

可以使用`step`参数定义上下调整时的步进值：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnFloatInput name="调整(步长0.1)" 
               :value="1.0"
               :step="2"
               v-model="f.value" />
</template>
<script lang='py'>
from vuepy import ref

f = ref(1.0)
</script>

```


## API

### 属性

| 属性名               | 说明                                                                 | 类型                          | 默认值  |
|---------------------|--------------------------------------------------------------------|-----------------------------|--------|
| value               | 当前值（按回车、失去焦点、点击箭头或键盘操作时更新，删除所有数字可能返回None） | ^[float｜None]              | None   |
| value_throttled     | 只读属性，行为与value相同                                            | ^[float｜None]              | None   |
| step                | 每次点击增加或减少的步长值                                            | ^[float]                    | 1.0    |
| start               | 可选的最小允许值                                                     | ^[float]                    | None   |
| end                 | 可选的最大允许值                                                     | ^[float]                    | None   |
| format              | 数值格式化字符串（参考numbrojs格式）                                  | ^[str]                      | ""     |
| page_step_multiplier | 按下PgUp/PgDown键时的步长乘数                                         | ^[int]                      | 10     |
| disabled            | 是否禁用编辑                                                        | ^[bool]                     | False  |
| name                | 控件标题                                                           | ^[str]                      | ""     |
| placeholder         | 未输入值时显示的占位文本                                             | ^[str]                      | ""     |

### Events

| 事件名         | 说明                       | 类型                                   |
| ------------- | -------------------------- | -------------------------------------- |
| change        | 当值更改时触发的事件         | ^[Callable]`(value) -> None`          |




# FileDownload 文件下载

文件下载组件允许在前端下载文件，通过在初始化时（如果`embed=True`）或点击按钮时将文件数据发送到浏览器。

底层实现为`panel.widgets.FileDownload`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/FileDownload.html


## 基本用法

基本的文件下载组件使用，默认情况下（`auto=True`和`embed=False`）文件只在按钮被点击后才传输到浏览器：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnFileDownload file="FileDownload.ipynb" 
                 filename="FileDownload.ipynb" />
</template>

```

## 嵌入文件数据

可以通过`embed`参数立即嵌入文件数据，这允许在静态导出中使用此组件：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnFileDownload file="FileDownload.ipynb" 
                 filename="FileDownload.ipynb"
                 embed />
</template>
<script lang='py'>
from vuepy import ref
</script>

```


## 手动保存

如果设置`auto=False`，文件不会在初次点击时下载，而是会在数据同步后将标签从"Transfer<文件>"更改为"Download<文件>"。这样可以在数据传输后使用"另存为"对话框下载。

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnFileDownload file="FileDownload.ipynb" 
                 filename="FileDownload.ipynb"
                 :auto="False"
                 button_type="success"
                 name="右键点击使用'另存为'对话框下载" />
</template>
<script lang='py'>
from vuepy import ref
</script>

```


## 使用文件对象

文件下载组件也可以接受文件对象，例如将`pandas DataFrame`保存为`CSV`到`StringIO`对象：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnFileDownload :file="file_obj" 
                 filename="data.csv"
                 embed />
</template>
<script lang='py'>
from vuepy import ref
from io import StringIO
import pandas as pd

# 创建示例数据
data = {'名称': ['张三', '李四', '王五'],
        '年龄': [28, 32, 45],
        '城市': ['北京', '上海', '广州']}
df = pd.DataFrame(data)

sio = StringIO()
df.to_csv(sio, index=False)
sio.seek(0)
file_obj = sio
</script>

```


## 动态生成文件

可以提供回调函数动态生成文件，例如根据某些小部件的参数：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnFileDownload :file="filtered_file()" 
                 filename="filtered_data.csv" />
  <PnRow :height=400>
    <PnMultiChoice name="选择年份" :options="years" v-model="selected_years.value" />
    <PnRangeSlider name="里程范围" :start="min_mpg" :end="max_mpg" v-model="mpg_range.value" />
  </PnRow>
</template>
<script lang='py'>
from vuepy import ref
from io import StringIO
import pandas as pd

# 创建示例数据
years_list = [2018, 2019, 2020, 2021, 2022]
mpg_data = []
for year in years_list:
    for i in range(10):
        mpg_data.append({'年份': year, '里程': 10 + i * 5})
df = pd.DataFrame(mpg_data)

min_mpg = df['里程'].min()
max_mpg = df['里程'].max()
years = years_list

selected_years = ref([years[0]])
mpg_range = ref((min_mpg, max_mpg))


def filtered_file():
    filtered = df
    if selected_years.value:
        filtered = filtered[filtered['年份'].isin(selected_years.value)]
    filtered = filtered[(filtered['里程'] >= mpg_range.value[0]) & 
                        (filtered['里程'] <= mpg_range.value[1])]
    
    sio = StringIO()
    filtered.to_csv(sio, index=False)
    sio.seek(0)
    print('update file')
    return sio
</script>

```


## 按钮样式

可以通过设置`button_type`和`button_style`来改变文件下载按钮的外观：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnRow>
    <PnCol v-for="style in ['solid', 'outline']">
      <PnFileDownload v-for="type in button_types" 
                     :button_type="type"
                     :button_style="style"
                     file="FileDownload.ipynb" 
                     :label="type + '-' + style"
                     style="margin: 5px" />
    </PnCol>
  </PnRow>
</template>
<script lang='py'>
from vuepy import ref

button_types = ['default', 'primary', 'success', 'warning', 'light', 'danger']
</script>

```


## 图标按钮

与其他按钮一样，可以提供显式的`icon`，可以是tabler-icons.io的命名图标：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnRow>
    <PnFileDownload icon="alert-triangle-filled" 
                   button_type="warning" 
                   file="FileDownload.ipynb" />
    <PnFileDownload icon="bug" 
                   button_type="danger" 
                   file="FileDownload.ipynb" />
  </PnRow>
</template>
<script lang='py'>
from vuepy import ref
</script>

```


也可以是显式的SVG：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnFileDownload  button_type="success" 
                   icon_size="2em" 
                   file="FileDownload.ipynb">
    <template #icon>
      <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-cash" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
        <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
        <path d="M7 9m0 2a2 2 0 0 1 2 -2h10a2 2 0 0 1 2 2v6a2 2 0 0 1 -2 2h-10a2 2 0 0 1 -2 -2z" />
        <path d="M14 14m-2 0a2 2 0 1 0 4 0a2 2 0 1 0 -4 0" />
        <path d="M17 9v-2a2 2 0 0 0 -2 -2h-10a2 2 0 0 0 -2 2v6a2 2 0 0 0 2 2h2" />
      </svg>
    </template>
  </PnFileDownload>
</template>

```


## API

### 属性

| 属性名        | 说明                 | 类型                                                | 默认值 |
| ------------ | ------------------- | -------------------------------------------------- | ------- |
| auto         | 是否在第一次点击时下载文件 | ^[bool]                                           | True    |
| callback     | 返回文件或类文件对象的可调用对象 | ^[callable]                                  | None    |
| embed        | 是否在初始化时嵌入数据    | ^[bool]                                           | False   |
| file         | 文件路径或类文件对象      | ^[str\|Path\|file-like]                           | None    |
| filename     | 保存文件的文件名        | ^[str]                                             | None    |
| button_style | 按钮样式              | ^[str] 'solid'或'outline'                          | 'solid' |
| button_type  | 按钮主题              | ^[str] 'default'、'primary'、'success'、'info'、'light'或'danger' | 'default' |
| icon         | 按钮左侧的图标         | ^[str] SVG字符串或tabler-icons.io图标名称           | None    |
| icon_size    | 图标大小              | ^[str] 如"12px"或"1em"                             | None    |
| label        | 下载按钮的自定义标签     | ^[str]                                             | None    |
| name         | 组件标题              | ^[str]                                             | ""      |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
|   icon      |          svg 图标         |




# DatetimeInput 日期时间输入框

日期时间输入框组件允许以文本形式输入日期时间值，并使用预定义的格式解析它。

底层实现为`panel.widgets.DatetimeInput`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/DatetimeInput.html


## 基本用法

基本的日期时间输入框使用：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnDatetimeInput name="日期时间输入" 
                  v-model="selected_datetime.value"/>
  <p>当前值: {{ selected_datetime.value }}</p>
</template>
<script lang='py'>
from vuepy import ref
import datetime

def dt(year, month, day, hour=0, minute=0, second=0):
    return datetime.datetime(year, month, day, hour, minute, second)

selected_datetime = ref(dt(2023, 2, 8))
</script>

```

## 自定义格式

可以通过format参数自定义日期时间的解析和显示格式：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnDatetimeInput name="标准格式" 
                  :value="dt(2023, 2, 8)" />
  <PnDatetimeInput name="自定义格式" 
                  :value="dt(2023, 2, 8)"
                  format="%Y年%m月%d日 %H:%M:%S" />
</template>
<script lang='py'>
import datetime

def dt(year, month, day, hour=0, minute=0, second=0):
    return datetime.datetime(year, month, day, hour, minute, second)
</script>

```


## 设置边界

可以设置日期时间的上下限：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnDatetimeInput name="有范围限制" 
                  :value="dt(2023, 12, 15)"
                  :start="dt(2023, 12, 10)"
                  :end="dt(2023, 12, 31)" />
</template>
<script lang='py'>
import datetime

def dt(year, month, day, hour=0, minute=0, second=0):
    return datetime.datetime(year, month, day, hour, minute, second)
</script>

```


## API

### 属性

| 属性名    | 说明                 | 类型                                             | 默认值 |
| -------- | ------------------- | ------------------------------------------------ | ------- |
| start    | 日期时间下限          | ^[datetime]                                     | None    |
| end      | 日期时间上限          | ^[datetime]                                     | None    |
| value    | 解析后的日期时间值    | ^[datetime]                                     | None    |
| disabled | 是否禁用组件          | ^[bool]                                         | False   |
| format   | 日期时间格式字符串     | ^[str]                                          | '%Y-%m-%d %H:%M:%S' |
| name     | 组件标题              | ^[str]                                          | ""      |

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |
| change | 当输入值变化时触发的事件 | ^[Callable]`(event: dict) -> None` |




# ToggleIcon 图标切换

图标切换组件允许在`True`/`False`状态之间切换一个条件，类似于`Checkbox`和`Toggle`组件，但使用图标来表示状态。

底层实现为`panel.widgets.ToggleIcon`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/ToggleIcon.html


## 基本用法

基本的图标切换组件使用：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnToggleIcon size="4em" 
               description="favorite desc" 
               name="favorite" 
               v-model='is_toggled.value'/>
  <p>value: {{ is_toggled.value }}</p>
</template>
<script lang='py'>
from vuepy import ref

is_toggled = ref(False)
</script>

```


## 自定义图标

可以自定义默认图标和激活状态图标：


```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnRow>
    <PnToggleIcon icon="thumb-down" 
                 active_icon="thumb-up" 
                 size="3em" />
    <PnToggleIcon icon="bell" 
                 active_icon="bell-ringing" 
                 size="3em" />
    <PnToggleIcon icon="star" 
                 active_icon="star-filled" 
                 size="3em" />
  </PnRow>
</template>
<script lang='py'>
from vuepy import ref
</script>

```


## 使用SVG图标

可以使用SVG字符串作为图标：

```vue
<!-- --plugins vpanel --show-code -->
<template>
<PnToggleIcon size="3em">
  <template #icon>
   <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-ad-off" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M9 5h10a2 2 0 0 1 2 2v10m-2 2h-14a2 2 0 0 1 -2 -2v-10a2 2 0 0 1 2 -2" /><path d="M7 15v-4a2 2 0 0 1 2 -2m2 2v4" /><path d="M7 13h4" /><path d="M17 9v4" /><path d="M16.115 12.131c.33 .149 .595 .412 .747 .74" /><path d="M3 3l18 18" /></svg>
  </template>                  
  <template #active-icon>
   <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-ad-filled" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M19 4h-14a3 3 0 0 0 -3 3v10a3 3 0 0 0 3 3h14a3 3 0 0 0 3 -3v-10a3 3 0 0 0 -3 -3zm-10 4a3 3 0 0 1 2.995 2.824l.005 .176v4a1 1 0 0 1 -1.993 .117l-.007 -.117v-1h-2v1a1 1 0 0 1 -1.993 .117l-.007 -.117v-4a3 3 0 0 1 3 -3zm0 2a1 1 0 0 0 -.993 .883l-.007 .117v1h2v-1a1 1 0 0 0 -1 -1zm8 -2a1 1 0 0 1 .993 .883l.007 .117v6a1 1 0 0 1 -.883 .993l-.117 .007h-1.5a2.5 2.5 0 1 1 .326 -4.979l.174 .029v-2.05a1 1 0 0 1 .883 -.993l.117 -.007zm-1.41 5.008l-.09 -.008a.5 .5 0 0 0 -.09 .992l.09 .008h.5v-.5l-.008 -.09a.5 .5 0 0 0 -.318 -.379l-.084 -.023z" stroke-width="0" fill="currentColor" /></svg>
  </template>                  
</PnToggleIcon>
</template>

```


## API

### 属性

| 属性名       | 说明                 | 类型                                         | 默认值 |
| ----------- | ------------------- | ------------------------------------------- | ------- |
| active_icon | 切换开启时显示的图标   | ^[str] tabler-icons.io图标名称或SVG字符串    | —       |
| icon        | 切换关闭时显示的图标   | ^[str] tabler-icons.io图标名称或SVG字符串    | —       |
| value       | 切换的状态            | ^[bool]                                     | False   |
| description | 鼠标悬停时显示的描述   | ^[str]                                       | —      |
| disabled    | 是否禁用组件          | ^[bool]                                      | False  |
| name        | 组件标题              | ^[str]                                       | ""     |
| size        | 图标大小              | ^[str] CSS字体大小值，如'1em'或'20px'         | —      |

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |
| change | 当切换状态变化时触发的事件 | ^[Callable]`(event: dict) -> None` |




# TextInput 文本输入框

文本输入框允许使用文本输入框输入任何字符串。

底层实现为`panel.widgets.TextInput`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/TextInput.html


## 基本用法

基本的文本输入框，可以输入和获取字符串：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnTextInput name="Text Input" 
               placeholder="Enter a string here..." 
               description="tooltip" 
               v-model="text.value"/>
  <p>value: {{ text.value }}</p>
</template>
<script lang='py'>
from vuepy import ref

text = ref("")
</script>

```


## 实时输入

TextInput 组件提供了`value_input`参数，可以在每次按键时更新：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnTextInput name="Text Input" 
               placeholder="Enter a string here..." 
               v-model:value_input="text.value"/>
  <p>value: {{ text.value }}</p>
</template>
<script lang='py'>
from vuepy import ref

text = ref("")
</script>

```


## API

### 属性

| 属性名        | 说明                    | 类型      | 默认值     |
| ------------ | ----------------------- | -------- | --------- |
| value        | 当前值，在按下Enter键或组件失去焦点时更新 | ^[str] | ""        |
| value_input  | 当前值，在每次按键时更新     | ^[str]   | ""        |
| disabled     | 是否禁用                 | ^[bool]  | False     |
| max_length   | 输入字段的最大字符长度     | ^[int]   | 5000      |
| name         | 组件标题                 | ^[str]   | ""        |
| description  | 鼠标悬停时显示的描述      | ^[str]      | ""        |
| placeholder  | 未输入值时显示的占位字符串  | ^[str]   | ""        |

### Events

| 事件名         | 说明                       | 类型                                   |
| ------------- | -------------------------- | -------------------------------------- |
| change        | 当值更改时触发的事件         | ^[Callable]`(event: dict) -> None`    |
| enter_pressed | 当按下Enter键时触发的事件    | ^[Callable]`() -> None`               |




# DatetimeSlider 日期时间滑块

日期时间滑块组件允许用户在设定的日期时间范围内使用滑块选择一个日期时间值。

底层实现为`panel.widgets.DatetimeSlider`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/DatetimeSlider.html


## 基本用法

基本的日期时间滑块使用：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnDatetimeSlider name="日期时间滑块" 
                    :start="dt(2023, 1, 1)" 
                    :end="dt(2023, 6, 1)" 
                    v-model="selected_datetime.value"/>
</template>
<script lang='py'>
from vuepy import ref
import datetime

def dt(year, month, day, hour=0, minute=0, second=0):
    return datetime.datetime(year, month, day, hour, minute, second)

selected_datetime = ref(dt(2023,1,1))
</script>

```


## 自定义格式

可以通过format参数自定义日期时间的显示格式：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnDatetimeSlider name="自定义格式" 
                    :start="dt(2023, 1, 1)" 
                    :end="dt(2023, 6, 1)" 
                    :value="dt(2023, 2, 8, 15, 40, 30)"
                    format="%Y年%m月%d日 %H:%M:%S" />
</template>
<script lang='py'>
import datetime

def dt(year, month, day, hour=0, minute=0, second=0):
    return datetime.datetime(year, month, day, hour, minute, second)
</script>

```


## 步长设置

可以通过step参数设置滑块的步长（单位为秒）：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnDatetimeSlider name="小时步长" 
                    :start="dt(2023, 1, 1)" 
                    :end="dt(2023, 1, 2)" 
                    :value="dt(2023, 1, 1, 12)"
                    :step="60 * 60" />
  <PnDatetimeSlider name="天步长" 
                    :start="dt(2023, 1, 1)" 
                    :end="dt(2023, 1, 31)" 
                    :value="dt(2023, 1, 15)"
                    :step="24 * 60 * 60" />
</template>
<script lang='py'>
import datetime

def dt(year, month, day, hour=0, minute=0, second=0):
    return datetime.datetime(year, month, day, hour, minute, second)
</script>

```


## 垂直方向

滑块可以设置为垂直方向显示：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnRow>
    <PnDatetimeSlider name="垂直滑块" 
                      :start="dt(2023, 1, 1)" 
                      :end="dt(2023, 6, 1)" 
                      :value="dt(2023, 3, 15)"
                      orientation="vertical" 
                      :height="300" />
  </PnRow>
</template>
<script lang='py'>
import datetime

def dt(year, month, day, hour=0, minute=0, second=0):
    return datetime.datetime(year, month, day, hour, minute, second)
</script>

```


## API

### 属性

| 属性名           | 说明                 | 类型                                                | 默认值 |
| --------------- | ------------------- | --------------------------------------------------- | ------- |
| start           | 范围的下限           | ^[datetime]                                         | —       |
| end             | 范围的上限           | ^[datetime]                                         | —       |
| value           | 选择的日期时间        | ^[datetime]                                         | —       |
| value_throttled | 鼠标释放前节流的日期时间值 | ^[datetime]                                    | —       |
| step            | 滑块的步长（单位：秒） | ^[int]                                             | 60      |
| bar_color       | 滑块条的颜色         | ^[str] 十六进制RGB颜色值                             | —       |
| direction       | 滑块方向             | ^[str] 'ltr'（从左到右）或'rtl'（从右到左）          | 'ltr'   |
| disabled        | 是否禁用组件         | ^[bool]                                             | False   |
| name            | 组件标题             | ^[str]                                              | ""      |
| orientation     | 滑块的方向           | ^[str] 'horizontal'（水平）或'vertical'（垂直）      | 'horizontal' |
| tooltips        | 是否在滑块手柄上显示提示 | ^[bool]                                          | True    |
| format          | 日期时间的格式字符串   | ^[str]                                             | —       |

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |
| change | 当滑块值变化时触发的事件 | ^[Callable]`(event: dict) -> None` |




# NestedSelect 嵌套选择器

嵌套选择组件允许用户从多层级的嵌套选项中进行选择，每个级别的选择会影响下一个级别的可用选项。

底层实现为`panel.widgets.NestedSelect`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/NestedSelect.html


## 基本用法

基本的嵌套选择组件，提供多层级的选项：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnNestedSelect :options="nested_options" 
                  :levels="['模型', '分辨率', '初始化']" 
                  @change="on_change" />
  <p>value: {{ selected.value }}</p>
</template>
<script lang='py'>
from vuepy import ref

nested_options = {
    "GFS": {
        "0.25度": ["00Z", "06Z", "12Z", "18Z"],
        "0.5度": ["00Z", "12Z"],
        "1度": ["00Z", "12Z"],
    },
    "NAME": {
        "12km": ["00Z", "12Z"],
        "3km": ["00Z", "12Z"],
    },
}

selected = ref({})

def on_change(event):
    selected.value = event.new
</script>

```


## 自定义布局

嵌套选择组件支持不同的布局类型：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnNestedSelect :options="nested_options" 
                  :levels="['模型', '分辨率', '初始化']"
                  layout="row" />
</template>
<script lang='py'>
from vuepy import ref

nested_options = {
    "GFS": {
        "0.25度": ["00Z", "06Z", "12Z", "18Z"],
        "0.5度": ["00Z", "12Z"],
        "1度": ["00Z", "12Z"],
    },
    "NAME": {
        "12km": ["00Z", "12Z"],
        "3km": ["00Z", "12Z"],
    },
}
</script>

```


网格布局示例：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnNestedSelect :options="nested_options" 
                  :levels="['模型', '分辨率', '初始化']"
                  :layout='{"type": pn.GridBox, "ncols": 2}' />
</template>
<script lang='py'>
from vuepy import ref
import panel as pn

nested_options = {
    "GFS": {
        "0.25度": ["00Z", "06Z", "12Z", "18Z"],
        "0.5度": ["00Z", "12Z"],
        "1度": ["00Z", "12Z"],
    },
    "NAME": {
        "12km": ["00Z", "12Z"],
        "3km": ["00Z", "12Z"],
    },
}
</script>

```


## 设置默认值

可以通过设置`v-model`/`value`参数来指定默认选中的值：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnNestedSelect :options="nested_options" 
                  :levels="['模型', '分辨率', '初始化']"
                  v-model="default_value.value" />
 <p>value: {{ default_value.value }}</p>
</template>
<script lang='py'>
from vuepy import ref

nested_options = {
    "GFS": {
        "0.25度": ["00Z", "06Z", "12Z", "18Z"],
        "0.5度": ["00Z", "12Z"],
        "1度": ["00Z", "12Z"],
    },
    "NAME": {
        "12km": ["00Z", "12Z"],
        "3km": ["00Z", "12Z"],
    },
}

default_value = ref({"模型": "NAME", "分辨率": "12km", "初始化": "12Z"})
</script>

```


## 动态选项

动态生成选项options：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnNestedSelect :options="list_options"
                  :levels='["time_step", "level_type", "file_type"]' />
</template>
<script lang='py'>
from vuepy import ref
import panel as pn

# @pn.cache() # can help improve user experience and reduce the risk of rate limits.
def list_options(level, value):
    if level == "time_step":
        options = {
            "Daily": list_options, 
            "Monthly": list_options,
        }
    elif level == "level_type":
        options = {
            f"{value['time_step']}_upper": list_options, 
            f"{value['time_step']}_lower": list_options,
        }
    else:
        options = [
            f"{value['level_type']}.json", 
            f"{value['level_type']}.csv",
        ]

    return options
</script>

```


## API

### 属性

| 属性名    | 说明                 | 类型                                                           | 默认值 |
| -------- | ------------------- | ---------------------------------------------------------------| ------- |
| options  | 选择项，可以是嵌套字典，列表，或返回这些类型的可调用对象 | ^[dict\|callable] | — |
| value    | 所有选择组件的值，键是级别名称 | ^[dict] | — |
| layout   | 组件的布局类型，'column'、'row'、'grid'或包含type和其他参数的字典 | ^[str\|dict] | 'column' |
| levels   | 级别名称列表或字典列表 | ^[list] | None |
| disabled | 是否禁用选择器 | ^[bool] | False |
| name     | 组件标题 | ^[str] | "" |


### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |
| change | 当选择发生变化时触发的事件 | ^[Callable]`(event: dict) -> None` |




# TimePicker 时间选择器

时间选择器组件允许用户选择一个时间，可以以文本形式输入或使用浏览器的时间选择工具。

底层实现为`panel.widgets.TimePicker`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/TimePicker.html


## 基本用法

基本的时间选择器使用：

```vue
<!-- --plugins vpanel --show-code -->
<template>
 <PnCol :height='150'>
  <PnTimePicker name="TimePicker" v-model='time.value'/>
 </PnCol>
 <p>value: {{ time.value }}</p>
</template>
<script lang='py'>
from vuepy import ref
import datetime as dt

time = ref(None)
</script>

```


## 时间范围限制

可以使用`start`和`end`参数限制可选择的时间范围：

```vue
<!-- --plugins vpanel --show-code -->
<template>
 <PnCol :height='150'>
  <PnTimePicker name="TimePicker" 
               start="09:00"
               end="13:00"
               v-model="time.value"/>
 </PnCol>
 <p>value: {{ time.value }}</p>
</template>
<script lang='py'>
from vuepy import ref
import datetime as dt

time = ref(dt.time(12, 0))
</script>

```


## 自定义时间格式

可以使用`format`参数自定义时间的显示格式：

```vue
<!-- --plugins vpanel --show-code -->
<template>
 <p>value: {{ time1.value }}</p>
 <PnCol :height='150'>
  <PnTimePicker name="12小时制" 
               format="h:i K"
               v-model="time1.value"/>
 </PnCol>

 <p>value: {{ time2.value }}</p>
 <PnCol :height='150'>
  <PnTimePicker name="24小时制" 
               format="H:i"
               v-model="time2.value"/>
 </PnCol>

 <p>value: {{ time3.value }}</p>
 <PnCol :height='150'>
  <PnTimePicker name="带秒的格式" 
               format="H:i:s"
               :seconds="True"
               v-model="time3.value"/>
 </PnCol>
</template>
<script lang='py'>
from vuepy import ref
import datetime as dt

time1 = ref(dt.time(14, 30))
time2 = ref(dt.time(14, 30))
time3 = ref(dt.time(14, 30, 45))
</script>

```


## 自定义步长

可以通过`hour_increment`、`minute_increment`和`second_increment`参数控制时、分、秒的调整步长：

```vue
<!-- --plugins vpanel --show-code -->
<template>
 <PnCol :height='150'>
  <PnTimePicker name="小时步长:2 分钟步长:15" 
               :hour_increment="2"
               :minute_increment="15"
               v-model="time.value"/>
 </PnCol>
 <p>value: {{ time.value }}</p>
</template>
<script lang='py'>
from vuepy import ref
import datetime as dt

time = ref(dt.time(12, 0))
</script>

```


## API

### 属性

| 属性名            | 说明                         | 类型                             | 默认值      |
| ---------------- | ---------------------------- | -------------------------------- | ----------- |
| value            | 当前选择的时间                | ^[datetime.time\|str]            | None        |
| start            | 允许选择的最早时间            | ^[datetime.time\|str]            | None        |
| end              | 允许选择的最晚时间            | ^[datetime.time\|str]            | None        |
| format           | 时间显示格式                  | ^[str]                           | "H:i"       |
| seconds          | 是否允许选择秒                | ^[bool]                          | False       |
| hour_increment   | 小时调整的步长                | ^[int]                           | 1           |
| minute_increment | 分钟调整的步长                | ^[int]                           | 1           |
| second_increment | 秒调整的步长                  | ^[int]                           | 1           |
| clock            | 时钟制式，'12h'或'24h'        | ^[str]                           | "12h"       |
| disabled         | 是否禁用                      | ^[bool]                          | False       |
| name             | 组件标题                      | ^[str]                           | ""          |
| description      | 鼠标悬停时显示的描述          | ^[str]                           | ""          |

format:

```
+---+------------------------------------+------------+
| H | Hours (24 hours)                   | 00 to 23   |
| h | Hours                              | 1 to 12    |
| G | Hours, 2 digits with leading zeros | 1 to 12    |
| i | Minutes                            | 00 to 59   |
| S | Seconds, 2 digits                  | 00 to 59   |
| s | Seconds                            | 0, 1 to 59 |
| K | AM/PM                              | AM or PM   |
+---+------------------------------------+------------+
```

### Events

| 事件名  | 说明                | 类型                                 |
| ------ | ------------------ | ------------------------------------ |
| change | 当时间更改时触发的事件 | ^[Callable]`(value) -> None`        |




# CodeEditor 代码编辑器

代码编辑器组件允许嵌入基于[Ace](https://ace.c9.io/)的代码编辑器。

目前仅启用了Ace功能的一小部分：
- 多种语言的**语法高亮**
- **主题**
- 通过`ctrl+space`的基本**自动完成**支持（仅使用代码的静态分析）
- **注释**
- **只读**模式

底层实现为`panel.widgets.CodeEditor`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/CodeEditor.html


## 基本用法

基本的代码编辑器，可以编辑和高亮显示代码：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnCodeEditor v-model="code.value" 
               sizing_mode="stretch_width" 
               language="python" 
               :height="200"
               @change="on_change" />
  <div>当前代码长度: {{ len(code.value) }} 字符</div>
</template>
<script lang='py'>
from vuepy import ref

initial_code = """import sys
import math

def calculate_distance(x, y):
    return math.sqrt(x**2 + y**2)

print(calculate_distance(3, 4))  # 输出：5.0
"""
code = ref(initial_code)

def on_change(event):
    print(f"代码已更新，新长度: {len(code.value)}")
</script>

```

## 延迟更新

默认情况下，代码编辑器会在每次按键时更新`value`，但可以设置`on_keyup=False`，使其仅在编辑器失去焦点或按下`<Ctrl+Enter>`/`<Cmd+Enter>`时更新`value`：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnCodeEditor v-model="code.value" 
               :on_keyup="False"
               language="python" 
               @change="on_change" />
  <PnButton @click="show_code()">显示当前代码</PnButton>
</template>
<script lang='py'>
from vuepy import ref

initial_code = "# 按Ctrl+Enter/Cmd+Enter或点击外部提交更改\nimport sys\n"
code = ref(initial_code)

def on_change(event):
    print("代码已更新（失去焦点或按下Ctrl+Enter/Cmd+Enter）")
    
def show_code():
    print(f"当前代码:\n{code.value}")
</script>

```

## 语言和主题

可以更改编辑器的语言和主题：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnRow>
    <PnSelect name="语言" 
              :options="languages"
              v-model="selected_language.value" />
    <PnSelect name="主题" 
              :options="themes"
              v-model="selected_theme.value" />
  </PnRow>
  <PnCodeEditor :value="sample_code" 
               :language="selected_language.value"
               :theme="selected_theme.value"
               :height="300" :width="400"/>
</template>
<script lang='py'>
from vuepy import ref

languages = ['python', 'html', 'javascript', 'css', 'sql']
themes = ['chrome', 'monokai', 'twilight', 'tomorrow_night', 'github']

selected_language = ref('html')
selected_theme = ref('chrome')

sample_code = r"""<!DOCTYPE html>
<html>
    <head>
        <title>示例页面</title>
    </head>
    <body>
        <h1>标题1</h1>
        <h2>标题2</h2>
        <p>段落</p>
    </body>
</html>
"""
</script>

```

## 注释和只读模式

可以为编辑器添加注释，并设置为只读模式：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnCodeEditor :value="py_code" 
               :annotations="annotations"
               :readonly="True"
               language="python"
               :height="200" />
</template>
<script lang='py'>
from vuepy import ref

py_code = """import math

# 这里有一个错误
x = math.cos(x)**2 + math.cos(y)**2

# 这里有一个警告
for i in range(10)
    print(i)
"""

annotations = [
    dict(row=3, column=0, text='未定义变量 x 和 y', type='error'),
    dict(row=6, column=17, text='缺少冒号', type='warning')
]
</script>

```

## 通过文件名自动检测语言

如果设置了`filename`属性，编辑器会根据文件扩展名自动检测语言：

```vue
<!-- --plugins vpanel --show-code --backend='panel' -->
<template>
  <PnSelect name="文件" 
            :options="files"
            v-model="selected_file.value" />
  <PnCodeEditor :value="file_contents[selected_file.value]"
                :filename="selected_file.value"
                :height="200" />
</template>
<script lang='py'>
from vuepy import ref

files = ['test.py', 'test.html', 'test.js', 'test.css']
file_contents = {
    'test.py': "def hello():\n    print('Hello World')\n\nhello()",
    'test.html': "<html>\n  <body>\n    <h1>Hello World</h1>\n  </body>\n</html>",
    'test.js': "function hello() {\n  console.log('Hello World');\n}\n\nhello();",
    'test.css': "body {\n  background-color: #f0f0f0;\n  color: #333;\n}",
}

selected_file = ref('test.py')
</script>

```


## API

### 属性

| 属性名          | 说明                           | 类型                                | 默认值     |
| -------------- | ------------------------------ | ---------------------------------- | --------- |
| annotations    | 注释列表，每个注释是一个包含'row'、'column'、'text'和'type'键的字典 | ^[list]    | []        |
| filename       | 文件名，如果提供，将使用文件扩展名来确定语言 | ^[str]                     | ""        |
| indent         | 默认缩进的空格数                | ^[int]                             | 4         |
| language       | 用于代码语法高亮的语言字符串      | ^[str]                             | 'text'    |
| on_keyup       | 是否在每次按键时更新值或仅在失去焦点/热键时更新 | ^[bool]                | True      |
| print_margin   | 是否在编辑器中显示打印边距       | ^[bool]                            | False     |
| soft_tabs      | 是否使用空格而不是制表符进行缩进  | ^[bool]                            | True      |
| theme          | 编辑器主题                      | ^[str]                             | 'chrome'  |
| readonly       | 编辑器是否应以只读模式打开       | ^[bool]                            | False     |
| value          | 编辑器中当前代码的状态           | ^[str]                             | ""        |
| value_input    | 在每次按键时更新的当前代码状态    | ^[str]                             | ""        |

### Events

| 事件名         | 说明                       | 类型                                   |
| ------------- | -------------------------- | -------------------------------------- |
| change        | 当值更改时触发的事件         | ^[Callable]`(event: dict) -> None`    |




# EditableRangeSlider 可编辑范围滑块

可编辑范围滑块组件允许使用带有两个手柄的滑块选择浮点范围，并提供数字输入框以便进行更精确的控制。

底层实现为`panel.widgets.EditableRangeSlider`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/EditableRangeSlider.html


## 基本用法

基本的可编辑范围滑块，可以通过滑动两个手柄或直接输入数字来选择范围：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnEditableRangeSlider name="范围滑块" 
                        :start="0" 
                        :end="pi" 
                        :step="0.01"
                        v-model="value.value"
                        @change="on_change" />
  <p>当前范围: {{ value.value }}</p>
</template>
<script lang='py'>
from vuepy import ref

pi = 3.14

initial_value = (pi/4., pi/2.)
value = ref(initial_value)

def on_change(event):
    print(f"范围已更新为: {value.value}")
</script>

```


## 固定范围

滑块的`value`默认没有界限，可以超过`end`或低于`start`。如果需要将`value`固定在特定范围内，可以使用`fixed_start`和`fixed_end`：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnEditableRangeSlider name="固定范围滑块" 
                        :start="0" 
                        :end="10" 
                        :fixed_start="-1" 
                        :fixed_end="12"
                        :value="(2, 7)" />
</template>
<script lang='py'>
from vuepy import ref
</script>

```


## 自定义格式

可以使用自定义格式字符串或Bokeh TickFormatter来格式化滑块值：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnEditableRangeSlider name="距离（字符串格式）" 
                        format="0.0a"
                        :start="100000" 
                        :end="1000000"
                        :value="(200000, 800000)" />
  <PnEditableRangeSlider name="距离（格式化器）" 
                        :format="tick_formatter"
                        :start="0" 
                        :end="10" 
                        :value="(2, 7)" />
</template>
<script lang='py'>
from vuepy import ref
from bokeh.models.formatters import PrintfTickFormatter

tick_formatter = PrintfTickFormatter(format='%.3f 米')
</script>

```


## API

### 属性

| 属性名          | 说明                           | 类型                                | 默认值     |
| -------------- | ------------------------------ | ---------------------------------- | --------- |
| start          | 滑块的下限，可被更低的`value`覆盖 | ^[float]                           | 0.0       |
| end            | 滑块的上限，可被更高的`value`覆盖 | ^[float]                           | 1.0       |
| fixed_start    | 滑块和输入的固定下限，`value`不能低于此值 | ^[float\|None]              | None      |
| fixed_end      | 滑块和输入的固定上限，`value`不能高于此值 | ^[float\|None]              | None      |
| step           | 值之间的间隔                    | ^[float]                           | 0.1       |
| value          | 所选范围的上下界元组             | ^[(float, float)]                   | (0.0, 1.0) |
| value_throttled| 鼠标释放前阻止的所选范围的上下界元组 | ^[(float, float)]                | (0.0, 1.0) |
| bar_color      | 滑块条的颜色，十六进制RGB值      | ^[str]                             | None      |
| direction      | 滑块方向，从左到右('ltr')或从右到左('rtl') | ^[str]                    | 'ltr'     |
| disabled       | 是否禁用                       | ^[bool]                            | False     |
| format         | 应用于滑块值的格式化器           | ^[str\|bokeh.models.TickFormatter] | None      |
| name           | 组件标题                       | ^[str]                             | ""        |
| orientation    | 滑块的显示方向，'horizontal'或'vertical' | ^[str]                    | 'horizontal' |
| tooltips       | 是否在滑块手柄上显示工具提示      | ^[bool]                           | True      |

### Events

| 事件名         | 说明                       | 类型                                   |
| ------------- | -------------------------- | -------------------------------------- |
| change        | 当值更改时触发的事件         | ^[Callable]`(event: dict) -> None`    |




# ArrayInput 数组输入框

数组输入框组件允许使用文本输入框渲染和编辑NumPy数组，其内容随后在Python中解析。为避免大型数组的问题，`ArrayInput`定义了一个`max_array_size`，如果数组超过此大小，文本表示将被汇总，编辑将被禁用。

底层实现为`panel.widgets.ArrayInput`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/ArrayInput.html


## 基本用法

基本的数组输入框，可以显示和编辑NumPy数组：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnArrayInput name="Array input" 
                :value="initial_array"
                v-model="array.value"
                @change="on_change" />
  <div>array shape: {{ array.value.shape }}</div>
</template>
<script lang='py'>
import numpy as np
from vuepy import ref

initial_array = np.random.randint(0, 10, (10, 2))
array = ref(initial_array)

def on_change(event):
    print(f"update ，shape: {array.value.shape}")
</script>

```


## 大型数组

对于大型数组，可以设置`max_array_size`以避免浏览器负担过重：

```vue
<!-- --plugins vpanel --show-code -->
<template>
<PnArrayInput name="Small Array (Editable)" 
              :value="small_array" :max_array_size="1000" />
<PnArrayInput name="Large Array (Non-editable)"
              :value="large_array"
              :max_array_size="1000" />
</template>
<script lang='py'>
import numpy as np
from vuepy import ref

small_array = np.random.randint(0, 10, (10, 5))
large_array = np.random.randint(0, 10, (100, 20))
</script>

```


## 自定义占位符

可以自定义占位符文本：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnArrayInput name="placeholder" 
                placeholder="[1, 2, 3]" />
</template>
<script lang='py'>
from vuepy import ref
</script>

```


## API

### 属性

| 属性名          | 说明                           | 类型                                | 默认值     |
| -------------- | ------------------------------ | ---------------------------------- | --------- |
| max_array_size | 大于此限制的数组将在Python中允许，但不会序列化到JavaScript中。虽然这样大的数组因此无法在小部件中编辑，但这种限制有助于避免浏览器负担过重，并让其他小部件保持可用 | ^[int] | 1000 |
| value          | 指定类型的解析值                | ^[numpy.ndarray]                    | None      |
| disabled       | 是否禁用                       | ^[bool]                            | False     |
| name           | 组件标题                       | ^[str]                             | ""        |
| placeholder    | 未输入值时显示的占位符字符串      | ^[str]                            | ""        |

### Events

| 事件名         | 说明                       | 类型                                   |
| ------------- | -------------------------- | -------------------------------------- |
| change        | 当值更改时触发的事件         | ^[Callable]`(event: Event) -> None`    |




# DateRangeSlider 日期范围滑块

日期范围滑块组件允许使用带有两个手柄的滑块选择日期范围。

底层实现为`panel.widgets.DateRangeSlider`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/DateRangeSlider.html


## 基本用法

可以通过拖动手柄调整滑块的开始和结束日期，也可以通过拖动选定范围来整体移动范围：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <div>当前选择范围: {{ value.value }}</div>
  <PnDateRangeSlider name="日期范围滑块"
                     :start="start_date"
                     :end="end_date"
                     :value="initial_value"
                     :step="2"
                     v-model="value.value"/>
</template>
<script lang='py'>
import datetime as dt
from vuepy import ref

start_date = dt.datetime(2017, 1, 1)
end_date = dt.datetime(2019, 1, 1)
initial_value = (dt.datetime(2017, 1, 1), dt.datetime(2018, 1, 10))
value = ref(initial_value)

</script>

```


## 自定义格式

可以使用自定义格式字符串来格式化滑块值：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnDateRangeSlider name="自定义格式日期范围"
                    :start="start_date"
                    :end="end_date"
                    :value="initial_value"
                    :step="2"
                    format="%Y-%m-%d" />
</template>
<script lang='py'>
import datetime as dt
from vuepy import ref

start_date = dt.datetime(2017, 1, 1)
end_date = dt.datetime(2019, 1, 1)
initial_value = (dt.datetime(2017, 1, 1), dt.datetime(2018, 1, 10))
</script>

```


## 垂直方向

滑块可以设置为垂直方向显示：

```vue
<!-- --plugins vpanel --show-code -->
<template>
 <PnColumn style='height:400px;'>
  <PnDateRangeSlider name="垂直日期范围滑块"
                    orientation="vertical"
                    :start="start_date"
                    :end="end_date"
                    :value="initial_value"
                    :height="400" />
 </PnColumn>
</template>
<script lang='py'>
import datetime as dt
from vuepy import ref

start_date = dt.datetime(2017, 1, 1)
end_date = dt.datetime(2019, 1, 1)
initial_value = (dt.datetime(2017, 3, 1), dt.datetime(2018, 9, 10))
</script>

```


## API

### 属性

| 属性名          | 说明                           | 类型                                | 默认值     |
| -------------- | ------------------------------ | ---------------------------------- | --------- |
| start          | 范围的下限                     | ^[datetime]                         | None      |
| end            | 范围的上限                     | ^[datetime]                         | None      |
| step           | 以天为单位的步长                | ^[int]                             | 1         |
| value          | 所选范围的上下界元组，以datetime类型表示 | ^[(datetime, datetime)]      | (None, None) |
| value_throttled| 鼠标释放前阻止的所选范围的上下界元组，以datetime类型表示 | ^[(datetime, datetime)] | (None, None) |
| bar_color      | 滑块条的颜色，十六进制RGB值      | ^[str]                             | None      |
| direction      | 滑块方向，从左到右('ltr')或从右到左('rtl') | ^[str]                    | 'ltr'     |
| disabled       | 是否禁用                       | ^[bool]                            | False     |
| format         | 应用于滑块值的格式化器           | ^[str]                             | None      |
| name           | 组件标题                       | ^[str]                             | ""        |
| orientation    | 滑块的显示方向，'horizontal'或'vertical' | ^[str]                    | 'horizontal' |
| tooltips       | 是否在滑块手柄上显示工具提示      | ^[bool]                           | True      |

### Events

| 事件名         | 说明                       | 类型                                   |
| ------------- | -------------------------- | -------------------------------------- |
| change        | 当值更改时触发的事件         | ^[Callable]`(event: dict) -> None`    |




# CheckBoxGroup 复选框组

允许通过选中相应的复选框从选项列表中选择多个选项。它属于多选项选择组件的广泛类别，提供兼容的API，包括`MultiSelect`、`CrossSelector`和`CheckButtonGroup`组件。

底层实现为`panel.widgets.CheckBoxGroup`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/CheckBoxGroup.html


## 基本用法

基本的复选框组，可以选择多个选项：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnCheckBoxGroup name="复选框组" 
                  :value="['苹果', '梨']" 
                  :options="['苹果', '香蕉', '梨', '草莓']"
                  :inline="True"
                  v-model="selected.value"
                  @change="on_change" />
  <div>当前选择: {{ selected.value }}</div>
</template>
<script lang='py'>
from vuepy import ref

selected = ref(['苹果', '梨'])

def on_change(ev):
    print(ev) # Event(what='value', name='value', 
              #  obj=CheckBoxGroup(inline=True,...), cls=CheckBoxGroup(...), 
              #  old=[], new=[], type='changed')
    print(f"{ev.new}") # value is ['苹果']
</script>

```

## 垂直布局

通过设置`inline=False`可以将选项垂直排列：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnCheckBoxGroup name="" 
                  :options="['Opt1', 'Opt2', 'Opt3']" 
                  :inline="False" />
</template>

```

## 字典选项

可以使用字典作为选项，键作为显示标签，值作为实际值：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnCheckBoxGroup name="字典选项" 
                  :options="options"
                  :value="[1, 3]"
                  v-model="value.value" />
  <div>ID: {{ value.value }}</div>
</template>
<script lang='py'>
from vuepy import ref

options = {'苹果': 1, '香蕉': 2, '梨': 3, '草莓': 4}
value = ref([1, 3])
</script>

```


## API

### 属性

| 属性名       | 说明                           | 类型                                | 默认值     |
| ----------- | ------------------------------ | ---------------------------------- | --------- |
| options     | 选项列表或字典                  | ^[list\|dict]                       | []        |
| value       | 当前选择的选项                  | ^[list]                            | []        |
| disabled    | 是否禁用                       | ^[bool]                            | False     |
| inline      | 是否将项目垂直排列在一列中(False)或水平排列在一行中(True) | ^[bool]      | False     |
| name        | 组件标题                       | ^[str]                             | ""        |


### Events

| 事件名         | 说明                       | 类型                                   |
| ------------- | -------------------------- | -------------------------------------- |
| change        | 当value更改时触发的事件         | ^[Callable]`(event: dict) -> None`    |




# DatePicker 日期选择器

日期选择器组件允许使用文本框和浏览器的日期选择工具选择日期值。

底层实现为`panel.widgets.DatePicker`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/DatePicker.html


## 基本用法

日期选择器使用浏览器依赖的日历小部件来选择日期：

```vue
<!-- --plugins vpanel --show-code -->
<template>
 <PnColumn style='height:400px;'>
  <PnDatePicker name="日期选择器" 
               :value="initial_date" 
               v-model="date.value"
               @change="on_change" />
 </PnColumn>
</template>
<script lang='py'>
import datetime as dt
from vuepy import ref

initial_date = dt.date(2024, 4, 1)
date = ref(initial_date)

def on_change(event):
    print(f"{date.value}") # 2024-04-02
</script>

```

## 日期范围限制

可以通过`start`和`end`参数限制可选日期的范围：

```vue
<!-- --plugins vpanel --show-code -->
<template>
 <PnColumn style='height:400px;'>
  <PnDatePicker name="限制范围" 
               :start="start_date" 
               :end="end_date" />
 </PnColumn>
</template>
<script lang='py'>
import datetime as dt

start_date = dt.date(2024, 12, 10)
end_date = dt.date(2024, 12, 31)
</script>

```


## 可用/禁用日期

可以通过`disabled_dates`和`enabled_dates`参数设置不可用和可用的日期：

```vue
<!-- --plugins vpanel --show-code -->
<template>
 <PnColumn style='height:400px;'>
  <PnDatePicker name="禁用特定日期: 禁用周末"
               :disabled_dates="disabled_dates" />
 </PnColumn>
 <PnColumn style='height:400px;'>
  <PnDatePicker name="仅允许特定日期: 只允许本月的奇数日期"
               :enabled_dates="enabled_dates" />
 </PnColumn>
</template>
<script lang='py'>
import datetime as dt
from vuepy import ref

# 禁用周末
today = dt.datetime.now().date()
disabled_dates = [(today + dt.timedelta(days=i)) for i in range(30) if (today + dt.timedelta(days=i)).weekday() >= 5]

# 只允许本月的奇数日期
month_start = today.replace(day=1)
next_month = month_start.replace(month=month_start.month % 12 + 1, day=1)
enabled_dates = [(month_start + dt.timedelta(days=i-1)) for i in range(1, 31, 2) 
                if (month_start + dt.timedelta(days=i-1)).month == month_start.month]
</script>

```


## API

### 属性

| 属性名          | 说明                           | 类型                                | 默认值     |
| -------------- | ------------------------------ | ---------------------------------- | --------- |
| end            | 最晚可选日期                    | ^[datetime]                         | None      |
| start          | 最早可选日期                    | ^[datetime]                         | None      |
| value          | 所选值，datetime类型            | ^[datetime]                         | None      |
| disabled       | 是否禁用                       | ^[bool]                            | False     |
| name           | 组件标题                       | ^[str]                             | ""        |
| disabled_dates | 使不可用于选择的日期；其他日期将可用 | ^[list]                          | None      |
| enabled_dates  | 使可用于选择的日期；其他日期将不可用 | ^[list]                          | None      |

### Events

| 事件名         | 说明                       | 类型                                   |
| ------------- | -------------------------- | -------------------------------------- |
| change        | 当值更改时触发的事件         | ^[Callable]`(event: dict) -> None`    |




# AutocompleteInput 自动完成输入框

自动完成输入框组件允许通过在自动完成文本字段中输入值来从选项列表或字典中选择一个`value`。它属于单值、选项选择组件的广泛类别，提供兼容的API，包括`RadioBoxGroup`、`Select`和`DiscreteSlider`组件。

底层实现为`panel.widgets.AutocompleteInput`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/AutocompleteInput.html


## 基本用法

基本的自动完成输入框，可以从选项列表中选择一个值：

```vue
<!-- --plugins vpanel --show-code -->
<template>
<PnCol :height='300'>
  <PnAutocompleteInput name="自动完成输入框" 
                      :options="['Apple', 'banana', 'orange']"
                      :case_sensitive="False"
                      :min_characters='1'
                      search_strategy="includes"
                      placeholder="Select a fruit: apple, ..."
                      v-model="value.value"
                      description='tooltip'
                      @change="on_change" />
</PnCol>
</template>
<script lang='py'>
from vuepy import ref

value = ref("")

def on_change(event):
    print(f"选择已更新为: {value.value}")
</script>

```


## 不限制输入

如果设置`restrict=False`，自动完成输入框将允许任何输入，而不仅限于它提供的自动完成选项：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnAutocompleteInput name="不限制输入" 
                       value="math"
                      :options="['banana', 'apple']"
                      :restrict="False" />
</template>

```


## 字典选项

`options`参数也接受一个字典，其键将是下拉菜单的标签：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnAutocompleteInput name="Dict options" 
                      :options="options"
                      v-model="value.value" />
  <PnButton @click="update_value()">to Apple</PnButton>
  <div>当前值: {{ value.value }}</div>
</template>
<script lang='py'>
from vuepy import ref

options = {'Banana': 1, 'Apple': 2, 'Orange': 3}
value = ref(1)

def update_value():
    value.value = 2
</script>

```


## 搜索策略

可以通过`search_strategy`参数定义如何搜索完成字符串列表：

```vue
<!-- --plugins vpanel --show-code -->
<template>
<PnCol :height='150'>
  <PnAutocompleteInput name="Starts with match" 
                      :options="fruits"
                      search_strategy="starts_with"
                      placeholder="Enter fruit name" />
</PnCol>
<PnCol :height='150'>
  <PnAutocompleteInput name="Contains match" 
                      :options="fruits"
                      search_strategy="includes"
                      :min_characters='1'
                      placeholder="Enter fruit name" />
</PnCol>
</template>
<script lang='py'>
from vuepy import ref

fruits = ['Apple', 'Banana', 'Orange', 'Pear', 'Grape', 'Mango', 'Strawberry', 'Watermelon']
</script>

```


## API

### 属性

| 属性名           | 说明                           | 类型                                | 默认值     |
| --------------- | ------------------------------ | ---------------------------------- | --------- |
| options         | 要选择的选项列表或字典           | ^[list\|dict]                       | []        |
| restrict        | 设置为False以允许用户输入不在选项列表中的文本 | ^[bool]                | True      |
| search_strategy | 定义如何搜索完成字符串列表 | ^[str]`starts_with,includes`      | starts_with |
| value           | 当前值，如果restrict=True，则必须是选项值之一 | ^[str]               | ""        |
| value_input     | 在每次按键时更新的当前值         | ^[str]                             | ""        |
| case_sensitive  | 启用或禁用区分大小写的完成匹配     | ^[bool]                           | True      |
| disabled        | 是否禁用                       | ^[bool]                            | False     |
| name            | 组件标题                       | ^[str]                             | ""        |
| placeholder     | 未选择选项时显示的占位符字符串     | ^[str]                             | ""        |
| description      | 鼠标悬停时显示的描述      | ^[str]      | ""        |
| min_characters  | 用户必须输入多少字符才会显示自动完成 | ^[int]                           | 2         |

### Events

| 事件名         | 说明                       | 类型                                   |
| ------------- | -------------------------- | -------------------------------------- |
| change        | 当值更改时触发的事件         | ^[Callable]`(event: dict) -> None`    |




# CrossSelector 交叉选择器

交叉选择器组件允许通过在两个列表之间移动项目来从选项列表中选择多个值。它属于多选项选择组件的广泛类别，提供兼容的API，包括`MultiSelect`、`CheckBoxGroup`和`CheckButtonGroup`组件。

底层实现为`panel.widgets.CrossSelector`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/CrossSelector.html


## 基本用法

交叉选择器由多个组件组成：
* 两个列表，分别用于未选择（左）和已选择（右）的选项值
* 过滤框，允许使用正则表达式匹配下方值列表中的选项
* 按钮，用于将值从未选择列表移动到已选择列表（`>>`）或反之（`<<`）

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnCrossSelector name="Fruits" 
                  :value="['Apple', 'Pear']" 
                  :options="['Apple', 'Banana', 'Pear', 'Strawberry']"
                  v-model="selected.value"
                  @change="on_change" />
</template>
<script lang='py'>
from vuepy import ref

selected = ref(['Apple', 'Pear'])

def on_change(event):
    print(f"Selection: {event.new}") # Selection: ['Apple']
</script>

```

## 自定义过滤函数

可以自定义过滤函数来控制如何根据搜索模式过滤选项：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnCrossSelector name="Cities" 
                  :options="cities"
                  :filter_fn="custom_filter" />
</template>
<script lang='py'>
from vuepy import ref

cities = ['New York', 'London', 'Paris', 'Tokyo', 'Beijing', 'Shanghai', 'Sydney', 'Berlin']

def custom_filter(pattern, option):
    """Custom filter function that only matches beginning"""
    if not pattern:
        return True
    return option.startswith(pattern)
</script>

```


## 保持定义顺序

通过`definition_order`参数可以控制是否在过滤后保留定义顺序：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnCrossSelector name="保持定义顺序" 
                  definition_order
                  :options="options"
                  :value="initial_value" />
  <PnCrossSelector name="按选择顺序" 
                  :definition_order="False"
                  :options="options"
                  :value="initial_value" />
</template>
<script lang='py'>
from vuepy import ref

options = ['选项1', '选项2', '选项3', '选项4']
initial_value = ['选项2', '选项4']
</script>

```


## API

### 属性

| 属性名           | 说明                           | 类型                                | 默认值     |
| --------------- | ------------------------------ | ---------------------------------- | --------- |
| definition_order | 是否在过滤后保留定义顺序。禁用以允许选择顺序定义已选择列表的顺序 | ^[bool] | True      |
| filter_fn      | 使用文本字段搜索时用于过滤选项的函数。提供的函数必须允许两个参数：用户提供的搜索模式和来自提供的`options`列表的标签 | ^[function] | re.search |
| options        | 可用选项的列表或字典             | ^[list\|dict]                       | []        |
| value          | 当前选择的选项                  | ^[list]                            | []        |
| disabled       | 是否禁用                       | ^[bool]                            | False     |
| name           | 组件标题                       | ^[str]                             | ""        |

### Events

| 事件名         | 说明                       | 类型                                   |
| ------------- | -------------------------- | -------------------------------------- |
| change        | 当值更改时触发的事件         | ^[Callable]`(event: dict) -> None`    |



# RadioBoxGroup 单选框组

单选框组组件允许使用一组复选框从值列表或字典中进行选择。它属于单值、选项选择组件的广泛类别，提供兼容的API，包括`RadioButtonGroup`、`Select`和`DiscreteSlider`组件。

底层实现为`panel.widgets.RadioBoxGroup`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/RadioBoxGroup.html


## 基本用法

基本的单选框组，可以从选项列表中选择一个值：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnRadioBoxGroup name="RadioBoxGroup" 
                  :options="['Apple', 'Orange', 'Banana']" 
                  :inline="True" 
                  v-model="value.value"
                  @change="on_change" />
  <p>value: {{ value.value }}</p>
</template>
<script lang='py'>
from vuepy import ref

value = ref('Apple')

def on_change(event):
    print(event.new) # Orange
</script>

```


## 字典选项

使用字典作为选项，键作为显示标签，值作为实际值：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnRadioBoxGroup name="RadioBoxGroup" 
                  :options="options" 
                  v-model="value.value" />
  <p>value: {{ value.value }}</p>
</template>
<script lang='py'>
from vuepy import ref

options = {'Apple': 101, 'Orange': 102, 'Banana': 103}
value = ref(101)
</script>

```


## API

### 属性

| 属性名       | 说明                           | 类型                                | 默认值     |
| ----------- | ------------------------------ | ---------------------------------- | --------- |
| options     | 要选择的选项列表或字典           | ^[list\|dict]                       | []        |
| value       | 当前值，必须是选项值之一         | ^[object]                           | None      |
| disabled    | 是否禁用                       | ^[bool]                            | False     |
| inline      | 是否将项目垂直排列在一列中(False)或水平排列在一行中(True) | ^[bool]      | False     |
| name        | 组件标题                       | ^[str]                             | ""        |

### Events

| 事件名         | 说明                       | 类型                                   |
| ------------- | -------------------------- | -------------------------------------- |
| change        | 当值更改时触发的事件         | ^[Callable]`(event: dict) -> None`    |




# IntSlider 整数滑块

整数滑块组件允许使用滑块在设定的范围内选择整数值。

底层实现为`panel.widgets.IntSlider`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/IntSlider.html


## 基本用法

基本的整数滑块，可以通过滑动选择整数值：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnIntSlider name="整数滑块" 
              :start="0" 
              :end="8" 
              :step="2" 
              :value="4" 
              v-model="value.value"/>
</template>
<script lang='py'>
from vuepy import ref

value = ref(4)
</script>

```


## 自定义格式

可以使用自定义格式字符串或Bokeh TickFormatter来格式化滑块值：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnIntSlider name="计数" 
               :format="tick_formatter" 
               :start="0" 
               :end="100" 
               :value="42" />
</template>
<script lang='py'>
from vuepy import ref
from bokeh.models.formatters import PrintfTickFormatter

tick_formatter = PrintfTickFormatter(format='%d 只鸭子')
</script>

```


## 垂直方向

滑块可以设置为垂直方向显示：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnIntSlider name="垂直滑块" 
               orientation="vertical" 
               :start="0" 
               :end="100" 
               :value="50"
               :height="200" />
</template>
<script lang='py'>
from vuepy import ref
</script>

```


## API

### 属性

| 属性名          | 说明                           | 类型                                | 默认值     |
| -------------- | ------------------------------ | ---------------------------------- | --------- |
| start          | 范围的下限                     | ^[int]                             | 0         |
| end            | 范围的上限                     | ^[int]                             | 1         |
| step           | 值之间的间隔                    | ^[int]                             | 1         |
| value          | 所选值，整数类型                | ^[int]                             | 0         |
| value_throttled| 鼠标释放前阻止的所选值，整数类型  | ^[int]                             | 0         |
| bar_color      | 滑块条的颜色，十六进制RGB值      | ^[str]                             | None      |
| direction      | 滑块方向，从左到右('ltr')或从右到左('rtl') | ^[str]                    | 'ltr'     |
| disabled       | 是否禁用                       | ^[bool]                            | False     |
| format         | 应用于滑块值的格式化器           | ^[str\|bokeh.models.TickFormatter] | None      |
| name           | 组件标题                       | ^[str]                             | ""        |
| orientation    | 滑块的显示方向，'horizontal'或'vertical' | ^[str]                    | 'horizontal' |
| tooltips       | 是否在滑块手柄上显示工具提示      | ^[bool]                           | True      |

### Events

| 事件名         | 说明                       | 类型                                   |
| ------------- | -------------------------- | -------------------------------------- |
| change        | 当值更改时触发的事件         | ^[Callable]`(event: dict) -> None`    |




# EditableFloatSlider 可编辑浮点滑块

可编辑浮点滑块组件允许使用滑块在设定的范围内选择浮点数值，并提供一个可编辑的数字输入框以便进行精确控制。

底层实现为`panel.widgets.EditableFloatSlider`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/EditableFloatSlider.html


## 基本用法

基本的可编辑浮点滑块，可以通过滑动或直接输入数字来选择值：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnEditableFloatSlider name="浮点滑块" 
                        :start="0" 
                        :end="3.141" 
                        :step="0.01" 
                        :value="1.57" 
                        v-model="value.value"/>
  <div>当前值: {{ value.value }}</div>
</template>
<script lang='py'>
from vuepy import ref

value = ref(1.57)
</script>

```


## 固定范围

滑块的`value`默认没有界限，可以超过`end`或低于`start`。如果需要将`value`固定在特定范围内，可以使用`fixed_start`和`fixed_end`：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnEditableFloatSlider name="固定范围滑块" 
                        :start="0" 
                        :end="10" 
                        :fixed_start="-3.14" 
                        :fixed_end="15.0"
                        :value="5" />
</template>
<script lang='py'>
from vuepy import ref
</script>

```


## 自定义格式

可以使用自定义格式字符串或Bokeh TickFormatter来格式化滑块值：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnEditableFloatSlider name="距离" 
                        format="1[.]00"
                        :start="0" 
                        :end="10" 
                        :value="5" />
  <PnEditableFloatSlider name="距离（米）" 
                        :format="tick_formatter"
                        :start="0" 
                        :end="10" 
                        :value="5" />
</template>
<script lang='py'>
from vuepy import ref
from bokeh.models.formatters import PrintfTickFormatter

tick_formatter = PrintfTickFormatter(format='%.3f m')
</script>

```


## API

### 属性

| 属性名          | 说明                           | 类型                                | 默认值     |
| -------------- | ------------------------------ | ---------------------------------- | --------- |
| start          | 滑块的下限，可被更低的`value`覆盖 | ^[float]                           | 0.0       |
| end            | 滑块的上限，可被更高的`value`覆盖 | ^[float]                           | 1.0       |
| fixed_start    | 滑块和输入的固定下限，`value`不能低于此值 | ^[float\|None]              | None      |
| fixed_end      | 滑块和输入的固定上限，`value`不能高于此值 | ^[float\|None]              | None      |
| step           | 值之间的间隔                    | ^[float]                           | 0.1       |
| value          | 所选值，浮点类型                | ^[float]                           | 0.0       |
| value_throttled| 鼠标释放前阻止的所选值，浮点类型  | ^[float]                           | 0.0       |
| bar_color      | 滑块条的颜色，十六进制RGB值      | ^[str]                             | None      |
| direction      | 滑块方向，从左到右('ltr')或从右到左('rtl') | ^[str]                    | 'ltr'     |
| disabled       | 是否禁用                       | ^[bool]                            | False     |
| format         | 应用于滑块值的格式化器           | ^[str\|bokeh.models.TickFormatter] | None      |
| name           | 组件标题                       | ^[str]                             | ""        |
| orientation    | 滑块的显示方向，'horizontal'或'vertical' | ^[str]                    | 'horizontal' |
| tooltips       | 是否在滑块手柄上显示工具提示      | ^[bool]                           | True      |

### Events

| 事件名         | 说明                       | 类型                                   |
| ------------- | -------------------------- | -------------------------------------- |
| change        | 当值更改时触发的事件         | ^[Callable]`(event: dict) -> None`    |




# TextAreaInput 多行文本输入框

多行文本输入框允许使用文本输入框输入任何多行字符串。行与行之间使用换行符`\n`连接。

底层实现为`panel.widgets.TextAreaInput`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/TextAreaInput.html


## 基本用法

基本的多行文本输入框，可以输入和获取多行字符串：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnTextAreaInput name="TextAreaInput" 
                   description='tooltip'
                   placeholder='Enter a string here...'
                   v-model="text.value" 
                   sizing_mode='stretch_width'/>
  <p>value: {{ text.value }} </p>
</template>
<script lang='py'>
from vuepy import ref

text = ref("")
</script>

```


## 自动增长

自动增长的 TextAreaInput 会根据输入的文本自动调整高度。设置 `rows` 和 `auto_grow` 可以设置行数下限，而设置 `max_rows` 可以提供上限：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnTextAreaInput name="Growing TextArea" 
                  :auto_grow="True" 
                  :max_rows="10" 
                  :rows="6" 
                  :value="initial_text" 
                  :width="500" />
</template>
<script lang='py'>
from vuepy import ref

initial_text = """\
This text area will grow when newlines are added to the text:

1. Foo
2. Bar
3. Baz
"""
</script>

```


## 可调整大小

可以设置文本区域只在垂直方向可调整大小：

```vue
<!-- --plugins vpanel --show-code -->
<template>
  <PnTextAreaInput name="垂直可调整文本框" resizable="height" />
</template>
<script lang='py'>
from vuepy import ref
</script>

```


## API

### 属性

| 属性名        | 说明                    | 类型      | 默认值     |
| ------------ | ----------------------- | -------- | --------- |
| value        | 当前值，在组件失去焦点时更新 | ^[str]   | ""        |
| value_input  | 当前值，在每次按键时更新    | ^[str]   | ""        |
| auto_grow    | 文本区域是否自动增长以适应内容 | ^[bool] | False     |
| cols         | 文本输入字段的列数         | ^[int]   | 2         |
| disabled     | 是否禁用                 | ^[bool]  | False     |
| max_length   | 输入字段的最大字符长度     | ^[int]   | 5000      |
| max_rows     | 当auto_grow=True时文本输入字段的最大行数 | ^[int] | None |
| name         | 组件标题                 | ^[str]   | ""        |
| placeholder  | 未输入值时显示的占位字符串  | ^[str]   | ""        |
| description      | 鼠标悬停时显示的描述      | ^[str]      | ""        |
| rows         | 文本输入字段的行数         | ^[int]   | 2         |
| resizable    | 布局是否可交互调整大小，如果是，则指定哪个维度：height、width、both、False | ^[bool\|str] | 'both' |

### Events

| 事件名         | 说明                       | 类型                                   |
| ------------- | -------------------------- | -------------------------------------- |
| change        | 当值更改时触发的事件         | ^[Callable]`(event: dict) -> None`    |




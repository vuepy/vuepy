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


# ChatFeed 聊天消息流组件

中层级的布局组件，用于管理一系列 ChatMessage 消息组件。该组件提供后端方法来：
- 发送(附加)消息到聊天记录
- 将字符流式显示到最近的 ChatMessage 中
- 当用户发送消息时执行回调
- 撤销多条 ChatMessage 消息
- 清空所有 ChatMessage 消息

底层实现为`panel.chat.ChatFeed`，参数基本一致，参考文档：https://panel.holoviz.org/reference/chat/ChatFeed.html


## 基本用法

基本的消息流组件可以不带任何参数初始化：


可以通过 send 方法发送消息：


## 消息回调

可以通过设置 callback 来创建更有趣的交互：


回调函数可以根据需要包含不同的参数：
- 只有一个参数时为 contents (消息内容)
- 两个参数时为 contents 和 user (用户名)
- 三个参数时为 contents、user 和 instance (组件实例)

可以通过设置 callback_user 和 callback_avatar 来修改响应者的默认名称和头像：


## 消息流式显示

通过 async generators 可以实现最简单和最理想的输出流式显示：


对于非生成器输出(比如LangChain输出)，也可以使用 stream 方法进行流式显示：


## 自定义样式

可以通过 message_params 传递 ChatEntry 参数：


还可以通过 CSS 自定义消息外观：


## API

### 属性

| 属性名            | 说明                   | 类型                                                   | 默认值  |
| ---------------- | --------------------- | ----------------------------------------------------- | ------- |
| callback         | 消息回调函数           | ^[Callable]                                           | None    |
| callback_user    | 回调消息的默认用户名    | ^[str]                                                | —      |
| callback_avatar  | 回调消息的默认头像      | ^[str]                                               | —      |
| message_params   | ChatEntry 参数         | ^[dict]                                              | {}     |
| show_activity_dot| 显示活动状态点         | ^[bool]                                              | False  |
| height          | 组件高度              | ^[int \| str]                                         | —      |
| width           | 组件宽度              | ^[int \| str]                                         | —      |

### Events

| 事件名   | 说明                  | 类型                                     |
| ------- | -------------------- | ---------------------------------------- |
| message | 发送新消息时触发       | ^[Callable]`(message: dict) -> None`     |
| clear   | 清空消息时触发        | ^[Callable]`() -> None`                  |

### Slots

| 插槽名   | 说明               |
| ------- | ----------------- |
| default | 自定义默认内容      |

### 方法

| 方法名    | 说明                  | 参数                                    |
| -------- | ------------------- | --------------------------------------- |
| send     | 发送消息            | value, user, avatar, footer_objects     |
| stream   | 流式发送消息         | value, user, avatar, message            |
| clear    | 清空所有消息         | -                                       |
| undo     | 撤销最后的消息       | count: int = 1                          |




# ChatAreaInput 聊天输入组件

多行文本输入组件，继承自 TextAreaInput，允许通过文本输入框输入任意多行字符串。支持使用 Enter 键或可选的 Ctrl-Enter 键提交消息。

与 TextAreaInput 不同，ChatAreaInput 默认 auto_grow=True 且 max_rows=10，并且 value 在消息实际发送前不会同步到服务器。如果需要访问输入框中当前的文本，请使用 value_input。

底层实现为`panel.chat.ChatAreaInput`，参数基本一致，参考文档：https://panel.holoviz.org/reference/chat/ChatAreaInput.html


## 基本用法

根据 enter_sends 参数的值(默认为 True)，按 Enter 键或 Ctrl-Enter/Cmd-Enter 键提交消息：


## 实时更新

要查看当前输入的内容而不等待提交，可以使用 value_input 属性：


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

### Slots

| 插槽名   | 说明               |
| ------- | ----------------- |

### 方法

| 方法名    | 说明         | 参数                    |
| -------- | ----------- | ---------------------- |




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

### Events

| 事件名   | 说明           | 类型                               |
| ------- | ------------- | ---------------------------------- |
| -       | -            | -                                  |

### Slots

| 插槽名   | 说明               |
| ------- | ----------------- |
| -       | -                |

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

![image.png](attachment:84748a4a-e38b-4573-b6b5-557e3dc970c9.png)

## 基本用法

基本的聊天界面组件：


## 输入组件

可以自定义输入组件，支持多种输入类型：


可以添加文件上传等其他输入组件：


可以使用 `reset_on_send` 参数控制发送后是否重置输入值：


## 按钮控制

可以通过 `show_rerun`、`show_undo`、`show_clear` 等参数控制底部按钮的显示：


使用 `show_button_name=False` 可以隐藏按钮标签，创建更紧凑的界面：


可以通过 `button_properties` 添加自定义功能按钮：


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


通过 `stream` 方法对内容实现以下操作：
- 附加内容，支持`Markdown`、图像等任何内容
- 覆盖内容

标题也可以通过 `stream_title` 方法对标题实现类似操作。
## Badges

默认头像是 `BooleanStatus` 组件，但可以通过提供 `default_badges` 进行更改。值可以是表情符号、图像、文本或 Panel 对象

## 状态管理

为了显示该步骤正在处理，您可以将`status`设置为 `running` 并提供 `running_title`，使用 `success_title` 在成功时更新标题。

## 错误处理

处理失败状态：


## 标题流式显示

支持标题的流式更新：


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




# PnChatFeed 聊天流

PnChatFeed是一个中层布局组件，用于管理一系列聊天消息(ChatMessage)项。该组件提供后端方法来发送消息、流式传输令牌、执行回调、撤销消息以及清除聊天记录。

底层实现为`panel.chat.ChatFeed`，参数基本一致，参考文档：https://panel.holoviz.org/reference/chat/ChatFeed.html


## 基本用法

`PnChatFeed`可以不需要任何参数初始化，通过`send`方法发送聊天消息。


## 回调函数

添加回调函数可以使`PnChatFeed`更加有趣。回调函数的签名必须包含最新可用的消息值`contents`。
除了`contents`之外，签名还可以包含最新可用的`user`名称和聊天`instance`。


可以更新`callback_user`和`callback_avatar`来分别更改响应者的默认名称和头像。


指定的`callback`也可以返回一个包含`value`、`user`和`avatar`键的字典，这将覆盖默认的`callback_user`和`callback_avatar`。


如果不希望与`send`一起触发回调，请将`respond`设置为`False`。


可以通过将`callback_exception`设置为`"summary"`来显示异常。


## 异步回调

`PnChatFeed`还支持*异步*`callback`。我们建议尽可能使用*异步*`callback`以保持应用程序的快速响应，*只要函数中没有阻塞事件循环的内容*。


流式输出的最简单和最优方式是通过*异步生成器*。如果您不熟悉这个术语，只需在函数前加上`async`，并用`yield`替换`return`。


如果不连接字符，也可以持续替换原始消息。


也可以手动触发回调与`respond`。这对于从初始消息实现一系列响应很有用！


## 编辑回调

可以将`edit_callback`附加到`PnChatFeed`以处理消息编辑。签名必须包含最新可用的消息值`contents`、编辑消息的索引和聊天`instance`。


## 步骤

可以通过一系列`ChatStep`提供中间步骤，如思想链。


## 提示用户

可以使用`prompt_user`暂时暂停代码执行并提示用户回答问题或填写表单，该方法接受任何Panel `component`和后续`callback`（带有`component`和`instance`作为args）在提交后执行。


还可以设置一个`predicate`来评估组件的状态，例如小部件是否有值。如果提供，当谓词返回`True`时，提交按钮将被启用。


## 序列化

聊天历史可以通过`serialize`并设置`format="transformers"`来序列化，以供`transformers`或`openai`包使用。


可以设置`role_names`来显式映射角色到ChatMessage的用户名。


## 流式传输

如果返回的对象不是生成器（特别是LangChain输出），仍然可以使用`stream`方法流式传输输出。


## 自定义

可以通过`message_params`传递`ChatEntry`参数。


直接将这些参数传递给ChatFeed构造函数，它将自动转发到`message_params`中。


也可以通过设置`message_params`参数来自定义聊天流的外观。


## 自定义聊天界面

您也可以在`PnChatFeed`的基础上构建自己的自定义聊天界面。


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

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |

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


ChatMessage可以显示任何Panel可以显示的Python对象，例如Panel组件、数据框和图表：


可以指定自定义用户名和头像：


## 消息更新

组件的值、用户名和头像都可以动态更新：

将输出流式传输到`ChatMessage`最简单、最好的方式是通过异步生成器。

## 样式

如果您想要一个仅显示 `value` 的普通界面，请将 `show_user` 、 `show_copy_icon` 、 `show_avatar` 和 `show_timestamp` 设置为 `False` ，并为 `reaction_icons` 提供一个空的 `dict` 。

可以设置常用的样式和布局参数，如 `sizing_mode` 、 `height` 、 `width` 、 `max_height` 、 `max_width` 和 `styles` 。

## 代码高亮

支持代码块的语法高亮（需要安装 pygments）：


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



# Trend 趋势指示器

趋势指示器提供了一个值及其最近趋势的可视化表示。它支持向图表组件流式传输数据，使得能够对某个值的最近趋势提供高性能的实时更新。

底层实现为`panel.widgets.Trend`，参数基本一致，参考文档：https://panel.holoviz.org/reference/indicators/Trend.html


## 基本用法

最简单的`Trend`只需要提供带有x和y值的`data`，可以声明为字典或`pandas.DataFrame`。`value`和`value_change`值将从数据中自动计算：


## 数据流式传输

`Trend`指示器还提供了一个方便的方法来流式传输新数据，支持`rollover`参数来限制显示的数据量。我们将使用`setInterval`来定期更新图表：


## 图表类型

除了默认的`plot_type`外，流指示器还支持其他几种选项：


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

### Slots

| 插槽名   | 说明               |
| ---     | ---               |

### 方法

| 名称      | 说明                             | 参数                                                  |
| -------- | -------------------------------- | ----------------------------------------------------|
| stream   | 向图表流式传输新数据，支持限制显示的数据量 | data: 要添加的新数据, rollover: 保留的最大数据点数量    |



# TooltipIcon 提示图标

提示图标组件提供了一个带有工具提示的图标。`value`将是工具提示内的文本。

底层实现为`panel.widgets.TooltipIcon`，参数基本一致，参考文档：https://panel.holoviz.org/reference/indicators/TooltipIcon.html


## 基本用法

`TooltipIcon`指示器可以使用字符串进行实例化：


## 使用Bokeh.models.Tooltip

也可以使用`bokeh.models.Tooltip`进行实例化：


## 与其他组件组合使用

`TooltipIcon`可以用来为组件添加更多信息：


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

### Slots

| 插槽名   | 说明               |
| ---     | ---               |

### 方法

| 属性名 | 说明 | 类型 |
| --- | --- | --- |



# Gauge 仪表盘

仪表盘提供了一个值的可视化表示，以仪表或速度计形式展示。`Gauge`组件使用ECharts库渲染。

底层实现为`panel.widgets.Gauge`，参数基本一致，参考文档：https://panel.holoviz.org/reference/indicators/Gauge.html


## 基本用法

最简单的仪表盘只需要设置一个在指定范围内的`value`。默认的格式化器和范围假设你提供的是百分比值：


## 自定义格式与颜色阈值

如果我们想要显示其他值，例如发动机每分钟转速，我们可以设置不同的`bounds`值并重写`format`。此外，我们还可以提供一组不同的颜色，定义应在提供范围的哪个点上更改颜色。`colors`接受一个元组列表，定义分数和颜色：


## 自定义指针颜色

您还可以通过传递自定义选项来更改指针的颜色：


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

### Slots

| 插槽名   | 说明               |
| ---     | ---               |

### 方法

| 属性名 | 说明 | 类型 |
| --- | --- | --- |



# Tqdm 进度指示器

Tqdm指示器包装了著名的[`tqdm`](https://github.com/tqdm/tqdm)进度指示器，并显示某个目标的进度。可以在笔记本或Panel Web应用程序中使用它。

[![Tqdm](https://raw.githubusercontent.com/tqdm/tqdm/master/images/logo.gif)](https://github.com/tqdm/tqdm)

底层实现为`panel.widgets.Tqdm`，参数基本一致，参考文档：https://panel.holoviz.org/reference/indicators/Tqdm.html


## 基本用法

要使用`Tqdm`指示器，只需实例化该对象，然后像使用`tqdm.tqdm`一样使用生成的变量，即可迭代任何可迭代对象：


大多数[tqdm支持的参数](https://github.com/tqdm/tqdm#parameters)都可以传递给`Tqdm`指示器的call方法。

## 嵌套使用

当嵌套使用`Tqdm`指示器时，使用`margin`参数可以直观地表示嵌套级别。


## Pandas集成

要使用tqdm pandas集成，可以通过调用`tqdm.pandas`并传入所有配置选项来激活它。激活后，`progress_apply`方法在`pandas.DataFrame`上可用：


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


## 自定义格式与颜色

如果我们想要显示其他值，例如发动机每分钟转速，我们可以设置不同的`bounds`值并重写`format`。此外，我们还可以提供一组不同的颜色，定义应在提供范围的哪个点上更改颜色。`colors`可以接受颜色列表或元组列表：


## 显示颜色边界

如果我们想要显示不同颜色之间的过渡点，我们也可以启用`show_boundaries`：


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

### Slots

| 插槽名   | 说明               |
| ---     | ---               |

### 方法

| 属性名 | 说明 | 类型 |
| --- | --- | --- |



# Progress 进度条

进度条组件根据当前`value`和`max`值显示朝着某个目标的进度。如果未设置`value`或设置为-1，则`Progress`组件处于不确定模式，若`active`设置为True，将会显示动画效果。

底层实现为`panel.widgets.Progress`，参数基本一致，参考文档：https://panel.holoviz.org/reference/indicators/Progress.html


## 基本用法

`Progress`组件可以使用或不使用值来实例化。如果给定`value`，进度条将根据`max`值（默认为100）的进度进行填充：


## 不确定状态

`Progress`也可以在不设置`value`的情况下实例化，显示不确定状态：


## 不同颜色

`Progress`组件支持多种条形颜色：


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

### Slots

| 插槽名   | 说明               |
| ---     | ---               |

### 方法

| 属性名 | 说明 | 类型 |
| --- | --- | --- |



# LoadingSpinner 加载旋转器

加载旋转器提供了加载状态的可视化表示。当`value`设置为`True`时，旋转部分会旋转；设置为`False`时，旋转部分会停止旋转。

底层实现为`panel.widgets.LoadingSpinner`，参数基本一致，参考文档：https://panel.holoviz.org/reference/indicators/LoadingSpinner.html


## 基本用法

`LoadingSpinner`可以实例化为旋转或静止状态：


## 颜色与背景

`LoadingSpinner`支持多种旋转部分颜色和背景：


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

### Slots

| 插槽名   | 说明               |
| ---     | ---               |

### 方法

| 属性名 | 说明 | 类型 |
| --- | --- | --- |



# Number 数字指示器

数字指示器提供了一个值的可视化表示，该值可以根据提供的阈值进行着色。

底层实现为`panel.widgets.Number`，参数基本一致，参考文档：https://panel.holoviz.org/reference/indicators/Number.html


## 基本用法

`Number`指示器可用于指示一个简单的数字，并根据需要进行格式化：


## 颜色阈值

如果我们想要指定特定的阈值，在这些阈值下指示器会改变颜色：


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

### Slots

| 插槽名   | 说明               |
| ---     | ---               |

### 方法

| 属性名 | 说明 | 类型 |
| --- | --- | --- |



# BooleanStatus 布尔状态指示器

布尔状态指示器提供了布尔状态的可视化表示，以填充或非填充圆圈的形式展示。当`value`设置为`True`时，指示器将被填充；设置为`False`时，指示器将不被填充。

底层实现为`panel.widgets.BooleanStatus`，参数基本一致，参考文档：https://panel.holoviz.org/reference/indicators/BooleanStatus.html


## 基本用法

BooleanStatus组件可以实例化为`False`或`True`状态：


## 颜色设置

BooleanStatus指示器支持多种颜色：


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

### Slots

| 插槽名   | 说明               |
| ---     | ---               |

### 方法

| 属性名 | 说明 | 类型 |
| --- | --- | --- |



# Dial 刻度盘指示器

刻度盘指示器提供了一个简单的径向刻度盘来可视化表示数值。

底层实现为`panel.widgets.Dial`，参数基本一致，参考文档：https://panel.holoviz.org/reference/indicators/Dial.html


## 基本用法

最简单的刻度盘只需要设置一个在指定范围内的`value`。默认的格式化器和范围假设你提供的是百分比值：


## 自定义格式与颜色阈值

如果我们想要显示其他值，例如发动机每分钟转速，我们可以设置不同的`bounds`值并重写`format`。此外，我们还可以提供一组不同的颜色，定义应在提供范围的哪个点上更改颜色。`colors`接受一个元组列表，定义分数和颜色：


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

### Slots

| 插槽名   | 说明               |
| ---     | ---               |

### 方法

| 属性名 | 说明 | 类型 |
| --- | --- | --- |



# FlexBox 弹性布局

FlexBox是一种基于CSS Flexbox的列表式布局组件，提供了灵活的内容排列方式，可以自动换行和调整元素布局。

底层实现为`panel.layout.FlexBox`，参数基本一致，参考文档：https://panel.holoviz.org/reference/layouts/FlexBox.html


## 基本用法

默认情况下，FlexBox使用`direction='row'`和`flex_wrap='wrap'`，使得元素按行排列并在必要时换行：


## 列式布局

可以通过设置`flex_direction='column'`让FlexBox按列排列元素：


## 元素对齐方式

可以通过`align_content`、`align_items`和`justify_content`控制元素如何在容器中对齐和分布：


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

### 方法

| 方法名 | 说明 | 类型 |
| --- | --- | --- |



# Divider 分割线

分割线用于分隔内容，在视觉上创建一个水平分隔，自动占据容器的全宽。

底层实现为`panel.layout.Divider`，参数基本一致，参考文档：https://panel.holoviz.org/reference/layouts/Divider.html


## 基本用法

使用分割线将不同组件清晰地分隔开：


## 响应式布局

启用响应式尺寸后，分割线会自动占据全宽：


## API

### 属性

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| style | 分割线的样式 | ^[Object] | — |
| margin | 分割线的外边距 | ^[Tuple] | — |

### Events

| 事件名 | 说明 | 类型 |
| --- | --- | --- |

### Slots

| 插槽名 | 说明 |
| --- | --- |

### 方法

| 方法名 | 说明 | 类型 |
| --- | --- | --- |



# Row 行容器

Row 允许在水平容器中排列多个组件。它拥有类似列表的 API，包含 append 、 extend 、 clear 、 insert 、 pop 、 remove 和 __setitem__ 方法，从而可以交互式地更新和修改布局

底层实现为`panel.Row`，参数基本一致，参考文档：https://panel.holoviz.org/reference/layouts/Row.html


## 基本用法


## API

### 属性

| 属性名    | 说明                 | 类型   | 默认值 |
| -------- | ------------------- | ------ | ------ |
| objects  | List of child nodes  | list   | —      |
| scroll   | Enable scrollbars    | bool   | False  |

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




# Feed 信息流

Feed组件继承自Column布局，允许在垂直容器中排列多个组件，但限制了任何时刻渲染的对象数量，适用于显示大量条目。

底层实现为`panel.layout.Feed`，参数基本一致，参考文档：https://panel.holoviz.org/reference/layouts/Feed.html


## 基本用法

Feed组件可以显示大量条目，但只会加载和渲染当前可见的部分和缓冲区内的内容：


## 初始化显示最新条目

通过设置`view_latest=True`，可以让Feed在初始化时显示最新条目：


## 添加滚动按钮

通过设置`scroll_button_threshold`，可以让Feed显示一个可点击的滚动按钮，帮助用户快速滚动到底部：


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

## 固定尺寸

可以给Column设置固定的宽度和高度，内部元素会根据布局模式进行调整。


## 自适应宽度

当没有指定固定尺寸时，Column会根据其内容的大小自动调整。


## 启用滚动条

当内容超出容器大小时，可以启用滚动条。


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


## 比较数据可视化

该布局可以比较任何类型的组件，例如，我们可以比较两个小提琴图：


## 自定义滑块样式

您可以自定义滑块的宽度和颜色：


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

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| —       | —                 |

### 方法

| 属性名 | 说明 | 类型 |
| --- | --- | --- |



# WidgetBox 组件容器

用于分组小部件的垂直容器，具有默认样式。

底层实现为`panel.WidgetBox`，参数基本一致，参考文档：https://panel.holoviz.org/reference/layouts/WidgetBox.html


## 基本用法


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


## 响应式网格

通过设置合适的响应式布局参数，GridStack可以适应不同的屏幕尺寸：


## 禁用拖拽或调整大小

可以通过设置`allow_drag`和`allow_resize`参数来控制是否允许拖拽和调整大小：


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

### 方法

| 方法名 | 说明 | 类型 |
| --- | --- | --- |

## GridStackItem API

### 属性

| 属性名        | 说明                             | 类型    | 默认值  |
|--------------|-------------------------------------------|---------------------|--------|
| row_start    | 开始行的索引                      | ^[Number]           | 0 |
| row_end      | 结束行的索引，开区间               | ^[Number]           | `row_start+1` |
| col_start    | 开始列的索引                      | ^[Number]           | 0 |
| col_end      | 结束列的索引，开区间               | ^[Number]           | `col_start+1` |


### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | 默认内容 |

### 方法

| 方法名 | 说明 | 类型 |
| --- | --- | --- |



# GridBox 网格布局

GridBox是一种列表式布局，将对象按照指定的行数和列数包装成网格。

底层实现为`panel.layout.GridBox`，参数基本一致，参考文档：https://panel.holoviz.org/reference/layouts/GridBox.html


## 基本用法

GridBox可以将元素按指定的列数排列，自动换行形成网格：


## 动态调整列数

可以动态地调整GridBox的列数，从而改变网格的排列：


## 按行数排列

除了指定列数，也可以使用`nrows`指定行数：


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

### 方法

| 方法名 | 说明 | 类型 |
| --- | --- | --- |



# FloatPanel 浮动面板

FloatPanel提供一个可拖动的容器，可以放置在其父容器内部或完全自由浮动。

底层实现为`panel.layout.FloatPanel`，参数基本一致，参考文档：https://panel.holoviz.org/reference/layouts/FloatPanel.html


## 基本用法

浮动面板可以包含在父容器内：


## 自由浮动

浮动面板也可以配置为自由浮动，不受父容器限制：


## 自定义配置

FloatPanel可以通过`config`参数进行高度自定义，比如移除关闭按钮：

要了解更多配置选项，请查看 [jsPanel 文档](https://jspanel.de/)


## 状态控制

可以通过`status`属性控制FloatPanel的状态：


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

### 方法

| 方法名 | 说明 | 类型 |
| --- | --- | --- |



# Accordion 折叠面板

折叠面板将内容区域组织进多个折叠面板，通过点击面板的标题可以展开或收缩内容。

底层实现为`panel.layout.Accordion`，参数基本一致，参考文档：https://panel.holoviz.org/reference/layouts/Accordion.html


## 基本用法

折叠面板可以包含任意数量的子项，每个子项可以包含任意内容。


## 切换模式

当`toggle`属性设置为`True`时，同一时间只能展开一个面板。


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

The Modal component displays content in a dialog overlay. Use the `open` prop to control visibility, and you can add any content via slot.


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


## 动态添加标签页

==Todo==
## 动态渲染

启用 dynamic 选项后，仅当前活动的标签页会被渲染，只有当切换到新标签页时才会加载其内容。这对于服务器环境或笔记本环境中显示大量标签页，或当单个组件渲染体量极大/渲染成本极高时尤为有用。但需注意：在没有实时服务器的情况下，非活动标签页的内容将不会被加载。
## 可关闭标签页

设置 closable 为 True 后，标签页会显示关闭按钮：
## 标签位置

通过 tabs_location 参数可以调整标签头的位置：
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


## 折叠控制

卡片可以通过`collapsible`和`collapsed`属性来控制是否可折叠以及初始状态是否折叠。


## 自定义头部

卡片可以使用自定义的头部，而不仅仅是标题文本。


## 隐藏头部

可以通过`hide_header`属性完全隐藏卡片的头部。


## 布局控制

可以设置卡片的固定尺寸，或者让它根据内容自适应。


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

### 方法

| 方法名 | 说明 | 类型 |
| --- | --- | --- |



# GridSpec 网格规格

GridSpec布局是一种类似数组的布局，允许使用简单的API将多个Panel对象排列在网格中，可以将对象分配到单个网格单元或网格跨度。

底层实现为`panel.layout.GridSpec`，参数基本一致，参考文档：https://panel.holoviz.org/reference/layouts/GridSpec.html


## 基本用法

GridSpec可以创建固定大小的网格布局，并通过GridSpecItem放置组件：


## 响应式网格

除了固定大小的网格外，GridSpec还支持响应式尺寸，可以在浏览器窗口调整大小时动态调整：


## 复杂布局示例

使用GridSpec可以创建复杂的仪表板布局：


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

### 方法

| 方法名 | 说明 | 类型 |
| --- | --- | --- |


## GridSpecItem API

### 属性

| 属性名        | 说明                             | 类型    | 默认值  |
|--------------|-------------------------------------------|---------------------|--------|
| row_start    | 开始行的索引                      | ^[Number]           | 0 |
| row_end      | 结束行的索引，开区间               | ^[Number]           | `row_start+1` |
| col_start    | 开始列的索引                      | ^[Number]           | 0 |
| col_end      | 结束列的索引，开区间               | ^[Number]           | `col_start+1` |


### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | 默认内容 |

### 方法

| 方法名 | 说明 | 类型 |
| --- | --- | --- |



# Column 垂直布局

Column组件允许在垂直容器中排列多个组件。

底层实现为`panel.layout.Column`，参数基本一致，参考文档：https://panel.holoviz.org/reference/layouts/Column.html


## 基本用法

Column组件可以垂直排列多个元素。

`Col`是`Column`的同名组件。


# VTK 三维可视化

`PnVTK` 组件可以在 Panel 应用程序中渲染 VTK 场景，使得可以与复杂的 3D 几何体进行交互。
它允许在 Python 端定义的 `vtkRenderWindow` 与通过 vtk-js 在组件中显示的窗口之间保持状态同步。
在这种情况下，Python 充当服务器，向客户端发送有关场景的信息。
同步只在一个方向进行：Python => JavaScript。在 JavaScript 端所做的修改不会反映回 Python 的 `vtkRenderWindow`。

底层实现为`panel.pane.VTK`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/VTK.html


## 基本用法

与直接使用 `VTK` 相比，在 Panel 中使用它有一些区别。由于 VTK 面板处理对象的渲染和与视图的交互，我们不需要调用 `vtkRenderWindow` 的 `Render` 方法（这会弹出传统的 VTK 窗口），也不需要指定 `vtkRenderWindowInteractor`。


我们还可以向场景添加其他 actor，然后调用 `synchronize` 方法来更新组件：

## 与 PyVista 集成

这些示例大多使用 [PyVista](https://docs.pyvista.org/) 库作为 VTK 的便捷接口。

虽然这些示例通常可以重写为仅依赖于 VTK 本身，但 `pyvista` 支持简洁的 Python 语法，用于处理 VTK 对象所需的主要功能。

例如，上面的 VTK 示例可以使用 PyVista 重写如下：


## 导出场景

场景可以导出，生成的文件可以由官方的 vtk-js 场景导入器加载：


## 高级用法和交互性

### 键盘绑定和方向部件

`PnVTK` 组件支持键盘绑定和方向部件，以增强用户交互体验：


键盘绑定允许用户使用以下键:
- s: 将所有 actor 表示设置为*表面*
- w: 将所有 actor 表示设置为*线框*
- v: 将所有 actor 表示设置为*顶点*
- r: 居中 actor 并移动相机，使所有 actor 可见

## 添加坐标轴

使用 `axes` 参数可以在 3D 视图中显示坐标轴：


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

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |

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


或者，该组件也可以从`vtkImageData`对象构建。这种类型的对象可以直接使用vtk或pyvista模块构建：


## 交互控制

`PnVTKVolume`组件公开了许多选项，可以从Python和JavaScript更改。尝试交互式地测试这些参数的效果：


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

### Events

| 事件名 | 说明 | 类型 |
| ------ | ---- | ---- |
|        |      |      |

### Slots

| 插槽名   | 说明           |
| -------- | -------------- |
|          |                |

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


## 控制播放

播放器可以使用其自身的控件控制，也可以通过 Python 代码控制。要在代码中暂停或取消暂停，请使用 `paused` 属性：


## NumPy 数组输入

当提供 NumPy 数组或 Torch 张量时，应指定 `sample_rate`。

在此示例中，我们绘制了一个频率调制信号：


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



# Video 视频组件

`PnVideo` 组件允许在 Panel 应用程序中显示视频播放器，可以用于显示本地或远程视频文件。该组件还提供对播放器状态的访问和控制，包括切换播放/暂停状态、循环状态、当前时间和音量。根据浏览器的不同，视频播放器支持 `mp4`、`webm` 和 `ogg` 容器以及多种编解码器。

底层实现为`panel.pane.Video`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/Video.html


## 基本用法

`PnVideo` 组件可以通过 URL 指向远程视频文件或本地视频文件（在这种情况下，数据将被嵌入）：


## 控制视频播放

可以通过播放器自身的控件以及使用组件属性来控制视频播放。例如，通过修改 `paused` 属性来暂停或恢复播放：


## 音量控制

可以通过设置 `volume` 属性来控制视频的音量：


## 访问当前播放时间

可以通过 `time` 属性读取和设置当前播放时间（以秒为单位）：


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



# Folium 地图

`PnFolium` 组件渲染 [folium](http://python-visualization.github.io/folium/) 交互式地图。

底层实现为`panel.pane.plot.Folium`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/Folium.html


## 基本用法

`PnFolium` 组件使用 `folium` 提供的内置 HTML 表示来渲染地图：


## 更新地图

与任何其他组件一样，可以通过设置 `object` 参数来更新 `PnFolium` 组件的视图：


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



# SVG 矢量图

`PnSVG` 组件如果提供本地路径，则将 `.svg` 矢量图文件嵌入到面板中，或者如果提供 URL，则会链接到远程图像。

底层实现为`panel.pane.SVG`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/SVG.html


## 基本用法

`PnSVG` 组件可以指向任何本地或远程 `.svg` 文件。如果给定以 `http` 或 `https` 开头的 URL，则 `embed` 参数决定图像是嵌入还是链接到：


## 调整大小

我们可以通过设置特定的固定 `width` 或 `height` 来调整图像的大小：


与任何其他组件一样，`PnSVG` 组件可以通过设置 `object` 参数来更新：


## 响应式 SVG

您也可以使用 *响应式* `sizing_mode`，如 `'stretch_width'`：


请注意，默认情况下图像的宽高比是固定的，要覆盖此行为，请设置 `fixed_aspect=false` 或提供固定的 `width` 和 `height` 值。

## 编码选项

SVG 图像可以使用 base64 编码进行嵌入。使用 `encode` 参数可以控制是否对 SVG 进行编码：


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



# HoloViews 可视化

[HoloViews](https://holoviews.org/) 是一个流行且功能强大的数据可视化库，支持多种数据和绘图后端。

[hvPlot](https://hvplot.holoviz.org/index.html)（快速可视化）和 [GeoViews](https://holoviz.org/assets/geoviews.png)（空间可视化）都是基于 HoloViews 构建的，并产生 `HoloViews` 对象。

**Panel、HoloViews、hvPlot 和 GeoViews 都是 [HoloViz](https://holoviz.org) 生态系统的成员，它们可以完美地协同工作**。

`PnHoloViews` 组件使用 HoloViews 支持的绘图后端之一渲染 [HoloViews](https://holoviews.org/) 对象。这包括 [hvPlot](https://hvplot.holoviz.org/index.html) 和 [GeoViews](https://holoviz.org/assets/geoviews.png) 生成的对象。

`PnHoloViews` 组件支持显示包含小部件的交互式 [`HoloMap`](https://holoviews.org/reference/containers/bokeh/HoloMap.html) 和 [`DynamicMap`](https://holoviews.org/reference/containers/bokeh/DynamicMap.html) 对象。`PnHoloViews` 组件甚至允许自定义小部件类型及其相对于图表的位置。

底层实现为`panel.pane.HoloViews`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/HoloViews.html


## 基本用法

`PnHoloViews` 组件将任何 `HoloViews` 对象自动转换为可显示的面板，同时保持其所有交互功能：


通过设置组件的 `object` 可以像所有其他组件对象一样更新图表：


您也可以显示 [hvPlot](https://hvplot.holoviz.org/)（和 [GeoViews](https://geoviews.org/)）对象，因为它们是 `HoloViews` 对象：


您还可以显示 [`HoloMap`](https://holoviews.org/reference/containers/bokeh/HoloMap.html) 和 [`DynamicMap`](https://holoviews.org/reference/containers/bokeh/DynamicMap.html) 对象。

[HoloViews](https://holoviews.org/)（框架）如果 [`HoloMap`](https://holoviews.org/reference/containers/bokeh/HoloMap.html) 或 [DynamicMap](https://holoviews.org/reference/containers/bokeh/DynamicMap.html) 声明了任何键维度，它原生渲染带有小部件的图表。这种方法高效地仅更新图表内的数据，而不是完全替换图表。


## 后端选择

`PnHoloViews` 组件默认使用 'bokeh' 绘图后端（如果没有通过 `holoviews` 加载后端），但您可以根据需要将后端更改为 'bokeh'、'matplotlib' 和 'plotly' 中的任何一个。

### Bokeh

Bokeh 是默认的绘图后端，所以通常您不必指定它。但让我们在这里展示它是如何工作的：


### Matplotlib

Matplotlib 后端允许生成用于打印和出版的图形。如果你想允许响应式大小调整，你可以设置 `format='svg'`，然后使用标准的响应式 `sizing_mode` 设置：


### Plotly

要使用 'plotly' 绘图后端，您需要运行 `hv.extension("plotly")` 来配置 'plotly' 后端。

如果您使用的是 `hvPlot`，您可以使用 `hvplot.extension("plotly")` 来代替：


### 动态后端切换

您还可以通过小部件动态更改绘图后端：


## 链接坐标轴

默认情况下，具有共享键或值维度的图表的坐标轴是链接的。您可以通过将 `linked_axes` 参数设置为 `False` 来删除链接：


## 主题

您可以更改 `theme`：


## 布局和小部件参数

`PnHoloViews` 组件提供了 `layout` 属性，其中包含 `HoloViews` 组件和 `widget_box`。

### 居中

您可以通过 `center` 参数将图表居中：


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


为 LaTeX 字符串添加前缀 `r` 很重要，这样可以使字符串成为*原始*字符串，不会转义 `\\` 字符：


与其他组件一样，`PnLaTeX` 组件可以动态更新：


如果两个渲染器都已加载，我们可以覆盖默认渲染器：


## 复杂公式示例

`PnLaTeX` 组件可以渲染复杂的数学公式：


## SymPy 集成

可以渲染 SymPy 表达式：


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



# Matplotlib 图表

`PnMatplotlib` 组件允许在 Panel 应用程序中显示 [Matplotlib](http://matplotlib.org) 图表。这包括由 [Seaborn](https://seaborn.pydata.org/)、[Pandas `.plot`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.plot.html)、[Plotnine](https://plotnine.readthedocs.io/) 和任何其他基于 `Matplotlib` 构建的绘图库创建的图表。

`PnMatplotlib` 组件将以声明的 DPI 将 `object` 渲染为 PNG 或 SVG，然后显示它。

底层实现为`panel.pane.Matplotlib`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/Matplotlib.html


## 基本用法

创建一个简单的 Matplotlib 图表并显示：


通过修改图表并使用组件对象的 `param.trigger('object')` 方法，我们可以轻松更新图表：


与所有其他模型一样，`PnMatplotlib` 组件也可以通过直接设置 `object` 来更新：


## 使用 Matplotlib pyplot 接口

您可能已经注意到，我们在上面没有使用 `matplotlib.pyplot` API。我们这样做是为了避免需要特意关闭图形。如果图形未关闭，将导致内存泄漏。

**您可以使用 `matplotlib.pyplot` 接口，但随后必须像下面所示特别关闭图形！**


## 修复裁剪问题

如果您发现图形在边缘被裁剪，可以设置 `tight=true`：


## 响应式图表

如果您希望您的图表能够响应式地适应它们所在的任何容器，那么您应该使用适当的 `sizing_mode` 结合：

- `format="svg"`：获得更好看的调整大小后的图表
- `fixed_aspect=true`：允许 'svg' 图像独立调整其高度和宽度 
- `fixed_aspect=false`（默认）：允许 'svg' 图像调整其高度和宽度，同时保持宽高比

让我们先使用默认的 `'png'` 格式和 `sizing_mode="stretch_width"` 显示：


如果您的窗口宽度较大，您会在两侧看到一些大的粉色区域。如果减小窗口宽度，您会看到图表自适应调整大小。

使用 `'svg'` 格式可以使图形占据全宽：


但这可能会使图形太高。让我们尝试使用固定的 `height`：


但也许我们希望图形占据全宽。让我们将 `fixed_aspect` 更改为 `false`：


总之，通过使用适当组合的 `format`、`fixed_aspect` 和 `sizing_mode` 值，您应该能够实现所需的响应式大小调整。

## 使用 Seaborn

我们建议创建一个 Matplotlib `Figure` 并将其提供给 Seaborn：


您也可以直接使用 Seaborn，但请记住手动关闭 `Figure` 以避免内存泄漏：


## 使用 Pandas.plot

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

## 布局示例

`PnPlotly` 组件支持任意复杂度的布局和子图，允许显示即使是深度嵌套的 Plotly 图形：


## 响应式图表

通过在 Plotly 布局上使用 `autosize` 选项和 `PnPlotly` 组件的响应式 `sizing_mode` 参数，可以使 Plotly 图表具有响应性：


## 图表配置

您可以通过 `config` 参数设置 [Plotly 配置选项](https://plotly.com/javascript/configuration-options/)。让我们尝试配置 `scrollZoom`：


尝试在图表上用鼠标滚动！

## 增量更新

您可以通过使用字典而不是 Plotly Figure 对象来高效地增量更新轨迹或布局，而不是更新整个 Figure。

请注意，增量更新只有在将 `Figure` 定义为字典时才会高效，因为 Plotly 会复制轨迹，这意味着原地修改它们没有效果。修改数组将仅发送该数组（使用二进制协议），从而实现快速高效的更新。


## 事件处理

`PnPlotly` 组件提供对 [Plotly 事件](https://plotly.com/javascript/plotlyjs-events/)的访问，如点击、悬停和选择(使用`Box Select`、`Lasso Select`工具)等：


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

### 方法

| 属性名 | 说明 | 类型 |
| --- | --- | --- |



# PDF 文档

`PnPDF` 组件如果提供本地路径，则将 `.pdf` 文档嵌入到面板中，或者如果提供 URL，则会链接到远程文件。

底层实现为`panel.pane.PDF`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/PDF.html


## 基本用法

`PnPDF` 组件可以指向任何本地或远程 `.pdf` 文件。如果给定以 `http` 或 `https` 开头的 URL，则 `embed` 参数决定 PDF 是嵌入还是链接到：


与任何其他组件一样，可以通过设置 `object` 参数来更新 `PnPDF` 组件：


## 设置起始页

使用 `start_page` 参数，您可以指定加载页面时 PDF 文件的起始页：


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



# ReactiveExpr 响应式表达式

`PnReactiveExpr` 组件可以渲染 [Param `rx` 对象](https://param.holoviz.org/user_guide/Reactive_Expressions.html)，它代表一个响应式表达式，同时显示表达式中包含的小部件和表达式的最终输出。小部件相对于输出的位置可以设置，也可以完全移除小部件。

请注意，当导入 `panel_vuepy as vpanel` 时，可以使用 `vpanel.rx` 代替 [`param.rx`](https://param.holoviz.org/user_guide/Reactive_Expressions.html)。

有关使用 `rx` 的详细信息，请参阅 [`param.rx` 文档](https://param.holoviz.org/user_guide/Reactive_Expressions.html)。

底层实现为`panel.pane.ReactiveExpr`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/ReactiveExpr.html

建议用`vuepy`的`computed` 来代替该功能。

## 基本用法

[`param.rx`](https://param.holoviz.org/user_guide/Reactive_Expressions.html) API 是构建声明式和响应式 UI 的强大工具。

让我们看几个例子：


在底层，Panel 确保上面的*响应式表达式*被渲染在 `PnReactiveExpr` 组件中。您也可以显式地这样做：


响应式表达式从不是"死胡同"。您始终可以更新和更改*响应式表达式*。


您还可以组合*响应式表达式*：


## 布局选项

您可以更改 `widget_location`：


您可以将 `widget_layout` 更改为 `Row`：


您可以水平 `center` 输出：


通过设置 `show_widgets=False` 可以隐藏小部件：


## 响应式表达式作为引用

在笔记本中显式或隐式地使用 `PnReactiveExpr` 组件非常适合探索。但这并不是很高效，因为每当响应式表达式重新渲染时，Panel 都必须创建一个新的组件来渲染您的输出。

相反，您可以并且应该将*响应式表达式*作为*引用*传递给特定的 Panel 组件。Panel 组件可以动态解析表达式的值：



> **引用方法通常应该是首选**，因为它更具声明性和明确性，允许 Panel 有效地更新现有视图，而不是完全重新渲染输出。

## 样式化 DataFrame 示例

让我们通过一个稍微复杂一点的例子来展示，构建一个表达式来动态加载一些数据并从中采样 N 行：


现在我们有了一个符合我们需求的表达式，可以将其用作引用来响应式地更新 `Tabulator` 小部件的 `value`：


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



# PNG 图像

`PnPNG` 组件如果提供本地路径，则将 `.png` 图像文件嵌入到面板中，或者如果提供 URL，则会链接到远程图像。

底层实现为`panel.pane.PNG`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/PNG.html


## 基本用法

`PnPNG` 组件可以指向任何本地或远程 `.png` 文件。如果给定以 `http` 或 `https` 开头的 URL，则 `embed` 参数决定图像是嵌入还是链接到：


## 调整大小

我们可以通过设置特定的固定 `width` 或 `height` 来调整图像的大小：


或者，我们可以使用 `sizing_mode` 来调整宽度和高度：


请注意，默认情况下，图像的宽高比是固定的，因此即使在响应式调整大小模式下，图像旁边或下方也可能有空隙。要覆盖此行为，请设置 `fixed_aspect=false` 或提供固定的 `width` 和 `height` 值。

## 设置链接 URL

使用 `link_url` 参数，您可以使图像可点击并链接到其他网站：


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



# Markdown 文本

`PnMarkdown` 组件允许在面板中渲染任意 [Markdown](https://python-markdown.github.io)。它渲染包含有效 Markdown 的字符串以及具有 `_repr_markdown_` 方法的对象，还可以定义自定义 CSS 样式。

底层实现为`panel.pane.Markdown`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/Markdown.html


## 基本用法

`PnMarkdown`/`PnMD` 组件接受所有*基本* Markdown 语法，包括嵌入式 HTML。它还支持大多数*扩展* Markdown 语法。

要在代码块中启用代码高亮显示，需要安装 `pip install pygments`

还可以通过`object`设置内容。
## 动态内容

vuepy 的响应式特性可以与 `Markdown` 组件的无缝集成，`Slider` 调整时，`Markdown` 内容中的值会实时更新，

## 样式

如果您想控制从 Markdown 源生成的 HTML 的行为，通常可以通过向此组件的 `style` 参数传递参数来实现。例如，您可以在 Markdown 表格周围添加蓝色边框，如下所示：


但是，以这种方式指定的样式只会应用于最外层的 Div，目前没有任何方法以这种方式将样式应用于 HTML 的特定内部元素。在这种情况下，我们无法使用 `style` 参数来控制生成表格的行或标题的样式。

如果我们想更改生成的 HTML 的特定内部元素，我们可以通过提供 HTML/CSS &lt;style&gt; 部分来实现。例如，我们可以按如下方式更改标题和数据的边框厚度，但请注意，更改将应用于后续的 Markdown，包括笔记本上下文中的其他单元格：


如果您只想为特定的 Markdown 文本更改样式，您可以通过添加可以用样式表针对的 CSS 类来轻松实现这一点。这里我们添加了 `special_table` 类，然后表格使用红色边框：


## 渲染器

自 1.0 版本以来，Panel 使用 [`markdown-it`](https://markdown-it-py.readthedocs.io/en/latest/) 作为默认的 markdown 渲染器。如果您想恢复之前的默认值 `'markdown'` 或切换到 `MyST` 风格的 Markdown，可以通过 `renderer` 参数设置它。例如，这里我们使用 'markdown-it' 和 'markdown' 渲染一个任务列表：


## LaTeX 支持

`PnMarkdown` 组件也支持数学渲染，方法是用 `$$` 分隔符封装要渲染的字符串。要启用 LaTeX 渲染，您必须在 `pn.extension` 调用中显式加载 'mathjax' 扩展。


请注意使用 `r` 前缀创建字符串作为*原始*字符串。Python 原始字符串将反斜杠字符 (\\) 视为文字字符。例如，这不起作用：


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

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | markdown内容      |

### 方法

| 属性名 | 说明 | 类型 |
| --- | --- | --- |



# Placeholder 占位符组件

占位符组件用于其他Panel组件的占位符。例如，可以在计算运行时显示一条消息。

底层实现为`panel.pane.Placeholder`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/Placeholder.html


## 基本用法

`PnPlaceholder`组件可以接受任何Panel组件作为其参数，包括其他panes。


使用`PnPlaceholder`的好处是它允许您替换窗格的内容，而不受特定类型组件的限制。这意味着您可以用任何其他窗格类型替换占位符，包括图表、图像和小部件。


## 临时替换内容

如果你想临时替换内容，可以使用上下文管理器。


## API

### 属性

| 属性名       | 说明                                                     | 类型       | 默认值 |
| ------------ | -------------------------------------------------------- | ---------- | ------ |
| value        | 要显示的Panel对象，如果对象不是Panel对象，将使用`panel(...)`函数转换 | ^[Any]     | —      |
| stylesheets  | 样式表列表                                               | ^[List]    | []     |

### Events

| 事件名 | 说明 | 类型 |
| ------ | ---- | ---- |
|        |      |      |

### Slots

| 插槽名   | 说明           |
| -------- | -------------- |
|          |                |

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


这对于简单的应用程序和更复杂的应用程序都适用。作为示例，这里我们嵌入了 Textual 文档中的计算器示例应用程序：


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



# GIF 图片

`PnGif` 组件在提供本地路径时将 `.gif` 图像文件嵌入到面板中，或者在提供 URL 时将链接到远程图像。

底层实现为`panel.pane.GIF`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/GIF.html


## 基本用法

`PnGIF` 组件可以指向任何本地或远程的 `.gif` 文件。如果给定以 `http` 或 `https` 开头的 URL，`embed` 参数决定图像是嵌入还是链接，可以通过设置特定的固定 `width` 或 `height` 来调整图像的大小：


或者，我们可以使用 `sizing_mode` 来调整宽度和高度：


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



# JPG 图像

`PnJpg` 组件如果提供本地路径，则将 `.jpg` 或 `.jpeg` 图像文件嵌入到面板中，或者如果提供 URL，则会链接到远程图像。

底层实现为`panel.pane.JPG`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/JPG.html


## 基本用法

`PnJPG` 组件可以指向任何本地或远程 `.jpg` 文件。如果给定以 `http` 或 `https` 开头的 URL，则 `embed` 参数决定图像是嵌入还是链接到：


## 调整大小

我们可以通过设置特定的固定 `width` 或 `height` 来调整图像的大小：


或者，我们可以使用 `sizing_mode` 来调整宽度和高度：


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



# WebP WebP图像组件

`WebP`组件可以在面板中嵌入`.webp`图像文件。如果提供本地路径，则嵌入该文件；如果提供URL，则链接到远程图像。

底层实现为`panel.pane.WebP`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/WebP.html


## 基本用法

`PnWebP`组件可以指向任何本地或远程的`.webp`文件。如果给定的URL以`http`或`https`开头，`embed`参数决定图像是嵌入还是链接：


我们可以通过设置特定的固定`width`或`height`来调整图像的大小：


或者，我们可以使用`sizing_mode`来调整宽度和高度：


请注意，默认情况下，图像的宽高比是固定的，因此即使在响应式尺寸模式下，图像的旁边或下方也可能存在间隙。要覆盖此行为，请设置`fixed_aspect=False`或提供固定的`width`和`height`值。


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

### Events

| 事件名 | 说明 | 类型 |
| ------ | ---- | ---- |
|        |      |      |

### Slots

| 插槽名   | 说明           |
| -------- | -------------- |
|          |                |

### 方法

| 方法名 | 说明 | 类型 |
| ------ | ---- | ---- |
|        |      |      |



# Perspective 数据可视化

`PnPerspective` 组件提供了一个强大的可视化工具，用于处理大型实时数据集，基于 [Perspective 项目](https://perspective.finos.org/)。**`PnPerspective` 为您的数据应用程序带来了*类似Excel*的功能**。查看 [Perspective 示例库](https://perspective.finos.org/examples/) 获取灵感。

`PnPerspective` 组件是 [`Tabulator`](../widgets/Tabulator.ipynb) 小部件的一个很好的替代品。

底层实现为`panel.pane.Perspective`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/Perspective.html


## 基本用法

`PnPerspective` 组件将指定为字典列表或数组以及 pandas DataFrame 的数据列呈现为交互式表格：


试着与 `PnPerspective` 组件交互：

- 左上角的三个垂直点会切换*配置菜单*
- 每列顶部的三条垂直线会切换*列配置菜单*
- 顶部菜单提供选项来更改*插件*以及*分组*、*拆分*、*排序*和*过滤*数据
- 底部菜单提供选项来*重置*、*下载*和*复制*以及*更改主题*

默认情况下会显示 `index`。如果您默认不想显示它，可以提供要显示的 `columns` 列表：


您也可以通过 `settings` 参数隐藏*配置菜单*：


通过点击左上角的 3 个垂直点，尝试切换*配置菜单*与 `PnPerspective` 组件交互。

## 插件配置

您可以手动配置活动*插件*，如下所示为*数据网格*

![perspective_edit](https://panel.holoviz.org/assets/perspective_edit.png)

您还可以通过 `columns_config` 参数以编程方式配置*列*配置：


请注意：

- 提供 `plugin_config` 时，您也可以使用*命名*颜色，如 'green'。但如果这样做，它们将不会在*列配置菜单*的*颜色选择器*中设置。

有关可用选项的更多详细信息，请参阅下面的[列配置选项部分](#列配置选项)。

## 时区处理

底层的 Perspective Viewer 假设*非时区*感知的日期时间是 UTC 时间。默认情况下，它会在您的本地时区中显示它们。

如果您的数据不是时区感知的，您可以将它们设置为时区感知。我的服务器时区是 'cet'，我可以按如下方式使它们感知时区：


如上节所示，您可以强制日期时间以特定时区显示：


## 流式处理和补丁更新

`PnPerspective` 组件还支持 `stream` 和 `patch` 方法，使我们能够高效地更新数据：


或者，我们也可以使用 `patch` 方法更新数据：


通过流式处理您想要可见的数据并将 rollover 设置为等于新数据的行数，可以实现删除行。通过这种方式，有效地删除旧行。目前不支持以类似于修补的方式按索引删除特定行。


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


## 调整大小

我们可以通过设置特定的固定 `width` 或 `height` 来调整图像的大小：


或者，我们可以使用 `sizing_mode` 来调整宽度和高度：


您可以通过使用 `caption` 为图像添加标题：


请注意，默认情况下，图像的宽高比是固定的，因此即使在响应式调整大小模式下，图像旁边或下方也可能有空隙。要覆盖此行为，请设置 `fixed_aspect=false` 或提供固定的 `width` 和 `height` 值。

## PIL 图像支持

Image 组件将渲染任何定义了 `_repr_[png | jpeg | svg]_` 方法的组件，包括 PIL 图像：


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



# Param 参数组件

`PnParam` 组件允许自定义 `param.Parameterized` 类参数的小部件、布局和样式。通过该组件，可以轻松地为参数化模型创建交互式界面。

底层实现为`panel.pane.Param`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/Param.html


## 基本用法

`PnParam` 组件可以用来查看和编辑参数化模型。下面我们构建一个骑行运动员及其功率曲线的模型作为示例：

## 自定义小部件

我们可以为特定参数自定义小部件类型：


## 展开子对象

我们可以通过 `expand` 参数默认展开子对象：


## 选择特定参数和自定义布局

我们可以选择只显示特定参数，并自定义布局：


## 滑块控件的连续更新禁用

当函数运行时间较长并且依赖于某个参数时，实时反馈可能成为负担，而不是有帮助。因此，如果参数使用的是滑块控件，可以通过设置 `throttled` 关键字为 `True` 来仅在释放鼠标按钮后才执行函数。


## 组合参数控件与结果显示

可以组合参数控件与计算结果显示：


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

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| Param的字段 | 自定义widget      |

### 方法

| 属性名 | 说明 | 类型 |
| --- | --- | --- |



# JSON 数据

`PnJson` 组件允许在面板中渲染任意 JSON 字符串、字典和其他 JSON 可序列化对象。

底层实现为`panel.pane.JSON`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/JSON.html


## 基本用法

`PnJSON` 组件可用于渲染任意 JSON 对象的树视图，这些对象可以定义为字符串或 JSON 可序列化的 Python 对象。


## 控制选项

`PnJson` 组件公开了许多可以从 Python 和 Javascript 更改的选项。尝试交互式地体验这些参数的效果：


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



# ECharts 图表

`PnECharts` 组件在 Panel 中渲染 [Apache ECharts](https://echarts.apache.org/en/index.html) 和 [pyecharts](https://pyecharts.org/#/) 图表。请注意，要在 notebook 中使用 `PnECharts` 组件，必须以 'echarts' 作为参数加载 Panel 扩展，以确保初始化 echarts.js。

底层实现为`panel.pane.ECharts`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/ECharts.html


## 基本用法

让我们尝试 `PnECharts` 组件对 ECharts 规范的原始形式（即字典）的支持，例如，这里我们声明一个柱状图：


与所有其他组件一样，`PnECharts` 组件的 `object` 可以更新，要么是就地更新并触发更新：


ECharts 规范也可以通过声明宽度或高度以匹配容器来进行响应式调整大小：


## PyECharts 支持

ECharts 组件还支持 pyecharts。例如，我们可以直接将 `pyecharts.charts.Bar` 图表传递给 `PnECharts` 组件：


## 仪表盘示例

ECharts 库支持各种图表类型，由于图表使用 JSON 数据结构表示，我们可以轻松更新数据，然后发出更改事件以更新图表：


## 事件处理

`PnECharts` 组件允许您监听 JavaScript API 中定义的任何事件，方法是使用 `on_event` 方法在 Python 中监听事件，或者使用 `js_on_event` 方法触发 JavaScript 回调。

有关可以监听的事件的详细信息，请参阅 [ECharts 事件文档](https://echarts.apache.org/handbook/en/concepts/event)。

### Python 事件处理

让我们从一个简单的点击事件开始，我们想从 Python 监听这个事件。要添加事件监听器，只需使用事件类型（在本例中为 'click'）和 Python 处理程序调用 `on_event` 方法：


尝试单击折线上的点。点击后检查 `event_data.value` 时，您应该看到类似以下内容的数据。

要限制特定事件适用的对象类型，还可以向 `on_event` 方法提供 `query` 参数。`query` 的格式应该是 `mainType` 或 `mainType.subType`，例如：

- `'series'`：单击数据系列时触发事件
- `'series.line'`：仅当单击折线数据系列时才触发事件
- `'dataZoom'`：单击缩放时触发事件
- `'xAxis.category'`：单击 x 轴上的类别时触发事件

### JavaScript 事件处理

相同的概念适用于 JavaScript，但这里我们传入 JavaScript 代码片段。命名空间允许您访问事件数据 `cb_data` 和 ECharts 图表本身作为 `cb_obj`。这样，您可以访问事件并自己操作图表：


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


要更新 `object` 或 `styles`，我们可以直接设置它：


## HTML 文档

`PnHTML` 组件设计用于显示*基本* HTML 内容。它不适合渲染包含 JavaScript 或其他动态元素的完整 HTML 文档。

要显示完整的 HTML 文档，您可以转义 HTML 内容并将其嵌入在 [`iframe`](https://www.w3schools.com/html/html_iframe.asp) 中。以下是实现方式：


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
| sizing_mode       | 尺寸调整模式                   | ^[str]                                                         | 'fixed'  |
| width             | 宽度                          | ^[int, str]                                                    | None    |
| height            | 高度                          | ^[int, str]                                                    | None    |
| min_width         | 最小宽度                      | ^[int]                                                         | None    |
| min_height        | 最小高度                      | ^[int]                                                         | None    |
| max_width         | 最大宽度                      | ^[int]                                                         | None    |
| max_height        | 最大高度                      | ^[int]                                                         | None    |
| margin            | 外边距                        | ^[int, tuple]                                                  | 5       |
| css_classes       | CSS类名列表                   | ^[list]                                                        | []      |

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



# Vega 图表

`PnVega` 组件可以渲染基于 Vega 的图表（包括来自 Altair 的图表）。它通过对 Vega/Altair 对象中的数组数据使用二进制序列化来优化图表渲染，与 Vega 原生使用的标准 JSON 序列化相比，提供了显著的加速。请注意，要在 Jupyter 笔记本中使用 `PnVega` 组件，必须使用 'vega' 作为参数加载 Panel 扩展，以确保正确初始化 vega.js。

底层实现为`panel.pane.Vega`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/Vega.html


## 基本用法

`PnVega` 组件支持 [`vega`](https://vega.github.io/vega/docs/specification/) 和 [`vega-lite`](https://vega.github.io/vega-lite/docs/spec.html) 规范，可以以原始形式（即字典）提供，或者通过定义一个 `altair` 图表。

### Vega 和 Vega-lite

要显示 `vega` 和 `vega-lite` 规范，只需直接构造一个 `PnVega` 组件：


与所有其他组件一样，`PnVega` 组件的 `object` 可以更新：


### 响应式大小调整

`vega-lite` 规范还可以通过将宽度或高度声明为匹配容器来进行响应式大小调整：


请注意，`vega` 规范不支持将 `width` 和 `height` 设置为 `container`。

### DataFrame 数据值

为了方便起见，我们支持将 Pandas DataFrame 作为 `data` 的 `values`：


## Altair

定义 Vega 图表的一种更便捷的方式是使用 [altair](https://altair-viz.github.io)，它在 vega-lite 之上提供了声明式 API。`PnVega` 组件在传入 Altair 图表时会自动渲染 Vega-Lite 规范：


Altair 图表也可以通过更新组件的 `object` 来更新：


Altair 支持的所有常规布局和组合操作符也可以渲染：


## 选择

`PnVega` 组件自动同步在 Vega/Altair 图表上表达的任何选择。目前支持三种类型的选择：

- `selection_interval`：允许使用框选工具选择区间，以 `{<x轴名称>: [x最小值, x最大值], <y轴名称>: [y最小值, y最大值]}` 的形式返回数据
- `selection_single`：允许使用点击选择单个点，返回整数索引列表
- `selection_multi`：允许使用（shift+）点击选择多个点，返回整数索引列表

### 区间选择

作为一个例子，我们可以在图表中添加一个 Altair `selection_interval` 选择：


请注意，我们指定了一个单一的 `debounce` 值，如果我们声明多个选择，可以通过将其指定为字典来为每个命名事件声明一个去抖动值，例如 `debounce={'brush': 10, ...}`。

## 主题

可以使用 `theme` 参数为图表应用主题：


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



# Streamz 数据流组件

`PnStreamz` 组件可以渲染 [Streamz](https://streamz.readthedocs.io/en/latest/) Stream 对象发出的任意对象，与专门处理 streamz DataFrame 和 Series 对象并公开各种格式化选项的 `DataFrame` 组件不同。

底层实现为`panel.pane.Streamz`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/Streamz.html


## 基本用法

> **注意**：如果您尚未使用 Streamz 库，我们建议使用 Param 和 Panel 生态系统中的功能，例如[反应式表达式](https://param.holoviz.org/user_guide/Reactive_Expressions.html)、[生成器函数](https://param.holoviz.org/user_guide/Generators.html)和/或*周期性回调*。我们发现这些功能得到更加可靠的支持。

`PnStreamz` 组件使用默认的 Panel 解析方式来确定如何渲染 Stream 返回的对象。默认情况下，该组件只有在显示时才会监视 `Stream`，我们可以通过设置 `always_watch=True` 让它在创建后立即开始监视流：


现在我们可以定义一个周期性回调，它在 `Stream` 上发出递增的计数：


## 复杂数据流

`PnStreamz` 组件可以用于流式传输任何类型的数据。例如，我们可以创建一个 streamz DataFrame，将数据累积到滑动窗口中，然后将其映射到 Altair `line_plot` 函数：


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



# Alert 警告

警告组件用于提供针对典型用户操作的上下文反馈消息，具有多种可用且灵活的警告消息样式。

底层实现为`panel.pane.Alert`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/Alert.html


## 基本用法

`PnAlert` 支持 Markdown 和 HTML 语法：

## 不同类型

`PnAlert` 组件有多种 `alert_type` 选项，用于控制警告消息的颜色：


## 长文本消息

它也可以用于较长的消息：


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

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
| default | 警告消息内容        |

### 方法

| 属性名 | 说明 | 类型 |
| --- | --- | --- |



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


与所有其他组件一样，`PnVTKJS` 组件可以通过替换 `object` 来更新：


## 相机控制

一旦显示了 VTKJS 组件，它将自动将相机状态与组件对象同步。相机参数仅在交互结束时更新。我们可以在相应的参数上读取相机状态：


这种技术也使得可以将两个或多个 VTKJS 组件的相机链接在一起：

还可以在 Python 中修改相机状态并触发更新：

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

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |

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


与其他组件一样，`PnStr`组件可以通过设置其`object`参数进行更新。如前所述，非字符串类型会自动转换为字符串：


## API

### 属性

| 属性名    | 说明                                     | 类型                | 默认值 |
| --------- | ---------------------------------------- | ------------------- | ------ |
| value     | 要显示的字符串。如果提供非字符串类型，将显示该对象的`repr` | ^[str\|object]     | —      |
| styles    | 指定CSS样式的字典                       | ^[dict]             | {}     |

### Events

| 事件名 | 说明 | 类型 |
| ------ | ---- | ---- |
|        |      |      |

### Slots

| 插槽名   | 说明           |
| -------- | -------------- |
|          |                |

### 方法

| 方法名 | 说明 | 类型 |
| ------ | ---- | ---- |
|        |      |      |



# Vizzu 可视化图表组件

`Vizzu`组件在Panel中渲染[Vizzu](https://lib.vizzuhq.com/)图表。注意，要在notebook中使用`Vizzu`组件，必须在加载Panel扩展时将'vizzu'作为参数传递，以确保初始化vizzu.js。

底层实现为`panel.pane.Vizzu`，参数基本一致，参考文档：https://panel.holoviz.org/reference/panes/Vizzu.html


## 基本用法

`PnVizzu`组件可以根据`config`定义如何绘制数据（以列字典或DataFrame的形式定义）：


Vizzu的主要卖点之一是在数据或`config`更新时的动态动画。例如，如果我们更改"geometry"，可以看到动画在两种状态之间平滑过渡。


## 列类型

`PnVizzu`支持两种列类型：

- `'dimension'`：通常用于非数值数据和/或图表的独立维度（例如x轴）
- `'measure'`：数值通常用于图表的因变量（例如y轴值）

`PnVizzu`组件会根据数据的dtypes自动推断类型，但在某些情况下，可能需要使用`column_types`参数显式覆盖列的类型。一个常见的例子是在x轴上绘制整数时，通常会被视为"measure"，但在折线图或条形图的情况下应该被视为独立维度。

下面的示例演示了这种情况，这里我们希望将"index"视为独立变量，并使用`column_types={'index': 'dimension'}`覆盖默认推断的类型：


## 预设

Vizzu提供了各种[预设图表类型](https://lib.vizzuhq.com/latest/examples/presets/)。在`PnVizzu`组件中，您可以通过在`config`中提供`'preset'`作为键来使用这些预设。在下面的示例中，我们动态创建一个`config`，根据`RadioButtonGroup`切换`preset`：


## 交互控制

`PnVizzu`组件公开了许多选项，可以从Python和JavaScript更改。尝试交互式地测试这些参数的效果：


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

### Events

| 事件名 | 说明 | 类型 |
| ------ | ---- | ---- |
|        |      |      |

### Slots

| 插槽名   | 说明           |
| -------- | -------------- |
|          |                |

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


## 更新 Bokeh 对象

要使用实时服务器更新图表，我们可以简单地修改底层模型。如果我们在 Jupyter notebook 中工作，我们还必须在组件上调用 `pn.io.push_notebook` 辅助函数，或者明确使用 `bokeh_pane.param.trigger('object')` 触发事件：


## 交互式 Bokeh 应用

使用 Panel 渲染 Bokeh 对象的另一个很好的特性是回调将像在服务器上一样工作。因此，您可以简单地将现有的 Bokeh 应用程序包装在 Panel 中，它将可以渲染并开箱即用，无论是在 notebook 中还是作为独立应用程序提供服务：


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



# StaticText 静态文本

StaticText组件显示文本值但不允许编辑它，适用于展示只读信息。

底层实现为`panel.widgets.StaticText`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/StaticText.html


## 基本用法

静态文本组件提供了一种简单的方式来显示不可编辑的文本内容。


## 动态内容

静态文本组件可以与响应式数据结合使用，以显示动态更新的内容。


## 样式自定义

可以通过样式参数自定义静态文本的外观。


## API

### 属性

| 属性名 | 说明 | 类型 | 默认值 |
| -------- | ------------------- | ---------------------------------------------------------------| ------- |
| name | 组件标题 | ^[string] | — |
| value | 文本内容 | ^[string] | — |

### Events

| 事件名 | 说明 | 类型 |
| --- | --- | --- |
| | | |

### Slots

| 插槽名 | 说明 |
| --- | --- |
| | |

### 方法

| 属性名 | 说明 | 类型 |
| --- | --- | --- |
| | | |



# ButtonIcon 图标按钮

此小部件最初显示一个默认 `icon` 。点击后，会在指定的 `toggle_duration` 时间内显示 `active_icon`。

例如，可以有效利用 `ButtonIcon` 来实现类似于 `ChatGPT` 的复制到剪贴板按钮的功能。

底层实现为`panel.widgets.ButtonIcon`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/ButtonIcon.html


## 基本用法

基本的图标按钮使用：[tabler-icons.io](https://tabler-icons.io/) 图标

## 使用SVG图标

可以使用SVG字符串作为图标：

## 自定义 css style

通过`style`设置组件外层DOM节点(意味着无法设置某些组件内的样式，如background-color，font-size等)的CSS样式:
* `width`、`height` 设置组件的高和宽
* `border` 设置组件的边框
* `size`  设置大小
* ...

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

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |



# IntRangeSlider 整数范围滑块

整数范围滑块组件允许使用带有两个手柄的滑块选择整数范围，与RangeSlider类似，但专门用于整数值。

底层实现为`panel.widgets.IntRangeSlider`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/IntRangeSlider.html


## 基本用法

基本的整数范围滑块使用：


## 自定义步长

可以设置`step`参数来控制值的间隔：


## 垂直方向

滑块可以设置为垂直方向显示：


## 滑块颜色和方向

可以自定义滑块条的颜色和方向：


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

### Slots

| 插槽名   | 说明               |
| ------- | ----------------- |
|         |                   |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |



# Player 播放器

播放器组件是一个用于循环播放数值范围的工具，可用于动画或步进通过数据。它提供了播放、暂停、步进和循环控制。

底层实现为`panel.widgets.Player`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/Player.html


## 基本用法

基本的播放器使用：


## 设置循环和间隔

可以设置播放器是否循环以及播放间隔：


## 设置显示模式

可以设置播放器的显示模式，如只显示按钮或者同时显示值等：


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

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
|         |                   |

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


## 默认选中状态

可以通过设置`value`参数为`True`使复选框默认处于选中状态：


## 禁用状态

可以通过设置`disabled`参数为`True`使复选框处于禁用状态：


## 结合其他组件使用

复选框通常用于控制其他组件的显示或行为：


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

### Slots

| 插槽名   | 说明               |
| ------- | ----------------- |
|         |                   |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |



# Tabulator 表格

Tabulator组件提供了一个功能丰富的交互式表格，可用于显示、编辑和操作`Pandas DataFrame`数据。

底层实现为`panel.widgets.Tabulator`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/Tabulator.html

## 基本用法
在编辑单元格时，Tabulator 的 value 数据会实时更新，你可以通过常规的 `@change` 监听变化。但如果需要精确获取被修改的单元格信息，还可以绑定 `@edit`，该回调会接收一个 TableEditEvent 对象，其中包含以下字段：
* column：被编辑列的名称
* row：被编辑行在 DataFrame 中的整数索引
* old：单元格的旧值
* value：单元格的新值
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
### 使用 Tabulator Formatter

除了使用 Bokeh 提供的格式化器之外，还可以使用 Tabulator 库内置的有效格式化器。这些格式化器可以定义为字符串，或者以字典形式声明类型及其他参数（作为 `formatterParams` 传递给 Tabulator）。  

可用的 Tabulator 格式化器列表可在 [Tabulator 文档](https://tabulator.info/docs/6.3.1/format#format-builtin)中查阅。  

需要注意的是，类似的规则也可通过 `title_formatters` 参数应用于列标题（但不支持 Bokeh 的 `CellFormatter` 类型）。
## Editors 编辑器

与格式化器类似，Tabulator 能够原生支持 Bokeh 的编辑器类型，但在底层实现中，它会将大部分 Bokeh 编辑器替换为 Tabulator 库原生支持的等效编辑器。

因此，通常更推荐直接使用 Tabulator 的原生编辑器。将某列的编辑器设为 None 会使该列不可编辑。需要注意的是，除了标准的 Tabulator 编辑器外，Tabulator 组件还额外支持 'date'（日期）和 'datetime'（日期时间）编辑器。
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
## 列布局

默认情况下，DataFrame 组件会根据内容自动调整列宽和表格大小，这对应参数 `layout="fit_data_table"` 的默认行为。此外，还支持其他布局模式，例如手动指定列宽、均分列宽或仅调整列尺寸。

### 手动设置列宽

如需手动设置列宽，只需为每列显式指定宽度：
### 自动调整列宽

通过 `layout` 参数自动调整列宽:
* fit_data_table（默认模式）：自动调整列宽并优化表格整体尺寸（最常用且推荐）：
* fit_data：根据列内容自动调整列宽（不拉伸表格整体宽度）。
* fit_data_stretch：在适应内容的同时，拉伸最后一列以填满可用空间。
* fit_data_fill：适应内容并填充空间，但不拉伸最后一列（其余列均分剩余宽度）。
* fit_columns：每列相同大小
## 对齐方式
## 样式设置

### 基本样式设置

根据表格内容或其他条件进行样式定制是一项非常重要的功能。幸运的是，`pandas` 提供了一个强大的 [styling APIiiii](https://pandas.pydata.org/pandas-docs/stable/user_guide/style.html)，可与 `Tabulator` 组件配合使用。具体来说，`Tabulator` 组件暴露了与 `pandas.DataFrame` 类似的 `.style` 属性，允许用户通过 `.apply` 和 `.applymap` 等方法应用自定义样式。详细指南可参考 [Pandas 官方文档](https://pandas.pydata.org/pandas-docs/stable/user_guide/style.html)。

### 渐变样式设置

通过 `.text_gradient`（文本渐变）或 `.background_gradient`（背景渐变）方法，配合 [Matplotlib 配色方案](https://matplotlib.org/stable/gallery/color/colormap_reference.html)，可以为表格添加渐变效果：
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

### 更改字体大小

不同主题的字体大小可能有所不同。例如，“bootstrap”主题的字体大小为 13px，而“bootstrap5”主题的字体大小为 16px。以下是将主题“bootstrap5”的字体大小值覆盖为 10px 的一种方法。

```python
 <PnTabulator :stylesheets='[":host .tabulator {font-size: 10px;}"]' ...
```
## 选择/点击
## 冻结行列
### 冻结列
### 冻结行

## Row Content 行内容扩展
## Groupby 分组

### 分层多级索引

## 分页

## 过滤

### 客户端过滤
## 下载


## 按钮

## 流式数据

## 数据补丁

## 静态配置

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


## 使用字典作为选项

`options`参数也接受一个字典，其键将作为滑块上显示的文本标签：


## 垂直方向

滑块可以设置为垂直方向显示：


## 自定义样式

可以自定义滑块条的颜色和方向：


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

### Slots

| 插槽名   | 说明               |
| ------- | ----------------- |
|         |                   |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |



# PasswordInput 密码输入框

密码输入框组件是一个专用于输入密码的文本输入框，会将输入的字符显示为掩码以保护隐私。

底层实现为`panel.widgets.PasswordInput`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/PasswordInput.html


## 基本用法

基本的密码输入框使用： 可以通过设置`v-mode`/`value`参数为密码输入框设置默认值：


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

### Slots

| 插槽名   | 说明               |
| ------- | ----------------- |
|         |                   |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |



# TextEditor 文本编辑器

文本编辑器组件允许用户编辑和显示格式化文本，支持多种格式，包括Markdown和HTML。

底层实现为`panel.widgets.TextEditor`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/TextEditor.html


## 基本用法

基本的文本编辑器使用：


## 工具栏布局

可以设置工具栏的位置和是否显示：


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

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
|         |                   |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |



# MultiSelect 多选框

多选框组件允许从下拉菜单中选择多个选项。它与Select组件类似，但支持多选功能。

底层实现为`panel.widgets.MultiSelect`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/MultiSelect.html


## 基本用法

基本的多选框使用：


## 使用字典作为选项

`options`参数也接受一个字典，其键将作为下拉菜单的标签：


## 选择区域大小

可以通过`size`参数控制选择区域显示的选项数量：


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

### Slots

| 插槽名   | 说明               |
| ------- | ----------------- |
|         |                   |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |



# LiteralInput 字面量输入框

字面量输入框组件允许用户输入任意Python字面量（包括int、float、list、dict等）并将其解析为相应的Python对象。

底层实现为`panel.widgets.LiteralInput`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/LiteralInput.html


## 基本用法

基本的字面量输入框使用：


## 不同类型的值

字面量输入框可以处理各种Python数据类型：


## 指定类型

可以使用type参数指定输入的数据类型：


## 自定义高度

可以设置输入框的高度，特别是对于复杂类型很有用：


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

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
|         |                   |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |



# Button 按钮

常用的操作按钮。

按钮组件可以在被点击时触发事件。除了在处理点击事件期间会从`False`切换到`True`的`value`参数外，还有一个额外的`clicks`参数，可以被监听以订阅点击事件。

底层实现为`panel.widgets.Button`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/Button.html


## 基本用法

基本的按钮使用，点击时触发事件：

## 按钮样式

按钮的颜色可以通过设置`button_type`来改变，而`button_style`可以是`'solid'`或`'outline'`：


## 图标按钮

Button 组件可以添加图标，支持 Unicode、Emoji 字符，以及 [tabler-icons.io](https://tabler-icons.io) 的命名图标或自定义 SVG：

## 加载状态按钮

通过设置 loading 属性为 true 来显示加载中状态。  
## 自定义 css style

通过`style`设置组件外层DOM节点(意味着无法设置某些组件内的样式，如background-color，font-size等)的CSS样式:
* `width`、`height` 设置组件的高和宽
* `border` 设置组件的边框
* ...

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

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |



# SpeechToText 语音转文本

SpeechToText组件通过封装[HTML5 `SpeechRecognition` API](https://developer.mozilla.org/en-US/docs/Web/API/SpeechRecognition)控制浏览器的语音识别服务。

底层实现为`panel.widgets.SpeechToText`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/SpeechToText.html


## 基本用法

语音转文本组件提供了一个简单的界面来启动和停止语音识别服务，将用户的语音转换为文本。

> **注意**：此功能是**实验性的**，**只有Chrome和少数其他浏览器支持**。有关支持SpeechRecognition API的浏览器的最新列表，请参见[caniuse.com](https://caniuse.com/speech-recognition)或[MDN文档](https://developer.mozilla.org/en-US/docs/Web/API/SpeechRecognition#Browser_compatibility)。在某些浏览器（如Chrome）中，即使支持此功能，`grammars`、`interim_results`和`max_alternatives`参数也可能尚未实现。
> 
> 在像Chrome这样的浏览器上，在网页上使用语音识别涉及基于服务器的识别引擎。**您的音频会被发送到网络服务进行识别处理，因此它无法离线工作**。这对您的用例来说是否足够安全和保密，需要您自行评估。


## 自定义按钮

可以通过设置`button_type`、`button_not_started`和`button_started`参数来自定义按钮的外观。


## 连续识别

通过设置`continuous=True`，语音识别服务会保持打开状态，允许您连续说多个语句。


## 使用语法列表

可以使用`GrammarList`限制识别服务识别的单词或单词模式。


## 显示详细结果

可以通过`results`属性获取更详细的结果，包括置信度级别。


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

### Slots

| 插槽名 | 说明 |
| --- | --- |
| | |

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


## 自定义格式

可以通过format参数自定义日期时间的显示格式。


## 自定义样式

通过设置bar_color和orientation等属性可以自定义滑块样式。


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

### Slots

| 插槽名 | 说明 |
| --- | --- |
| | |

### 方法

| 属性名 | 说明 | 类型 |
| --- | --- | --- |
| | | |



# ColorMap 色彩映射选择器

ColorMap组件允许从包含色彩映射的字典中选择一个值。该组件类似于Select选择器，但只允许选择有效的色彩映射，即十六进制值列表、命名颜色或matplotlib色彩映射。

底层实现为`panel.widgets.ColorMap`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/ColorMap.html


## 基本用法

色彩映射选择器可以提供色彩映射选项让用户进行选择，选项必须是一个包含色彩列表的字典。

## 自定义布局

可以通过设置`ncols`参数以及`swatch_width`和`swatch_height`选项来控制色彩映射的显示方式。


## Matplotlib支持

组件也支持matplotlib色彩映射：


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

### Slots

| 插槽名 | 说明 |
| --- | --- |
| | |

### 方法

| 属性名 | 说明 | 类型 |
| --- | --- | --- |
| | | |



# JSONEditor JSON编辑器

JSONEditor组件提供了一个可视化编辑器，用于编辑JSON可序列化的数据结构，如Python字典和列表，具有不同编辑模式、插入对象和使用JSON Schema进行验证的功能。

底层实现为`panel.widgets.JSONEditor`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/JSONEditor.html


## 基本用法

JSON编辑器提供了一个直观的界面来查看和编辑JSON数据。


## 编辑模式

JSON编辑器有多种模式，提供不同的查看和编辑`JSONEditor.value`的方式。注意，要启用对`mode='code'`的支持，必须使用`pn.extension('ace')`加载ace编辑器。


## 验证

JSONEditor通过提供JSON Schema可以对`value`进行验证。JSON Schema描述了JSON对象必须具有的结构，如必需的属性或值必须具有的类型。更多信息请参见 http://json-schema.org/。


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

### Slots

| 插槽名 | 说明 |
| --- | --- |
| | |

### 方法

| 属性名 | 说明 | 类型 |
| --- | --- | --- |
| | | |



# Debugger 调试器

Debugger是一个不可编辑的Card布局组件，可以在前端显示仪表板运行时可能触发的日志和错误。

底层实现为`panel.widgets.Debugger`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/Debugger.html


## 基本用法

调试器可以在应用程序运行时显示日志和错误信息，对于在前端跟踪和调试问题非常有用。如果未指定logger_names，则必须使用`panel`记录器或自定义子记录器（例如`panel.myapp`）记录事件。

注意：调试器基于terminal组件，需要调用`pn.extension('terminal')`。


## 错误捕获

调试器可以捕获和显示应用程序中发生的错误，帮助用户了解交互过程中遇到的问题。


## 日志级别

通过设置不同的日志级别，可以控制显示哪些级别的日志信息。


## API

### 属性

| 属性名 | 说明 | 类型 | 默认值 |
| -------- | ------------------- | ---------------------------------------------------------------| ------- |
| only_last | 记录异常时，指示是否仅提示堆栈中的最后一个跟踪 | ^[boolean] | false |
| level | 要在前端提示的日志级别 | ^[int] | logging.ERROR |
| formatter_args | 传递给格式化程序对象的参数 | ^[dict] | `{'fmt':"%(asctime)s [%(name)s - %(levelname)s]: %(message)s"}` |
| logger_names | 将提示到终端的记录器名称列表 | ^[list] | ['panel'] |
| name | 组件标题 | ^[string] | — |

### Events

| 事件名 | 说明 | 类型 |
| --- | --- | --- |
| | | |

### Slots

| 插槽名 | 说明 |
| --- | --- |
| | |

### 方法

| 属性名 | 说明 | 类型 |
| --- | --- | --- |
| btns | 获取调试器控制按钮 | ^[function] |



# EditableIntSlider 可编辑整数滑块

EditableIntSlider组件允许用户在设定范围内通过滑块选择整数值，并提供一个可编辑的数字输入框以进行更精确的控制。

底层实现为`panel.widgets.EditableIntSlider`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/EditableIntSlider.html


## 基本用法

可编辑整数滑块提供了滑块和输入框两种方式来选择和输入整数值。


## 固定范围

通过设置`fixed_start`和`fixed_end`参数，可以限制value的范围，使其不能超出这个范围。


## 自定义格式

可以通过format参数自定义整数的显示格式。


## 自定义样式

通过设置bar_color和orientation等属性可以自定义滑块样式。


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

### Slots

| 插槽名 | 说明 |
| --- | --- |
| | |

### 方法

| 属性名 | 说明 | 类型 |
| --- | --- | --- |
| | | |



# DateSlider 日期滑块

DateSlider组件允许用户在设定的日期范围内通过滑块选择一个日期值。

底层实现为`panel.widgets.DateSlider`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/DateSlider.html


## 基本用法

日期滑块组件提供了一种交互式方式来选择日期范围内的特定日期。

## 自定义样式

通过设置bar_color和orientation等属性可以自定义滑块样式。


## 步长设置

通过step参数可以设置日期滑块的步长（以天为单位）。


## 日期格式

可以通过format参数自定义日期的显示格式。


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

### Slots

| 插槽名 | 说明 |
| --- | --- |
| | |

### 方法

| 属性名 | 说明 | 类型 |
| --- | --- | --- |
| | | |



# FileInput 文件输入框

文件输入框组件允许用户上传一个或多个文件，支持拖放或点击选择文件。上传的文件可以作为字节字符串获取，也可以自动转换为其他格式。

底层实现为`panel.widgets.FileInput`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/FileInput.html


## 基本用法

基本的文件输入框使用：


## 多文件上传

可以通过设置`multiple=True`支持多文件上传：

## 接受特定文件类型

可以通过`accept`参数限制可接受的文件类型：


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

### Slots

| 插槽名   | 说明               |
| ------- | ----------------- |
|         |                   |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |



# TextToSpeech 文本转语音

TextToSpeech组件为Panel带来文本转语音功能，它封装了[HTML5 SpeechSynthesis API](https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesis)和[HTML SpeechSynthesisUtterance API](https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesisUtterance)。

底层实现为`panel.widgets.TextToSpeech`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/TextToSpeech.html


## 基本用法

文本转语音组件可以将文本转换为语音并播放出来。请注意，该组件本身在视觉上不显示任何内容，但仍需添加到应用程序中才能使用。


## 自动播放

当`auto_speak`设置为true时（默认值），每当`value`更改时，都会自动播放语音。


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

### Slots

| 插槽名 | 说明 |
| --- | --- |
| | |

### 方法

| 属性名 | 说明 | 类型 |
| --- | --- | --- |
| | | |



# FileDropper 文件拖放上传器

FileDropper组件允许用户将一个或多个文件上传到服务器。它基于[FilePond](https://pqina.nl/filepond/)库构建，如果您广泛使用此组件，请考虑向他们捐款。FileDropper类似于FileInput组件，但增加了对分块上传的支持，使上传大文件成为可能。UI还支持图像文件的预览。与FileInput不同，上传的文件存储为以文件名为索引的字节对象字典。

底层实现为`panel.widgets.FileDropper`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/FileDropper.html


## 基本用法

FileDropper提供了一个拖放区域，允许用户通过拖放或点击选择上传文件。


## 文件类型限制

通过`accepted_filetypes`参数可以限制用户可以选择的文件类型。这包括一个也允许通配符的mime类型列表。


## 多文件上传

通过设置`multiple=True`可以允许上传多个文件。


## 布局选项

FileDropper支持几种不同的布局选项：
- `"compact"`: 移除边距
- `"integrated"`: 移除背景和其他样式，当组件嵌入到更大的组件中时很有用
- `"circle"`: 圆形上传区域，适用于个人资料图片上传


## 上传大小限制

与FileInput组件不同，FileDropper组件通过分块上传绕过了网络浏览器、Bokeh、Tornado、笔记本等对最大文件大小的限制。这使得上传比以前可能的大得多的文件变得可行。默认的`chunk_size`是10MB（表示为10000000字节）。您可以配置`max_file_size`、`max_total_file_size`（如果设置了`multiple=True`，则限制总上传大小）和`max_files`，以提供对可上传数据量的上限。


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

### Slots

| 插槽名 | 说明 |
| --- | --- |
| | |

### 方法

| 属性名 | 说明 | 类型 |
| --- | --- | --- |
| | | |



# MultiChoice 多项选择器

多项选择器组件允许用户从可用选项列表中选择多个项目，并支持搜索过滤选项。

底层实现为`panel.widgets.MultiChoice`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/MultiChoice.html


## 基本用法

基本的多项选择器使用：


## 使用字典选项

可以使用字典作为选项，其中键是显示的标签，值是实际的数据值：


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

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
|         |                   |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |



# VideoStream 视频流

VideoStream组件可以显示来自本地流（例如网络摄像头）的视频，并允许从Python访问流式视频数据。

底层实现为`panel.widgets.VideoStream`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/VideoStream.html


## 基本用法

视频流组件默认情况下会显示视频流，可用于如网络摄像头实时视频的展示。


## 截图功能

可以调用`snapshot`方法触发组件的`value`更新，以获取当前视频帧的图像。


## 定时截图

通过设置`timeout`参数，可以指定视频流将以多大频率更新。


## 图像格式

可以通过`format`参数指定捕获的图像格式，如果需要高频率的截图，可以选择'jpeg'格式，因为图像尺寸要小得多。


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

### Slots

| 插槽名 | 说明 |
| --- | --- |
| | |

### 方法

| 属性名 | 说明 | 类型 |
| --- | --- | --- |
| | | |



# Select 选择器

选择器组件允许用户从下拉菜单或选择区域中选择一个值。它属于单值选择类组件，提供兼容的API，包括RadioBoxGroup、AutocompleteInput和DiscreteSlider等组件。

底层实现为`panel.widgets.Select`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/Select.html


## 基本用法

基本的选择器使用：


## 使用字典作为选项

`options`参数也接受一个字典，其键将作为下拉菜单的标签：


## 禁用选项

可以使用`disabled_options`参数禁用部分选项：


## 分组选项

可以使用`groups`参数对选项进行分组显示（也称为*optgroup*）：


## 列表选择区域

通过设置`size`参数大于1，可以从列表中选择一个选项，而不是使用下拉菜单：


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

### Slots

| 插槽名   | 说明               |
| ------- | ----------------- |
|         |                   |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |



# Toggle 切换开关

切换开关组件允许在`True`/`False`状态之间切换单一条件。Toggle、Checkbox和Switch组件功能类似，可互相替换。

底层实现为`panel.widgets.Toggle`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/Toggle.html


## 基本用法

基本的切换开关使用：


## 样式

按钮的颜色可以通过设置`button_type`来改变，而`button_style`可以是`'solid'`或`'outline'`：


## 图标

Toggle组件可以添加图标，支持Unicode、Emoji字符，以及 [tabler-icons.io](https://tabler-icons.io) 的命名图标或自定义SVG：


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

### Slots

| 插槽名   | 说明               |
| ------- | ----------------- |
|         |                   |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |



# ColorPicker 颜色选择器

颜色选择器组件允许使用浏览器的颜色选择小部件选择颜色。

底层实现为`panel.widgets.ColorPicker`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/ColorPicker.html


## 基本用法

基本的颜色选择器使用：


## 默认颜色设置

可以通过设置`value`参数来指定默认颜色：


## 禁用状态

可以通过设置`disabled`参数为`True`使颜色选择器处于禁用状态：

## 实时应用颜色

颜色选择器可以用于实时更新网页元素的样式：


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

### Slots

| 插槽名   | 说明               |
| ------- | ----------------- |
|         |                   |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |



# Switch 开关

开关组件允许通过滑动开关在`True`/`False`状态之间切换单一条件。Switch、Checkbox和Toggle组件功能类似，可互相替换。

底层实现为`panel.widgets.Switch`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/Switch.html


## 基本用法

基本的开关使用：


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

### Slots

| 插槽名   | 说明               |
| ------- | ----------------- |
|         |                   |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |



# DatetimePicker 日期时间选择器

日期时间选择器组件允许用户选择日期和时间，可以通过文本输入框和浏览器的日期时间选择工具进行选择。

底层实现为`panel.widgets.DatetimePicker`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/DatetimePicker.html


## 基本用法

基本的日期时间选择器使用：

## 日期范围限制

可以使用`start`和`end`参数限制可选择的日期范围：


## 自定义时间选项

可以使用`enable_time`、`enable_seconds`和`military_time`参数自定义时间选择功能：


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

### Slots

| 插槽名   | 说明               |
| ------- | ----------------- |
|         |                   |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |



# DiscretePlayer 离散播放器

离散播放器组件是一个用于循环播放一系列离散值的工具，可用于动画或步进通过数据集。与标准`Player`组件不同，它使用离散的选项值，而不是连续的数值范围。

底层实现为`panel.widgets.DiscretePlayer`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/DiscretePlayer.html


## 基本用法

基本的离散播放器使用：


## 设置循环和间隔

可以设置播放器是否循环以及播放间隔(毫秒）：


## 使用字典选项

可以使用字典作为选项，其中键是显示的标签，值是实际的数据值：


## 设置显示模式

可以设置播放器的显示模式，如只显示按钮或者同时显示值等：


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

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
|         |                   |

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


## 使用Box接口

可以设置为CheckBox样式：


## 垂直布局

可以设置为垂直布局：


## 使用字典选项

可以使用字典作为选项，其中键是显示的标签，值是实际的数据值：


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

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
|         |                   |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |



# DateRangePicker 日期范围选择器

日期范围选择器组件允许用户使用文本框和浏览器的日期选择工具选择一个日期范围。

底层实现为`panel.widgets.DateRangePicker`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/DateRangePicker.html


## 基本用法

基本的日期范围选择器使用：


## 设置日期范围限制

可以设置可选日期的范围：


## 禁用和启用特定日期

可以设置特定日期不可选或可选：


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

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
|         |                   |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |



# Display 小组件/Output 展示器

支持 IPython 提供的所有 display tools，如`Video`、`Audio`、`HTML` 等，详情见 [rich output generated by IPython](http://ipython.readthedocs.io/en/stable/api/generated/IPython.display.html#module-IPython.display)

也可以用来集成并展示第三方组件，如 Matplotlib、Pandas、Plotly、Panel、Bokeh 等。

::: tip 
默认使用 `display` 函数（对小组件的兼容性更好）来渲染组件，但是在多进程场景 `display` 的会有[意想不到的行为](https://ipywidgets.readthedocs.io/en/latest/examples/Output%20Widget.html#interacting-with-output-widgets-from-background-threads)。在多进程场景建议使用 `multi_thread` 参数把 `Display` 的渲染函数切换为另一个实现（对小组件的兼容性没有display好）。  
:::

::: warning
当前页面只能展示组件的样式，需要在 `notebook` 才有交互效果。
:::
## 展示 Matplotlib

展示 matplotlib 绘制的图，并利用布局组件进行排列。更推荐使用`PnMatplotlib`组件。
## 展示 PIL 图片
## 展示 Pandas Dataframe
## 展示 widget

利用 `Display` 组件集成基于 ipywidgets/Panel 的任意 widget。
## Display API

### Display 属性

| 属性名        | 说明                 | 类型                                                           | 默认值 |
| --------     | ------------------- | ---------------------------------------------------------------| ------- |
| obj | 支持 IPython display 的对象 | ^[any]                                                         | —       |

### Display 方法

| 属性名 | 说明 | 类型 |
| --- | --- | --- |



# FileSelector 文件选择器

文件选择器组件提供了一个用于在服务器端文件系统中选择文件或目录的界面。

底层实现为`panel.widgets.FileSelector`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/FileSelector.html


## 基本用法

基本的文件选择器使用：


## 显示隐藏文件

可以控制是否显示隐藏文件：


## 文件过滤

可以通过正则表达式过滤文件：

## 远程文件系统

利用 [fsspec](https://filesystem-spec.readthedocs.io/en/latest/) 的强大功能，我们可以连接到远程文件系统。在下面的示例中，我们使用 s3fs 包连接到远程 S3 服务器。

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

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
|         |                   |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |



# DatetimeRangeInput 日期时间范围输入框

日期时间范围输入框组件允许用户以文本形式输入日期时间范围，并使用预定义的格式解析它。

底层实现为`panel.widgets.DatetimeRangeInput`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/DatetimeRangeInput.html


## 基本用法

基本的日期时间范围输入框使用：


## 自定义格式

可以通过format参数自定义日期时间的解析和显示格式：


## 设置边界

可以设置日期时间的上下限：


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

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
|         |                   |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |



# Terminal 终端

终端组件提供了一个与底层命令行交互的终端界面。它基于xterm.js，并通过WebSocket连接到服务器端的虚拟终端。

底层实现为`panel.widgets.Terminal`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/Terminal.html


## 基本用法

创建一个基本的终端界面：


## 自定义参数

可以设置各种终端参数，如字体大小、是否显示光标等：


## 交互处理

终端还可以通过命令随时更新：


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

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
|         |                   |

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


## 自定义格式

可以使用自定义格式字符串或Bokeh TickFormatter来格式化滑块值：


## 垂直方向

滑块可以设置为垂直方向显示：


## 滑块颜色和方向

可以自定义滑块条的颜色和方向：


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

### Slots

| 插槽名   | 说明               |
| ------- | ----------------- |
|         |                   |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |



# IntInput 整数输入框

整数输入框组件允许输入整数值，可以通过箭头按钮调整或直接输入数值。

底层实现为`panel.widgets.IntInput`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/IntInput.html


## 基本用法

基本的整数输入框使用：


## 范围限制

可以使用`start`和`end`参数设定值的范围：


## 自定义步长

可以使用`step`参数定义上下调整时的步进值：


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

### Slots

| 插槽名   | 说明               |
| ------- | ----------------- |
|         |                   |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |



# MenuButton 菜单按钮

菜单按钮组件允许指定一个菜单项列表供用户选择，当点击菜单项时触发事件。与其他组件不同，它没有`value`参数，而是有一个`clicked`参数，可以通过监听此参数来触发事件，该参数报告最后点击的菜单项。

底层实现为`panel.widgets.MenuButton`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/MenuButton.html


## 基本用法

基本的菜单按钮使用，定义按钮名称和菜单项列表：菜单项可以是单个字符串或元组，用None分隔为不同组。


## 分离式菜单

可以使用`split`选项将下拉指示器移动到单独的区域：

在`split`模式下，如果点击按钮本身，将报告`name`参数的值。

## 按钮样式

可以通过设置`button_type`来改变按钮的颜色：


## 图标

菜单按钮的名称和菜单项可以包含Unicode字符和表情符号，为常见的图形按钮提供了一种便捷的方式：


对于按钮本身，可以通过提供SVG `icon`值或从[tabler-icons.io](https://tabler-icons.io)加载的命名`icon`来使用更高级的图标：


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

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
|         |                   |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |



# DatetimeRangePicker 日期时间范围选择器

日期时间范围选择器组件允许使用文本框和浏览器的日期时间选择工具选择日期时间范围。

底层实现为`panel.widgets.DatetimeRangePicker`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/DatetimeRangePicker.html


## 基本用法

基本的日期时间范围选择器使用：


## 设置日期范围限制

可以设置可选日期的范围：


## 禁用和启用特定日期

可以设置特定日期不可选或可选：**注意**是`datetime.date`类型。


## 时间格式设置

可以控制时间显示和编辑的方式：


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

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
|         |                   |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |



# CheckButtonGroup 多选按钮组

多选按钮组组件允许通过切换相应的按钮来选择多个选项。它属于多选项选择组件的广泛类别，提供兼容的API，包括[``MultiSelect``](MultiSelect.md)、[``CrossSelector``](CrossSelector.md)和[``CheckBoxGroup``](CheckBoxGroup.md)组件。

底层实现为`panel.widgets.CheckButtonGroup`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/CheckButtonGroup.html


## 基本用法

基本的多选按钮组使用：


## 垂直方向

可以将按钮组设置为垂直方向：


## 使用字典选项

可以使用字典作为选项，其中键是显示的标签，值是实际的数据值：


## 按钮样式

可以通过设置`button_type`和`button_style`来改变按钮的外观：


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

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
|         |                   |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |



# RadioButtonGroup 单选按钮组

单选按钮组组件允许使用一组切换按钮从列表或字典中选择一个值。它属于单值选项选择组件的广泛类别，提供兼容的API，包括[``RadioBoxGroup``](RadioBoxGroup.md)、[``Select``](Select.md)和[``DiscreteSlider``](DiscreteSlider.md)组件。

底层实现为`panel.widgets.RadioButtonGroup`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/RadioButtonGroup.html


## 基本用法

基本的单选按钮组使用：


## 垂直方向

可以将按钮组设置为垂直方向：


## 使用字典选项

可以使用字典作为选项，其中键是显示的标签，值是实际的数据值：


## 按钮样式

可以通过设置`button_type`和`button_style`来改变按钮的外观：


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

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
|         |                   |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |



# RangeSlider 范围滑块

范围滑块组件允许使用带有两个手柄的滑块选择整数范围。

底层实现为`panel.widgets.RangeSlider`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/RangeSlider.html


## 基本用法

基本的范围滑块，通过拖动两个手柄选择一个范围：


## 自定义格式

可以使用自定义格式字符串或Bokeh TickFormatter来格式化滑块值：


## 垂直方向

滑块可以设置为垂直方向显示：


## 滑块颜色和方向

可以自定义滑块条的颜色和方向：


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

### Slots

| 插槽名   | 说明               |
| ------- | ----------------- |
|         |                   |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |



# FloatInput 浮点输入框

浮点输入框组件允许输入浮点数值，可以通过箭头按钮调整或直接输入数值。

底层实现为`panel.widgets.FloatInput`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/FloatInput.html


## 基本用法

基本的浮点数输入框使用：


## 范围限制

可以使用`start`和`end`参数设定值的范围：


## 自定义步长

可以使用`step`参数定义上下调整时的步进值：


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

### Slots

| 插槽名   | 说明               |
| ------- | ----------------- |
|         |                   |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |



# FileDownload 文件下载

文件下载组件允许在前端下载文件，通过在初始化时（如果`embed=True`）或点击按钮时将文件数据发送到浏览器。

底层实现为`panel.widgets.FileDownload`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/FileDownload.html


## 基本用法

基本的文件下载组件使用，默认情况下（`auto=True`和`embed=False`）文件只在按钮被点击后才传输到浏览器：

## 嵌入文件数据

可以通过`embed`参数立即嵌入文件数据，这允许在静态导出中使用此组件：


## 手动保存

如果设置`auto=False`，文件不会在初次点击时下载，而是会在数据同步后将标签从"Transfer<文件>"更改为"Download<文件>"。这样可以在数据传输后使用"另存为"对话框下载。


## 使用文件对象

文件下载组件也可以接受文件对象，例如将`pandas DataFrame`保存为`CSV`到`StringIO`对象：


## 动态生成文件

可以提供回调函数动态生成文件，例如根据某些小部件的参数：


## 按钮样式

可以通过设置`button_type`和`button_style`来改变文件下载按钮的外观：


## 图标按钮

与其他按钮一样，可以提供显式的`icon`，可以是tabler-icons.io的命名图标：


也可以是显式的SVG：


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

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |
|       |                      |                                        |

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
|   icon      |          svg 图标         |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |



# DatetimeInput 日期时间输入框

日期时间输入框组件允许以文本形式输入日期时间值，并使用预定义的格式解析它。

底层实现为`panel.widgets.DatetimeInput`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/DatetimeInput.html


## 基本用法

基本的日期时间输入框使用：

## 自定义格式

可以通过format参数自定义日期时间的解析和显示格式：


## 设置边界

可以设置日期时间的上下限：


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

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
|         |                   |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |



# ToggleIcon 图标切换

图标切换组件允许在`True`/`False`状态之间切换一个条件，类似于`Checkbox`和`Toggle`组件，但使用图标来表示状态。

底层实现为`panel.widgets.ToggleIcon`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/ToggleIcon.html


## 基本用法

基本的图标切换组件使用：


## 自定义图标

可以自定义默认图标和激活状态图标：



## 使用SVG图标

可以使用SVG字符串作为图标：


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

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
|         |                   |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |



# TextInput 文本输入框

文本输入框允许使用文本输入框输入任何字符串。

底层实现为`panel.widgets.TextInput`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/TextInput.html


## 基本用法

基本的文本输入框，可以输入和获取字符串：


## 实时输入

TextInput 组件提供了`value_input`参数，可以在每次按键时更新：


## API

### 属性

| 属性名        | 说明                    | 类型      | 默认值     |
| ------------ | ----------------------- | -------- | --------- |
| value        | 当前值，在按下Enter键或组件失去焦点时更新 | ^[str] | ""        |
| value_input  | 当前值，在每次按键时更新     | ^[str]   | ""        |
| disabled     | 是否禁用                 | ^[bool]  | False     |
| max_length   | 输入字段的最大字符长度     | ^[int]   | 5000      |
| name         | 组件标题                 | ^[str]   | ""        |
| placeholder  | 未输入值时显示的占位字符串  | ^[str]   | ""        |

### Events

| 事件名         | 说明                       | 类型                                   |
| ------------- | -------------------------- | -------------------------------------- |
| change        | 当值更改时触发的事件         | ^[Callable]`(event: dict) -> None`    |
| enter_pressed | 当按下Enter键时触发的事件    | ^[Callable]`() -> None`               |

### Slots

| 插槽名   | 说明               |
| ------- | ----------------- |
|         |                   |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |



# DatetimeSlider 日期时间滑块

日期时间滑块组件允许用户在设定的日期时间范围内使用滑块选择一个日期时间值。

底层实现为`panel.widgets.DatetimeSlider`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/DatetimeSlider.html


## 基本用法

基本的日期时间滑块使用：


## 自定义格式

可以通过format参数自定义日期时间的显示格式：


## 步长设置

可以通过step参数设置滑块的步长（单位为秒）：


## 垂直方向

滑块可以设置为垂直方向显示：


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

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
|         |                   |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |



# NestedSelect 嵌套选择器

嵌套选择组件允许用户从多层级的嵌套选项中进行选择，每个级别的选择会影响下一个级别的可用选项。

底层实现为`panel.widgets.NestedSelect`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/NestedSelect.html


## 基本用法

基本的嵌套选择组件，提供多层级的选项：


## 自定义布局

嵌套选择组件支持不同的布局类型：


网格布局示例：


## 设置默认值

可以通过设置`v-model`/`value`参数来指定默认选中的值：


## 动态选项

动态生成选项options：


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

### Slots

| 插槽名   | 说明               |
| ---     | ---               |
|         |                   |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |



# TimePicker 时间选择器

时间选择器组件允许用户选择一个时间，可以以文本形式输入或使用浏览器的时间选择工具。

底层实现为`panel.widgets.TimePicker`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/TimePicker.html


## 基本用法

基本的时间选择器使用：


## 时间范围限制

可以使用`start`和`end`参数限制可选择的时间范围：


## 自定义时间格式

可以使用`format`参数自定义时间的显示格式：


## 自定义步长

可以通过`hour_increment`、`minute_increment`和`second_increment`参数控制时、分、秒的调整步长：


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

### Slots

| 插槽名   | 说明               |
| ------- | ----------------- |
|         |                   |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |



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

## 延迟更新

默认情况下，代码编辑器会在每次按键时更新`value`，但可以设置`on_keyup=False`，使其仅在编辑器失去焦点或按下`<Ctrl+Enter>`/`<Cmd+Enter>`时更新`value`：

## 语言和主题

可以更改编辑器的语言和主题：

## 注释和只读模式

可以为编辑器添加注释，并设置为只读模式：

## 通过文件名自动检测语言

如果设置了`filename`属性，编辑器会根据文件扩展名自动检测语言：


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

### Slots

| 插槽名   | 说明               |
| ------- | ----------------- |
|         |                   |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |



# EditableRangeSlider 可编辑范围滑块

可编辑范围滑块组件允许使用带有两个手柄的滑块选择浮点范围，并提供数字输入框以便进行更精确的控制。

底层实现为`panel.widgets.EditableRangeSlider`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/EditableRangeSlider.html


## 基本用法

基本的可编辑范围滑块，可以通过滑动两个手柄或直接输入数字来选择范围：


## 固定范围

滑块的`value`默认没有界限，可以超过`end`或低于`start`。如果需要将`value`固定在特定范围内，可以使用`fixed_start`和`fixed_end`：


## 自定义格式

可以使用自定义格式字符串或Bokeh TickFormatter来格式化滑块值：


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

### Slots

| 插槽名   | 说明               |
| ------- | ----------------- |
|         |                   |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |



# ArrayInput 数组输入框

数组输入框组件允许使用文本输入框渲染和编辑NumPy数组，其内容随后在Python中解析。为避免大型数组的问题，`ArrayInput`定义了一个`max_array_size`，如果数组超过此大小，文本表示将被汇总，编辑将被禁用。

底层实现为`panel.widgets.ArrayInput`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/ArrayInput.html


## 基本用法

基本的数组输入框，可以显示和编辑NumPy数组：


## 大型数组

对于大型数组，可以设置`max_array_size`以避免浏览器负担过重：


## 自定义占位符

可以自定义占位符文本：


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

### Slots

| 插槽名   | 说明               |
| ------- | ----------------- |
|         |                   |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |



# DateRangeSlider 日期范围滑块

日期范围滑块组件允许使用带有两个手柄的滑块选择日期范围。

底层实现为`panel.widgets.DateRangeSlider`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/DateRangeSlider.html


## 基本用法

可以通过拖动手柄调整滑块的开始和结束日期，也可以通过拖动选定范围来整体移动范围：


## 自定义格式

可以使用自定义格式字符串来格式化滑块值：


## 垂直方向

滑块可以设置为垂直方向显示：


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

### Slots

| 插槽名   | 说明               |
| ------- | ----------------- |
|         |                   |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |



# CheckBoxGroup 复选框组

允许通过选中相应的复选框从选项列表中选择多个选项。它属于多选项选择组件的广泛类别，提供兼容的API，包括`MultiSelect`、`CrossSelector`和`CheckButtonGroup`组件。

底层实现为`panel.widgets.CheckBoxGroup`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/CheckBoxGroup.html


## 基本用法

基本的复选框组，可以选择多个选项：

## 垂直布局

通过设置`inline=False`可以将选项垂直排列：

## 字典选项

可以使用字典作为选项，键作为显示标签，值作为实际值：


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

### Slots

| 插槽名   | 说明               |
| ------- | ----------------- |
|         |                   |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |



# DatePicker 日期选择器

日期选择器组件允许使用文本框和浏览器的日期选择工具选择日期值。

底层实现为`panel.widgets.DatePicker`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/DatePicker.html


## 基本用法

日期选择器使用浏览器依赖的日历小部件来选择日期：

## 日期范围限制

可以通过`start`和`end`参数限制可选日期的范围：


## 可用/禁用日期

可以通过`disabled_dates`和`enabled_dates`参数设置不可用和可用的日期：


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

### Slots

| 插槽名   | 说明               |
| ------- | ----------------- |
|         |                   |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |



# AutocompleteInput 自动完成输入框

自动完成输入框组件允许通过在自动完成文本字段中输入值来从选项列表或字典中选择一个`value`。它属于单值、选项选择组件的广泛类别，提供兼容的API，包括`RadioBoxGroup`、`Select`和`DiscreteSlider`组件。

底层实现为`panel.widgets.AutocompleteInput`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/AutocompleteInput.html


## 基本用法

基本的自动完成输入框，可以从选项列表中选择一个值：


## 不限制输入

如果设置`restrict=False`，自动完成输入框将允许任何输入，而不仅限于它提供的自动完成选项：


## 字典选项

`options`参数也接受一个字典，其键将是下拉菜单的标签：


## 搜索策略

可以通过`search_strategy`参数定义如何搜索完成字符串列表：


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
| min_characters  | 用户必须输入多少字符才会显示自动完成 | ^[int]                           | 2         |

### Events

| 事件名         | 说明                       | 类型                                   |
| ------------- | -------------------------- | -------------------------------------- |
| change        | 当值更改时触发的事件         | ^[Callable]`(event: dict) -> None`    |

### Slots

| 插槽名   | 说明               |
| ------- | ----------------- |
|         |                   |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |



# CrossSelector 交叉选择器

交叉选择器组件允许通过在两个列表之间移动项目来从选项列表中选择多个值。它属于多选项选择组件的广泛类别，提供兼容的API，包括`MultiSelect`、`CheckBoxGroup`和`CheckButtonGroup`组件。

底层实现为`panel.widgets.CrossSelector`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/CrossSelector.html


## 基本用法

交叉选择器由多个组件组成：
* 两个列表，分别用于未选择（左）和已选择（右）的选项值
* 过滤框，允许使用正则表达式匹配下方值列表中的选项
* 按钮，用于将值从未选择列表移动到已选择列表（`>>`）或反之（`<<`）

## 自定义过滤函数

可以自定义过滤函数来控制如何根据搜索模式过滤选项：


## 保持定义顺序

通过`definition_order`参数可以控制是否在过滤后保留定义顺序：


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

### Slots

| 插槽名   | 说明               |
| ------- | ----------------- |
|         |                   |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |



# RadioBoxGroup 单选框组

单选框组组件允许使用一组复选框从值列表或字典中进行选择。它属于单值、选项选择组件的广泛类别，提供兼容的API，包括`RadioButtonGroup`、`Select`和`DiscreteSlider`组件。

底层实现为`panel.widgets.RadioBoxGroup`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/RadioBoxGroup.html


## 基本用法

基本的单选框组，可以从选项列表中选择一个值：


## 字典选项

使用字典作为选项，键作为显示标签，值作为实际值：


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

### Slots

| 插槽名   | 说明               |
| ------- | ----------------- |
|         |                   |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |



# IntSlider 整数滑块

整数滑块组件允许使用滑块在设定的范围内选择整数值。

底层实现为`panel.widgets.IntSlider`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/IntSlider.html


## 基本用法

基本的整数滑块，可以通过滑动选择整数值：


## 自定义格式

可以使用自定义格式字符串或Bokeh TickFormatter来格式化滑块值：


## 垂直方向

滑块可以设置为垂直方向显示：


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

### Slots

| 插槽名   | 说明               |
| ------- | ----------------- |
|         |                   |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |



# EditableFloatSlider 可编辑浮点滑块

可编辑浮点滑块组件允许使用滑块在设定的范围内选择浮点数值，并提供一个可编辑的数字输入框以便进行精确控制。

底层实现为`panel.widgets.EditableFloatSlider`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/EditableFloatSlider.html


## 基本用法

基本的可编辑浮点滑块，可以通过滑动或直接输入数字来选择值：


## 固定范围

滑块的`value`默认没有界限，可以超过`end`或低于`start`。如果需要将`value`固定在特定范围内，可以使用`fixed_start`和`fixed_end`：


## 自定义格式

可以使用自定义格式字符串或Bokeh TickFormatter来格式化滑块值：


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

### Slots

| 插槽名   | 说明               |
| ------- | ----------------- |
|         |                   |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |



# TextAreaInput 多行文本输入框

多行文本输入框允许使用文本输入框输入任何多行字符串。行与行之间使用换行符`\n`连接。

底层实现为`panel.widgets.TextAreaInput`，参数基本一致，参考文档：https://panel.holoviz.org/reference/widgets/TextAreaInput.html


## 基本用法

基本的多行文本输入框，可以输入和获取多行字符串：


## 自动增长

自动增长的 TextAreaInput 会根据输入的文本自动调整高度。设置 `rows` 和 `auto_grow` 可以设置行数下限，而设置 `max_rows` 可以提供上限：


## 可调整大小

可以设置文本区域只在垂直方向可调整大小：


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
| rows         | 文本输入字段的行数         | ^[int]   | 2         |
| resizable    | 布局是否可交互调整大小，如果是，则指定哪个维度：height、width、both、False | ^[bool\|str] | 'both' |

### Events

| 事件名         | 说明                       | 类型                                   |
| ------------- | -------------------------- | -------------------------------------- |
| change        | 当值更改时触发的事件         | ^[Callable]`(event: dict) -> None`    |

### Slots

| 插槽名   | 说明               |
| ------- | ----------------- |
|         |                   |

### 方法

| 方法名 | 说明 | 类型 |
| ----- | ---- | ---- |



## 简介
vuep.py是一个用于构建用户界面的python框架。它基于标准html、python构建，并提供一套声明式、组件化的编程模型，与Vue3.js组合式API几乎完全兼容。

核心功能：
* 声明式渲染：Vue.py 基于标准 HTML 拓展了一套模板语法，使得我们可以声明式地描述最终输出的 HTML 和 Python 状态之间的关系。
* 响应性：Vue.py 会自动跟踪 Python 状态并在其发生变化时响应式地更新 DOM。

## 安装vuepy

```
pip install org.vuepy.core
```

## 单文件组件 SFC

语法和vue.js一致，不同点在与使用`<script lang='py'></script>`来包裹实现组件逻辑的python代码，以下为vuepy组合式API构建的SFC组件示例：

```vue
<template>
  <Button :label="f'Count is: {count.value}'"
          @click='counter()'
  ></Button>
</template>

<script lang='py'>
from vuepy import ref

count = ref(0)

def counter():
    count.value += 1
</script>
```

### SFC 语法定义

一个 Vue.py 单文件组件 (SFC)，通常使用 *.vue 作为文件扩展名，它是一种使用了类似 HTML 语法的自定义文件格式，用于定义 Vue.py 组件。一个 Vue.py 单文件组件在语法上是兼容 HTML 的。和vue.js的sfc组件非常相似。

`<template>`：每个vue文件最多可以包含一个顶层template块。

`<script lang='py'>`：每个vue文件最多可以包含一个。 script内为python代码，每一个组件实例都会执行该段代码，其中的变量、函数声明、import导入等都将自动暴露给模板。props, context, app等变量会自动传入，也会自动暴露给模板，script内可以直接使用。
```vue
<template>
 <p>{{ msg.value }}</p>
</template>
<script lang='py'>
from vuepy import ref
msg = ref("Hello World!")
</script>
```

`<script src="./xxx.py"></script>`：每个vue文件最多可以包含一个。通过src导入一个外部python文件。src为相对路径时以`./`开头，表示相对于当前vue文件的路径，该python文件中需要定义setup函数。
```python
def setup(props, context, app):
    # 声明变量、函数等
    ...
    # 手动调用 locals 将局部变量暴露给模版
    return locals()
```

`<script lang='py'>`和`<script src="./xxx.py"></script>`只能选一种

`<script setup>`：只作为IDE的自动补全提示使用，对实际运行没有影响。

`<style>`：暂不支持。

## 创建Vue.py应用

```python
from vuepy import create_app, import_sfc
App = import_sfc("./App.vue")
app = create_app(App)
app.mount()
```
## 模板语法

和vue.js基本一致，不同的是表达式是 python 表达式。

文本插值
```vue
<span>{{ exp }}</span>
```

Attribute绑定
```vue
<div v-bind:id="dynamicId"></div>
<div :id="dynamicId"></div>
```

使用Python表达式，支持完整的Python表达式，以当前组件实例为作用域解析执行
```vue
<span>
{{ var.value + 1 }}
{{ 'Y' if ok.value else 'N' }}
{{ ','.join(msgs) }}
{{ format(data) }}
</span>
<Input :value="f'list-{did.value}'"></Input>
```

指令 Directives：带有`v-`前缀的特殊attribute。指令attribute的期望值一般为一个Python表达式。其表达式的值变化时会响应式地更新UI。
```vue

```
## 响应式基础

ref、reactive和vue.js的基本一致。  
不同点：
* 获取ref对象的值需要显式地访问ref对象的value属性。

示例
```vue
<template>
  <p>{{ state.count }}</p>
  <InputNumber v-model="state.count"></InputNumber>
  <Button @click="add()">add</Button>
</template>
<script lang='py'>
from vuepy import reactive

state = reactive({'count': 0})

def add():
    state.count += 1
</script>
```

shallowRef是ref的浅层作用形式，可以放弃深层响应性，和vue.js的基本一致。

## 计算属性

computed和vue.js的基本一致。  
不同点：
* 可以使用装饰器声明计算属性
```python
from vuepy import ref, computed

count = ref(1)

@computed
def plus_one():
  return count.value + 1
```
## 条件渲染

v-if、v-else-if、v-else、v-show和vue.js的基本一致。
## 列表渲染

v-for指令：
* 特别注意：当有v-for有两个参数时，第一个参数index是循环索引，更符合python习惯。
  ```vue
  <li v-for="(index, item) in items">
  ```
* Vue.py 能够侦听响应式数组的变更方法：append ,clear ,extend ,insert ,pop ,remove ,reverse ,sort。

示例：
```vue
<template>
  <!-- list with index: The order is different from vue.js -->
  <div>
    <span v-for="(index, item) in l">
      {{ index }}: {{ item }}
    </span>
  </div>

  <!-- list -->
  <div>
    <span v-for="item in l">
      {{ item }}
    </span>
  </div>

  <!-- iter(dict) -->
  <div>
    <span v-for="key in d">
      {{ key }}
    </span>
  </div>

  <!-- ref dict -->
  <div>
    <span v-for="i, value in d_ref.value.values()">
      {{ i }}: {{ value }}
    </span>
  </div>

  <!-- list with func -->
  <div>
    <span v-for="i in filter(lambda x: x % 2 == 0, l)">
      {{ i }}
    </span>
  </div>
</template>
<script lang='py'>
from vuepy import ref

d = {'a': 1, 'b': 2}
d_ref = ref(d)
l = [1, 2, 3, 4, 5]
</script> 
```

## 事件处理

v-on和vue.js的基本一致。  
不同点：
* 只支持自定义组件(如 Button等)，暂不支持原生 html 元素（如 span等）
* 只实现了最基础的功能
## 表单输入绑定

v-model和vue.js的基本一致。  
不同点：
* 只支持自定义组件(如 Input、Dropdown等)，暂不支持原生 html 元素（如 input 等）
* 只实现了最基础的功能
## 生命周期钩子

当前版本未实现。
## 帧听器

watch和vue.js的基本一致。  
不同点：
* 只实现了最基础的功能
* 支持装饰器的使用方式
```py
# 单个 ref
@watch(x)
def x_update(newX, oldX, on_cleanup):
    print(f'x is {newX}')

# 停止帧听器
x_update()
```

## 模板引用

ref和vue.js的基本一致。  
不同点：
* ref引用的是元素对应的widget对象
* ref未实现自动解包
## 组件

### 组件定义
和vue.js的SFC基本一致，可以定义在`.vue`文件中。  
不同点：
* 组件逻辑包裹在`<script lang='py'></script>`中，使用python语言
```vue
<template>
  <Button :label="f'Count is: {count.value}'"
          @click='counter()'
  ></Button>
</template>

<script lang='py'>
from vuepy import ref

count = ref(0)

def counter():
    count.value += 1
</script>
```


### 使用组件

1. 局部注册的方式

```vue
<template>
  <h1>hello</h1>
  <Counter></Counter>
</template>

<script lang='py'>
from vuepy import import_sfc
Counter = import_sfc('./Counter.vue')
</script>
```

2. 全局注册的方式

```python
from vuepy import import_sfc

MyComponent = import_sfc('./Component.vue')
app.component('MyComponent', MyComponent)
```

### 传递props

defineProps和vue.js基本相同。  
不同点：
* 需要显式导入`from vuepy import defineProps`
* 需要显示地访问value来获取值`props.title.value`

在`<script lang='py'>`中的使用示例：

```vue
<!-- Hello.vue -->
<template>
  <p>hello {{ props.name.value }}</p>
</template>
<script lang='py'>
from vuepy import defineProps

props = defineProps(['name'])
</script>
```

```vue
<!-- App.vue -->
<template>
  <Hello name="world"></Hello>
</template>
```

在`<script src='xxx.py'>`中的使用示例：

```vue
<!-- Hello.vue -->
<template>
  <p>hello {{ props.name.value }}</p>
</template>
<script src='hello.py'></script>
```

```python
# hello.py
from vuepy import defineProps

def setup(props, ctx, app):
    props = defineProps(['name'])
    return locals()
```

```vue
<!-- App.vue -->
<template>
  <Hello name="world"></Hello>
</template>
```
### 监听事件

defineEmits和vue.js基本相同。  
不同点：
* 需要显式导入`from vuepy import defineEmits`
* 原生html标签的监听事件暂不支持

在`<script lang='py'>`中的使用示例：

```vue
<!-- Hello.vue -->
<template>
  <p>hello</p>
  <Button @click="submit">submit</Button>
</template>
<script lang='py'>
from vuepy import defineEmits

emit = defineEmits(['submit'])

def submit(ev):
    print(ev) # Button(description='submit', ...)
    emit('submit', 1, 2, 3)
</script>
```

```vue
<!-- App.vue -->
<template>
  <Hello @submit="on_child_submit"></Hello>
</template>
<script lang='py'>
def on_child_submit(a, b, c):
    print(a, b, c) # 1 2 3
</script>
```

在`<script src='xxx.py'>`中的使用示例：

```vue
<!-- Hello.vue -->
<template>
  <p>hello</p>
  <Button @click="submit">submit</Button>
</template>
<script src='hello.py'></script>
```

```python
# hello.py
from vuepy import defineEmits

def setup(props, ctx, app):
    emit = defineEmits(['submit'])

    def submit(ev):
        print(ev) # Button(description='submit', ...)
        emit('submit', 1, 2, 3)

    return locals()
```

```vue
<!-- App.vue -->
<template>
  <Hello @submit="on_child_submit"></Hello>
</template>
<script lang='py'>
def on_child_submit(a, b, c):
    print(a, b, c) # 1 2 3
</script>
```

### 组件 v-model

definModel和vue.js基本相同  
不同点：
* 需要显式导入`from vuepy import defineModel`
* 需要显示地访问value来获取值`xxx.value`
* 不支持处理v-model修饰符

在`<script lang='py'>`中的使用示例：

```vue
<!-- Hello.vue -->
<template>
  <Input v-model="model.value" placeholder="name"></Input>
  <p>child:hello {{ model.value }}</p>
</template>
<script lang='py'>
from vuepy import defineModel

model = defineModel('model_a')
model.value = 'world'
</script>
```

```vue
<!-- App.vue -->
<template>
  <Hello v-model:model_a="m.value"></Hello>
  <p>parent: hello {{ m.value }}</p>
</template>
<script lang='py'>
from vuepy import ref

m = ref('world')
</script>
```

在`<script src='xxx.py'>`中的使用示例：

```vue
<!-- Hello.vue -->
<template>
  <Input v-model="model.value" placeholder="name"></Input>
  <p>child:hello {{ model.value }}</p>
</template>
<script src='hello.py'></script>
```

```python
# hello.py
from vuepy import defineModel

def setup(props, ctx, app):
    model = defineModel() # default
    model.value = 'world'

    return locals()
```

```vue
<!-- App.vue -->
<template>
  <Hello v-model="m.value"></Hello>
  <p>parent: hello {{ m.value }}</p>
</template>
<script lang='py'>
from vuepy import ref

m = ref('world')
</script>
```
### 通过slot分配内容

slot和vue.js基本相同  
不同点：
* 只实现了最基本的功能
* 不支持动态插槽名
* 不支持作用域插槽

### 模版解析注意事项

和vue.js基本相同  
不同点：
* 不支持闭合标签，必须显式地写出关闭标签`<A></A>`
* 元素位置限制，在HTML元素中不支持嵌套自定义组件，例如div中不能放置Input等自定义组件，可以使用VBox或HBox替代div作为一种解决方案。
```vue
<!-- 原生html标签中不能嵌套自定义组件 -->
<div><Input></Input></div>
```
可用VBox代替
```vue
<VBox><Input></Input></VBox>
```
## 插件

和vue.js基本相同。  
不同点：
* 编写插件，继承`VuePlugin`并实现install方法。
```python
# plugins/i18n.py
from vuepy import VuePlugin

class I18nPlugin(VuePlugin):
    @classmethod
    def install(cls, app, options):
        # 在这里编写插件代码
        def s1_translate(key):
            # 获取 `options` 对象的深层属性
            # 使用 `key` 作为索引
            ret = option
            for k in key.split('.'):
                ret = option.get(k, {})
            return ret
            
        # 注入一个全局可用的 s1_translate() 方法
        # s1_ 与vue.js的$类似
        app.config.globalProperties.s1_translate = s1_translate
```
* 使用插件
```python
from plugin.i18n import I18nPlugin

app.use(I18nPlugin, options={
  'greetings': {
    'hello': 'Bonjour!',
  },
})
```
## ipython magic函数

需要先通过`from vuepy.utils import magic`导入。

### 导入SFC组件

1. `%vuepy_import`通过文件导入组件
```python
from vuepy.utils import magic
# 导入 test.vue 组件
App=%vuepy_import test.vue
```
2. `%%vuepy_import`通过字符串导入组件，并将组件对象赋值给`{Component1}`变量
```python
%%vuepy_import Component1
<template>
  <Button description="add"
  ></Button>
</template>
```
如果需要访问当前jupyter笔记本中的变量可以通过以下方式
```python
# --- cell 1 ---
a = 1
# --- cell 2 ---
%%vuepy_import A
<template>
  <p>{{ a }}</p>
</template>
<script lang='py'>
from IPython import get_ipython
# 获取jupyter笔记本中的变量
locals().update(get_ipython().user_ns)
</script>
```

### 运行vuepy应用

1. `%vuepy_run`通过文件或组件变量运行应用
```python
%vuepy_run app.vue
```
```python
from vuepy import import_sfc
App = import_sfc("App.vue")
# 通过$$来引用变量
%vuepy_run $$App
```
2. `%%vuepy_run`通过字符串运行应用
```python
%%vuepy_run
<template>
  <Button description="add"
          button_style="info"
  ></Button>
</template>
```
如果需要访问当前jupyter笔记本中的变量可以通过以下方式
```python
# --- cell 1 ---
a = 1
# --- cell 2 ---
%%vuepy_run
<template>
  <p>{{ a }}</p>
</template>
<script lang='py'>
from IPython import get_ipython
# 获取jupyter笔记本中的变量
locals().update(get_ipython().user_ns)
</script>
```

### 实时获取vuepy运行日志

```python
# 打印所有日志
%vuepy_log
# 打印日志，但会清除之前的日志。
%vuepy_log clear
```
## 集成 Anywidget

示例演示与 anywidget 组件进行状态同步，并实现事件机制。

```vue
<template>
  <p>count: {{ count.value }}</p>
  <Counter v-model="count.value"></Counter>
</template>

<script lang="py">
import anywidget
import traitlets

from vuepy import ref, VueComponent

class CounterWidget(anywidget.AnyWidget):
    _esm = """
    function render({ model, el }) {
      let count = () => model.get("value");
      let btn = document.createElement("button");
      btn.classList.add("counter-button");
      btn.innerHTML = `count is ${count()}`;
      btn.addEventListener("click", () => {
        model.set("value", count() + 1);
        model.save_changes();
      });
      model.on("change:value", () => {
        btn.innerHTML = `count is ${count()}`;
      });
      el.appendChild(btn);
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
    value = traitlets.Int(0).tag(sync=True)

class Counter(VueComponent):
    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return CounterWidget(**props, **attrs)

count = ref(0)
</script>
```

实现 container 类型的组件并集成 ipywui 组件 Button。

```vue
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
```
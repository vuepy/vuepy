## ipywui组件库

IPywUI 是基于 Vue.py 和 ipywidgets 开发的 UI 组件库。当前作为 Vue.py 内置的 UI 组件库。

ipywui组件作为Vuepy的插件提供，一般会自动注册，也可以手动注册：
```py
from ipywui import wui
app.use(wui)
```

设置ipywui组件的style属性可以改变其样式（与css非常相似）：
```
Sizes相关
* height
* width
* max_height
* max_width
* min_height
* min_width

颜色相关
* background-color
* color

Display相关
* visibility
* display
* overflow

Box model相关
* border
* margin
* padding

Positioning相关
* top
* left
* bottom
* right
```
示例
```vue
<Button style="background-color: #626aef;"></Button>
<Button style="width: 90px; height: 60px"></Button>
```
### Component, Button

对于click的事件处理函数有两种方式：
1. 指定参数的方式：`@click=far()` 或 `@click=far(arg)`
2. 不指定参数的方式：`@click=handle`，会自动传入btn参数(当前按钮的widget对象)，所以handle函数必须接受一个参数：
```python
def handle(btn):
  ...
```

 可以通过icon属性为按钮添加图标，图标为fontawesome v5。
```vue
<!-- button/basic.vue -->
<template>
  <HBox>
    <Button @click="on_click()">Default</Button>
    <Button type="info">Info</Button>
    <Button type="success">Success</Button>
    <Button type="warning">Warning</Button>
    <Button label="Danger" type="danger"></Button>
  </HBox>
  <HBox>
    <Button icon="search" @click="on_click2"></Button>
    <Button type="info" icon="edit"></Button>
    <Button type="success" icon="check"></Button>
    <Button type="warning" icon="star">{{ count.value }}</Button>
    <Button type="danger" icon="trash-alt"></Button>
  </HBox>
</template>

<script setup>
import Button from "../../../src/ipywui/components/Button";
import HBox from "../../../src/ipywui/components/HBox";
</script>
<script lang="py">
from vuepy import ref

count = ref(1)

def on_click():
  count.value += 1
  print("on click")

def on_click2(btn):
  print(f"{btn} on click") # Button(icon='search', style=ButtonStyle()) on click
</script>
```

### Component, Layout

通过基础的24分栏创建布局。
```vue
<!-- layout/layout-basic.vue -->
<template>
  <Row>
    <Col :span="24">
      <Button label="span 24" style="width: auto; background-color: #9dacc1"></Button>
    </Col>
  </Row>

  <Row>
    <Col :span="12">
      <Button label="span 12" style="width: auto; background-color: #d4dde6"></Button>
    </Col>
    <Col :span="12">
      <Button label="span 12" style="width: auto; background-color: #e5e9f2"></Button>
    </Col>
  </Row>

  <Row>
    <Col :span="8">
      <Button label="span 8" style="width: auto; background-color: #d4dde6"></Button>
    </Col>
    <Col :span="8">
      <Button label="span 8" style="width: auto; background-color: #e5e9f2"></Button>
    </Col>
    <Col :span="8">
      <Button label="span 8" style="width: auto; background-color: #d4dde6"></Button>
    </Col>
  </Row>

  <Row>
    <Col :span="6">
      <Button label="span 6" style="width: auto; background-color: #d4dde6"></Button>
    </Col>
    <Col :span="6">
      <Button label="span 6" style="width: auto; background-color: #e5e9f2"></Button>
    </Col>
    <Col :span="6">
      <Button label="span 6" style="width: auto; background-color: #d4dde6"></Button>
    </Col>
    <Col :span="6">
      <Button label="span 6" style="width: auto; background-color: #e5e9f2"></Button>
    </Col>
  </Row>
</template>

<script setup>
import Col from "../../../src/ipywui/components/Col";
import Row from "../../../src/ipywui/components/Row";
import Button from "../../../src/ipywui/components/Button";
</script>
```

### Component, AppLayout

用于布局的容器组件，方便搭建页面的基本结构：
```vue
<!-- layout_app/layout-hc.vue -->
<template>
  <AppLayout>
    <template v-slot:header>
      <Button
          label="header"
          style="width: auto; height: auto; background-color: #c8e3fe"
      ></Button>
    </template>
    <template v-slot:center>
      <Button
          style="width: auto; height: auto; background-color: #ecf5fe"
      ></Button>
      <Button
          label="center"
          style="width: auto; height: auto; background-color: #ecf5fe"
      ></Button>
      <Button
          style="width: auto; height: auto; background-color: #ecf5fe"
      ></Button>
    </template>
  </AppLayout>
</template>

<script setup>
import Button from "../../../src/ipywui/components/Button";
import AppLayout from "../../../src/ipywui/components/AppLayout";
</script>
```

```vue
<!-- layout_app/custom.vue -->
<template>
  <AppLayout :pane_widths="['100px', 1, 1]" :pane_heights="[1, 3, '30px']">
    <template v-slot:header>
      <Button label="header" style="width: auto; height: auto; background-color: #c8e3fe"></Button>
    </template>
    <template v-slot:left_sidebar>
      <Button label="" style="width: auto; height: auto; background-color: #dbecfe"></Button>
      <Button label="left 100px" style="width: auto; height: auto; background-color: #dbecfe"></Button>
      <Button label="" style="width: auto; height: auto; background-color: #dbecfe"></Button>
    </template>
    <template v-slot:right_sidebar>
      <Button label="" style="width: auto; height: auto; background-color: #dbecfe"></Button>
      <Button label="right" style="width: auto; height: auto; background-color: #dbecfe"></Button>
      <Button label="" style="width: auto; height: auto; background-color: #dbecfe"></Button>
    </template>
    <template v-slot:center>
      <Button style="width: auto; height: auto; background-color: #ecf5fe"></Button>
      <Button label="center" style="width: auto; height: auto; background-color: #ecf5fe"></Button>
      <Button style="width: auto; height: auto; background-color: #ecf5fe"></Button>
    </template>
    <template v-slot:footer>
      <Button label="footer" style="width: auto; height: auto; background-color: #c8e3fe"></Button>
    </template>
  </AppLayout>
</template>

<script setup>
import Button from "../../../src/ipywui/components/Button";
import AppLayout from "../../../src/ipywui/components/AppLayout";
</script>
```

您还可以使用 pane_widths（左侧边栏、主区域、右侧边栏的宽度）和 pane_heights（顶栏、主区域、右侧边栏高度）参数修改AppLayout窗格的相对和绝对宽度和高度。两者都接受三个元素的序列，每个元素要么是整数（相当于赋予行/列的权重），要么是格式为 '1fr' （与整数相同）或 '100px'。  
注意使用绑定属性的形式：
```vue
<AppLayout :pane_widths="['100px', 1, 1]" :pane_heights="[1, 5, '60px']">
...
</AppLayout>
```
### Component, Box Layout 
```vue
<!-- layout_box/vbox-basic.vue -->
<template>
  <VBox>
    <Button label="1" style="width: auto; background-color: #c8e3fe"></Button>
    <Button label="2" style="width: auto; background-color: #ecf5fe"></Button>
    <Button label="3" style="width: auto; background-color: #c8e3fe"></Button>
  </VBox>
</template>

<script setup>
import Button from "../../../src/ipywui/components/Button";
import VBox from "../../../src/ipywui/components/VBox";
</script>
```

```vue
<!-- layout_box/hbox-basic.vue -->
<template>
  <HBox>
    <Button label="1" style="width: auto;background-color: #c8e3fe"></Button>
    <Button label="2" style="width: auto;background-color: #ecf5fe"></Button>
    <Button label="3" style="width: auto;background-color: #c8e3fe"></Button>
  </HBox>
</template>

<script setup>
import Button from "../../../src/ipywui/components/Button";
import HBox from "../../../src/ipywui/components/HBox";
</script>
```

### Component, Checkbox
```vue
<!-- checkbox/basic.vue -->
<template>
  <HBox>
    <Checkbox v-model="checked1.value" label="Option1"></Checkbox>
    <Checkbox v-model="checked2.value" label="Option2"></Checkbox>
    <Checkbox v-model="checked3.value" label="Option3"></Checkbox>
  </HBox>
  <HBox>
    <Checkbox v-model="checked1.value" label="Option1" :disabled="True"></Checkbox>
    <Checkbox v-model="checked2.value" label="Option2" :disabled="True"></Checkbox>
    <Checkbox v-model="checked3.value" label="Option3" :disabled="True"></Checkbox>
  </HBox>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import HBox from "../../../src/ipywui/components/HBox";
import Checkbox from "../../../src/ipywui/components/Checkbox";
</script>
```
```python
# ./basic_setup.py

from vuepy import ref


def setup(props, ctx, vm):
    checked1 = ref(True)
    checked2 = ref(True)
    checked3 = ref(True)

    return locals()

```

### Component, ColorPicker
```vue
<!-- color_picker/basic.vue -->
<template>
  <ColorPicker label="Pick1"
               v-model="color1.value"></ColorPicker>

  <ColorPicker label="Pick2"
               value="lightblue"></ColorPicker>

  <ColorPicker label="Concise"
               v-model="color2.value" concise></ColorPicker>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import ColorPicker from "../../../src/ipywui/components/ColorPicker";
</script>
```
```python
# ./basic_setup.py

from vuepy import ref


def setup(props, ctx, vm):
    color1 = ref("#8f8fcc")
    color2 = ref("green")

    return locals()

```

### Component, Combobox

Provide corresponding input suggestions based on the input content.
```vue
<!-- combobox/basic.vue -->
<template>
  <Combobox label="auto"
            placeholder="Choose someone"
            v-model="someone.value"
            :options="['Paul', 'John', 'George', 'Ringo']"
  ></Combobox>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import Combobox from "../../../src/ipywui/components/Combobox";
</script>
```
```python
# ./basic_setup.py

from vuepy import ref


def setup(props, ctx, vm):
    someone = ref('')

    return locals()

```

### Component, DatePicker
```vue
<!-- date_picker/basic.vue -->
<template>
  <DatePicker label="Pick a day" v-model="date.value"></DatePicker>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import DatePicker from "../../../src/ipywui/components/DatePicker";
</script>
```
```python
# ./basic_setup.py

from vuepy import ref


def setup(props, ctx, vm):
    date = ref(None)

    return locals()

```

```vue
<!-- date_picker/basic-range.vue -->
<template>
  <Input :value="str(min_day) + ' to ' + str(max_day)"></Input>
  <DatePicker label="Pick a day"
              v-model="day.value"
              :min="min_day"
              :max="max_day"
  ></DatePicker>
</template>

<script src="./basic_range_setup.py"></script>
<script setup>
import DatePicker from "../../../src/ipywui/components/DatePicker";
import Input from "../../../src/ipywui/components/Input";
</script>
```
```python
# ./basic_range_setup.py

import datetime

from vuepy import ref


def setup(props, ctx, vm):
    day = ref(None)

    min_day = datetime.date(2021, 1, 1)
    max_day = datetime.date(2024, 1, 1)

    return locals()

```

### Component, DateTimePicker
```vue
<!-- datetime_picker/basic.vue -->
<template>
  <DateTimePicker label="Pick a time"
                  v-model="datetime.value"
  ></DateTimePicker>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import DateTimePicker from "../../../src/ipywui/components/DateTimePicker";
</script>
```
```python
# ./basic_setup.py

from vuepy import ref


def setup(props, ctx, vm):
    datetime = ref(None)

    return locals()

```

```vue
<!-- datetime_picker/basic-range.vue -->
<template>
  <Input :value="str(min_time) + ' to ' + str(max_time)"></Input>
  <DateTimePicker label="Pick a day"
              v-model="time.value"
              :min="min_time"
              :max="max_time"
  ></DateTimePicker>
</template>

<script src="./basic_range_setup.py"></script>
<script setup>
import DateTimePicker from "../../../src/ipywui/components/DateTimePicker";
import Input from "../../../src/ipywui/components/Input";
</script>
```
```python
# ./basic_range_setup.py

import datetime

from vuepy import ref


def setup(props, ctx, vm):
    time = ref(None)

    tz = datetime.timezone(datetime.timedelta(seconds=28800), 'CST')
    min_time = datetime.datetime(2021, 1, 1, tzinfo=tz)
    max_time = datetime.datetime(2024, 1, 1, tzinfo=tz)

    return locals()

```

### Component, TimePicker
```vue
<!-- time_picker/basic.vue -->
<template>
  <TimePicker label="HH::mm"
              v-model="time.value"
  ></TimePicker>

  <TimePicker label="HH::mm::ss"
              v-model="time.value"
              :step="1"
  ></TimePicker>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import TimePicker from "../../../src/ipywui/components/TimePicker";
</script>
```
```python
# ./basic_setup.py

from vuepy import ref


def setup(props, ctx, vm):
    time = ref(None)

    return locals()

```

```vue
<!-- time_picker/basic-range.vue -->
<template>
  <Input :value="str(min_time) + ' to ' + str(max_time)"></Input>
  <TimePicker label="HH::mm::ss"
              v-model="time.value"
              :min="min_time"
              :max="max_time"
              :step="1"
  ></TimePicker>
</template>

<script src="./basic_range_setup.py"></script>
<script setup>
import TimePicker from "../../../src/ipywui/components/TimePicker";
import Input from "../../../src/ipywui/components/Input";
</script>
```
```python
# ./basic_range_setup.py

import datetime

from vuepy import ref


def setup(props, ctx, vm):
    time = ref(None)
    min_time = datetime.time(10, 10, 0)
    max_time = datetime.time(12, 10, 0)

    return locals()

```

### Component, Input
```vue
<!-- input/basic.vue -->
<template>
  <VBox>
    <Input label="input"
           placeholder="Please input"
           v-model="text.value"
    ></Input>

    <Input label="input"
           placeholder="continuous update"
           v-model="text.value"
           continuous_update
    ></Input>
  </VBox>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import VBox from "../../../src/ipywui/components/VBox";
import Input from "../../../src/ipywui/components/Input";
</script>
```
```python
# ./basic_setup.py

from vuepy import ref


def setup(props, ctx, vm):
    text = ref("")
    return locals()

```

```vue
<!-- input/textarea.vue -->
<template>
  <Input label="Textarea" type="textarea" value="Please input"></Input>
</template>

<script setup>
import Input from "../../../src/ipywui/components/Input";
</script>
```

```vue
<!-- input/password.vue -->
<template>
  <Input label="Password" type="password" value="xxx"></Input>
</template>

<script setup>
import Input from "../../../src/ipywui/components/Input";
</script>
```

### Component, Input Number
```vue
<!-- input_number/basic.vue -->
<template>
  <VBox>
    <InputNumber description="int"
                 v-model="num.value"
                 :min="1"
                 :max="10"
    ></InputNumber>

    <InputNumber description="float"
                 v-model="num_float.value"
                 :min="1"
                 :max="10"
    ></InputNumber>
  </VBox>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import InputNumber from "../../../src/ipywui/components/InputNumber";
import VBox from "../../../src/ipywui/components/VBox";
</script>
```
```python
# ./basic_setup.py

from vuepy import ref


def setup(props, ctx, vm):
    num = ref(1)
    num_float = ref(1.1)
    return locals()

```

```vue
<!-- input_number/steps.vue -->
<template>
  <InputNumber description="step" :step="2"></InputNumber>
</template>

<script setup>
import InputNumber from "../../../src/ipywui/components/InputNumber";
</script>
```

### Component, RadioButtons

`v-model` 或初始值必须是 options 中的值或者为`None`。
```vue
<!-- radio_buttons/basic.vue -->
<template>
  <RadioButtons description="Options ['pepperoni', 'pineapple', 'anchovies']"
                v-model="choice1.value"
                :options="options1"
  ></RadioButtons>

  <RadioButtons description="Options [('One', 1), ('Two', 2), ('Three', 3)]"
                v-model="choice2.value"
                :options="options2"
  ></RadioButtons>

</template>

<script src="./basic_setup.py"></script>
<script setup>
import RadioButtons from "../../../src/ipywui/components/RadioButtons";
</script>
```
```python
# ./basic_setup.py

from vuepy import ref


def setup(props, ctx, vm):
    options1 = ['pepperoni', 'pineapple', 'anchovies']
    choice1 = ref('pepperoni')

    options2 = [('One', 1), ('Two', 2), ('Three', 3)]
    choice2 = ref(1)

    return locals()

```

### Component, Select
```vue
<!-- select/basic.vue -->
<template>
  <Select description="OS:"
          :rows="1"
          :options="['Linux', 'Win', 'macOS']"
  ></Select>

  <Select description="OS:"
          v-model="choice.value"
          :options="['Linux', 'Win', 'macOS']"
  ></Select>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import Select from "../../../src/ipywui/components/Select";
</script>
```
```python
# ./basic_setup.py

from vuepy import ref


def setup(props, ctx, vm):
    choice = ref('macOS')

    choice2 = ref(1)
    radio_items = [('One', 1), ('Two', 2), ('Three', 3)]
    return locals()

```

```vue
<!-- select/multiple.vue -->
<template>
  <Select description="OS:"
          v-model="choices.value"
          :rows="2"
          :options="['Linux', 'Win', 'macOS']"
          multiple
  ></Select>

  <Select description="OS:"
          v-model="choices2.value"
          :options="['Linux', 'Win', 'macOS']"
          multiple
  ></Select>
</template>

<script src="./multiple_setup.py"></script>
<script setup>
import Select from "../../../src/ipywui/components/Select";
</script>
```
```python
# ./multiple_setup.py

from vuepy import ref


def setup(props, ctx, vm):
    choices = ref([])

    choices2 = ref(['Linux', 'macOS'])
    return locals()

```

### Component, SelectColors
```vue
<!-- select_colors/basic.vue -->
<template>
  <SelectColors v-model="colors.value"></SelectColors>
  <Input :value="', '.join(colors.value)"></Input>

  <SelectColors unique></SelectColors>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import SelectColors from "../../../src/ipywui/components/SelectColors";
import Input from "../../../src/ipywui/components/Input";
</script>
```
```python
# ./basic_setup.py

from vuepy import ref


def setup(props, ctx, vm):
    colors = ref(['red', 'green', '#0000ff'])
    return locals()

```

```vue
<!-- select_colors/allowed_tags.vue -->
<template>
  <SelectColors
      :value="['lightgreen', 'lightgray']"
      :allowed_tags="['lightgreen', 'lightgray', 'lightblue']"
  ></SelectColors>
</template>

<script setup>
import SelectColors from "../../../src/ipywui/components/SelectColors";
</script>
```

### Component, SelectNumbers
```vue
<!-- select_numbers/basic.vue -->
<template>
  <SelectNumbers v-model="nums.value"></SelectNumbers>
  <Input label="float nums" :value="str(nums.value)"></Input>

  <SelectNumbers v-model="int_nums.value"
                 data_type="int"></SelectNumbers>
  <Input label="int nums" :value="str(int_nums.value)"></Input>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import SelectNumbers from "../../../src/ipywui/components/SelectNumbers";
import Input from "../../../src/ipywui/components/Input";
</script>
```
```python
# ./basic_setup.py

from vuepy import ref


def setup(props, ctx, vm):
    nums = ref([1, 2, 3])
    int_nums = ref([1, 2, 3])

    return locals()

```

```vue
<!-- select_numbers/basic-range.vue -->
<template>
  <SelectNumbers :value="[1, 2, 3]" :min="1" :max="10"
                 data_type="int"></SelectNumbers>
</template>

<script setup>
import SelectNumbers from "../../../src/ipywui/components/SelectNumbers";
</script>
```

### Component, SelectTags
```vue
<!-- select_tags/basic.vue -->
<template>
  <SelectTags v-model="tags.value"></SelectTags>
  <Input label='basic' :value="str(tags.value)"></Input>

  <SelectTags v-model="unique_tags.value" unique></SelectTags>
  <Input label='unique' :value="str(unique_tags.value)"></Input>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import SelectTags from "../../../src/ipywui/components/SelectTags";
import Input from "../../../src/ipywui/components/Input";
</script>
```
```python
# ./basic_setup.py

from vuepy import ref


def setup(props, ctx, vm):
    tags = ref(['tag1', 'tag2', 'tag3'])
    unique_tags = ref(['t1', 't2', 't3'])
    return locals()

```

```vue
<!-- select_tags/allowed_tags.vue -->
<template>
  <Input value="allowed_tags ['a', 'b', 'c']"></Input>
  <SelectTags
      :value="['a', 'b']"
      :allowed_tags="['a', 'b', 'c']"
  ></SelectTags>
</template>

<script setup>
import Input from "../../../src/ipywui/components/Input";
import SelectTags from "../../../src/ipywui/components/SelectTags";
</script>
```

### Component, Slider
```vue
<!-- slider/basic.vue -->
<template>
  <Slider description="Default" v-model="default.value"></Slider>
  <Slider description="Init val 5" v-model="init_val.value"></Slider>
  <Slider description="Float"
          v-model="float_val.value"
          :min="0"
          :max="30"
  ></Slider>
  <Slider description="Selection"
          v-model="selection_val.value"
          :options="selection_options"
  ></Slider>
  <Slider description="Disabled" :value="1" disabled></Slider>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import Slider from "../../../src/ipywui/components/Slider";
</script>
```
```python
# ./basic_setup.py

from vuepy import ref


def setup(props, ctx, vm):
    default = ref(0)
    init_val = ref(5)
    float_val = ref(10.1)
    selection_val = ref('a')
    selection_options = ['a', 'b', 'c', 'd']

    return locals()

```

```vue
<!-- slider/range-selection.vue -->
<template>
  <Slider description="Int range"
          v-model="int_range.value"
          :max="10"
          range
  ></Slider>
  <Slider description="Float range"
          v-model="float_range.value"
          :min="0"
          :max="10"
          range
  ></Slider>
  <Slider description="Selection range"
          v-model="selection_range.value"
          :options="selection_options"
          style="description-width: 100px"
          range
  ></Slider>
</template>

<script src="./range_selection_setup.py"></script>
<script setup>
import Slider from "../../../src/ipywui/components/Slider";
</script>

```
```python
# ./range_selection_setup.py

from vuepy import ref


def setup(props, ctx, vm):
    int_range = ref([1, 3])
    float_range = ref([1.1, 3.1])
    selection_range = ref(['a', 'c'])
    selection_options = ['a', 'b', 'c', 'd']

    return locals()

```

```vue
<!-- slider/vertical.vue -->
<template>
  <HBox>
    <Slider description="Float"
            :value="3"
            :min="0"
            :max="30"
            vertical
    ></Slider>
    <Slider description="Selection"
            value="b"
            :options="['a', 'b', 'c']"
            vertical
    ></Slider>
  </HBox>
</template>

<script setup>
import Slider from "../../../src/ipywui/components/Slider";
import HBox from "../../../src/ipywui/components/HBox";
</script>
```

```vue
<!-- slider/show-marks.vue -->
<template>
  <Input :value="str(selection.value)"></Input>
  <Slider description="Selection"
          v-model="selection.value"
          :options="selection_options"
          style="description-width: 100px"
  ></Slider>
  <Input :value="str(selection_range.value)"></Input>
  <Slider description="Selection range"
          v-model="selection_range.value"
          :options="selection_options"
          style="description-width: 100px"
          range
  ></Slider>
</template>

<script src="./show_marks_setup.py"></script>
<script setup>
import Slider from "../../../src/ipywui/components/Slider";
import Input from "../../../src/ipywui/components/Input";
</script>

```
```python
# ./show_marks_setup.py

from vuepy import ref


def setup(props, ctx, vm):
    selection_options = [('0°C', 0), ('5°C', 5), ('10°C', 10), ('37°C', 37)]
    selection = ref(10)
    selection_range = ref([5, 37])

    return locals()

```

### Component, ToggleButton

表示两种相互对立的状态间的切换，多用于触发「开/关」
```vue
<!-- toggle_button/basic.vue -->
<template>
  <HBox>
    <ToggleButton label="on" :value="True"></ToggleButton>
    <ToggleButton label="off" :value="False"></ToggleButton>
  </HBox>
  <HBox>
    <ToggleButton type="info" :value="True"></ToggleButton>
    <ToggleButton type="info" :value="False"></ToggleButton>
    </HBox>
  <HBox>
    <ToggleButton type="success" v-model="val1.value"></ToggleButton>
    <ToggleButton type="success" :value="False"></ToggleButton>
    </HBox>
  <HBox>
    <ToggleButton type="warning" :value="True"></ToggleButton>
    <ToggleButton type="warning"></ToggleButton>
    </HBox>
  <HBox>
    <ToggleButton type="danger" :value="True"></ToggleButton>
    <ToggleButton type="danger" :value="False"></ToggleButton>
  </HBox>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import ToggleButton from "../../../src/ipywui/components/ToggleButton";
import HBox from "../../../src/ipywui/components/HBox";
</script>
```
```python
# ./basic_setup.py

from vuepy import ref


def setup(props, ctx, vm):
    val1 = ref(True)
    return locals()

```

### Component, ToggleButtons

在一组备选项中进行单选
```vue
<!-- toggle_buttons/basic.vue -->
<template>
  <ToggleButtons description="Options ['pepperoni', 'pineapple', 'anchovies']"
                 v-model="choice1.value"
                 :options="options1"
  ></ToggleButtons>

  <ToggleButtons description="Options [('One', 1), ('Two', 2), ('Three', 3)]"
                 v-model="choice2.value"
                 :options="options2"
  ></ToggleButtons>

  <!--  style-->
  <ToggleButtons description="Style success"
                 type="success"
                 :options="options2"
  ></ToggleButtons>
  <ToggleButtons description="Style info"
                 type="info"
                 :options="options2"
  ></ToggleButtons>
  <ToggleButtons description="Style warning"
                 type="warning"
                 :options="options2"
  ></ToggleButtons>
  <ToggleButtons description="Style danger"
                 type="danger"
                 :options="options2"
  ></ToggleButtons>

  <!--  icon-->
  <ToggleButtons description="With icons"
                 :icons="['walking', 'car-side', 'plane']"
                 :options="['walking ', 'car ', 'plane ']"
  ></ToggleButtons>

</template>

<script src="./basic_setup.py"></script>
<script setup>
import ToggleButtons from "../../../src/ipywui/components/ToggleButtons";
</script>
```
```python
# ./basic_setup.py

from vuepy import ref


def setup(props, ctx, vm):
    options1 = ['pepperoni', 'pineapple', 'anchovies']
    choice1 = ref('pepperoni')

    options2 = [('One', 1), ('Two', 2), ('Three', 3)]
    choice2 = ref(1)

    return locals()

```

### Component, File Upload
```vue
<!-- file_upload/basic.vue -->
<template>
  <FileUpload v-model="files.value" accept=".txt"></FileUpload>
  <Input label="file info"
         :value="upload_file.value"
         type="textarea"
         style="height: 200px"
  ></Input>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import FileUpload from "../../../src/ipywui/components/FileUpload";
import Input from "../../../src/ipywui/components/Input";
</script>
```
```python
# ./basic_setup.py

import codecs
import json

from vuepy import computed
from vuepy import ref


def setup(props, ctx, vm):
    files = ref([])

    def get_first_file():
        file_info = {}
        if files.value:
            file_info = files.value[0]
            content = file_info['content']
            file_info['content'] = codecs.decode(content, encoding='utf-8')
            file_info['last_modified'] = str(file_info['last_modified'])

        return json.dumps(file_info, indent=2)

    upload_file = computed(get_first_file)

    return locals()

```

### Component, Accordion
```vue
<!-- accordion/basic.vue -->
<template>
  <Accordion v-model="selected.value">
    <AccordionItem title="Item0">
      <Slider description="slider"></Slider>
    </AccordionItem>

    <AccordionItem title="Item1">
      <Input placeholder="input"></Input>
    </AccordionItem>

    <AccordionItem title="Item2">
      <Button label="click" type="info"></Button>
    </AccordionItem>

  </Accordion>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import Accordion from "../../../src/ipywui/components/Accordion";
import AccordionItem from "../../../src/ipywui/components/AccordionItem";
import Slider from "../../../src/ipywui/components/Slider";
import Input from "../../../src/ipywui/components/Input";
import Button from "../../../src/ipywui/components/Button";
</script>
```
```python
# ./basic_setup.py

from vuepy import ref


def setup(props, ctx, vm):
    selected = ref(1)

    return locals()

```

### Component, Display

支持IPython提供的所有display tools，如Video、Audio、HTML等，也可以用来集成并展示第三方组件。
展示 matplotlib 绘制的图，并利用布局组件进行排列。
```vue
<!-- display/matplotlib.vue -->
<template>
  <HBox>
    <Display :obj="plt1.value"></Display>
    <Display :obj="plt2.value"></Display>
  </HBox>
  <Display :obj="plt3.value" multi_thread></Display>
</template>

<script src="./matplotlib_setup.py"></script>
<script setup>
import Display from "../../../src/ipywui/components/Display";
import HBox from "../../../src/ipywui/components/HBox";
</script>
```
```python
# ./matplotlib_setup.py

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


def plt_cos():
    x = np.arange(0, 5 * np.pi, 0.1)
    y = np.cos(x)
    plt.plot(x, y, color='blue')
    return plt_to_img('Cosine Curve using Matplotlib', 'x', 'sin(x)')


def plt_scatter():
    np.random.seed(1)
    data_x = np.random.randn(100)
    data_y = np.random.randn(100)
    plt.scatter(data_x, data_y, color='blue', alpha=0.5)
    return plt_to_img('Scatter Plot Example', 'x', 'y')


def setup(props, ctx, vm):
    plt1 = ref(plt_sin())
    plt2 = ref(plt_scatter())
    plt3 = ref(plt_cos())

    return locals()

```

展示 PIL 图片
```vue
<!-- pil.vue -->
<template>
  <Display :obj="pil_img"></Display>
</template>

<script setup>
import Display from "../../../src/ipywui/components/Display";
</script>
<script lang="py">
from PIL import Image

pil_img = Image.open("jupyter_logo.jpg")

</script>
```
展示 Video、Audio
```vue
<!-- display/video_audio.vue -->
<template>
  <Display :obj="video"></Display>
  <p>注意：先调节音量</p>
  <Display :obj="audio"></Display>
</template>

<script setup>
import Display from "../../../src/ipywui/components/Display";
</script>
<script lang="py">
import numpy as np
from IPython.display import Video
from IPython.display import Audio

video_src = "https://github.com/vuepy/vuepy/raw/refs/heads/master/examples/ipywui/display/sora.mp4"
video = Video(video_src, width=350)

# gen sound
sr = 22050
T = 0.5
t = np.linspace(0, T, int(T * sr), endpoint=False)
x = 0.5 * np.sin(2 * np.pi * 440 * t)

audio = Audio(x, rate=sr)


</script>

```

展示 Pandas Dataframe
```vue
<!-- display/pandas-dataframe.vue -->
<template>
  <Display :obj="df1"></Display>
  <Display :obj="df2"></Display>
</template>

<script setup>
import Display from "../../../src/ipywui/components/Display";
</script>
<script lang="py">
import pandas as pd

df1 = pd.DataFrame(data={
    'col1': [1, 2],
    'col2': [3, 4],
    'col3': [5, 6],
})

df2 = pd.DataFrame(data={
    'col1': ['a', 'b'],
    'col2': ['c', 'd'],
    'col3': ['e', 'f'],
})

</script>

```

利用 Display 组件集成基于 plotly 的绘图组件。
```vue
<!-- display/plotly.vue -->
<template>
  <Dropdown v-model="freq.value" :options="frequencies" description="Frequency"></Dropdown>
  <Slider v-model="amplitude.value" description="Amplitude"></Slider>
  <Display :obj="fig"></Display>
</template>

<script setup>
import Display from "../../../src/ipywui/components/Display";
import Dropdown from "../../../src/ipywui/components/Dropdown";
import Slider from "../../../src/ipywui/components/Slider";
</script>
<script lang="py">
import plotly.graph_objects as go
import numpy as np
from vuepy import ref, watch

frequencies = [1, 2, 3, 4]

freq = ref(frequencies[0])
amplitude = ref(1.0)

fig = go.FigureWidget()
x = np.linspace(0, 10, 400)
waves = {f: np.sin(x * f) for f in frequencies}
fig.add_trace(go.Scatter(x=x, y=waves[freq.value], name=f'Frequency {freq.value}'))


@watch([freq, amplitude])
def update_figure(new_val, _, __):
    frequency, amplitude = new_val
    fig.data[0].y = waves[frequency] * amplitude
    fig.data[0].name = f'Frequency {frequency} (Amp: {amplitude:.1f})'
    fig.update_layout(title=f'Interactive Sine Wave (Frequency: {frequency}, Amplitude: {amplitude:.1f})')

</script>

```

利用 Display 组件集成基于 ipywidgets 的任意 widget。
```vue
<!-- display/ipywidgets.vue -->
<template>
<Display :obj="widget.value"></Display>
</template>

<script src="./ipywidgets_setup.py"></script>
<script setup>
import Display from "../../../src/ipywui/components/Display";
</script>
```
```python
# ./ipywidgets_setup.py

import ipywidgets as widgets
from IPython.display import display

from vuepy import ref


def setup(props, ctx, vm):
    a = widgets.IntSlider(description='a')
    b = widgets.IntSlider(description='b')
    c = widgets.IntSlider(description='c')

    def f(a, b, c):
        html = '<p style="color: red">{}*{}*{}={}</p>'.format(a, b, c, a * b * c)
        display(widgets.HTML(html))

    out = widgets.interactive_output(f, {'a': a, 'b': b, 'c': c})
    vbox = widgets.VBox([widgets.VBox([a, b, c]), out])
    widget = ref(vbox)

    return locals()

```

### Component, Image
```vue
<!-- image/basic.vue -->
<template>
  <Image v-model="img.value" format="png" style="width: 200px"></Image>

  <Image
      v-model="img.value" format="png"
      style="width: 200px; border: 2px solid deepskyblue"
  ></Image>

  <Image
      v-model="img.value" format="png"
      :style="'width: 200px; border: 2px solid {}'.format('blue')"
  ></Image>
</template>

<script setup>
import Image from "../../../src/ipywui/components/Image";
</script>
<script lang="py">
from vuepy import ref

file = open("jupyter_logo.png", "rb")
img = ref(file.read())
</script>
```

```vue
<!-- image/pil_img.vue -->
<template>
  <Image :value="pil_img" style="width: 200px"></Image>
</template>

<script setup>
import Image from "../../../src/ipywui/components/Image";
</script>
<script lang="py">
from vuepy import ref
from PIL import Image

pil_img = Image.open("jupyter_logo.png")
</script>
```

```vue
<!-- image/numpy_ndarray.vue -->
<template>
  <Image :value="rgb_png" width="30%"></Image>
  <Image :value="gray_png" width="100px"></Image>
  <Image :value="img_png" width="100px"></Image>
</template>

<script src="./numpy_ndarray.py"></script>
<script>
import Image from "../../../src/ipywui/components/Image";
</script>

```
```python
# ./numpy_ndarray.py

import numpy as np
from PIL import Image

from vuepy.utils.image_processer import convert_opencv_image_to_bin
from vuepy.utils.image_processer import convert_pil_image_to_bin


def setup(props, ctx, vm):
    img_array = np.zeros([100, 100, 3], dtype=np.uint8)
    img_array[:, :, 2] = 200
    # ndarray to rgb img
    rgb_png = Image.fromarray(img_array, mode='RGB')
    # 必须指定format
    rgb_png.format = 'PNG'


    img_array = np.zeros([100, 100, 1], dtype=np.uint8)
    img_array += 122
    # ndarray to gray img
    img = Image.fromarray(img_array.squeeze(), 'L')
    gray_png = convert_pil_image_to_bin(img, 'PNG')


    import cv2 as cv
    cv_img = cv.imread("jupyter_logo.png", cv.IMREAD_UNCHANGED)

    # method1: opencv to pil
    img_png = Image.fromarray(cv.cvtColor(cv_img, cv.COLOR_BGRA2RGBA))
    img_png.format = "PNG"

    # # method2: opencv to bin
    # img_png = convert_opencv_image_to_bin(cv_img, '.png')

    return locals()

```

### Component, Label
```vue
<!-- label/basic.vue -->
<template>
  <HBox>
    <Label>The $E=mc^2$ </Label><Slider :value="1.0"></Slider>
  </HBox>
  <HBox>
    <Label>Value {{ val.value }}</Label><Slider v-model="val.value"></Slider>
  </HBox>
  <HBox>
    <Label value="slider"></Label><Slider :value="1.0"></Slider>
  </HBox>
</template>

<script setup>
import Label from "../../../src/ipywui/components/Label";
import Slider from "../../../src/ipywui/components/Slider";
import HBox from "../../../src/ipywui/components/HBox";
</script>
<script lang="py">
from vuepy import ref

val = ref(1)
</script>
```

```vue
<!-- label/custom.vue -->
<template>
  <Label value="background lightblue" style="background: lightblue"></Label>
  <Label value="description-width: 100px" style="description-width: 100px"></Label>
  <Label value="font-size 16px" style="font-size: 16px"></Label>
  <Label value="font-style italic" style="font-style: italic"></Label>
  <Label value="font-weight bold" style="font-weight: bold"></Label>
  <Label value="color red" style="color: red"></Label>
  <Label value="text-decoration: underline" style="text-decoration: underline"></Label>
</template>

<script setup>
import Label from "../../../src/ipywui/components/Label";
</script>
```

### Component, MarkdownViewer
```vue
<!-- markdown_viewer/basic.vue -->
<template>
  <HBox>
    <Input v-model="md.value" type="textarea" style="height: 400px">
    </Input>
    <MarkdownViewer :value="md.value"></MarkdownViewer>
  </HBox>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import Input from "../../../src/ipywui/components/Input";
import MarkdownViewer from
      "../../../src/ipywui/components/MarkdownViewer";
import HBox from "../../../src/ipywui/components/HBox";
</script>
```
```python
# ./basic_setup.py

from vuepy import ref

md_src = r"""
### H3

This is a **bold** text and this is an *italic* text.   
link to [vuepy](https://github.com/vuepy)

### Code

    def foo():
        print("hello world")
        return 1

### List

- item1
- item2

### LaTeX
$$
a > b,b > c \Rightarrow a > c 
$$

$$
\begin{array}{c} 
  \forall A \in S \\ 
  P \left( A \right) \ge 0 
\end{array}
$$
"""

def setup(props, ctx, vm):
    md = ref(md_src)
    return locals()

```

### Component, Play
```vue
<!-- play/basic.vue -->
<template>
  <VBox>
    <Input :value="str(frame.value)"></Input>
    <Play label="int"
          v-model="frame.value"
          :min="1"
          :max="10"
          :step="1"
          :interval="500"
    ></Play>

    <Input :value="str(frame2.value)"></Input>
    <Play label="int"
          v-model="frame2.value"
          :min="1"
          :max="10"
          :step="1"
          :interval="1000"
    ></Play>
  </VBox>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import VBox from "../../../src/ipywui/components/VBox";
import Play from "../../../src/ipywui/components/Play";
import Input from "../../../src/ipywui/components/Input";
</script>
```
```python
# ./basic_setup.py

from vuepy import ref


def setup(props, ctx, vm):
    frame = ref(1)
    frame2 = ref(1)
    return locals()

```

### Component, Progress
```vue
<!-- progress/basic.vue -->
<template>
  <VBox>
    <Progress label="Default"
              :value="80" :min="1" :max="100"></Progress>

    <Progress label="Info" type="info"
              :value="60" :min="1" :max="100"></Progress>

    <Progress label="Success" type="success"
              :value="50" :min="1" :max="100"></Progress>

    <Progress label="Warning" type="warning"
              :value="40" :min="1" :max="100"></Progress>

    <Progress label="Danger" type="danger"
              :value="30" :min="1" :max="100"></Progress>
  </VBox>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import Progress from "../../../src/ipywui/components/Progress";
import VBox from "../../../src/ipywui/components/VBox";
</script>
```
```python
# ./basic_setup.py

from vuepy import ref


def setup(props, ctx, vm):
    progress = ref(0)
    return locals()

```

```vue
<!-- progress/vertical.vue -->

<template>
  <HBox>
    <Progress label="Default" vertical
              :value="80" :min="1" :max="100"></Progress>

    <Progress label="Info" type="info" vertical
              :value="60" :min="1" :max="100"></Progress>

    <Progress label="Success" type="success" vertical
              :value="50" :min="1" :max="100"></Progress>

    <Progress label="Warning" type="warning" vertical
              :value="40" :min="1" :max="100"></Progress>

    <Progress label="Danger" type="danger" vertical
              :value="30" :min="1" :max="100"></Progress>
  </HBox>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import Progress from "../../../src/ipywui/components/Progress";
import HBox from "../../../src/ipywui/components/HBox";
</script>
```
```python
# ./basic_setup.py

from vuepy import ref


def setup(props, ctx, vm):
    progress = ref(0)
    return locals()

```

```vue
<!-- progress/custom.vue -->

<template>
  <VBox>
    <Progress label="lightblue"
              style="color: lightblue"
              :value="80" :min="1" :max="100"></Progress>

    <Progress label="#8a54a8"
              style="color: #8a54a8"
              :value="60" :min="1" :max="100"></Progress>
  </VBox>
</template>
```

### Component, Valid
```vue
<!-- valid/basic.vue -->
<template>
  <Valid :value="True" description="Valid"></Valid>
  <Valid :value="False" description="Invalid"></Valid>
</template>

<script setup>
import Valid from "../../../src/ipywui/components/Valid";
</script>
```

### Component, Dropdown

v-model 或初始值必须是 options 中的值或者为`None`
```vue
<!-- dropdown/basic.vue -->
<template>
  <VBox>
    <Dropdown description="dropdown1"
              v-model="choice1.value"
              :options="dropdown_items1"
    ></Dropdown>

    <Dropdown description="dropdown2"
              v-model="choice2.value"
              :options="dropdown_items2"
    ></Dropdown>
  </VBox>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import VBox from "../../../src/ipywui/components/VBox";
import Dropdown from "../../../src/ipywui/components/Dropdown";
</script>
```
```python
# ./basic_setup.py

from vuepy import ref


def setup(props, ctx, vm):
    choice1 = ref('1')
    dropdown_items1 = ['1', '2', '3']

    choice2 = ref(1)
    dropdown_items2 = [('One', 1), ('Two', 2), ('Three', 3)]

    return locals()

```

### Component, Tabs
```vue
<!-- tabs/basic.vue -->
<template>
  <Tabs v-model="selected.value">
    <TabPane title="Tab1">
      <Slider description="slider"></Slider>
    </TabPane>

    <TabPane title="Tab2">
      <Input placeholder="input"></Input>
    </TabPane>

    <TabPane title="Tab3">
      <Button label="click" type="info"></Button>
    </TabPane>

  </Tabs>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import Tabs from "../../../src/ipywui/components/Tabs";
import TabPane from "../../../src/ipywui/components/TabPane";
import Slider from "../../../src/ipywui/components/Slider";
import Input from "../../../src/ipywui/components/Input";
import Button from "../../../src/ipywui/components/Button";
</script>
```
```python
# ./basic_setup.py

from vuepy import ref


def setup(props, ctx, vm):
    selected = ref(1)

    return locals()

```

### Component, Stack
```vue
<!-- stack/basic.vue -->
<template>
  <HBox>
    <Button label="s1" style="width: auto" @click="to('s1')"></Button>
    <Button label="s2" style="width: auto" @click="to('s2')"></Button>
    <Button label="s3" style="width: auto" @click="to('s3')"></Button>
  </HBox>

  <Stack v-model="selected.value">
    <StackItem label="s1">
      <Slider description="s1 slider"></Slider>
    </StackItem>

    <StackItem label="s2">
      <Input placeholder="s2 input"></Input>
    </StackItem>

    <StackItem label="s3">
      <Button label="s3 click" type="info"></Button>
    </StackItem>

  </Stack>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import Stack from "../../../src/ipywui/components/Stack";
import StackItem from "../../../src/ipywui/components/StackItem";
import Slider from "../../../src/ipywui/components/Slider";
import Input from "../../../src/ipywui/components/Input";
import Button from "../../../src/ipywui/components/Button";
import HBox from "../../../src/ipywui/components/HBox";
</script>
```
```python
# ./basic_setup.py

from vuepy import ref


def setup(props, ctx, vm):
    selected = ref('s1')

    def to(label):
        selected.value = label

    return locals()

```

### Component, Dialog
```vue
<!-- dialog/basic.vue -->
<template>
  <Button label="show dialog" type='info' @click="show()"></Button>
  <Label value="Placeholder" style="height: 200px"></Label>
  <Dialog title="Shipping address" v-model="is_show.value" width="55%">
    <template>
      <Input placeholder="name"></Input>
    </template>
    <template v-slot:footer>
      <HBox>
        <Button label="Cancel" type="warning" @click="close()"></Button>
        <Button label="Ok" type="info" @click="close()"></Button>
      </HBox>
    </template>
  </Dialog>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import Dialog from "../../../src/ipywui/components/Dialog";
import Button from "../../../src/ipywui/components/Button";
import Label from "../../../src/ipywui/components/Label";
import Input from "../../../src/ipywui/components/Input";
import HBox from "../../../src/ipywui/components/HBox";
</script>
```
```python
# ./basic_setup.py

from vuepy import ref


def setup(props, ctx, vm):
    is_show = ref(True)

    def show():
        is_show.value = True

    def close():
        is_show.value = False

    return locals()

```

```vue
<!-- dialog/events.vue -->
<template>
  <Button label="show dialog" type='info' @click="show()"></Button>
  <Label :value="state.value" style="height: 200px"></Label>
  <Dialog title="Shipping address" v-model="is_show.value" width="55%"
          @close="handle_close()"
          @open="handle_open()"
  >
    <template>
      <Input placeholder="name"></Input>
    </template>
    <template v-slot:footer>
      <HBox>
        <Button label="Cancel" type="warning" @click="close()"></Button>
        <Button label="Ok" type="info" @click="close()"></Button>
      </HBox>
    </template>
  </Dialog>
</template>

<script src="./events_setup.py"></script>
<script setup>
import Dialog from "../../../src/ipywui/components/Dialog";
import Button from "../../../src/ipywui/components/Button";
import Label from "../../../src/ipywui/components/Label";
import Input from "../../../src/ipywui/components/Input";
import HBox from "../../../src/ipywui/components/HBox";
</script>
```
```python
# ./events_setup.py

from vuepy import ref


def setup(props, ctx, vm):
    is_show = ref(True)

    state = ref("-")

    def show():
        is_show.value = True

    def close():
        is_show.value = False

    def handle_open():
        state.value = 'open'

    def handle_close():
        state.value = 'close'

    return locals()

```

### Component, Message 
```vue
<!-- message/basic.vue -->
<template>
  <Button label="Show Message" type="info" @click="show_msg()"></Button>
  <Label value="" style="height: 80px"></Label>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import Button from "../../../src/ipywui/components/Button";
import Label from "../../../src/ipywui/components/Label";
</script>
```
```python
# ./basic_setup.py


def setup(props, ctx, vm):
    def show_msg():
        vm.message.info({
            'message': 'This is message.',
            'duration': 2000,
        })

    return locals()

```

```vue
<!-- message/different-types.vue -->
<template>
  <Button label="Success" type="info" @click="show_success()"></Button>
  <Button label="Info" type="info" @click="show_info()"></Button>
  <Button label="Warning" type="info" @click="show_warning()"></Button>
  <Button label="Error" type="info" @click="show_error()"></Button>
  <Label value="" style="height: 80px"></Label>
</template>

<script src="./different_types_setup.py"></script>
<script setup>
import Button from "../../../src/ipywui/components/Button";
import Label from "../../../src/ipywui/components/Label";
</script>
```
```python
# ./different_types_setup.py


def setup(props, ctx, vm):
    def show_success():
        vm.message.success({
            'message': 'Congrats, this is a success message.',
        })

    def show_info():
        vm.message.info({
            'message': 'This is message.',
        })

    def show_warning():
        vm.message.warning({
            'message': 'Warning, this is a warning message.',
        })

    def show_error():
        vm.message.error({
            'message': 'Oops, this is a error message.',
        })

    return locals()

```

```vue
<!-- message/closeable.vue -->
<template>
  <Button label="show" type="info" @click="show()"></Button>
  <Label value="" style="height: 80px"></Label>
</template>

<script src="./closeable_setup.py"></script>
<script setup>
import Button from "../../../src/ipywui/components/Button";
import Label from "../../../src/ipywui/components/Label";
</script>
```
```python
# ./closeable_setup.py


def setup(props, ctx, vm):
    def show():
        msg = vm.message.success({
            'message': 'Congrats, this is a success message.',
            'show_close': True,
        })
        # tips: you can use msg.close() to close the message box
        # msg.close()

    return locals()

```

### Component, Clipboard
```vue
<!-- clipboard/basic.vue -->
<template>
  <HBox>
    <Input v-model="copytext.value"></Input>
    <Clipboard :copy="copytext.value">
      <Button label="copy" type="info"></Button>
    </Clipboard>
  </HBox>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import Clipboard from "../../../src/ipywui/components/Clipboard";
import Button from "../../../src/ipywui/components/Button";
import HBox from "../../../src/ipywui/components/HBox";
import Input from "../../../src/ipywui/components/Input";
</script>
```
```python
# ./basic_setup.py

from vuepy import ref


def setup(props, ctx, vm):
    copytext = ref("hello")

    return locals()

```

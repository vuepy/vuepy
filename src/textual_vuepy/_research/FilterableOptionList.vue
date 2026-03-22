<template>
  <VBox>
    <Input v-if="show_filter_input.value"
           v-model="filter_input.value"
           :placeholder="placeholder_str.value"
           style="width: 1fr;"
           @input_submitted="on_input_submitted"
           @keyup.up="on_input_key_up"
           @keyup.down="on_input_key_down"
           ref="filter_input_ref"
    />
    <OptionList v-model:highlighted="highlighted_model.value" ref="list_ref"
                @option_list_option_selected="forward_option_selected" >
        <slot name="default"></slot>
    </OptionList>
  </VBox>
</template>

<script lang="py">
"""
可搜索的 OptionList：顶部可选 Input，根据 filterable / filter-method 过滤 options。

Props:
  - options: 选项数据源（列表），与父组件传入的 ref.value 同步
  - filterable: 是否显示搜索框并过滤；默认 True
  - filter_method: (query, item) -> bool，仅 filterable 为 True 时参与过滤；未传时用默认子串匹配
  - input_placeholder: 搜索框占位符
  - option_prompt: (item) -> str，生成 Option 的 prompt；未传时对 (a,b) 元组用 \"a  b\"

v-model:filter   — 当前筛选字符串
v-model:highlighted — 与 OptionList 一致

事件:
  - option_list_option_selected — 自内层 OptionList 原样转发
"""
from vuepy import ref, computed, watch, onMounted, defineProps, defineModel, defineEmits
from vuepy.reactivity.watch import WatchOptions
from textual.widgets.option_list import Option as TextualOption

option_model = defineModel('value')
filter_input = ref('')
highlighted_model = defineModel('highlighted')
props = defineProps([
    'options',
    'filterable',
    'filter_method',
    'input_placeholder',
    'option_prompt',
])
emit = defineEmits(['option_list_option_selected'])

list_ref = ref(None)
filter_input_ref = ref(None)

def force_input():
    fi = filter_input_ref.value.unwrap()
    fi.focus()
    fi.move_cursor(len(fi.value))

def _prop_options():
    p = props.options.value
    return list(p) if p is not None else []


def _prop_filterable():
    v = props.filterable.value
    return True if v is None else bool(v)


show_filter_input = computed(lambda: _prop_filterable())
force_focus = computed(lambda: props.force.value if props.force.value is not None else True)
placeholder_str = computed(lambda: props.input_placeholder.value or "")


def _default_filter_method(query, item):
    q = (query or "").strip().lower()
    if not q:
        return True
    if isinstance(item, (list, tuple)):
        return any(q in str(x).lower() for x in item)
    return q in str(item).lower()


def _user_filter_method():
    fn = props.filter_method.value
    return fn if callable(fn) else None


@computed
def filtered_items():
    src = _prop_options()
    if not _prop_filterable():
        return src
    q = filter_input.value if filter_input.value is not None else ""
    fn = _user_filter_method() or _default_filter_method
    return [it for it in src if fn(q, it)]


def _prompt_for(item):
    fn = props.option_prompt.value
    if callable(fn):
        return fn(item)
    if isinstance(item, (list, tuple)) and len(item) >= 2:
        return f"{item[0]}  {item[1]}"
    return str(item)


def _id_for(item, idx):
    if isinstance(item, (list, tuple)) and len(item) >= 1:
        return str(item[0])
    return str(idx)


def rebuild_option_list():
    lr = list_ref.value
    if not lr:
        return
    w = lr.unwrap()
    w.clear_options()
    items = filtered_items.value
    for idx, it in enumerate(items):
        w.add_option(TextualOption(prompt=_prompt_for(it), id=_id_for(it, idx)))
    if items:
        hi = highlighted_model.value
        if hi is None or hi < 0 or hi >= len(items):
            highlighted_model.value = 0
        w.highlighted = highlighted_model.value
    else:
        highlighted_model.value = None


@watch(filtered_items, WatchOptions(immediate=True))
def _watch_filtered(*args):
    rebuild_option_list()


@onMounted
def _on_mount():
    rebuild_option_list()

def on_input_submitted(event):
    opts = filtered_items.value
    if opts:
        hi = highlighted_model.value
        option_model.value = opts[hi][0]
        emit('option_list_option_selected', option_model.value)

def forward_option_selected(event):
    option_model.value = event.option.id
    emit('option_list_option_selected', option_model.value)

def on_input_key_up():
    highlighted_model.value = max(highlighted_model.value - 1, 0)

def on_input_key_down():
    highlighted_model.value = min(highlighted_model.value + 1, len(filtered_items.value) - 1)
</script>

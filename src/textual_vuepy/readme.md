
```vue
<tag :class='' style='' />
```

* class 在更新事通过 TextualNode的setattr的ATTR_MAP设置到widget的classes上
* style 通过 _WidgetBase 的 sytle变化触发 _watch_sytle() -> widget.set_styles(style)
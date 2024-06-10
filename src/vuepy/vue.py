#!coding: utf-8
# from __future__ import annotations

# from vuepy import log as logging

# logger = logging.getLogger()


# def get_block_content_from_sfc(sfc_file, block):
#     with open(sfc_file) as f:
#         blocks = re.findall(f'<{block}>(.*)</{block}>', f.read(), flags=re.S | re.I)
#     return blocks
#
#
# def get_script_py_block_content_from_sfc(sfc_file):
#     with open(sfc_file) as f:
#         match = re.search(
#             fr'<script\s+lang=(["\'])py\1\s*>(?P<content>.*)?</script>',
#             f.read(),
#             flags=re.S | re.I
#         )
#
#     if not match:
#         logger.debug("can't find <script lang=py>")
#         return None
#
#     return match.group('content')
#
#
# def get_template_from_sfc(sfc_file):
#     return get_block_content_from_sfc(sfc_file, 'template')[0]
#
#
# def get_script_src_from_sfc(sfc_file):
#     with open(sfc_file) as f:
#         match = re.search(r"<script (.*?)src=(['\"])(?P<src>.*?)\2></script>", f.read())
#         if not match:
#             return None
#         return match.group('src')


# class WatcherBase(metaclass=abc.ABCMeta):
#     @abc.abstractmethod
#     def update(self):
#         pass
#
#
# class PubEnum(enum.Enum):
#     PROPERTY = 'property'
#     SETUP = 'setup'
#
#
# # Map<target_id, Map<key, List<effect>>>
# SUBS_MAP = {
#     PubEnum.PROPERTY: {},
#     PubEnum.SETUP: {},
# }
#
#
# def get_subscribers_for_property_by_id(target_id, key, pub=PubEnum.PROPERTY):
#     subs_map = SUBS_MAP[pub]
#     if target_id not in subs_map:
#         subs_map[target_id] = {}
#
#     if key not in subs_map[target_id]:
#         subs_map[target_id][key] = []
#
#     return subs_map[target_id][key]
#
#
# def get_subscribers_for_property(target, key, pub=PubEnum.PROPERTY):
#     return get_subscribers_for_property_by_id(id(target), key, pub)
#
#
# def add_subscribers_for_property(target, key, sub: WatcherBase, pub=PubEnum.PROPERTY):
#     effects = get_subscribers_for_property(target, key, pub)
#     effects.append(sub)
#
#
# def clear_subscribers_for_property(target, key, pub=PubEnum.PROPERTY):
#     effects = get_subscribers_for_property(target, key, pub)
#     effects.clear()
#
#
# def trigger_subscribers_for_property(target, key):
#     for pub in PubEnum:
#         effects = get_subscribers_for_property(target, key, pub)
#         for effect in effects:
#             effect.update()
#             if isinstance(effect, WatcherForRerender):
#                 return
#
#
# g_active_effect = None
# g_pub = None
#
#
# def track(target, key):
#     if not g_active_effect:
#         return
#
#     if g_pub:
#         add_subscribers_for_property(target, key, g_active_effect, g_pub)
#     else:
#         add_subscribers_for_property(target, key, g_active_effect, PubEnum.PROPERTY)
#
#
# def trigger(target, key):
#     trigger_subscribers_for_property(target, key)
#
#
# class ActivateEffect:
#     def __init__(self, effect, pub=PubEnum.PROPERTY):
#         self.effect = effect
#         self.pub = pub
#
#     def __enter__(self):
#         global g_active_effect
#         global g_pub
#         g_active_effect = self.effect
#         g_pub = self.pub
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         global g_active_effect
#         global g_pub
#         g_active_effect = None
#         g_pub = None
#
#
# class Dep:
#     def __init__(self):
#         self.subs: List[WatcherBase] = []
#
#     def add_sub(self, sub):
#         if sub in self.subs:
#             return
#
#         self.subs.append(sub)
#
#     def reset_subs(self):
#         self.subs.clear()
#
#     def notify(self):
#         for sub in self.subs:
#             sub.update()
#
#
# class DepStoreField:
#     _deps: Dict[int, Dict[str, Dep]] = {}
#
#     def __init__(self):
#         pass
#
#     @classmethod
#     def reset(cls):
#         cls._deps = {}
#
#     def __get__(self, instance, owner):
#         instance_id = id(instance)
#         if instance_id not in self._deps:
#             self._deps[instance_id] = defaultdict(Dep)
#
#         return self._deps[instance_id]
#
#     def __set__(self, instance, new_value):
#         pass
#
#     def __delete__(self, instance):
#         instance_id = id(instance)
#         if instance_id in self._deps:
#             del self._deps[instance_id]
#
#
# class Reactive(metaclass=abc.ABCMeta):
#     _deps = DepStoreField()
#
#     @abc.abstractmethod
#     def add_dep(self, attr, sub):
#         pass
#
#     @abc.abstractmethod
#     def reset_deps(self):
#         pass
#
#
# class ReactiveDict(dict, Reactive):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#     def __getitem__(self, attr):
#         track(self, attr)
#         return super().__getitem__(attr)
#
#     def __setitem__(self, attr, value):
#         super().__setitem__(attr, value)
#         trigger(self, attr)
#
#     def __getattr__(self, attr):
#         return self.__getitem__(attr)
#
#     def __setattr__(self, attr, value):
#         self.__setitem__(attr, value)
#
#     def __delete__(self, instance):
#         del self._deps
#
#     def add_dep(self, attr, sub):
#         self._deps[attr].add_sub(sub)
#
#     def reset_deps(self):
#         for k, v in self.items():
#             clear_subscribers_for_property(self, k, PubEnum.PROPERTY)
#             if isinstance(v, Reactive):
#                 v.reset_deps()
#
#
# class ReactiveList(list, Reactive):
#     _SUB_KEY = '__reactive_list_sub_key'
#
#     def append(self, __object) -> None:
#         super().append(__object)
#         trigger(self, self._SUB_KEY)
#
#     def extend(self, __iterable) -> None:
#         super().extend(__iterable)
#         trigger(self, self._SUB_KEY)
#
#     def insert(self, __index: SupportsIndex, __object) -> None:
#         super().insert(__index, __object)
#         trigger(self, self._SUB_KEY)
#
#     def __setitem__(self, key, value):
#         super().__setitem__(key, value)
#         trigger(self, self._SUB_KEY)
#
#     def sort(self, *, key: None = ..., reverse: bool = ...) -> None:
#         super().sort(key=key, reverse=reverse)
#         trigger(self, self._SUB_KEY)
#
#     def reverse(self) -> None:
#         super().reverse()
#         trigger(self, self._SUB_KEY)
#
#     def pop(self, __index: SupportsIndex = ...):
#         ret = super().pop(__index)
#         trigger(self, self._SUB_KEY)
#         return ret
#
#     def remove(self, __value) -> None:
#         super().remove(__value)
#         trigger(self, self._SUB_KEY)
#
#     def __delete__(self, instance):
#         del self._deps
#
#     def add_dep(self, sub):
#         add_subscribers_for_property(self, self._SUB_KEY, sub)
#
#     def reset_deps(self):
#         clear_subscribers_for_property(self, self._SUB_KEY, PubEnum.PROPERTY)
#         for item in self:
#             if isinstance(item, Reactive):
#                 item.reset_deps()
#
#
# def observe(data):
#     if isinstance(data, Reactive):
#         data.reset_deps()
#
#     if isinstance(data, dict):
#         for attr, item in data.items():
#             data[attr] = observe(item)
#         if not isinstance(data, Reactive):
#             data = ReactiveDict(data)
#
#     elif isinstance(data, list):
#         for i, item in enumerate(data):
#             data[i] = observe(item)
#         if not isinstance(data, Reactive):
#             data = ReactiveList(data)
#
#     return data


# class VueRef(Reactive):
#     _SUB_KEY = '__ref_sub_key'
#
#     def __init__(self, value):
#         super().__init__()
#         self._value = value
#
#     @property
#     def value(self):
#         track(self, self._SUB_KEY)
#         return self._value
#
#     @value.setter
#     def value(self, new_value):
#         self._value = new_value
#         trigger(self, self._SUB_KEY)
#
#     def add_dep(self, sub):
#         add_subscribers_for_property(self, self._SUB_KEY, sub)
#
#     def reset_deps(self):
#         clear_subscribers_for_property(self, self._SUB_KEY, PubEnum.PROPERTY)
#         if isinstance(self._value, Reactive):
#             self._value.reset_deps()


# def ref(value):
#     return VueRef(value)
#
#
# def reactive(obj):
#     return observe(obj)


# def computed(func, setter=None):
#     val_ref = ref(None)
#     watcher = WatcherForComputed(val_ref, func)
#     with ActivateEffect(watcher, PubEnum.SETUP):
#         val_ref.value = func()
#     return val_ref


# def watch(source, callback, options=None):
#     def _watch_reactive_obj(data: Reactive, source, callback):
#         if isinstance(data, dict):
#             for attr, item in data.items():
#                 _watch_reactive_obj(item, source, callback)
#
#         elif isinstance(data, list):
#             for i, item in enumerate(data):
#                 _watch_reactive_obj(item, source, callback)
#
#     options = options or {}
#     watcher = WatcherForWatchFunc(source, callback, options)
#     with ActivateEffect(watcher, PubEnum.SETUP):
#         if isinstance(source, VueRef):
#             _ = source.value
#         elif isinstance(source, Reactive):
#             _watch_reactive_obj(source, source, callback)
#         elif callable(source):
#             deep = options.get('deep', True)
#             _ = source()
#
#
# class WatcherForRerender(WatcherBase):
#     def __init__(self, vm, name):
#         self.vm = vm
#         self.name = name
#
#     def update(self):
#         self.vm.render()
#
#
# class WatcherForComputed(WatcherBase):
#     def __init__(self, source, func, options=None):
#         self.source = source
#         self.func = func
#         self.value = self.get_val()
#
#     def get_val(self):
#         return self.func()
#
#     def update(self):
#         old_val = self.value
#         new_val = self.get_val()
#         try:
#             if new_val == self.value:
#                 return
#         except Exception as e:
#             pass
#
#         self.value = new_val
#         self.source.value = new_val


# class WatcherForWatchFunc(WatcherBase):
#     def __init__(self, source, callback, options=None):
#         self.source = source
#         self.callback = callback
#         self.value = self.get_val()
#
#     def get_val(self):
#         if isinstance(self.source, VueRef):
#             return self.source.value
#         else:
#             return self.source
#
#     def update(self):
#         old_val = self.value
#         new_val = self.get_val()
#         try:
#             if new_val == self.value:
#                 return
#         except Exception as e:
#             pass
#
#         self.value = new_val
#         self.callback(new_val, old_val)
#
#
# class WatcherForAttrUpdate(WatcherBase):
#     def __init__(self, ns: "VueCompNamespace", val_expr_or_fn, callback, options=None):
#         self.callback = callback
#         self.val_expr_or_fn = val_expr_or_fn
#         self.ns = ns
#         self.value = self.get_val()
#
#     def get_val(self):
#         if callable(self.val_expr_or_fn):
#             return self.val_expr_or_fn()
#         else:
#             return self.val_expr_or_fn.eval(self.ns)
#
#     def update(self):
#         new_val = self.get_val()
#         old_val = self.value
#         try:
#             if new_val == old_val:
#                 return
#         except Exception as e:
#             pass
#
#         self.value = new_val
#         self.callback(new_val, old_val)


# class VForStatement:
#     def __init__(self, target, iters, index=None):
#         self.i = index
#         self.target = target
#         self.iter = iters
#
#     @classmethod
#     def parse(cls, s):
#         """
#         (i, target) in iter
#         :param s:
#         :return:
#         """
#         i_target, iters = [i.strip() for i in s.split(' in ')]
#         i_target = [i.strip() for i in i_target.strip('()').split(',')]
#         if len(i_target) == 1:
#             i, target = None, i_target[0]
#         else:
#             i, target = i_target[0], i_target[1]
#
#         return cls(target.strip(), iters, i)
#
#
# class ForScope:
#     def __init__(self, i_val, for_stmt: VForStatement, vm: 'VueComponent'):
#         self.for_stmt = for_stmt
#         self.i = i_val
#         self.iter = VueCompNamespace.get_by_attr_chain(vm._data, for_stmt.iter)
#         self.target = self.iter[self.i]
#
#     def to_ns(self):
#         return {
#             self.for_stmt.i: self.i,
#             self.for_stmt.target: self.target,
#             self.for_stmt.iter: self.iter,
#         }


# def vue_comp_expr_parse(expr_str):
#     # _ast = VueCompExprParser.parse(expr_str)
#     # transformer = VueCompExprTransformer()
#     # comp_expr_ast = transformer.transformer(_ast)
#     # comp_expr_ast.exp_str = expr_str
#     # return comp_expr_ast
#     return VueCompExprAst.parse(expr_str)


# def vue_comp_expr_compile(expr_ast: VueCompExprAst):
#     return compile(expr_ast.exp_ast, "<string>", "eval")
#
#
# def vue_comp_expr_eval(expr_ast: VueCompExprAst, ns: "VueCompNamespace", local_vars=None):
#     code_obj = expr_ast if isinstance(expr_ast, types.CodeType) else vue_comp_expr_compile(expr_ast)
#     return eval(code_obj, {"__builtin__": None}, ns.to_py_eval_ns(local_vars))




#
# def create_vnode(component: VueComponent, props):
#     """
#     https://cn.vuejs.org/guide/extras/render-function.html#render-function-recipes
#     h函数实际就是接受了一个component的ast表示
#     h(tag, props | attrs, children) => vnode
#
#     :param component:
#     :param props:
#     :return:
#     """
#     pass
#
#
# def create_element_vnode(tag, props):
#     pass
#
#
# def create_element_block():
#     pass
#
#
# def render_slot():
#     pass



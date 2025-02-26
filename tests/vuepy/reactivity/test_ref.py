from copy import deepcopy
from unittest import TestCase

from vuepy.reactivity.computed import computed
from vuepy.reactivity.effect import IgnoreTracking
from vuepy.reactivity.effect import ReactiveEffectOptions
from vuepy.reactivity.effect import effect
from vuepy.reactivity.effect import targetMap
from vuepy.reactivity.reactive import reactive
from vuepy.reactivity.reactive import reactiveMap
from vuepy.reactivity.ref import ref
from vuepy.reactivity.ref import shallowRef
from vuepy.reactivity.ref import triggerRef
from vuepy.reactivity.watch import WatchOptions
from vuepy.reactivity.watch import watch
from vuepy.reactivity.watch import watchEffect


class BaseTestCase(TestCase):
    def setUp(self) -> None:
        def onTrack(info):
            with IgnoreTracking():
                print(f"track: {info}")

        def onTrigger(info):
            with IgnoreTracking():
                print(f"trigger: {info}")

        self.reactive_effect_options = ReactiveEffectOptions(onTrack=onTrack, onTrigger=onTrigger)

    def tearDown(self) -> None:
        targetMap.clear()
        reactiveMap.clear()


class TestRef(BaseTestCase):
    def test_ref_should_be_reactive(self):
        a = ref(1)
        dummy = 0
        calls = 0

        @effect
        def f():
            nonlocal dummy, calls
            calls += 1
            dummy = a.value

        self.assertEqual(calls, 1)
        self.assertEqual(dummy, 1)

        a.value = 2
        self.assertEqual(calls, 2)
        self.assertEqual(dummy, 2)
        # same value should not trigger
        a.value = 2
        self.assertEqual(calls, 2)
        self.assertEqual(dummy, 2)

    def test_ref_should_be_reactive_when_value_dict(self):
        raw = {
            'l1': 10,
            'l2': 20,
        }
        a = ref(raw)
        dummy = 0
        calls = 0

        @effect
        def f():
            nonlocal dummy, calls
            calls += 1
            dummy = a.value.l1

        self.assertEqual(calls, 1)
        self.assertEqual(dummy, 10)

        a.value.l1 = 100
        self.assertEqual(calls, 2)
        self.assertEqual(dummy, 100)
        # same value should not trigger
        a.value.l1 = 100
        self.assertEqual(calls, 2)
        self.assertEqual(dummy, 100)

        a.value.l2 = 200
        self.assertEqual(calls, 2)
        self.assertEqual(dummy, 100)


class TestShallowRef(BaseTestCase):
    def test_shallow_ref_should_be_reactive(self):
        a = shallowRef(1)
        dummy = 0
        calls = 0

        @effect
        def f():
            nonlocal dummy, calls
            calls += 1
            dummy = a.value

        self.assertEqual(calls, 1)
        self.assertEqual(dummy, 1)

        a.value = 2
        self.assertEqual(calls, 2)
        self.assertEqual(dummy, 2)
        # same value should not trigger
        a.value = 2
        self.assertEqual(calls, 2)
        self.assertEqual(dummy, 2)

    def test_shallow_ref_should_not_reactive_when_value_dict(self):
        raw = {'count': 10}
        a = shallowRef(raw)
        dummy = 0
        calls = 0

        @effect
        def f():
            nonlocal dummy, calls
            calls += 1
            dummy = a.value['count']

        self.assertEqual(calls, 1)
        self.assertEqual(dummy, 10)

        # trigger
        a.value = {'count': 20}
        self.assertEqual(calls, 2)
        self.assertEqual(dummy, 20)

        # not trigger
        a.value['count'] = 100
        self.assertEqual(calls, 2)
        self.assertEqual(dummy, 20)

    def test_shallow_ref_should_reactive_when_active_trigger(self):
        shallow = shallowRef({'greet': 10})
        dummy = 0
        calls = 0

        @watchEffect
        def f(on_cleanup):
            nonlocal dummy, calls
            calls += 1
            dummy = shallow.value['greet']

        self.assertEqual(calls, 1)
        self.assertEqual(dummy, 10)

        # not trigger
        shallow.value['greet'] = 100
        self.assertEqual(calls, 1)
        self.assertEqual(dummy, 10)

        # active trigger
        triggerRef(shallow)
        self.assertEqual(calls, 2)
        self.assertEqual(dummy, 100)


class TestReactive(BaseTestCase):
    def test_reactive_dict_should_reactive_when_set(self):
        a = reactive({'count': 1})
        dummy = 0
        calls = 0

        @effect
        def f():
            nonlocal dummy, calls
            calls += 1
            dummy = a.count

        self.assertEqual(calls, 1)
        self.assertEqual(dummy, 1)

        a.count = 2
        self.assertEqual(calls, 2)
        self.assertEqual(dummy, 2)
        # same value should not trigger
        a.count = 2
        self.assertEqual(calls, 2)
        self.assertEqual(dummy, 2)

    def test_reactive_dict_should_reactive_when_deep_update(self):
        a = reactive({
            'count': 1,
            'l1': {
                'l2a': 1,
                'l2b': 2,
            }
        })
        dummy = 0
        l1_l2a_calls = 0
        l1_l2b_calls = 0

        @effect(self.reactive_effect_options)
        def effect_a_l1_l2a():
            nonlocal dummy, l1_l2a_calls
            l1_l2a_calls += 1
            dummy = a.l1.l2a

        @effect(self.reactive_effect_options)
        def effect_a_l1_l2b():
            nonlocal dummy, l1_l2b_calls
            l1_l2b_calls += 1
            dummy = a.l1.l2b

        self.assertEqual(l1_l2a_calls, 1)
        self.assertEqual(l1_l2b_calls, 1)
        self.assertEqual(dummy, a.l1.l2b)

        value = 2
        print(f"1.1 set a.l1.l2a = {value}")
        a.l1.l2a = value
        self.assertEqual(l1_l2a_calls, 2)
        self.assertEqual(l1_l2b_calls, 1)
        self.assertEqual(dummy, value)
        # same value should not trigger
        print(f"1.2 set a.l1.l2a = {value}")
        a.l1.l2a = value
        self.assertEqual(l1_l2a_calls, 2)
        self.assertEqual(l1_l2b_calls, 1)
        self.assertEqual(dummy, value)
        value = 3
        print(f"1.3 set a.l1.l2a = {value}")
        a.l1.l2a = value
        self.assertEqual(l1_l2a_calls, 3)
        self.assertEqual(l1_l2b_calls, 1)
        self.assertEqual(dummy, value)

        value = 3
        print(f"2.1 set a.l1.l2b = {value}")
        a.l1.l2b = value
        self.assertEqual(l1_l2a_calls, 3)
        self.assertEqual(l1_l2b_calls, 2)
        self.assertEqual(dummy, value)
        # same value should not trigger
        print(f"2.2 set a.l1.l2b = {value}")
        a.l1.l2b = value
        self.assertEqual(l1_l2a_calls, 3)
        self.assertEqual(l1_l2b_calls, 2)
        self.assertEqual(dummy, value)

        value = {
            'l2a': 10,
            'l2b': 20,
        }
        print(f"3.1 set a.l1 = {value}")
        a.l1 = value
        self.assertEqual(l1_l2a_calls, 4)
        self.assertEqual(l1_l2b_calls, 3)

    def test_reactive_dict_should_still_reactive_when_parent_reset(self):
        a = reactive({
            'count': 1,
            'l1': {
                'l2a': 1,
                'l2b': 2,
            }
        })
        dummy = 0
        l1_l2a_calls = 0

        @effect(self.reactive_effect_options)
        def effect_a_l1_l2a():
            nonlocal dummy, l1_l2a_calls
            l1_l2a_calls += 1
            dummy = a.l1.l2a

        self.assertEqual(l1_l2a_calls, 1)

        value = 2
        print(f"1.1 set a.l1.l2a = {value}")
        a.l1.l2a = value
        self.assertEqual(l1_l2a_calls, 2)
        self.assertEqual(dummy, value)

        # reset l2a parent
        a_l1_l1a = 10
        value = {
            'l2a': a_l1_l1a,
            'l2b': 20,
        }
        print(f"2.1 set a.l1 = {value}")
        a.l1 = value
        self.assertEqual(l1_l2a_calls, 3)
        self.assertEqual(a.l1.l2a, a_l1_l1a)
        self.assertEqual(dummy, 10)
        self.assertEqual(targetMap.len(), 2)  # l1, l2a
        self.assertEqual(reactiveMap.len(), 2)  # l1, l2a

        value = 20
        print(f"3.1 set a.l1.l2a = {value}")
        a.l1.l2a = value
        self.assertEqual(l1_l2a_calls, 4)
        self.assertEqual(dummy, value)

    def test_reactive_list_should_reactive_when_item_dict(self):
        gt = [
            {'l1': 10},
            {'l2': 100},
        ]
        a = reactive(deepcopy(gt))
        dummy = 0
        calls = 0

        @effect
        def f():
            nonlocal dummy, calls
            calls += 1
            dummy = a[0].l1

        self.assertEqual(calls, 1)
        self.assertEqual(dummy, 10)

        gt[0]['l1'] = 20
        a[0].l1 = 20
        self.assertListEqual(a._vp_target_, gt)
        self.assertEqual(calls, 2)
        self.assertEqual(dummy, 20)

        # same value should not trigger
        gt[0]['l1'] = 20
        a[0].l1 = 20
        self.assertListEqual(a._vp_target_, gt)
        self.assertEqual(calls, 2)
        self.assertEqual(dummy, 20)

        gt[1]['l2'] = 3
        a[1].l2 = 3
        self.assertListEqual(a._vp_target_, gt)
        self.assertEqual(calls, 2)
        self.assertEqual(dummy, 20)

    def test_reactive_list_should_reactive_when_setitem(self):
        gt = [1, 2, 3, 4]
        a = reactive([*gt])
        dummy = 0
        calls = 0

        @effect
        def f():
            nonlocal dummy, calls
            calls += 1
            dummy = a[0]

        self.assertEqual(calls, 1)
        self.assertEqual(dummy, 1)

        a[0] = 2
        gt[0] = 2
        self.assertListEqual(a._vp_target_, gt)
        self.assertEqual(calls, 2)
        self.assertEqual(dummy, 2)

        # same value should not trigger
        a[0] = 2
        gt[0] = 2
        self.assertListEqual(a._vp_target_, gt)
        self.assertEqual(calls, 2)
        self.assertEqual(dummy, 2)

        # negative index
        a[-1] = 3
        gt[-1] = 3
        self.assertListEqual(a._vp_target_, gt)
        self.assertEqual(calls, 3)
        self.assertEqual(dummy, 2)

        # slice index
        a[1:3] = [0, 1]
        gt[1:3] = [0, 1]
        self.assertListEqual(a._vp_target_, gt)
        self.assertEqual(calls, 4)
        self.assertEqual(dummy, 2)

    def test_reactive_list_should_reactive_when_append(self):
        gt = [2, 1]
        a = reactive(deepcopy(gt))
        dummy = 0
        calls = 0

        @effect(self.reactive_effect_options)
        def f():
            nonlocal dummy, calls
            calls += 1
            dummy = a[-1]

        self.assertEqual(calls, 1)
        self.assertEqual(dummy, 1)

        gt.append(2)
        a.append(2)
        self.assertListEqual(a._vp_target_, gt)
        self.assertEqual(calls, 2)
        self.assertEqual(dummy, 2)

    def test_reactive_list_should_reactive_when_slice_index(self):
        gt = [1, 2, 3, 4]
        a = reactive(deepcopy(gt))
        dummy = 0
        calls = 0
        index = slice(1, 1+2)

        @effect(self.reactive_effect_options)
        def f():
            nonlocal dummy, calls
            calls += 1
            # slice index
            dummy = a[index]

        self.assertEqual(calls, 1)
        self.assertListEqual(list(dummy), gt[index])

        gt.append(2)
        a.append(2)
        self.assertListEqual(a._vp_target_, gt)
        self.assertEqual(calls, 2)
        self.assertListEqual(list(dummy), gt[index])


class TestComputed(BaseTestCase):
    def test_computed_should_reactive_when_src_is_ref(self):
        count = ref(1)
        count_b = ref(2)

        @computed
        def plus_one():
            return count.value + 1

        @computed
        def plus_two():
            return count.value + count_b.value

        self.assertEqual(plus_one.value, 2)
        self.assertEqual(plus_two.value, 3)

        count.value = 2
        self.assertEqual(plus_one.value, 3)
        self.assertEqual(plus_two.value, 4)

        count_b.value = 3
        self.assertEqual(plus_one.value, 3)
        self.assertEqual(plus_two.value, 5)

    def test_computed_should_reactive_when_src_is_reactive(self):
        count = reactive({'count': 1})
        count_b = reactive({'count': 2})

        @computed
        def plus_one():
            return count.count + 1

        @computed
        def plus_two():
            return count.count + count_b.count

        self.assertEqual(plus_one.value, 2)
        self.assertEqual(plus_two.value, 3)

        count.count = 2
        self.assertEqual(plus_one.value, 3)
        self.assertEqual(plus_two.value, 4)

        count_b.count = 3
        self.assertEqual(plus_one.value, 3)
        self.assertEqual(plus_two.value, 5)

    def test_computed_should_reactive_when_src_is_ref_and_reactive(self):
        author = reactive({
            'name': 'aa',
            'books': [],
        })
        published_call = 0
        name_call = 0

        @computed
        def published():
            nonlocal published_call
            published_call += 1
            return 'Yes' if len(author.books) > 0 else 'No'

        self.assertEqual(published.value, 'No')
        self.assertEqual(published_call, 1)

        author.books.append('book1')
        self.assertEqual(published.value, 'Yes')
        self.assertEqual(published_call, 2)

        @computed
        def author_name():
            nonlocal name_call
            name_call += 1
            return author.name

        self.assertEqual(name_call, 0)

        author.name = 'bb'
        self.assertEqual(author_name.value, 'bb')
        self.assertEqual(name_call, 1)


class TestWatch(BaseTestCase):
    def test_watch_effect_should_reactive_when_change(self):
        a = reactive({'count': 1})
        dummy = 0
        calls = 0

        @watchEffect
        def f(on_cleanup):
            nonlocal dummy, calls
            calls += 1
            dummy = a.count

        self.assertEqual(calls, 1)
        self.assertEqual(dummy, 1)

        a.count = 2
        self.assertEqual(calls, 2)
        self.assertEqual(dummy, 2)
        # same value should not trigger
        a.count = 2
        self.assertEqual(calls, 2)
        self.assertEqual(dummy, 2)

    def test_watch_effect_should_cleanup_when_change(self):
        a = reactive({'count': 1})
        dummy = 0
        calls = 0
        cleanup_call = 0

        def cleanup():
            nonlocal cleanup_call
            cleanup_call += 1

        @watchEffect
        def f(on_cleanup):
            nonlocal dummy, calls
            calls += 1
            dummy = a.count
            on_cleanup(cleanup)

        self.assertEqual(calls, 1)
        self.assertEqual(dummy, 1)
        self.assertEqual(cleanup_call, 0)

        a.count = 2
        self.assertEqual(calls, 2)
        self.assertEqual(dummy, 2)
        self.assertEqual(cleanup_call, 1)
        # same value should not trigger
        a.count = 2
        self.assertEqual(calls, 2)
        self.assertEqual(dummy, 2)
        self.assertEqual(cleanup_call, 1)

    def test_watch_effect_should_stop_when_stop_watch(self):
        a = reactive({'count': 1})
        dummy = 0
        calls = 0

        @watchEffect
        def f(on_cleanup):
            nonlocal dummy, calls
            calls += 1
            dummy = a.count

        stop = f

        self.assertEqual(calls, 1)
        self.assertEqual(dummy, 1)

        stop()
        a.count = 2
        self.assertEqual(calls, 1)
        self.assertEqual(dummy, 1)

    def test_watch_should_reactive_when_src_is_ref(self):
        count = ref(1)

        curr_count = 0
        prev_count = 0
        watch_call = 0

        @watch(count)
        def watch_state_handle_with_stop(curr, old, on_cleanup):
            nonlocal watch_call, curr_count, prev_count
            watch_call += 1
            curr_count = curr
            prev_count = old

        self.assertEqual((watch_call, curr_count, prev_count), (0, 0, 0))

        count.value = 2
        self.assertEqual((watch_call, curr_count, prev_count), (1, 2, 1))

    def test_watch_should_reactive_when_src_is_computed_ref(self):
        count = ref(1)

        computed_call = 0

        @computed
        def computed_count():
            nonlocal computed_call
            computed_call += 1
            return count.value + 1

        self.assertEqual(computed_call, 0)

        curr_count = 0
        prev_count = 0
        watch_call = 0

        @watch(computed_count)
        def watch_state_handle_with_stop(curr, old, on_cleanup):
            nonlocal watch_call, curr_count, prev_count
            watch_call += 1
            curr_count = curr
            prev_count = old

        self.assertEqual((watch_call, computed_call, curr_count, prev_count), (0, 1, 0, 0))

        count.value = 2
        self.assertEqual((watch_call, computed_call, curr_count, prev_count), (1, 2, 3, 2))

    def test_watch_should_reactive_when_src_is_getter_function(self):
        state = reactive({
            'count': 0,
            'l1': {'l2a': 1},
        })

        curr_count = 0
        prev_count = 0
        watch_call = 0
        getter_call = 0

        def getter():
            nonlocal getter_call
            getter_call += 1
            return state.count

        # default deep = False
        @watch(getter)
        def watch_state_handle_with_stop(curr, old, on_cleanup):
            nonlocal watch_call, curr_count, prev_count
            watch_call += 1
            curr_count = curr
            prev_count = old

        self.assertEqual((watch_call, getter_call, curr_count, prev_count), (0, 1, 0, 0))

        state.count = 2
        self.assertEqual((watch_call, getter_call, curr_count, prev_count), (1, 2, 2, 0))

    def test_watch_should_reactive_when_src_is_getter_function_deep(self):
        # todo deep = true
        state = reactive({'count': 0})

        @watch(state, WatchOptions(deep=True))
        def handle(new_val, old_val, on_cleanup):
            self.assertTrue(new_val is old_val)

    def test_watch_should_reactive_when_src_is_list(self):
        a_ref = ref(1)
        b_ref = ref(2)
        curr = [a_ref.value, b_ref.value]
        watch_call = 0

        @watch([a_ref, b_ref])
        def handle(_curr, _, __):
            nonlocal watch_call, curr
            watch_call += 1
            curr = _curr

        self.assertEqual((watch_call, curr), (0, [1, 2]))

        a_ref.value = 2
        self.assertEqual((watch_call, curr), (1, [2, 2]))
        b_ref.value = 3
        self.assertEqual((watch_call, curr), (2, [2, 3]))
        a_ref.value = 2
        self.assertEqual((watch_call, curr), (2, [2, 3]))

    def test_watch_should_reactive_when_src_is_reactive(self):
        state = reactive({
            'count': 0,
            'l1': {'l2a': 1},
        })

        curr = 0
        watch_call = 0

        @watch(state)
        def watch_state_handle_with_stop(_curr, _, on_cleanup):
            nonlocal watch_call, curr
            watch_call += 1
            curr = _curr

        self.assertEqual((watch_call, curr), (0, 0))

        state.count = 2
        self.assertEqual((watch_call, curr.count), (1, 2))
        state.count = 2
        self.assertEqual((watch_call, curr.count), (1, 2))

        # deep
        state.l1.l2a = 2
        self.assertEqual((watch_call, curr.count), (2, 2))
        self.assertEqual((watch_call, curr.l1.l2a), (2, 2))

    def test_watch_should_stop_when_stop_watch(self):
        source = reactive({'count': 1})
        dummy = 0
        calls = 0

        @watch(source)
        def watch_source(_, __, ___):
            nonlocal dummy, calls
            calls += 1
            dummy = source.count

        stop_handle = watch_source

        self.assertEqual(calls, 0)
        self.assertEqual(dummy, 0)

        stop_handle()
        source.count = 2
        self.assertEqual(calls, 0)
        self.assertEqual(dummy, 0)

    def test_watch_should_cleanup_when_change(self):
        source = reactive({'count': 1})
        dummy = 0
        calls = 0
        cleanup_call = 0

        def cleanup():
            nonlocal cleanup_call
            cleanup_call += 1

        @watch(source)
        def f(_, __, on_cleanup):
            nonlocal dummy, calls
            calls += 1
            dummy = source.count
            on_cleanup(cleanup)

        self.assertEqual((calls, dummy, cleanup_call), (0, 0, 0))

        source.count = 2
        self.assertEqual((calls, dummy, cleanup_call), (1, 2, 0))

        source.count = 3
        self.assertEqual((calls, dummy, cleanup_call), (2, 3, 1))
        # same value should not trigger
        source.count = 3
        self.assertEqual((calls, dummy, cleanup_call), (2, 3, 1))


class TestEffect(BaseTestCase):
    def test_effect_should_trigger_when_effect_deps_change(self):
        switch = ref(True)
        count_true = ref(0)
        count_false = ref(0)

        @effect
        def f():
            if switch.value:
                count_true.value += 1
            else:
                count_false.value += 1

        self.assertEqual(count_true.value, 1)
        self.assertEqual(count_false.value, 0)

        switch.value = False
        self.assertEqual(count_true.value, 1)
        self.assertEqual(count_false.value, 1)

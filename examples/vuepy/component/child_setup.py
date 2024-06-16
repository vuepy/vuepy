from vuepy.runtime.core.api_setup_helpers import defineEmits
from vuepy.runtime.core.api_setup_helpers import defineModel
from vuepy.runtime.core.api_setup_helpers import defineProps
from vuepy import ref


def setup(props, ctx, app):
    emit = defineEmits(['submit'])
    props = defineProps(['dynamic', 'static'])
    model = defineModel('modela')
    model.value = 'model_default'

    print(f"props.dynamic is {props.dynamic.value}")
    print(f"props.static is {props.static.value}")

    text = ref('hello')

    def submit(ev):
        print(ev)
        emit('submit', 1, 2, 3)
    return locals()
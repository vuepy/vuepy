from vuepy import defineEmits
from vuepy import defineModel
from vuepy import defineProps
from vuepy import ref


def setup(props, ctx, app):
    emit = defineEmits(['submit'])
    props = defineProps(['dynamic', 'static'])
    model = defineModel('modela')
    model.value = 'dfasdf'

    text = ref('hello')

    def submit():
        emit('submit', '')

    return locals()

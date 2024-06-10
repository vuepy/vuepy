import enum


class LifecycleHooks(enum.Enum):
    BEFORE_CREATE = 'bc'
    CREATED = 'c'
    BEFORE_MOUNT = 'bm'
    MOUNTED = 'm'
    BEFORE_UPDATE = 'bu'
    UPDATED = 'u'
    BEFORE_UNMOUNT = 'bum'
    UNMOUNTED = 'um'
    DEACTIVATED = 'da'
    ACTIVATED = 'a'
    RENDER_TRIGGERED = 'rtg'
    RENDER_TRACKED = 'rtc'
    ERROR_CAPTURED = 'ec'
    SERVER_PREFETCH = 'sp'


class Hook:
    pass


class OnMounted:
    def __init__(self, callback):
        self.callback = callback


class OnBeforeMount:
    def __init__(self, callback):
        self.callback = callback


class OnUnmounted:
    def __init__(self, callback):
        self.callback = callback


class OnBeforeUnmount:
    def __init__(self, callback):
        self.callback = callback


def onMounted(callback):
    return OnMounted(callback)


def onBeforeMount(callback):
    return OnBeforeMount(callback)


def onUnmounted(callback):
    return OnUnmounted(callback)


def onBeforeUnmount(callback):
    return OnBeforeUnmount(callback)

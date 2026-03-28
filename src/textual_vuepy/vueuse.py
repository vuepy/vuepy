from textual.events import MouseEvent
from vuepy import ref
from vuepy.runtime.core.api_lifecycle import _get_active_setup_context, onMounted


def onKeyStroke(key, cb):
    app = _get_active_setup_context().app

    @onMounted
    def setup_key_store():
        app.tt_app.vp_register_on_keyup(key, cb)


def useMouse():
    """
    Returns:
        tuple[Ref[int], Ref[int]]: The x and y coordinates of the mouse relative to the screen.
    """
    x = ref(0)
    y = ref(0)

    def update_xy(ev: MouseEvent):
        x.value = ev.screen_x
        y.value = ev.screen_y

    app = _get_active_setup_context().app

    @onMounted
    def setup_mouse():
        app.tt_app.vp_register_on('mouse_move', update_xy)

    return x, y

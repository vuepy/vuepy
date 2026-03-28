import pathlib
from textual.color import Color

from textual.app import App
from vuepy import create_app, import_sfc


def create_rgb_vue_app():
    RGBVueApp = import_sfc(pathlib.Path(__file__).parent / "test_onKeyStroke.vue")
    vue_app = create_app(RGBVueApp, backend="textual")
    # vue_app.provide(TextualProvides.APP_MIXIN, RGBAppMixin)
    vue_app.mount(run=False)
    return vue_app.tt_app


class RGBVueApp(App):
    def __new__(cls, *args, **kwargs):
        return create_rgb_vue_app()


async def test_rgb_vue_keys():
    app = create_rgb_vue_app()

    async with app.run_test() as pilot:
        await pilot.press("r")
        assert app.screen.styles.background == Color.parse("red")

        await pilot.press("g")
        assert app.screen.styles.background == Color.parse("green")

        await pilot.press("b")
        assert app.screen.styles.background == Color.parse("blue")


async def test_rgb_vue_buttons():
    app = create_rgb_vue_app()
    async with app.run_test() as pilot:
        await pilot.click("#red")
        assert app.screen.styles.background == Color.parse("red")
        await pilot.click("#green")
        assert app.screen.styles.background == Color.parse("green")
        await pilot.click("#blue")
        assert app.screen.styles.background == Color.parse("blue")


def test_rgb_vue_snapshot(snap_compare):
    # https://textual.textualize.io/api/pilot/#textual.pilot
    async def run_before(pilot):
        await pilot.press("r")

    # assert snap_compare('./test_example.py:RGBVueApp', run_before=run_before)
    assert snap_compare('./test_onKeyStroke.py', run_before=run_before)


if __name__ == "__main__":
    '''
    For testing:
    pip install pytest-asyncio
    pip install pytest-textual-snapshot
    pytest --asyncio-mode=auto test_onKeyStroke.py -v
    To update snapshots:
    pytest --snapshot-update
    '''
    app = create_rgb_vue_app()
    app.run()

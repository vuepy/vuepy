from textual.app import App, ComposeResult, RenderResult
from textual.containers import VerticalScroll
from textual.reactive import reactive
from textual.widgets import Footer, Static, Label


class Counter(Static, can_focus=True):  
    """A counter that can be incremented and decremented by pressing keys."""

    count = reactive(0)

    def render(self) -> RenderResult:
        return f"Count: {self.count}"

class Child(VerticalScroll):
    DEFAULT_CSS = '''
    #v1 {
        background: blue;
    }
    Label {
        background: blue;
    }
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.DEFAULT_CSS = self.CSS
    
    def compose(self) -> ComposeResult:
        yield Label("from child 1 (blue)", id='lbl1')

class Child2(VerticalScroll):
    DEFAULT_CSS = '''
    #v2scroll {
        background: red;
        Label {
            background: red;
        }
    }
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.DEFAULT_CSS = self.CSS
    
    def compose(self) -> ComposeResult:
        with VerticalScroll(id='v2scroll'):
            yield Label("from child 2 (red)", id='v2')
            yield Child()


class CounterApp(App[None]):
    # CSS_PATH = "counter.tcss"
    CSS = '''
Label {
    # background: gray;
    }
Counter {
    background: $panel-darken-1;
    padding: 1 2;
    color: $text-muted;

    &:focus {  
        background: $primary;
        color: $text;
        text-style: bold;
        outline-left: thick $accent;
    }
}'''

    def compose(self) -> ComposeResult:
        yield Child()
        yield Child2()
        yield Label("from app (gray)!")
        yield Counter(id='c1')
        yield Counter()
        yield Counter()
        yield Footer()


if __name__ == "__main__":
    app = CounterApp()
    app.run()
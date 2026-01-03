from textual.screen import Screen
from textual.app import App, ComposeResult
from textual.widgets import Button, Label, Input, Checkbox, ListView, ListItem, Placeholder, Footer
from textual.containers import Horizontal, VerticalScroll, Vertical, Grid


class DashboardScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Placeholder("Dashboard Screen")
        yield Footer()

class LApp(App):
    BINDINGS = [
        ("d", "switch_mode('dashboard')", "Dashboard"),  
    ]
    MODES = {
        "dashboard": DashboardScreen,  
    }

    def compose(self) -> ComposeResult:
        # with Vertical():
        #     pass
        with VerticalScroll():
            with Vertical():
                yield Input(placeholder="计数器示例", id="counter_label")
                yield Button("增加", id="inc")
                yield Button("减少", id="dec")
                yield Button("重置", id="reset")
    
    def on_mount(self):
        # self.v.print_tree()
        self.switch_mode("dashboard")
        # self.debug()
        self.print_dom_tree()
        pass

    def _print_dom_tree(self, widget, indent=0, s=''):
        """递归打印DOM树结构"""
        indent_str = "  " * indent
        widget_id = f" (id={widget.id})" if widget.id else ""
        widget_classes = f" [classes={widget.classes}]" if widget.classes else ""

        s += f"{indent_str}{widget.__class__.__name__}{widget_id}{widget_classes}\n"

        for child in widget.children:
            s = self._print_dom_tree(child, indent + 1, s)

        return s

    def print_dom_tree(self, widget=None):
        """打印DOM树结构"""
        if widget is None:
            widget = self
        s = self._print_dom_tree(widget)
        print(s)

app = LApp()
app.run()

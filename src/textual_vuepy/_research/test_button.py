from textual.screen import Screen
from textual.app import App, ComposeResult
from textual.widgets import Button, Label, Input, Checkbox, ListView, ListItem
from textual.containers import Horizontal, VerticalScroll, Vertical


class ParamActionApp(App):
    def compose(self) -> ComposeResult:
        yield Input(placeholder="计数器示例", id="counter_label")
        yield Button("增加", id="inc", action="increment_counter")
        yield Button("减少", id="dec", action=self.decrement_counter)
        yield Button("重置", id="reset", action=self.reset_counter)
    
    def on_mount(self):
        self.counter = 0
        self.title = f"计数器: {self.counter}"
        self.update_title()
    
    def action_increment_counter(self):
        self.counter += 1
        self.update_title()
    
    def decrement_counter(self):
        self.counter -= 1
        self.update_title()
    
    def reset_counter(self):
        self.counter = 0
        self.update_title()
    
    def update_title(self):
        self.title = f"计数器: {self.counter}"
        self.query_one(Input).value = self.title

from textual.app import App, ComposeResult
from textual.widgets import Button
from textual import on

class ButtonApp(App):
    def compose(self) -> ComposeResult:
        yield Button("操作1", id="btn1")
        yield Button("操作2", id="btn2")
    
    @on(Button.Pressed, "#btn1")
    def handle_btn1(self) -> None:
        self.notify("按钮1被点击")
    
    @on(Button.Pressed, "#btn2")
    def handle_btn2(self) -> None:
        self.notify("按钮2被点击")


from textual.app import App, ComposeResult
from textual.widgets import Button


class Column(VerticalScroll):

    def append(self, widget):
        await_mount = self.mount(*[widget])
        return await_mount
    
    def prepend_child(self, widget):
        await_mount = self.mount(widget, before=self.children[0] if self.children else None)
        return await_mount
    
    def clear(self):
        await_remove = self.remove_children()
        return await_remove

    def replace_children(self, children):
        self.clear()
        await_mount = self.mount(*children)
        return await_mount

class I(Input):
    def on_input_changed(self, event: Input.Changed) -> None:
        self.notify(f"输入框内容改变为: {event.value}")

class EventButtonApp(App):
    def compose(self) -> ComposeResult:
        btn1 = Button("+", id="btn1")
        btn2 = Button("-", id="btn2")
        c = [btn1, btn2]
        # for btn in c:
        #     yield btn
        self.col = Column(*c)

        self.ck = Checkbox("c", id="chk1")
        # self.l = ListView(
        #     ListItem(ck),
        # )
        self.label = Label("test")
        self.l = Column(
            Label('1'),
            I(),
        )
        return [self.col, self.ck, self.l, self.label]
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        
        if button_id == "btn1":
            self.notify("1")
            self.ck.value = not self.ck.value
            self.l.prepend_child(Label("按钮1被点击"))
            self.label.update('label: 按钮1被点击')
            # self.label.content = 'label: 按钮1被点击'
        elif button_id == "btn2":
            self.notify("2")
            self.l.replace_children([Label("按钮2被点击")])
    
    def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
        checkbox_id = event.checkbox.id
        is_checked = event.value
        event.checkbox.value
        
        self.notify(f"{checkbox_id} 状态改变为: {'选中' if is_checked else '未选中'}")
    

# app = EventButtonApp()
class MyApp(App):
    def on_mount(self) -> None:
        # v = VerticalScroll()
        # b = Button('btn')
        # self.mount(v)
        # v.mount(b)
        c(self)

app = MyApp()
# app.push_screen(Screen())
# app.mount(Button('1'))

def c(app):
    b = Button('btn')
    v1 = VerticalScroll()
    app.mount(v1)
    v1.mount(b)

    v2 = Vertical(Button('btn21'))
    b1 = Button('btn2')
    # app.mount(v2)
    # v1.mount(v2)
    # v2.mount(b1)

    # v1.mount(b)
    return v1


app.run()
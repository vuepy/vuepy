import sys
import os
from textual.app import App, ComposeResult
from textual.widgets import Label, Log
from textual_vuepy.utils import fix_stdin

class PipeApp(App):
    def __init__(self, piped_data=None):
        super().__init__()
        self.piped_data = piped_data

    def compose(self) -> ComposeResult:
        yield Label("从管道接收的数据：")
        log = Log()
        yield log
        if self.piped_data:
            log.write(self.piped_data)
        else:
            log.write("无管道数据")



if __name__ == "__main__":
    # 在初始化 App 之前，必须先修复 stdin
    pipe_stdin = fix_stdin()

    # 现在 fd 0 已经是 TTY 了，Textual 会识别出这是一个交互式终端
    app = PipeApp(pipe_stdin=pipe_stdin.read())
    app.run()
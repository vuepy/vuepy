<template>
  <VBox>
    <Header :title="f'Cursor Agent({resume_id.value})'" />
    <VBox id="chat-container" style="height: 1fr; overflow-y: auto; padding: 1 2;" ref="chat_container_ref">
      <RichLog ref="chat_log" id="chat-log" markup />
    </VBox>
    {{ user_input.value }}
    <HBox id="input-area" style="height: auto; padding: 1 2;">
      <TextArea
        ref="input_ref"
        style="height: auto;"
        v-model="user_input.value"
        placeholder="输入消息发送。/ 命令补全，! 执行 shell，↑↓ 历史，Ctrl+b 发送"
        :disabled="is_loading.value"
        @text_area_changed="_check_slash_trigger"
        @submitted="send_message"
        @keyup.ctrl.b="send_message"
        @keyup.ctrl.up="history_up"
        @keyup.ctrl.down="history_down"
      />
      <Button label="发送" ref="send_btn_ref" @click="send_message" variant="primary" />
      <Button label="清空" @click="clear_chat" />
      <Button label="退出" @click="exit" variant="warning" />
      <Button label="自定义" style="background: rgb(128,0,128); border: block rgb(128,0,128);" />
    </HBox>
    <Footer />
    <Dialog v-model="show_slash_dialog.value" name="slash_cmd" style="width: 70; min-height: 25;"
            @open="on_slash_dialog_open"
            @keyup.escape="close_slash_dialog"
    >
      <VBox style="width: auto;">
        <FilterableOptionList
          :options="SLASH_COMMANDS"
          :filterable="True"
          :filter_method="slash_filter_method"
          :foce="True"
          input_placeholder="输入 / 后过滤命令…"
          @option_list_option_selected="on_slash_option_selected"
          ref="slash_option_list_ref"
        />
        <Button label="取消" @click="close_slash_dialog" />
      </VBox>
    </Dialog>
  </VBox>
</template>

<script lang="py">
from pathlib import Path

from vuepy import ref, watch, computed, onMounted, import_sfc
import os
import re
from rich.markdown import Markdown

FilterableOptionList = import_sfc(Path(__file__).parent / "FilterableOptionList.vue")

# 斜杠命令： (命令, 描述)
SLASH_COMMANDS = [
    ("/model <model>", "Set the current model"),
    ("/auto-run", "Toggle Run Everything"),
    ("/plan [prompt]", "Create a plan or show existing plan with options"),
    ("/ask", "Toggle ask mode (Q&A, read-only; no edits or command execution)"),
    ("/debug", "Toggle debug mode (log server for debugging agent runs)"),
    ("/max-mode", "Toggle max mode"),
    ("/clear", "Start a new chat session"),
    ("/compress", "Summarize the conversation to reduce context"),
    ("/vim", "Toggle Vim keys"),
    ("/vuepy", "Vuepy 相关提示词模板"),
]

# 聊天消息列表（用于 v-model 绑定）
resume_id = ref('caa0e6f6-9a33-4e1a-8a8d-5694fa9163cd')

# https://www.douban.com/topic/353510081/?_spm_id=MTEzNzU5MQ&_dtcc=1
chat_lines = ref([])
# user_input = ref('''
# /vuepy 使用textual_vuepy实现一个倒计时器, 只返回vue文件的代码（纯代码, 不要任何其他内容）, 代码包裹在<ui_content>...</ui_content>中
# 注意和vuejs的差异
# ''')
user_input = ref("")
chat_log = ref(None)
input_ref = ref(None)
is_loading = ref(False)
send_btn_ref = ref(None)
chat_container_ref = ref(None)
slash_option_list_ref = ref(None)

slash_highlighted = ref(None)

# 输入历史（方案 3：prompt_toolkit 风格）
input_history = ref([])
history_index = ref(-1)
history_draft = ref("")
MAX_HISTORY = 100
# AI 后端：Cursor Agent > DeepSeek > Echo
_ai_backend = None

def get_ai_backend():
    # return 'echo'
    nonlocal _ai_backend
    if _ai_backend is not None:
        return _ai_backend
    # 1. 尝试 Cursor Agent CLI（需安装 cursor CLI: curl https://cursor.com/install -fsSL | bash）
    try:
        import subprocess
        r = subprocess.run(["agent", "--help"], capture_output=True, timeout=3)
        if r.returncode == 0:
            _ai_backend = "cursor_agent"
            return _ai_backend
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    # 2. 尝试 DeepSeek
    try:
        import sys
        from pathlib import Path
        project_root = Path(__file__).resolve().parent.parent.parent.parent
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))
        from deepseek import DeepSeekChat
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if api_key:
            _ai_backend = DeepSeekChat(api_key=api_key)
            return _ai_backend
    except Exception:
        pass
    _ai_backend = "echo"
    return _ai_backend

def append_message(role, text, format='markdown'):
    """追加消息到聊天区域，用户输入和 AI 输出均以 Markdown 渲染"""
    prefix = "[bold cyan]你:[/]\n" if role == "user" else "[bold green]AI:[/]\n"
    line = f"{prefix}{text}"
    chat_lines.value.append(line)
    try:
        log_widget = chat_log.value.unwrap() if chat_log.value else None
    except Exception:
        log_widget = None
    if not log_widget:
        try:
            log_widget = app.tt_app.query_one("#chat-log")
        except Exception:
            log_widget = None

    if log_widget:
        log_widget.write(prefix)
        if format == 'markdown':
            log_widget.write(Markdown(text or ""))
        else:
            log_widget.write(text or "")
        log_widget.write("\n")


def append_ui_content(content):
    """将 UI 组件内容挂载到聊天区域"""
    try:
        chat_container = chat_container_ref.value
        if not chat_container:
            return
        Comp = import_sfc(content.strip(), raw_content=True)
        props = {}
        ctx = {}
        comp = Comp.gen(props, ctx, app)
        node = comp.render(ctx, props, {})
        chat_container.append(node)
    except Exception as e:
        app.tt_app.copy_to_clipboard(content)
        append_message("assistant", f"{content} \n[red]加载失败: {e}[/]", format='text')
        app.message(f"[red]UI 组件加载失败: {e}[/]")
        return False
    return True


def process_ai_response(result):
    """解析 AI 返回内容：提取 <ui_content>...</ui_content> 调用 append_ui_content，其余用 append_message 渲染"""
    if not result:
        return
    # 按 <ui_content>...</ui_content> 分割，保留分隔符以便判断类型
    parts = re.split(r'(<ui_content>.*?</ui_content>)', result, flags=re.DOTALL)
    for part in parts:
        part = part.strip()
        if not part:
            continue
        m = re.match(r'<ui_content>(.*)</ui_content>', part, re.DOTALL)
        if m:
            append_ui_content(m.group(1).strip())
        else:
            append_message("assistant", part)


def clear_chat(event=None):
    """清空聊天记录"""
    nonlocal slash_option_list_ref
    chat_lines.value = []
    try:
        log_widget = app.tt_app.query_one("#chat-log")
    except Exception:
        log_widget = None
    if log_widget:
        log_widget.clear()
    backend = get_ai_backend()
    if backend != "echo" and hasattr(backend, "clear_history"):
        backend.clear_history()

def _run_shell_sync(cmd):
    """在 worker 线程中执行 shell 命令"""
    import subprocess
    try:
        r = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=os.getcwd(),
        )
        out = (r.stdout or "").strip()
        err = (r.stderr or "").strip()
        if r.returncode != 0 and err:
            return f"[red]exit {r.returncode}[/]\n{err}\n{out}".strip()
        return out or "(无输出)"
    except subprocess.TimeoutExpired:
        return "[red]命令超时 (30s)[/]"
    except Exception as e:
        return f"[red]错误: {e}[/]"


def _call_ai_sync(user_text):
    """在 worker 线程中执行的同步 AI 调用"""
    backend = get_ai_backend()
    if backend == "echo":
        return f"（回显模式）你说了: \n{user_text}"
    if backend == "cursor_agent":
        try:
            import subprocess
            cmd = [
                "agent", "--model", "composer-1.5", 
                # f"--resume={resume_id.value}", 
                "-p", user_text,
                # "--output-format json"
            ]
            r = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120,
                cwd=os.getcwd(),
            )
            out = (r.stdout or "").strip() or (r.stderr or "").strip()
            return out or "（Cursor Agent 无输出）"
        except subprocess.TimeoutExpired:
            return "（Cursor Agent 超时）"
        except Exception as e:
            return f"错误: {str(e)}"
    try:
        return backend.chat(user_text, stream=False)
    except Exception as e:
        return f"错误: {str(e)}"

async def send_message(event=None):
    """发送用户消息并获取 AI 回复；以 ! 开头的输入执行 shell 命令"""
    # 优先从 TextArea 控件读取最新文本（v-model 可能尚未同步）
    try:
        ta = input_ref.value.unwrap() if input_ref.value else None
        text = (getattr(ta, "text", None) or user_input.value or "").strip()
    except Exception:
        text = (user_input.value or "").strip()
    send_btn = send_btn_ref.value.unwrap() if send_btn_ref.value else None

    if not text:
        return
    # 加入输入历史（非重复、非空）
    hist = input_history.value
    if not hist or hist[-1] != text:
        hist = list(hist) + [text]
        if len(hist) > MAX_HISTORY:
            hist = hist[-MAX_HISTORY:]
        input_history.value = hist
    history_index.value = -1
    history_draft.value = ""
    user_input.value = ""
    append_message("user", text)
    try:
        is_loading.value = True
        if send_btn and hasattr(send_btn, 'loading'):
            send_btn.loading = True
        # 以 ! 或 ！（全角）开头时执行 shell
        _first = text.lstrip()
        if _first.startswith("!") or _first.startswith("！"):
            cmd = (_first[1:]).strip()
            worker = app.tt_app.run_worker(
                lambda c=cmd: _run_shell_sync(c),
                thread=True,
            )
            result = await worker.wait()
            append_message("assistant", result or "", format="text")
        else:
            worker = app.tt_app.run_worker(
                lambda: _call_ai_sync(text),
                thread=True,
            )
            result = await worker.wait()
            process_ai_response(result or "")
    except Exception as e:
        append_message("assistant", f"错误: {str(e)}")
    finally:
        is_loading.value = False
        if send_btn and hasattr(send_btn, 'loading'):
            send_btn.loading = False

def _set_input_text(value):
    """设置输入框文本，并同步到 TextArea 控件"""
    user_input.value = value
    try:
        inp = input_ref.value.unwrap()
        if inp and hasattr(inp, 'move_cursor'):
            # inp.text = value
            lines = value.split('\n')
            inp.move_cursor((len(lines) - 1, len(lines[-1])))
    except Exception:
        pass

def history_up(event=None):
    """上一条历史（更早）"""
    hist = input_history.value
    if not hist:
        return
    if history_index.value < 0:
        try:
            ta = input_ref.value.unwrap() if input_ref.value else None
            history_draft.value = (getattr(ta, "text", None) or user_input.value or "").strip()
        except Exception:
            history_draft.value = (user_input.value or "").strip()
        history_index.value = len(hist) - 1  # 从最新一条开始
    else:
        if history_index.value > 0:
            history_index.value -= 1  # 往更早的
    _set_input_text(hist[history_index.value])

def history_down(event=None):
    """下一条历史（更新）"""
    hist = input_history.value
    idx = history_index.value
    if idx < 0:
        return  # 已在草稿
    if idx >= len(hist) - 1:
        history_index.value = -1
        _set_input_text(history_draft.value)
    else:
        history_index.value = idx + 1
        _set_input_text(hist[history_index.value])

def exit(event=None):
    app.tt_app.exit(return_code=0)


# ---------- 斜杠命令补全（使用 Dialog）----------
show_slash_dialog = ref(False)
slash_prefix = ref("")
slash_filter = ref("/")


def slash_filter_method(query, item):
    """filter-method：首参为当前输入；与 FilterableOptionList 内过滤规则一致。"""
    f = (query or "").strip().lower()
    f = f[1:] if f.startswith("/") else f
    cmd = item[0]
    return f in cmd.lower()


def open_slash_dialog(prefix: str):
    slash_prefix.value = prefix
    # slash_filter.value = ""
    show_slash_dialog.value = True


def close_slash_dialog(event=None):
    show_slash_dialog.value = False


def on_slash_dialog_open(event=None):
    # TODO 统一使用 unwrap().force_input
    # slash_option_list_ref.value.setup_returned['force_input']()
    slash_option_list_ref.value.force_input()


def on_slash_option_selected(option):
    """选中命令后插入到输入框并关闭弹窗"""
    close_slash_dialog()
    _set_input_text(slash_prefix.value + option + " ")


# def _check_slash_trigger(new_val, *args):
def _check_slash_trigger(event):
    new_val = event.text_area.text
    """当输入以 / 结尾时打开斜杠命令弹窗"""
    if show_slash_dialog.value or is_loading.value:
        return
    text = (new_val or "").strip()
    if not text.endswith("/"):
        return
    idx = text.rfind("/")
    open_slash_dialog(text[:idx])

# watch(user_input, _check_slash_trigger)

@onMounted
def init():
    def _welcome():
        backend = get_ai_backend()
        mode = {"cursor_agent": "Cursor Agent", "echo": "回显"}.get(backend, "DeepSeek")
        append_message("assistant", f"已就绪，当前模式: {mode}。输入消息开始对话。")
        input_ref.value.unwrap().focus()
    app.tt_app.call_later(_welcome)
</script>

<style lang="tcss">
Screen {
    background: rgb(40, 44, 52);
}

#chat-container {
    min-height: 5;
}

#chat-log {
    height: 100%;
    min-height: 5;
    border: solid $secondary 50%;
    padding: 1;
}

#input-area Input {
    width: 1fr;
    margin: 0 1 0 0;
}
</style>

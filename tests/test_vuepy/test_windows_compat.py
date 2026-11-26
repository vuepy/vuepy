import argparse
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from vuepy.cli.create_vue import render_app_vue
from vuepy.cli.run_vue import _textual_serve_run_command
from vuepy.compiler_sfc.sfc_parser import SFCMetadata
from vuepy.utils.shell_argv import join_shell_command
from vuepy.utils.shell_argv import split_shell_args


class TestShellArgv(unittest.TestCase):
    def test_split_keeps_windows_path_when_platform_is_win32(self):
        line = r'C:\Users\用户1\Downloads\App.vue --plugins wui,leaflet --app app'
        with mock.patch.object(sys, "platform", "win32"):
            args = split_shell_args(line)
        self.assertEqual(
            args,
            [r"C:\Users\用户1\Downloads\App.vue", "--plugins", "wui,leaflet", "--app", "app"],
        )

    def test_split_keeps_quoted_windows_path_with_spaces(self):
        line = r'"C:\Users\my file\App.vue" --app app'
        with mock.patch.object(sys, "platform", "win32"):
            args = split_shell_args(line)
        self.assertEqual(args, [r"C:\Users\my file\App.vue", "--app", "app"])

    def test_split_posix_still_honors_quotes(self):
        line = "'/tmp/my file.vue' --app app"
        with mock.patch.object(sys, "platform", "linux"):
            args = split_shell_args(line)
        self.assertEqual(args, ["/tmp/my file.vue", "--app", "app"])

    def test_join_windows_uses_cmd_quoting(self):
        parts = [r"C:\Program Files\用户1\python.exe", "-m", "vuepy", "run", r"C:\Users\用户1\App.vue"]
        with mock.patch.object(sys, "platform", "win32"):
            cmd = join_shell_command(parts)
        self.assertEqual(
            cmd,
            r'"C:\Program Files\用户1\python.exe" -m vuepy run C:\Users\用户1\App.vue',
        )
        self.assertNotIn("'", cmd)

    def test_join_posix_quotes_spaces(self):
        parts = ["/home/x px/python", "-m", "vuepy"]
        with mock.patch.object(sys, "platform", "linux"):
            cmd = join_shell_command(parts)
        self.assertEqual(cmd, "'/home/x px/python' -m vuepy")


class TestServableCommand(unittest.TestCase):
    def test_windows_command_does_not_use_posix_quotes(self):
        args = argparse.Namespace(
            dev=False,
            devtools_host=None,
            devtools_port=None,
            plugins=[],
        )
        with mock.patch.object(sys, "platform", "win32"), \
                mock.patch.object(sys, "executable", r"C:\Program Files\用户1\python.exe"):
            cmd = _textual_serve_run_command("playground", args)
        self.assertTrue(cmd.startswith(r'"C:\Program Files\用户1\python.exe" -X utf8'))
        self.assertNotIn("'", cmd)
        self.assertIn("--backend textual", cmd)
        self.assertNotIn("--servable", cmd)


class TestRenderAppVue(unittest.TestCase):
    def test_writes_utf8_and_posix_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            app_vue = Path(tmp) / "App.vue"
            app_vue.write_text(
                "<template>头</template>\n<script setup>\nfrom '$js_stubs_path/vue'\n</script>\n",
                encoding="utf-8",
            )
            render_app_vue(app_vue, Path("C:/Users/用户1/pkg/js_stubs"))
            raw = app_vue.read_bytes()
            text = raw.decode("utf-8")
            self.assertIn("头", text)
            self.assertIn("C:/Users/用户1/pkg/js_stubs/vue", text)
            self.assertNotIn("\\", text)
            self.assertNotIn(b"\r\n", raw)
            meta = SFCMetadata.load(app_vue)
            self.assertIn("头", meta.template)

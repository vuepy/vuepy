from __future__ import annotations

import dataclasses
import pathlib
import re

from vuepy import log
from vuepy.compiler_sfc.compile_script import ScriptCompiler

logger = log.getLogger()


@dataclasses.dataclass
class SFCFile:
    file: pathlib.Path
    content: str
    template: str
    script_src: str
    script_py: str

    @property
    def setup_fn(self):
        if self.script_src:
            return ScriptCompiler.compile_script_src(self.file.parent, self.script_src)
        elif self.script_py:
            return ScriptCompiler.compile_script_block(
                self.script_py, str(self.file.absolute()))
        else:
            return lambda *args: {}

    @classmethod
    def load(cls, sfc_file):
        sfc_file = pathlib.Path(sfc_file)
        with open(sfc_file) as f:
            raw_content = f.read()

        content = re.sub(r'<!--(.*?)-->', '\n', raw_content, re.S)
        instance = cls(
            file=sfc_file,
            content=raw_content,
            template=cls.get_block_content('template', content)[0],
            script_src=cls.get_script_src(content),
            script_py=cls.get_script_py(content),
        )
        if instance.script_py and instance.script_src:
            raise ValueError(
                "Syntax error: script lang and script src cannot exist at the same time"
            )

        return instance

    @staticmethod
    def get_block_content(tag, content):
        blocks = re.findall(f'<{tag}>(.*)</{tag}>', content, flags=re.S | re.I)
        return blocks

    @staticmethod
    def get_script_src(content):
        match = re.search(r"<script (.*?)src=(['\"])(?P<src>.*?)\2></script>", content)
        return match.group('src') if match else None

    @staticmethod
    def get_script_py(content):
        match = re.search(
            fr'<script\s+lang=(["\'])py\1\s*>(?P<content>.*)?</script>',
            content,
            flags=re.S | re.I
        )

        if not match:
            logger.debug("can't find <script lang=py>")
            return None

        return match.group('content')

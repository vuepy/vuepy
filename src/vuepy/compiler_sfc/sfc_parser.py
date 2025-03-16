# ---------------------------------------------------------
# Copyright (c) vuepy.org. All rights reserved.
# ---------------------------------------------------------
from __future__ import annotations

import dataclasses
import pathlib
import re
from html.parser import HTMLParser
from typing import List
from typing import Tuple

from vuepy import log
from vuepy.compiler_sfc.compile_script import ScriptCompiler

logger = log.getLogger()


@dataclasses.dataclass
class SFCTag:
    """
    start_pos: [row=1,col=0]
    |
    <tag>..</tag>
           |
           end_pos
    """
    name: str
    attrs: dict
    start_pos: Tuple[int, int]
    end_pos: Tuple[int, int] = None
    inner_html: str = ''

    def to_dict(self):
        return {
            'name': self.name,
            'attrs': self.attrs,
            'start_pos': self.start_pos,
            'end_pos': self.end_pos,
            'inner_html': self.inner_html,
        }


class SFCParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tag_stack = []
        self.level1_tags = []
        self.sfc_tags: List[SFCTag] = []

    def handle_starttag(self, tag, attrs):
        if not self.tag_stack:
            self.level1_tags.append(SFCTag(tag, dict(attrs), self.getpos()))
        self.tag_stack.append(tag)

    def handle_endtag(self, tag):
        if self.tag_stack:
            self.tag_stack.pop()

        if not self.tag_stack and self.level1_tags:
            sfc_tag = self.level1_tags.pop()
            if sfc_tag.name != tag:
                row_s, _ = sfc_tag.start_pos
                row_e, _ = self.getpos()
                msg = f"tag <{sfc_tag.name}> at {sfc_tag.start_pos} mismatch: " \
                      f"expected </{sfc_tag.name}>, got </{tag}> at {self.getpos()}.\n" \
                      f"-> {row_s} {self.html_lines[row_s - 1]}...\n" \
                      f"-> {row_e} {self.html_lines[row_e - 1]}"
                raise ValueError(msg)

            sfc_tag.end_pos = self.getpos()
            # todo
            s = self.vue_html.find('>', self.calc_idx_by_pos(sfc_tag.start_pos)) + 1
            e = self.calc_idx_by_pos(sfc_tag.end_pos)
            sfc_tag.inner_html = self.vue_html[s:e]

            self.sfc_tags.append(sfc_tag)

    def calc_idx_by_pos(self, pos):
        row, col = pos
        return self.html_lines_len_sum[row] + col

    def parse(self, vue_html) -> List[SFCTag]:
        self.vue_html = vue_html
        self.html_lines = vue_html.splitlines(keepends=True)
        html_lines_len = [len(i) for i in self.html_lines]
        self.html_lines_len_sum = [None, 0]
        acc = 0
        for i, line_len in enumerate(html_lines_len):
            acc += html_lines_len[i]
            self.html_lines_len_sum.append(acc)

        self.tag_stack = []
        self.level1_tags = []
        self.feed(vue_html)
        # handle last </tag>
        if self.level1_tags:
            sfc_tag = self.level1_tags.pop()
            row, col = sfc_tag.start_pos
            msg = f"tag <{sfc_tag.name}> at {sfc_tag.start_pos} not closed.\n"\
                  f"-> {row} {self.html_lines[row-1]}"
            raise ValueError(msg)
        return self.sfc_tags


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

        return cls.loads(raw_content, sfc_file)

    @classmethod
    def loads(cls, sfc_content, file_path='__tmp_for_str.vue') -> SFCFile:
        sfc_tags = SFCParser().parse(sfc_content)

        script_src_tag_attrs = {}
        script_py_tag: SFCTag = None
        template_tag = None
        for tag in sfc_tags:
            if tag.name == 'template':
                if template_tag:
                    raise ValueError("template tag duplicate")
                template_tag = tag
            elif tag.name == 'script':
                if 'src' in tag.attrs:
                    script_src_tag_attrs = tag.attrs
                elif tag.attrs.get('lang', '').lower() == 'py':
                    script_py_tag = tag

        if template_tag is None:
            raise ValueError(f"can't find <template> in {file_path}")

        instance = cls(
            file=pathlib.Path(file_path),
            content=sfc_content,
            template=template_tag.inner_html,
            script_src=script_src_tag_attrs.get("src"),
            script_py=script_py_tag and script_py_tag.inner_html,
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

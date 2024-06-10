from __future__ import annotations

import dataclasses
from dataclasses import field
from typing import List


@dataclasses.dataclass
class CompilerOptions:
    # Whitespace handling strategy
    whitespace = 'condense'  # preserve | condense
    delimiters: List[str] = field(default_factory=lambda: ['{{', '}}'])
    # Whether to keep comments in the templates AST
    comments: bool = False

    def is_custom_element(self, tag: str) -> bool:
        """
        Separate option for end users to extend the native elements list

        :param tag:
        :return:
        """
        pass

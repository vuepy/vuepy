"""
Workaround: pytest_textual_snapshot assumes node.reportinfo() returns a Path-like,
but pytest returns path as str. Patch node_to_report_path to accept str.
"""
import os
import re
from pathlib import Path

import pytest_textual_snapshot

# Textual renders monochrome when NO_COLOR is set, which changes snapshot SVGs.
os.environ.pop("NO_COLOR", None)

_SVGExtension = pytest_textual_snapshot.SVGImageExtension

# syrupy 7 reads file_extension. pytest-textual-snapshot 1.0.0 still sets
# _file_extension, so the assertion looks for .raw instead of the .svg snapshot.
_SVGExtension.file_extension = "svg"


def _normalize_svg(data):
    """Drop Rich's per-run terminal id. Saved snapshots store ``terminal-r1``."""
    if isinstance(data, bytes):
        text = data.decode()
        normalized = _normalize_svg(text)
        return data if normalized == text else normalized.encode()
    if not isinstance(data, str):
        return data
    return re.sub(r"\bterminal-\d+-([\w-]+)", r"terminal-\1", data)


def _normalize_method(method_name):
    original = getattr(_SVGExtension, method_name, None)
    if original is None:
        return

    def wrapped(self, *args, **kwargs):
        return _normalize_svg(original(self, *args, **kwargs))

    setattr(_SVGExtension, method_name, wrapped)


# pytest-textual-snapshot 1.0.0 compares the raw SVG, so a new random id fails
# the assertion even when the picture is unchanged. 1.1.0 already normalizes;
# doing it again leaves that text unchanged.
_normalize_method("serialize")
_normalize_method("read_snapshot_data_from_location")
_normalize_method("_read_snapshot_data_from_location")

_orig_node_to_report_path = pytest_textual_snapshot.node_to_report_path


def _node_to_report_path(node):
    path, lineno, name = node.reportinfo()
    path = Path(path) if isinstance(path, str) else path

    class _Node:
        reportinfo = lambda self: (path, lineno, name)

    return _orig_node_to_report_path(_Node())


pytest_textual_snapshot.node_to_report_path = _node_to_report_path

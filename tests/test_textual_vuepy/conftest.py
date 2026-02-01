"""
Workaround: pytest_textual_snapshot assumes node.reportinfo() returns a Path-like,
but pytest returns path as str. Patch node_to_report_path to accept str.
"""
from pathlib import Path

import pytest_textual_snapshot

_orig_node_to_report_path = pytest_textual_snapshot.node_to_report_path


def _node_to_report_path(node):
    path, lineno, name = node.reportinfo()
    path = Path(path) if isinstance(path, str) else path

    class _Node:
        reportinfo = lambda self: (path, lineno, name)

    return _orig_node_to_report_path(_Node())


pytest_textual_snapshot.node_to_report_path = _node_to_report_path

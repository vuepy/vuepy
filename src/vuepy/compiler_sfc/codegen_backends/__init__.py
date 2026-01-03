from vuepy.compiler_sfc.codegen_backends.backend import CodegenBackendMgr
from vuepy.compiler_sfc.codegen_backends.ipywidgets import IwCodegenBackend

PANEL_BACKEND = 'panel'
TEXTUAL_BACKEND = 'textual'

CodegenBackendMgr.register_lazy(
    PANEL_BACKEND, 'vuepy.compiler_sfc.codegen_backends.panel.PnCodegenBackend'
)

CodegenBackendMgr.register_lazy(
    TEXTUAL_BACKEND, 'vuepy.compiler_sfc.codegen_backends.textual.TextualCodegenBackend'
)

__all__ = [
    'CodegenBackendMgr',
    'IwCodegenBackend',
]

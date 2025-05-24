from vuepy.compiler_sfc.codegen_backends.backend import CodegenBackendMgr
from vuepy.compiler_sfc.codegen_backends.ipywidgets import IwCodegenBackend

PANEL_BACKEND = 'panel'

CodegenBackendMgr.register_lazy(
    PANEL_BACKEND, 'vuepy.compiler_sfc.codegen_backends.panel.PnCodegenBackend'
)

__all__ = [
    'CodegenBackendMgr',
    'IwCodegenBackend',
]

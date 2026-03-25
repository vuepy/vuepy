"""运行 hash 路由示例：python run_router.py（需 vuepy textual 环境）。"""
from pathlib import Path

from vuepy import create_app, import_sfc

App = import_sfc(Path(__file__).parent / "App.vue")
app = create_app(App, backend="textual")
app.mount()

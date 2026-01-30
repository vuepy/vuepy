from pathlib import Path
from vuepy import create_app, import_sfc

App = import_sfc(Path(__file__).parent / 'test_playground.vue')
app = create_app(App, backend='textual')
app.mount()

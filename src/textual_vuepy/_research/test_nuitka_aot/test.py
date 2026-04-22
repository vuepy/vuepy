import os
from pathlib import Path
from vuepy import create_app, import_sfc


os.environ['EN_VUEPY_AOT'] = '1'
App = import_sfc(Path(__file__).parent / 'App.vue')
app = create_app(App, backend='textual')
app.mount()

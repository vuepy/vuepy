from pathlib import Path

from vuepy import import_sfc
from vuepy.utils.appstore import VuepyAppStore


CUR_DIR = Path(__file__).parent

VuepyAppStore.register("playground", import_sfc(CUR_DIR / "Playground.vue"))
VuepyAppStore.register("keys", import_sfc(CUR_DIR / "Keys.vue"))

#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEXTUAL_VUEPY="$(python -c 'import textual_vuepy, os; print(os.path.dirname(textual_vuepy.__file__))')"
cd "$ROOT"
echo "build in $ROOT"

# After extracting in onefile mode, __file__ is under the root of a temporary directory,
# so all .vue files must be placed in the same directory as data files.
# Otherwise, import_sfc(Path(__file__).parent / "App.vue") will result in FileNotFoundError.
#
# All .vue files have been precompiled into _vue_aot_*.py using vue2py.py.
# Import _vue_aot_App or use the --include-module option to instruct Nuitka to bundle them!
include_modules=$(python vue2py.py ./* ./comps/* "${TEXTUAL_VUEPY}/components"/*)
INCLUDE_MODULES=""
for module in $include_modules; do
  INCLUDE_MODULES+=" --include-module=${module}"
done
echo "INCLUDE_MODULES: $INCLUDE_MODULES"

# export EN_VUEPY_AOT=1
# nuitka --standalone --jobs=12 \
nuitka --onefile --jobs=12 \
  --include-package=textual \
  --include-data-dir="${TEXTUAL_VUEPY}/apps=textual_vuepy/apps" \
  $INCLUDE_MODULES \
  --nofollow-import-to=IPython \
  --nofollow-import-to=matplotlib \
  --nofollow-import-to=ipykernel \
  --nofollow-import-to=ipywidgets \
  --nofollow-import-to=panel \
  --nofollow-import-to=bokeh \
  --macos-create-app-bundle \
  test.py

#   --include-module=_vue_aot_App \
#   --include-module=_vue_aot_Child \
#   --include-data-dir="${TEXTUAL_VUEPY}/components=textual_vuepy/components" \
#   --include-module="comps._vue_aot_Child" \
#   --include-module="comps._vue_aot_Child2" \

import glob
from pathlib import Path
from vuepy.runtime.core.import_sfc import import_sfc_aot


if __name__ == "__main__":
    import sys
    # python vue2py.py ./* ./comps/*
    for arg in sys.argv[1:]:
        for p in glob.glob(arg, recursive=True):
            if p.endswith('.vue'):
                # Force recompile by touching the vue file
                Path(p).touch()
                comp = import_sfc_aot(p, force_compile=True)
                print(f"{comp.__module__}")

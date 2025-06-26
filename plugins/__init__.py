import os
import glob

def import_modular():
    mod_paths = glob.glob(f"{os.path.dirname(__file__)}/**/*.py", recursive=True)
    return sorted(
        [
            os.path.splitext(os.path.relpath(f, os.path.dirname(__file__)))[0].replace("/", ".")
            for f in mod_paths
            if os.path.isfile(f)
            and f.endswith(".py")
            and not f.endswith("__init__.py")
        ]
    )

PLUGINS = import_modular()

import sys

from cx_Freeze import setup, Executable

import increment

if sys.platform == "win32":
    base = "Win32GUI"
else:
    base = None

executables = [
    Executable("increment_main.pyw", base=base, icon=increment.get_resource('favicon.ico'), targetName='Increment.exe',
               copyright='by ' + increment.__author__)
]

options = {
    'build_exe': {
        'packages': [],
    },
}

setup(
    name=increment.__name__,
    options=options,
    version=increment.__version__,
    executables=executables,
)

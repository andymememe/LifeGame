from cx_Freeze import setup, Executable
import os

os.environ['TCL_LIBRARY'] = r'C:\IntelPython3\Library\lib\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\IntelPython3\Library\lib\tk8.6'

base = None    

executables = [Executable("main.py", base=base)]

packages = ["lib"]
options = {
    'build_exe': {    
        'packages': packages,
    },    
}

setup(
    name = "LifeGame",
    options = options,
    version = "1.0",
    description = 'Some life games.',
    executables = executables
)
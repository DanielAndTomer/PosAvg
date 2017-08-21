import cx_Freeze
import sys
import os
import AvgPosGen

os.environ['TCL_LIBRARY'] = r'C:\Users\user\AppData\Local\Programs\Python\Python36\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\user\AppData\Local\Programs\Python\Python36\tcl\tk8.6'

base = None

if sys.platform == 'win32':
    base = "Win32GUI"

executables = [cx_Freeze.Executable("GUI.py", base=base, icon="chief.ico")]

cx_Freeze.setup(
    name = "SeaofBTC-Client",
    options = {"build_exe": {"packages":["tkinter","AvgPosGen"], "include_files":["chief.ico","tcl86t.dll", "tk86t.dll"]}},
    version = "0.01",
    description = "Sea of BTC trading application",
    executables = executables
    )

import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only
build_exe_options = {"packages": ["os"], "excludes": ["tkinter",], 
                    "include_files": ["BDSP.png", "Resources"]}

# base="Win32GUI" should be used only for Windows GUI app
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "BDSP Randomizers",
    version = "1.0",
    description = "A randomizer for Brilliant Diamond/Shining Pearl!",
    options = {"build_exe": build_exe_options},
    executables = [Executable("main.py", base=base, icon="RandomizerIcon.png")]
)

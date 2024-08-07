from cx_Freeze import setup, Executable
import numpy
import os

numpy_path = os.path.dirname(numpy.__file__)

build_exe_options = {
    "packages": ["os", "tkinter", "pathlib", "sys", "shutil", "gspread", "docx", "numpy", "tkcalendar"],
    "includes": [],
    "include_files": [(numpy_path, "numpy")]
}

executables = [Executable("main.py", base="Win32GUI")]
# executables = [Executable("main.py", base=None)]

setup(
    name="Bonus 70+",
    version="0.1",
    description="Розрахунок додаткової премії на 70 000 грн",
    options={"build_exe": build_exe_options},
    executables=executables
)

# run in console to start generate exe: python setup.py build

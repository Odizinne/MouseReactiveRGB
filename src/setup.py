import os
from cx_Freeze import setup, Executable

src_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = "build/MouseReactiveRGB"
icon_path = os.path.join(src_dir, "resources/icons/icon.ico")
zip_include_packages = ["PyQt6"]
include_files = [
    os.path.join(src_dir, "resources/"),
]

build_exe_options = {
    "include_files": include_files,
    "build_exe": build_dir,
    "packages": ["os", "sys", "openrgb", "pynput", "threading", "json", "multiprocessing"],
    "zip_include_packages": zip_include_packages,
    "excludes": ["tkinter"],
}


executables = [
    Executable(
        os.path.join(src_dir, "main.py"),
        base="Win32GUI",
        icon=icon_path,
        target_name="MouseReactiveRGB.exe",
    )
]


setup(
    name="MouseReactiveRGB",
    version="1.0",
    options={"build_exe": build_exe_options},
    executables=executables,
)

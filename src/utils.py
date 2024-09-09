import sys
import os
import psutil
import darkdetect
import winaccent
from PyQt6.QtGui import QIcon
from openrgb.utils import RGBColor


off = RGBColor(0, 0, 0)


def is_openrgb_running():
    openrgb_executable = "openrgb.exe" if sys.platform == "win32" else "openrgb"
    for process in psutil.process_iter(["pid", "name"]):
        if process.info["name"].lower() == openrgb_executable:
            return True
    return False


def get_icon():
    if darkdetect.isDark():
        return QIcon("resources/icon_light.png")
    else:
        return QIcon("resources/icon_dark.png")


def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip("#")

    r = int(hex_code[0:2], 16)
    g = int(hex_code[2:4], 16)
    b = int(hex_code[4:6], 16)

    return (r, g, b)


def get_accent_color():
    return hex_to_rgb(winaccent.accent_normal)


def get_settings_file():
    if sys.platform == "win32":
        return os.path.join(os.getenv("APPDATA"), "MouseReactiveRGB", "settings.json")
    else:
        return os.path.join(os.getenv("HOME"), ".config", "MouseReactiveRGB", "settings.json")

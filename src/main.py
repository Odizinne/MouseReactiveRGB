import sys
from PyQt6.QtWidgets import QApplication
from mousereactivergb import MouseReactiveRGB

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setStyle("Fusion")
    window = MouseReactiveRGB()
    sys.exit(app.exec())

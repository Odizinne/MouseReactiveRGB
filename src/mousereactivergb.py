from PyQt6.QtWidgets import QMainWindow, QSystemTrayIcon, QMenu, QApplication
from PyQt6.QtCore import QTimer, Qt, pyqtSlot, QMetaObject, QObject, pyqtSignal
from PyQt6.QtGui import QAction, QIcon
from ui_mousereactivergb import Ui_MouseReactiveRGB
from openrgb import OpenRGBClient
from openrgb.utils import RGBColor, DeviceType
from pynput.mouse import Listener
from color_utils import set_frame_color_based_on_window
import os
import sys
import threading
import json
import random

if sys.platform == "win32":
    settings_file = os.path.join(os.getenv("APPDATA"), "MouseReactiveRGB", "settings.json")
else:
    settings_file = os.path.join(os.getenv("HOME"), ".config", "MouseReactiveRGB", "settings.json")


class ConnectionWorker(QObject):
    connected = pyqtSignal()
    failed = pyqtSignal(str)

    def __init__(self, ip, port):
        super().__init__()
        self.ip = ip
        self.port = port
        self.client = None

    def run(self):
        try:
            self.client = OpenRGBClient(self.ip, self.port, "G502 Reactive RGB")
            devices = self.client.devices
            for device in devices:
                if device.type == DeviceType.MOUSE:
                    print(f"{device.name}: is a mouse")
                    supported_modes = [mode.name for mode in device.modes]
                    if "Direct" in supported_modes:
                        self.device = device
                        self.device.set_mode("Direct")
                        self.device.set_color(RGBColor(0, 0, 0), fast=True)
                        self.connected.emit()
                        print(f"{device.name}: direct mode supported.")
                        print(f"Using compatible device: {device.name}")
                        return
                    else:
                        self.failed.emit(f"{device.name}: direct mode not supported.")
        except Exception as e:
            self.failed.emit(str(e))


class MouseReactiveRGB(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MouseReactiveRGB()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon("resources/icon.png"))
        self.initial_color = RGBColor(0, 0, 0)
        self.current_color = self.initial_color
        self.settings_file = settings_file
        self.client = None
        self.mouse = None
        self.connected = False
        self.run_effect = False
        set_frame_color_based_on_window(self, self.ui.frame)
        set_frame_color_based_on_window(self, self.ui.frame_2)
        self.load_settings()
        self.connect_ui_signals()
        self.create_tray_icon()

        self.retry_timer = QTimer(self)
        self.retry_timer.timeout.connect(self.retry_connection)

        self.fade_timer = QTimer(self)
        self.fade_timer.timeout.connect(self.fade_out)
        self.fade_duration = 500
        self.steps = 30
        self.current_step = 0

        self.listener_thread = threading.Thread(target=self.start_listener, daemon=True)
        self.listener_thread.start()

        self.retry_connection()

    def connect_ui_signals(self):
        self.ui.rSpinBox.valueChanged.connect(self.save_settings)
        self.ui.gSpinBox.valueChanged.connect(self.save_settings)
        self.ui.bSpinBox.valueChanged.connect(self.save_settings)
        self.ui.ipLineEdit.editingFinished.connect(self.save_settings)
        self.ui.portSpinBox.valueChanged.connect(self.save_settings)
        self.ui.fadeDurationSlider.sliderReleased.connect(self.save_settings)
        self.ui.randomCheckBox.stateChanged.connect(self.save_settings)
        self.ui.fpsSpinBox.valueChanged.connect(self.save_settings)
        self.ui.autostartCheckBox.stateChanged.connect(self.save_settings)
        self.ui.startstopButton.clicked.connect(self.on_startstopButton_clicked)

    def retry_connection(self):
        ip = self.ui.ipLineEdit.text()
        port = self.ui.portSpinBox.value()
        self.connection_worker = ConnectionWorker(ip, port)
        self.connection_worker.connected.connect(self.on_connection_success)
        self.connection_worker.failed.connect(self.on_connection_failure)

        self.connection_thread = threading.Thread(target=self.connection_worker.run)
        self.connection_thread.start()

    def on_connection_success(self):
        self.connected = True
        self.ui.connectionStatusButton.setText("Connected ✅")
        self.mouse = self.connection_worker.device
        if self.mouse:
            self.mouse.set_color(self.initial_color, fast=True)
            self.retry_timer.stop()
        else:
            self.connected = False
            self.ui.connectionStatusButton.setText("Disonnected ❌")
            self.retry_timer.start(1000)

    def on_connection_failure(self, error_message):
        print(f"{error_message}")
        self.ui.connectionStatusButton.setText("Disonnected ❌")
        self.retry_timer.start(1000)

    def start_listener(self):
        with Listener(on_click=self.on_click) as listener:
            listener.join()

    def on_click(self, x, y, button, pressed):
        if not self.connected:
            return
        if pressed:
            QMetaObject.invokeMethod(self, "trigger_reactive_effect", Qt.ConnectionType.QueuedConnection)

    @pyqtSlot()
    def trigger_reactive_effect(self):
        if not self.mouse:
            self.retry_connection()
        self.start_reactive_effect()

    def start_reactive_effect(self):
        if not self.mouse.active_mode == 1:
            print("Mouse is not in direct mode.")
            return

        if not self.run_effect:
            return

        if self.ui.randomCheckBox.isChecked():
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
        else:
            r = self.ui.rSpinBox.value()
            g = self.ui.gSpinBox.value()
            b = self.ui.bSpinBox.value()

        self.current_color = RGBColor(r, g, b)
        if self.mouse:
            try:
                self.mouse.set_color(self.current_color, fast=True)
            except Exception as e:
                self.retry_timer.start()
                return

        self.fade_duration = self.ui.fadeDurationSlider.value()
        self.target_fps = self.ui.fpsSpinBox.value()
        self.frame_interval = 1000 // self.target_fps
        self.total_frames = self.fade_duration // self.frame_interval
        self.current_frame = 0

        self.fade_timer.start(self.frame_interval)

    def fade_out(self):
        if self.current_frame >= self.total_frames:
            if self.mouse:
                try:
                    self.mouse.set_color(RGBColor(0, 0, 0), fast=True)
                except Exception as e:
                    self.retry_timer.start()
                    return
            self.fade_timer.stop()
            return

        fade_factor = (self.total_frames - self.current_frame) / self.total_frames
        faded_color = RGBColor(
            max(0, int(self.current_color.red * fade_factor)),
            max(0, int(self.current_color.green * fade_factor)),
            max(0, int(self.current_color.blue * fade_factor)),
        )

        if self.mouse:
            try:
                self.mouse.set_color(faded_color, fast=True)
            except Exception as e:
                self.retry_timer.start()
                return

        self.current_frame += 1

    def create_default_settings(self):
        self.ui.rSpinBox.setValue(255)
        self.ui.gSpinBox.setValue(66)
        self.ui.bSpinBox.setValue(0)
        self.ui.fadeDurationSlider.setValue(500)
        self.ui.fpsSpinBox.setValue(60)

    def load_settings(self):
        os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, "r") as file:
                    settings = json.load(file)

                self.ui.rSpinBox.setValue(settings["red"])
                self.ui.gSpinBox.setValue(settings["green"])
                self.ui.bSpinBox.setValue(settings["blue"])
                self.ui.fadeDurationSlider.setValue(settings["fadeDuration"])
                self.ui.ipLineEdit.setText(settings["ip"])
                self.ui.portSpinBox.setValue(settings["port"])
                self.ui.randomCheckBox.setChecked(settings["random"])
                self.ui.fpsSpinBox.setValue(settings["fps"])
                self.ui.autostartCheckBox.setChecked(settings["autostart"])

                if settings["autostart"]:
                    self.ui.startstopButton.setText("Stop effect")
                    self.run_effect = True

            else:
                self.create_default_settings()
        except Exception as e:
            print(f"Unexpected error: {e}")
        self.save_settings()

    def save_settings(self):
        settings = {
            "red": self.ui.rSpinBox.value(),
            "green": self.ui.gSpinBox.value(),
            "blue": self.ui.bSpinBox.value(),
            "fadeDuration": self.ui.fadeDurationSlider.value(),
            "ip": self.ui.ipLineEdit.text(),
            "port": self.ui.portSpinBox.value(),
            "random": self.ui.randomCheckBox.isChecked(),
            "fps": self.ui.fpsSpinBox.value(),
            "autostart": self.ui.autostartCheckBox.isChecked(),
        }
        with open(self.settings_file, "w") as file:
            json.dump(settings, file)

    def create_tray_icon(self):
        icon = QIcon("resources/icon.png")
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(icon)
        self.tray_icon.setVisible(True)
        self.tray_icon.setToolTip("Mouse Reactive RGB")
        menu = QMenu()
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.cleanup)
        show_action = QAction("Show", self)
        show_action.triggered.connect(self.show)
        menu.addAction(show_action)
        menu.addAction(exit_action)
        self.tray_icon.setContextMenu(menu)

    def cleanup(self):
        self.retry_timer.stop()
        if self.mouse:
            self.mouse.set_color(RGBColor(0, 0, 0), fast=True)
        QApplication.quit()

    def on_startstopButton_clicked(self):
        if self.ui.startstopButton.text() == "Start effect":
            self.ui.startstopButton.setText("Stop effect")
            self.run_effect = True
        else:
            self.ui.startstopButton.setText("Start effect")
            self.fade_timer.stop()
            self.run_effect = False
            self.mouse.set_color(RGBColor(0, 0, 0))

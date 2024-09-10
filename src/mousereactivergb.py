from PyQt6.QtWidgets import QMainWindow, QSystemTrayIcon, QMenu, QApplication
from PyQt6.QtCore import QTimer, Qt, QMetaObject, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QAction
from ui_mousereactivergb import Ui_MouseReactiveRGB
from openrgb import OpenRGBClient
from openrgb.utils import RGBColor, DeviceType
from pynput.mouse import Listener, Button
from color_utils import set_frame_color_based_on_window
from utils import is_openrgb_running, get_icon, get_accent_color, get_settings_file, off
import os
import sys
import threading
import json
import random
import time
import colorsys


class MouseReactiveRGB(QMainWindow):
    start_timer_signal = pyqtSignal()
    stop_timer_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.ui = Ui_MouseReactiveRGB()
        self.ui.setupUi(self)
        self.setWindowIcon(get_icon(tiny=True))
        self.current_color = off
        self.settings_file = get_settings_file()
        self.first_hide_notification_sent = False
        self.client = None
        self.mouse = None
        self.connected = False
        self.run_effect = False
        self.first_run = False
        self.updating_widgets = False

        self.prepare_ui()
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

        self.start_timer_signal.connect(self.start_color_loop)
        self.stop_timer_signal.connect(self.stop_color_loop)

        self.color_loop_timer = QTimer(self)
        self.color_loop_timer.timeout.connect(self.color_loop)

        self.retry_timer.start(1000)

        if self.first_run:
            self.show()

    def prepare_ui(self):
        set_frame_color_based_on_window(self, self.ui.settingsFrame)
        set_frame_color_based_on_window(self, self.ui.effectFrame)
        self.ui.hexLineEdit.textChanged.connect(self.on_hex_line_edit_changed)
        self.ui.rSpinBox.valueChanged.connect(self.on_rgb_spinbox_changed)
        self.ui.gSpinBox.valueChanged.connect(self.on_rgb_spinbox_changed)
        self.ui.bSpinBox.valueChanged.connect(self.on_rgb_spinbox_changed)

        self.populateComboBox()

    def connect_ui_signals(self):
        self.ui.startstopButton.clicked.connect(self.on_startstopButton_clicked)
        self.ui.colorModeComboBox.currentIndexChanged.connect(self.on_colorModeComboBox_changed)

    def connect_to_openrgb(self):
        ip = self.ui.ipLineEdit.text()
        port = self.ui.portSpinBox.value()

        if not is_openrgb_running():
            return False

        try:
            self.client = OpenRGBClient(ip, port, "G502 Reactive RGB")

            devices = self.client.devices
            for device in devices:
                if device.type == DeviceType.MOUSE:
                    print(f"Found mouse: {device.name}")
                    if "Direct" in [mode.name for mode in device.modes]:
                        self.mouse = device
                        self.mouse.set_mode("Direct")
                        self.mouse.set_color(off)
                        print(f"Connected to {device.name} in Direct mode.")
                        return True
                    else:
                        print(f"{device.name}: Direct mode not supported.")
            return False
        except Exception as e:
            print(f"Failed to connect to OpenRGB: {e}")
            return False

    def disconnect_from_openrgb(self):
        if self.client:
            try:
                self.client.disconnect()
                self.client = None
                self.connected = False
            except Exception as e:
                print(f"Failed to disconnect: {e}")

    def retry_connection(self):
        if not self.connected:
            if self.connect_to_openrgb():
                self.on_connection_success()
            else:
                self.on_connection_failure()

    def on_connection_success(self):
        self.connected = True
        self.ui.connectionStatusButton.setText("Connected ✅")
        self.retry_timer.stop()

    def on_connection_failure(self):
        self.connected = False
        self.ui.connectionStatusButton.setText("Disconnected ❌")
        self.retry_timer.start(1000)

    def start_listener(self):
        with Listener(on_click=self.on_click) as listener:
            listener.join()

    @pyqtSlot()
    def start_color_loop(self):
        if not self.run_effect:
            return
        self.loop_color = self.get_color()
        target_fps = self.ui.fpsSpinBox.value()
        frame_interval = 1000 // target_fps
        self.color_loop_timer.start(frame_interval)

    @pyqtSlot()
    def stop_color_loop(self):
        self.color_loop_timer.stop()

    def on_click(self, x, y, button, pressed):
        if not self.connected:
            return

        selected_trigger = self.ui.triggerComboBox.currentIndex()

        if (
            (selected_trigger == 2 and button in [Button.left, Button.right])
            or (selected_trigger == 1 and button == Button.left)
            or (selected_trigger == 0)
        ):

            if pressed:
                if self.ui.fadeOnReleaseCheckBox.isChecked():
                    self.start_timer_signal.emit()
                QMetaObject.invokeMethod(self, "trigger_reactive_effect", Qt.ConnectionType.QueuedConnection)
            else:
                if self.ui.fadeOnReleaseCheckBox.isChecked():
                    self.stop_timer_signal.emit()
                    QMetaObject.invokeMethod(self, "start_fade_effect", Qt.ConnectionType.QueuedConnection)

    def color_loop(self):
        self.mouse.set_color(self.loop_color, fast=True)

    @pyqtSlot()
    def trigger_reactive_effect(self):
        if not self.mouse:
            self.retry_connection()

        if self.fade_timer.isActive():
            self.fade_timer.stop()
            self.mouse.set_color(self.get_color())

        self.start_reactive_effect()

    @pyqtSlot()
    def start_fade_effect(self):
        if not self.mouse:
            return

        if not self.run_effect:
            return

        self.current_frame = 0
        self.fade_duration = self.ui.fadeDurationSlider.value()
        self.target_fps = self.ui.fpsSpinBox.value()
        self.frame_interval = 1000 // self.target_fps
        self.total_frames = self.fade_duration // self.frame_interval

        if not self.fade_timer.isActive():
            self.fade_timer.start(self.frame_interval)

    def start_reactive_effect(self):
        if not self.mouse:
            return

        if not self.run_effect:
            return

        self.current_color = self.get_color()

        try:
            if self.ui.fadeOnReleaseCheckBox.isChecked() and self.ui.colorModeComboBox.currentIndex() == 1:
                self.current_color = self.loop_color

            self.mouse.set_color(self.current_color)
        except Exception as e:
            print(f"Failed to set color: {e}")
            self.retry_connection()
            self.connected = False
            self.retry_timer.start(1000)
            return
        if not self.ui.fadeOnReleaseCheckBox.isChecked():
            self.start_fade_effect()

    def fade_out(self):
        if self.current_frame >= self.total_frames:
            try:
                self.mouse.set_color(off)  # Set color to black after fade ends
            except Exception as e:
                print(f"Failed to set color: {e}")
                self.connected = False
                self.retry_connection()
                self.retry_timer.start(1000)

            self.fade_timer.stop()
            return

        fade_factor = (self.total_frames - self.current_frame) / self.total_frames
        faded_color = RGBColor(
            max(0, int(self.current_color.red * fade_factor)),
            max(0, int(self.current_color.green * fade_factor)),
            max(0, int(self.current_color.blue * fade_factor)),
        )

        try:
            self.mouse.set_color(faded_color, fast=True)
        except Exception as e:
            print(f"Failed to set color: {e}")
            self.connected = False
            self.retry_timer.start(1000)
            self.retry_connection()

        self.current_frame += 1

    def load_settings(self):
        os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, "r") as file:
                    settings = json.load(file)

                self.ui.rSpinBox.setValue(settings.get("red", 255))
                self.ui.gSpinBox.setValue(settings.get("green", 66))
                self.ui.bSpinBox.setValue(settings.get("blue", 0))
                self.ui.fadeDurationSlider.setValue(settings.get("fadeDuration", 500))
                self.ui.ipLineEdit.setText(settings.get("ip", "127.0.0.1"))
                self.ui.portSpinBox.setValue(settings.get("port", 6742))
                self.ui.fpsSpinBox.setValue(settings.get("fps", 60))
                self.ui.autostartCheckBox.setChecked(settings.get("autostart", False))
                self.ui.fadeOnReleaseCheckBox.setChecked(settings.get("fadeOnRelease", False))
                self.ui.colorModeComboBox.setCurrentIndex(settings.get("colorMode", 0))
                self.ui.triggerComboBox.setCurrentIndex(settings.get("trigger", 0))
                self.ui.brightnessSlider.setValue(settings.get("brightness", 100))
                self.ui.saturationSlider.setValue(settings.get("saturation", 100))

                enable_custom_color = self.ui.colorModeComboBox.currentIndex() == 0
                self.ui.rSpinBox.setEnabled(enable_custom_color)
                self.ui.gSpinBox.setEnabled(enable_custom_color)
                self.ui.bSpinBox.setEnabled(enable_custom_color)
                self.ui.hexLineEdit.setEnabled(enable_custom_color)
                self.on_rgb_spinbox_changed()

                self.first_hide_notification_sent = settings.get("firstHideNotificationSent", False)

                if settings["autostart"]:
                    self.ui.startstopButton.setText("Stop effect")
                    self.run_effect = True

            else:
                self.save_settings()
                self.first_run = True
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
            "fps": self.ui.fpsSpinBox.value(),
            "autostart": self.ui.autostartCheckBox.isChecked(),
            "fadeOnRelease": self.ui.fadeOnReleaseCheckBox.isChecked(),
            "colorMode": self.ui.colorModeComboBox.currentIndex(),
            "firstHideNotificationSent": self.first_hide_notification_sent,
            "trigger": self.ui.triggerComboBox.currentIndex(),
            "brightness": self.ui.brightnessSlider.value(),
            "saturation": self.ui.saturationSlider.value(),
        }
        with open(self.settings_file, "w") as file:
            json.dump(settings, file)

    def create_tray_icon(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(get_icon(tiny=True))
        self.tray_icon.setVisible(True)
        self.tray_icon.setToolTip("Mouse Reactive RGB")
        menu = QMenu()
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.cleanup)
        show_action = QAction("Show", self)
        show_action.triggered.connect(self.show_window)
        menu.addAction(show_action)
        menu.addAction(exit_action)
        self.tray_icon.setContextMenu(menu)

    def cleanup(self):
        self.color_loop_timer.stop()
        self.fade_timer.stop()
        self.retry_timer.stop()
        if self.mouse:
            self.mouse.set_color(off)
        self.disconnect_from_openrgb()

        QApplication.quit()

    def on_startstopButton_clicked(self):
        if self.ui.startstopButton.text() == "Start effect":
            self.ui.startstopButton.setText("Stop effect")
            self.run_effect = True
        else:
            self.ui.startstopButton.setText("Start effect")
            self.fade_timer.stop()
            self.run_effect = False
            if self.mouse:
                self.color_loop_timer.stop()
                time.sleep(0.05)
                self.mouse.set_color(off)

    def on_colorModeComboBox_changed(self):
        enable_custom_color = self.ui.colorModeComboBox.currentIndex() == 0
        self.ui.rSpinBox.setEnabled(enable_custom_color)
        self.ui.gSpinBox.setEnabled(enable_custom_color)
        self.ui.bSpinBox.setEnabled(enable_custom_color)
        self.save_settings()

    def get_color(self):
        if self.ui.colorModeComboBox.currentIndex() == 2:
            red, green, blue = get_accent_color()
        elif self.ui.colorModeComboBox.currentIndex() == 1:
            red, green, blue = (random.randint(0, 255) for _ in range(3))
        else:
            red, green, blue = self.ui.rSpinBox.value(), self.ui.gSpinBox.value(), self.ui.bSpinBox.value()

        brightness = self.ui.brightnessSlider.value() / 100
        saturation = self.ui.saturationSlider.value() / 100

        # Convert RGB to HSV
        r, g, b = red / 255.0, green / 255.0, blue / 255.0
        h, s, v = colorsys.rgb_to_hsv(r, g, b)

        # Apply saturation adjustment
        s *= saturation
        if s > 1:
            s = 1

        # Apply brightness adjustment
        v *= brightness
        if v > 1:
            v = 1

        # Convert HSV back to RGB
        r, g, b = colorsys.hsv_to_rgb(h, s, v)

        return RGBColor(int(r * 255), int(g * 255), int(b * 255))

    def populateComboBox(self):
        self.ui.colorModeComboBox.addItem("Custom")
        self.ui.colorModeComboBox.addItem("Random")
        if sys.platform == "win32":
            self.ui.colorModeComboBox.addItem("Accent")

        self.ui.triggerComboBox.addItem("Any button")
        self.ui.triggerComboBox.addItem("Left button")
        self.ui.triggerComboBox.addItem("Left / Right")

    def send_first_hide_notification(self):
        self.tray_icon.showMessage(
            "Mouse Reactive RGB",
            "The application is still running in the background.",
            get_icon(),
        )
        self.first_hide_notification_sent = True
        self.save_settings()

    def closeEvent(self, event):
        event.accept()
        self.save_settings()
        if not self.first_hide_notification_sent:
            self.send_first_hide_notification()

    def show_window(self):
        self.show()
        if self.isMinimized():
            self.showNormal()
        else:
            self.activateWindow()

    def on_hex_line_edit_changed(self):
        if self.updating_widgets:
            return

        hex_text = self.ui.hexLineEdit.text().strip("#")
        if len(hex_text) == 6:
            try:
                rgb = tuple(int(hex_text[i : i + 2], 16) for i in (0, 2, 4))
                self.updating_widgets = True
                self.ui.rSpinBox.setValue(rgb[0])
                self.ui.gSpinBox.setValue(rgb[1])
                self.ui.bSpinBox.setValue(rgb[2])
                self.updating_widgets = False
            except ValueError:
                pass

    def on_rgb_spinbox_changed(self):
        if self.updating_widgets:
            return

        r = self.ui.rSpinBox.value()
        g = self.ui.gSpinBox.value()
        b = self.ui.bSpinBox.value()

        hex_value = f"#{r:02X}{g:02X}{b:02X}"
        self.updating_widgets = True
        self.ui.hexLineEdit.setText(hex_value)
        self.updating_widgets = False

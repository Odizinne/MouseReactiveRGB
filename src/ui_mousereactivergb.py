# Form implementation generated from reading ui file '.\mousereactivergb.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MouseReactiveRGB(object):
    def setupUi(self, MouseReactiveRGB):
        MouseReactiveRGB.setObjectName("MouseReactiveRGB")
        MouseReactiveRGB.resize(350, 441)
        MouseReactiveRGB.setMinimumSize(QtCore.QSize(350, 0))
        self.centralwidget = QtWidgets.QWidget(parent=MouseReactiveRGB)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setSpacing(12)
        self.gridLayout.setObjectName("gridLayout")
        self.label_7 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_7.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setBold(True)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 0, 0, 1, 1)
        self.connectionStatusButton = QtWidgets.QToolButton(parent=self.centralwidget)
        self.connectionStatusButton.setMinimumSize(QtCore.QSize(0, 25))
        font = QtGui.QFont()
        font.setItalic(True)
        self.connectionStatusButton.setFont(font)
        self.connectionStatusButton.setObjectName("connectionStatusButton")
        self.gridLayout.addWidget(self.connectionStatusButton, 0, 1, 1, 1)
        self.effectFrame = QtWidgets.QFrame(parent=self.centralwidget)
        self.effectFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.effectFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.effectFrame.setObjectName("effectFrame")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.effectFrame)
        self.gridLayout_3.setSpacing(6)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.colorModeComboBox = QtWidgets.QComboBox(parent=self.effectFrame)
        self.colorModeComboBox.setMinimumSize(QtCore.QSize(0, 25))
        self.colorModeComboBox.setObjectName("colorModeComboBox")
        self.gridLayout_5.addWidget(self.colorModeComboBox, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_5.addItem(spacerItem, 0, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_5, 0, 1, 1, 2)
        self.frame = QtWidgets.QFrame(parent=self.effectFrame)
        self.frame.setAutoFillBackground(False)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.frame.setObjectName("frame")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setSpacing(6)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.fadeDurationSlider = QtWidgets.QSlider(parent=self.frame)
        self.fadeDurationSlider.setMinimumSize(QtCore.QSize(0, 25))
        self.fadeDurationSlider.setMinimum(250)
        self.fadeDurationSlider.setMaximum(2000)
        self.fadeDurationSlider.setSliderPosition(500)
        self.fadeDurationSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.fadeDurationSlider.setTickPosition(QtWidgets.QSlider.TickPosition.NoTicks)
        self.fadeDurationSlider.setObjectName("fadeDurationSlider")
        self.gridLayout_4.addWidget(self.fadeDurationSlider, 0, 0, 1, 1)
        self.gridLayout_4.setColumnStretch(0, 1)
        self.gridLayout_3.addWidget(self.frame, 4, 1, 1, 2)
        self.label_12 = QtWidgets.QLabel(parent=self.effectFrame)
        self.label_12.setMinimumSize(QtCore.QSize(0, 25))
        self.label_12.setObjectName("label_12")
        self.gridLayout_3.addWidget(self.label_12, 0, 0, 1, 1)
        self.label = QtWidgets.QLabel(parent=self.effectFrame)
        self.label.setMinimumSize(QtCore.QSize(31, 0))
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 1, 0, 1, 1)
        self.rSpinBox = QtWidgets.QSpinBox(parent=self.effectFrame)
        self.rSpinBox.setMinimumSize(QtCore.QSize(0, 25))
        self.rSpinBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.rSpinBox.setMaximum(255)
        self.rSpinBox.setObjectName("rSpinBox")
        self.gridLayout_3.addWidget(self.rSpinBox, 1, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(parent=self.effectFrame)
        self.label_2.setMinimumSize(QtCore.QSize(0, 0))
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 2, 0, 1, 1)
        self.gSpinBox = QtWidgets.QSpinBox(parent=self.effectFrame)
        self.gSpinBox.setMinimumSize(QtCore.QSize(0, 25))
        self.gSpinBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.gSpinBox.setMaximum(255)
        self.gSpinBox.setObjectName("gSpinBox")
        self.gridLayout_3.addWidget(self.gSpinBox, 2, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(parent=self.effectFrame)
        self.label_3.setMinimumSize(QtCore.QSize(31, 0))
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 3, 0, 1, 1)
        self.bSpinBox = QtWidgets.QSpinBox(parent=self.effectFrame)
        self.bSpinBox.setMinimumSize(QtCore.QSize(0, 25))
        self.bSpinBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.bSpinBox.setMaximum(255)
        self.bSpinBox.setObjectName("bSpinBox")
        self.gridLayout_3.addWidget(self.bSpinBox, 3, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(parent=self.effectFrame)
        self.label_4.setMinimumSize(QtCore.QSize(0, 0))
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 4, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(parent=self.effectFrame)
        self.label_10.setObjectName("label_10")
        self.gridLayout_3.addWidget(self.label_10, 5, 0, 1, 1)
        self.fpsSpinBox = QtWidgets.QSpinBox(parent=self.effectFrame)
        self.fpsSpinBox.setMinimumSize(QtCore.QSize(45, 25))
        self.fpsSpinBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.fpsSpinBox.setMinimum(10)
        self.fpsSpinBox.setMaximum(60)
        self.fpsSpinBox.setProperty("value", 60)
        self.fpsSpinBox.setObjectName("fpsSpinBox")
        self.gridLayout_3.addWidget(self.fpsSpinBox, 5, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_3.addItem(spacerItem1, 5, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(parent=self.effectFrame)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 6, 0, 1, 1)
        self.fadeOnReleaseCheckBox = QtWidgets.QCheckBox(parent=self.effectFrame)
        self.fadeOnReleaseCheckBox.setMinimumSize(QtCore.QSize(0, 25))
        self.fadeOnReleaseCheckBox.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.fadeOnReleaseCheckBox.setText("")
        self.fadeOnReleaseCheckBox.setObjectName("fadeOnReleaseCheckBox")
        self.gridLayout_3.addWidget(self.fadeOnReleaseCheckBox, 6, 2, 1, 1)
        self.gridLayout.addWidget(self.effectFrame, 3, 0, 1, 2)
        self.settingsFrame = QtWidgets.QFrame(parent=self.centralwidget)
        self.settingsFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.settingsFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.settingsFrame.setObjectName("settingsFrame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.settingsFrame)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_5 = QtWidgets.QLabel(parent=self.settingsFrame)
        self.label_5.setMinimumSize(QtCore.QSize(0, 0))
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 0, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 0, 1, 1, 1)
        self.label_11 = QtWidgets.QLabel(parent=self.settingsFrame)
        self.label_11.setMinimumSize(QtCore.QSize(0, 0))
        self.label_11.setObjectName("label_11")
        self.gridLayout_2.addWidget(self.label_11, 1, 0, 1, 1)
        self.portSpinBox = QtWidgets.QSpinBox(parent=self.settingsFrame)
        self.portSpinBox.setMinimumSize(QtCore.QSize(50, 25))
        self.portSpinBox.setMinimum(1)
        self.portSpinBox.setMaximum(65535)
        self.portSpinBox.setProperty("value", 6742)
        self.portSpinBox.setObjectName("portSpinBox")
        self.gridLayout_2.addWidget(self.portSpinBox, 0, 3, 1, 1)
        self.ipLineEdit = QtWidgets.QLineEdit(parent=self.settingsFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ipLineEdit.sizePolicy().hasHeightForWidth())
        self.ipLineEdit.setSizePolicy(sizePolicy)
        self.ipLineEdit.setMinimumSize(QtCore.QSize(0, 25))
        self.ipLineEdit.setObjectName("ipLineEdit")
        self.gridLayout_2.addWidget(self.ipLineEdit, 0, 2, 1, 1)
        self.autostartCheckBox = QtWidgets.QCheckBox(parent=self.settingsFrame)
        self.autostartCheckBox.setMinimumSize(QtCore.QSize(0, 25))
        self.autostartCheckBox.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.autostartCheckBox.setText("")
        self.autostartCheckBox.setObjectName("autostartCheckBox")
        self.gridLayout_2.addWidget(self.autostartCheckBox, 1, 2, 1, 2)
        self.gridLayout.addWidget(self.settingsFrame, 1, 0, 1, 2)
        self.label_8 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_8.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setBold(True)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 2, 0, 1, 2)
        self.startstopButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.startstopButton.setMinimumSize(QtCore.QSize(0, 25))
        self.startstopButton.setCheckable(False)
        self.startstopButton.setObjectName("startstopButton")
        self.gridLayout.addWidget(self.startstopButton, 4, 0, 1, 2)
        MouseReactiveRGB.setCentralWidget(self.centralwidget)

        self.retranslateUi(MouseReactiveRGB)
        QtCore.QMetaObject.connectSlotsByName(MouseReactiveRGB)

    def retranslateUi(self, MouseReactiveRGB):
        _translate = QtCore.QCoreApplication.translate
        MouseReactiveRGB.setWindowTitle(_translate("MouseReactiveRGB", "Mouse Reactive RGB"))
        self.label_7.setText(_translate("MouseReactiveRGB", "General Settings"))
        self.connectionStatusButton.setText(_translate("MouseReactiveRGB", "Disconnected ❌"))
        self.label_12.setText(_translate("MouseReactiveRGB", "Color mode"))
        self.label.setText(_translate("MouseReactiveRGB", "Red"))
        self.label_2.setText(_translate("MouseReactiveRGB", "Green"))
        self.label_3.setText(_translate("MouseReactiveRGB", "Blue"))
        self.label_4.setText(_translate("MouseReactiveRGB", "Fade duration"))
        self.label_10.setText(_translate("MouseReactiveRGB", "FPS"))
        self.label_6.setText(_translate("MouseReactiveRGB", "Fade on release"))
        self.label_5.setText(_translate("MouseReactiveRGB", "SDK IP / Port"))
        self.label_11.setText(_translate("MouseReactiveRGB", "Autostart effect"))
        self.ipLineEdit.setText(_translate("MouseReactiveRGB", "127.0.0.1"))
        self.label_8.setText(_translate("MouseReactiveRGB", "Reactive effect settings"))
        self.startstopButton.setText(_translate("MouseReactiveRGB", "Start effect"))

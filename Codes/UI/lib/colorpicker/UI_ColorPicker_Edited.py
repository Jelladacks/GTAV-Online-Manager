# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ColorPicker_EditedLCEGUX.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialogButtonBox, QFormLayout,
    QFrame, QHBoxLayout, QLabel, QLineEdit,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_ColorPicker(object):
    def setupUi(self, ColorPicker):
        if not ColorPicker.objectName():
            ColorPicker.setObjectName(u"ColorPicker")
        ColorPicker.resize(360, 272)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ColorPicker.sizePolicy().hasHeightForWidth())
        ColorPicker.setSizePolicy(sizePolicy)
        ColorPicker.setMinimumSize(QSize(0, 0))
        ColorPicker.setMaximumSize(QSize(360, 300))
        ColorPicker.setStyleSheet(u"QWidget{\n"
"	background-color: none;\n"
"}\n"
"QFrame{\n"
"	border-radius:5px;\n"
"}\n"
"\n"
"/*  LINE EDIT */\n"
"QLineEdit{\n"
"	color: rgb(221, 221, 221);\n"
"	background-color: #303030;\n"
"	border: 2px solid #303030;\n"
"	border-radius: 5px;\n"
"	selection-color: rgb(16, 16, 16);\n"
"	selection-background-color: rgb(221, 51, 34);\n"
"	font-family: Segoe UI;\n"
"	font-size: 11pt;\n"
"}\n"
"QLineEdit::focus{\n"
"	border-color: #aaaaaa;\n"
"}\n"
"")
        self.verticalLayout = QVBoxLayout(ColorPicker)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.ColorPickerMains = QWidget(ColorPicker)
        self.ColorPickerMains.setObjectName(u"ColorPickerMains")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.ColorPickerMains.sizePolicy().hasHeightForWidth())
        self.ColorPickerMains.setSizePolicy(sizePolicy1)
        self.ColorPickerMains.setMaximumSize(QSize(360, 200))
        self.horizontalLayout_5 = QHBoxLayout(self.ColorPickerMains)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.color_view = QFrame(self.ColorPickerMains)
        self.color_view.setObjectName(u"color_view")
        self.color_view.setMinimumSize(QSize(200, 200))
        self.color_view.setMaximumSize(QSize(5000, 5000))
        self.color_view.setStyleSheet(u"/* ALL CHANGES HERE WILL BE OVERWRITTEN */;\n"
"background-color: qlineargradient(x1:1, x2:0, stop:0 hsl(0%,100%,50%), stop:1 rgba(255, 255, 255, 255));\n"
"\n"
"")
        self.color_view.setFrameShape(QFrame.Shape.StyledPanel)
        self.color_view.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.color_view)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.black_overlay = QFrame(self.color_view)
        self.black_overlay.setObjectName(u"black_overlay")
        self.black_overlay.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(0, 0, 0, 0), stop:1 rgba(0, 0, 0, 255));\n"
"border-radius: 4px;\n"
"\n"
"")
        self.black_overlay.setFrameShape(QFrame.Shape.StyledPanel)
        self.black_overlay.setFrameShadow(QFrame.Shadow.Raised)
        self.selector = QFrame(self.black_overlay)
        self.selector.setObjectName(u"selector")
        self.selector.setGeometry(QRect(-6, 194, 12, 12))
        self.selector.setMinimumSize(QSize(12, 12))
        self.selector.setMaximumSize(QSize(12, 12))
        self.selector.setStyleSheet(u"background-color:none;\n"
"border: 1px solid white;\n"
"border-radius: 5px;")
        self.selector.setFrameShape(QFrame.Shape.StyledPanel)
        self.selector.setFrameShadow(QFrame.Shadow.Raised)
        self.black_ring = QLabel(self.selector)
        self.black_ring.setObjectName(u"black_ring")
        self.black_ring.setGeometry(QRect(1, 1, 10, 10))
        self.black_ring.setMinimumSize(QSize(10, 10))
        self.black_ring.setMaximumSize(QSize(10, 10))
        self.black_ring.setBaseSize(QSize(10, 10))
        self.black_ring.setStyleSheet(u"background-color: none;\n"
"border: 1px solid black;\n"
"border-radius: 5px;")

        self.verticalLayout_2.addWidget(self.black_overlay)


        self.horizontalLayout_5.addWidget(self.color_view)

        self.hue_frame = QFrame(self.ColorPickerMains)
        self.hue_frame.setObjectName(u"hue_frame")
        self.hue_frame.setMinimumSize(QSize(30, 0))
        self.hue_frame.setStyleSheet(u"QLabel{\n"
"	border-radius: 5px;\n"
"}")
        self.hue_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.hue_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.hue_bg = QFrame(self.hue_frame)
        self.hue_bg.setObjectName(u"hue_bg")
        self.hue_bg.setGeometry(QRect(10, 0, 20, 200))
        self.hue_bg.setMinimumSize(QSize(20, 200))
        self.hue_bg.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.166 rgba(255, 255, 0, 255), stop:0.333 rgba(0, 255, 0, 255), stop:0.5 rgba(0, 255, 255, 255), stop:0.666 rgba(0, 0, 255, 255), stop:0.833 rgba(255, 0, 255, 255), stop:1 rgba(255, 0, 0, 255));\n"
"border-radius: 5px;")
        self.hue_bg.setFrameShape(QFrame.Shape.StyledPanel)
        self.hue_bg.setFrameShadow(QFrame.Shadow.Raised)
        self.hue_selector = QLabel(self.hue_frame)
        self.hue_selector.setObjectName(u"hue_selector")
        self.hue_selector.setGeometry(QRect(7, 185, 26, 15))
        self.hue_selector.setMinimumSize(QSize(26, 0))
        self.hue_selector.setStyleSheet(u"background-color: #222;\n"
"")
        self.hue = QFrame(self.hue_frame)
        self.hue.setObjectName(u"hue")
        self.hue.setGeometry(QRect(7, 0, 26, 200))
        self.hue.setMinimumSize(QSize(20, 200))
        self.hue.setStyleSheet(u"")
        self.hue.setFrameShape(QFrame.Shape.StyledPanel)
        self.hue.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_5.addWidget(self.hue_frame)

        self.editfields = QFrame(self.ColorPickerMains)
        self.editfields.setObjectName(u"editfields")
        self.editfields.setMinimumSize(QSize(120, 200))
        self.editfields.setMaximumSize(QSize(120, 200))
        self.editfields.setStyleSheet(u"QLabel{\n"
"	font-family: Segoe UI;\n"
"font-weight: bold;\n"
"	font-size: 11pt;\n"
"	color: #aaaaaa;\n"
"	border-radius: 5px;\n"
"}\n"
"")
        self.editfields.setFrameShape(QFrame.Shape.StyledPanel)
        self.editfields.setFrameShadow(QFrame.Shadow.Raised)
        self.formLayout = QFormLayout(self.editfields)
        self.formLayout.setSpacing(5)
        self.formLayout.setContentsMargins(10, 10, 10, 10)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setHorizontalSpacing(5)
        self.formLayout.setVerticalSpacing(5)
        self.formLayout.setContentsMargins(5, 10, 15, 3)
        self.color_vis = QLabel(self.editfields)
        self.color_vis.setObjectName(u"color_vis")
        self.color_vis.setMinimumSize(QSize(0, 50))
        self.color_vis.setMaximumSize(QSize(16777215, 50))
        self.color_vis.setStyleSheet(u"/* ALL CHANGES HERE WILL BE OVERWRITTEN */;\n"
"background-color: #000;\n"
"")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.color_vis)

        self.lbl_red = QLabel(self.editfields)
        self.lbl_red.setObjectName(u"lbl_red")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lbl_red)

        self.red = QLineEdit(self.editfields)
        self.red.setObjectName(u"red")
        self.red.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.red.setClearButtonEnabled(False)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.red)

        self.lbl_green = QLabel(self.editfields)
        self.lbl_green.setObjectName(u"lbl_green")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.lbl_green)

        self.green = QLineEdit(self.editfields)
        self.green.setObjectName(u"green")
        self.green.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.green)

        self.lbl_blue = QLabel(self.editfields)
        self.lbl_blue.setObjectName(u"lbl_blue")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.lbl_blue)

        self.blue = QLineEdit(self.editfields)
        self.blue.setObjectName(u"blue")
        self.blue.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.blue)

        self.lbl_hex = QLabel(self.editfields)
        self.lbl_hex.setObjectName(u"lbl_hex")
        self.lbl_hex.setStyleSheet(u"font-size: 14pt;")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.lbl_hex)

        self.hex = QLineEdit(self.editfields)
        self.hex.setObjectName(u"hex")
        self.hex.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.hex)


        self.horizontalLayout_5.addWidget(self.editfields)


        self.verticalLayout.addWidget(self.ColorPickerMains)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(ColorPicker)
        self.label.setObjectName(u"label")
        palette = QPalette()
        brush = QBrush(QColor(170, 170, 170, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush)
        self.label.setPalette(palette)
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(11)
        font.setBold(True)
        self.label.setFont(font)

        self.horizontalLayout_2.addWidget(self.label)

        self.lineEdit = QLineEdit(ColorPicker)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout_2.addWidget(self.lineEdit)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.buttonBox = QDialogButtonBox(ColorPicker)
        self.buttonBox.setObjectName(u"buttonBox")
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setPointSize(11)
        self.buttonBox.setFont(font1)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Save)

        self.verticalLayout.addWidget(self.buttonBox)

#if QT_CONFIG(shortcut)
        self.lbl_red.setBuddy(self.red)
        self.lbl_green.setBuddy(self.green)
        self.lbl_blue.setBuddy(self.blue)
        self.lbl_hex.setBuddy(self.blue)
#endif // QT_CONFIG(shortcut)
        QWidget.setTabOrder(self.red, self.green)
        QWidget.setTabOrder(self.green, self.blue)

        self.retranslateUi(ColorPicker)

        QMetaObject.connectSlotsByName(ColorPicker)
    # setupUi

    def retranslateUi(self, ColorPicker):
        self.black_ring.setText("")
        self.hue_selector.setText("")
        self.color_vis.setText("")
        self.lbl_red.setText(QCoreApplication.translate("ColorPicker", u"R", None))
        self.red.setText(QCoreApplication.translate("ColorPicker", u"255", None))
        self.lbl_green.setText(QCoreApplication.translate("ColorPicker", u"G", None))
        self.green.setText(QCoreApplication.translate("ColorPicker", u"255", None))
        self.lbl_blue.setText(QCoreApplication.translate("ColorPicker", u"B", None))
        self.blue.setText(QCoreApplication.translate("ColorPicker", u"255", None))
        self.lbl_hex.setText(QCoreApplication.translate("ColorPicker", u"#", None))
        self.hex.setText(QCoreApplication.translate("ColorPicker", u"ffffff", None))
        self.label.setText(QCoreApplication.translate("ColorPicker", u"Crew Name", None))
        pass
    # retranslateUi


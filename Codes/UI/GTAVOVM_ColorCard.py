# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'GTAVOVM_ColorCardaotMfA.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QSizePolicy, QVBoxLayout, QWidget)

from Codes.UI.lib.ImageFittingLabel import ImageFittingLabel

class Ui_ColorPresetPreviewWidget(object):
    def setupUi(self, ColorPresetPreviewWidget):
        if not ColorPresetPreviewWidget.objectName():
            ColorPresetPreviewWidget.setObjectName(u"ColorPresetPreviewWidget")
        ColorPresetPreviewWidget.resize(300, 300)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ColorPresetPreviewWidget.sizePolicy().hasHeightForWidth())
        ColorPresetPreviewWidget.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(ColorPresetPreviewWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.ColorCardFrame = QFrame(ColorPresetPreviewWidget)
        self.ColorCardFrame.setObjectName(u"ColorCardFrame")
        self.ColorCardFrame.setEnabled(True)
        self.ColorCardFrame.setStyleSheet(u"")
        self.ColorCardFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.ColorCardFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.ColorPreviewFrame = QFrame(self.ColorCardFrame)
        self.ColorPreviewFrame.setObjectName(u"ColorPreviewFrame")
        self.ColorPreviewFrame.setEnabled(True)
        self.ColorPreviewFrame.setGeometry(QRect(0, 0, 300, 300))
        self.ColorPreviewFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.ColorPreviewFrame.setFrameShadow(QFrame.Shadow.Plain)
        self.ColorPreviewFrame.setLineWidth(0)
        self.horizontalLayout_2 = QHBoxLayout(self.ColorPreviewFrame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.NeonlightOutlineFrame = QFrame(self.ColorPreviewFrame)
        self.NeonlightOutlineFrame.setObjectName(u"NeonlightOutlineFrame")
        self.NeonlightOutlineFrame.setStyleSheet(u"#NeonlightOutlineFrame{\n"
"color:rgb(85, 0, 255)\n"
"}")
        self.NeonlightOutlineFrame.setFrameShape(QFrame.Shape.Panel)
        self.NeonlightOutlineFrame.setFrameShadow(QFrame.Shadow.Plain)
        self.NeonlightOutlineFrame.setLineWidth(5)
        self.PearlFrame = QFrame(self.NeonlightOutlineFrame)
        self.PearlFrame.setObjectName(u"PearlFrame")
        self.PearlFrame.setGeometry(QRect(5, 5, 289, 289))
        self.PearlFrame.setStyleSheet(u"#PearlFrame{\n"
"background-color:qlineargradient(spread:pad, x1:0.5, y1:0.443818, x2:0.840909, y2:0.869, stop:0.301136 rgba(255, 255, 255, 0), stop:1 rgba(255, 164, 0, 255))\n"
"}")
        self.PearlFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.PearlFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.LiveryImageLabel = ImageFittingLabel(self.NeonlightOutlineFrame)
        self.LiveryImageLabel.setObjectName(u"LiveryImageLabel")
        self.LiveryImageLabel.setGeometry(QRect(5, 5, 289, 289))
        font = QFont()
        font.setPointSize(20)
        font.setBold(False)
        self.LiveryImageLabel.setFont(font)
        self.LiveryImageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ColorPaletteFrame = QFrame(self.NeonlightOutlineFrame)
        self.ColorPaletteFrame.setObjectName(u"ColorPaletteFrame")
        self.ColorPaletteFrame.setGeometry(QRect(0, 5, 294, 289))
        self.ColorPaletteFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.ColorPaletteFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.ColorPaletteFrame)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.HeadlightColorFrame = QFrame(self.ColorPaletteFrame)
        self.HeadlightColorFrame.setObjectName(u"HeadlightColorFrame")
        self.HeadlightColorFrame.setStyleSheet(u"#HeadlightColorFrame{\n"
"background-color:rgb(255, 253, 242)\n"
"}")
        self.HeadlightColorFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.HeadlightColorFrame.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_3.addWidget(self.HeadlightColorFrame)

        self.WheelColorFrame = QFrame(self.ColorPaletteFrame)
        self.WheelColorFrame.setObjectName(u"WheelColorFrame")
        self.WheelColorFrame.setStyleSheet(u"#WheelColorFrame{\n"
"background-color:rgb(150, 20, 30)\n"
"}")
        self.WheelColorFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.WheelColorFrame.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_3.addWidget(self.WheelColorFrame)

        self.DialColorFrame = QFrame(self.ColorPaletteFrame)
        self.DialColorFrame.setObjectName(u"DialColorFrame")
        self.DialColorFrame.setStyleSheet(u"#DialColorFrame{\n"
"background-color:rgb(50, 30, 30)\n"
"}")
        self.DialColorFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.DialColorFrame.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_3.addWidget(self.DialColorFrame)

        self.TrimColorFrame = QFrame(self.ColorPaletteFrame)
        self.TrimColorFrame.setObjectName(u"TrimColorFrame")
        self.TrimColorFrame.setStyleSheet(u"#TrimColorFrame{\n"
"background-color:rgb(60, 70, 150)\n"
"}")
        self.TrimColorFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.TrimColorFrame.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_3.addWidget(self.TrimColorFrame)

        self.ScolorFrame = QFrame(self.ColorPaletteFrame)
        self.ScolorFrame.setObjectName(u"ScolorFrame")
        self.ScolorFrame.setStyleSheet(u"#ScolorFrame{\n"
"background-color:rgb(235, 255, 255)\n"
"}")
        self.ScolorFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.ScolorFrame.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_3.addWidget(self.ScolorFrame)

        self.PcolorFrame = QFrame(self.ColorPaletteFrame)
        self.PcolorFrame.setObjectName(u"PcolorFrame")
        self.PcolorFrame.setStyleSheet(u"#PcolorFrame{\n"
"background-color:rgb(255, 243, 242)\n"
"}")
        self.PcolorFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.PcolorFrame.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_3.addWidget(self.PcolorFrame)

        self.horizontalLayout_3.setStretch(0, 5)
        self.horizontalLayout_3.setStretch(1, 10)
        self.horizontalLayout_3.setStretch(2, 10)
        self.horizontalLayout_3.setStretch(3, 10)
        self.horizontalLayout_3.setStretch(4, 70)
        self.horizontalLayout_3.setStretch(5, 150)
        self.ColorPaletteFrame.raise_()
        self.LiveryImageLabel.raise_()
        self.PearlFrame.raise_()

        self.horizontalLayout_2.addWidget(self.NeonlightOutlineFrame)

        self.ColorDetailOverlayFrame = QFrame(self.ColorCardFrame)
        self.ColorDetailOverlayFrame.setObjectName(u"ColorDetailOverlayFrame")
        self.ColorDetailOverlayFrame.setGeometry(QRect(0, 0, 300, 300))
        self.ColorDetailOverlayFrame.setStyleSheet(u"#ColorDetailOverlayFrame{\n"
"background-color:rgba(0, 0, 0, 160)\n"
"}")
        self.ColorDetailOverlayFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.ColorDetailOverlayFrame.setFrameShadow(QFrame.Shadow.Plain)
        self.verticalLayout = QVBoxLayout(self.ColorDetailOverlayFrame)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(50, 50, 50, 50)
        self.PresetNameLabel = QLabel(self.ColorDetailOverlayFrame)
        self.PresetNameLabel.setObjectName(u"PresetNameLabel")
        font1 = QFont()
        font1.setPointSize(15)
        self.PresetNameLabel.setFont(font1)
        self.PresetNameLabel.setStyleSheet(u"#PresetNameLabel{\n"
"color:rgb(255, 255, 255)\n"
"}")
        self.PresetNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.PresetNameLabel.setMargin(8)

        self.verticalLayout.addWidget(self.PresetNameLabel)

        self.PrimaryColorGroup = QHBoxLayout()
        self.PrimaryColorGroup.setSpacing(0)
        self.PrimaryColorGroup.setObjectName(u"PrimaryColorGroup")
        self.PColorTagLabel = QLabel(self.ColorDetailOverlayFrame)
        self.PColorTagLabel.setObjectName(u"PColorTagLabel")
        self.PColorTagLabel.setStyleSheet(u"#PColorTagLabel{\n"
"color:rgb(255, 255, 255)\n"
"}")
        self.PColorTagLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.PrimaryColorGroup.addWidget(self.PColorTagLabel)

        self.PcolorTextLabel = QLabel(self.ColorDetailOverlayFrame)
        self.PcolorTextLabel.setObjectName(u"PcolorTextLabel")
        self.PcolorTextLabel.setStyleSheet(u"#PcolorTextLabel{\n"
"color:rgb(255, 255, 255)\n"
"}")

        self.PrimaryColorGroup.addWidget(self.PcolorTextLabel)


        self.verticalLayout.addLayout(self.PrimaryColorGroup)

        self.SecondaryColorGroup = QHBoxLayout()
        self.SecondaryColorGroup.setSpacing(0)
        self.SecondaryColorGroup.setObjectName(u"SecondaryColorGroup")
        self.ScolorTagLabel = QLabel(self.ColorDetailOverlayFrame)
        self.ScolorTagLabel.setObjectName(u"ScolorTagLabel")
        self.ScolorTagLabel.setStyleSheet(u"#ScolorTagLabel{\n"
"color:rgb(255, 255, 255)\n"
"}")
        self.ScolorTagLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.SecondaryColorGroup.addWidget(self.ScolorTagLabel)

        self.ScolorTextLabel = QLabel(self.ColorDetailOverlayFrame)
        self.ScolorTextLabel.setObjectName(u"ScolorTextLabel")
        self.ScolorTextLabel.setStyleSheet(u"#ScolorTextLabel{\n"
"color:rgb(255, 255, 255)\n"
"}")

        self.SecondaryColorGroup.addWidget(self.ScolorTextLabel)


        self.verticalLayout.addLayout(self.SecondaryColorGroup)

        self.PearlescentGroup = QHBoxLayout()
        self.PearlescentGroup.setSpacing(0)
        self.PearlescentGroup.setObjectName(u"PearlescentGroup")
        self.PearlTagLabel = QLabel(self.ColorDetailOverlayFrame)
        self.PearlTagLabel.setObjectName(u"PearlTagLabel")
        self.PearlTagLabel.setStyleSheet(u"#PearlTagLabel{\n"
"color:rgb(255, 255, 255)\n"
"}")
        self.PearlTagLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.PearlescentGroup.addWidget(self.PearlTagLabel)

        self.PearlTextGroup = QLabel(self.ColorDetailOverlayFrame)
        self.PearlTextGroup.setObjectName(u"PearlTextGroup")
        self.PearlTextGroup.setStyleSheet(u"#PearlTextGroup{\n"
"color:rgb(255, 255, 255)\n"
"}")

        self.PearlescentGroup.addWidget(self.PearlTextGroup)


        self.verticalLayout.addLayout(self.PearlescentGroup)

        self.LiveryGroup = QHBoxLayout()
        self.LiveryGroup.setSpacing(0)
        self.LiveryGroup.setObjectName(u"LiveryGroup")
        self.LiveryTagLabel = QLabel(self.ColorDetailOverlayFrame)
        self.LiveryTagLabel.setObjectName(u"LiveryTagLabel")
        self.LiveryTagLabel.setStyleSheet(u"#LiveryTagLabel{\n"
"color:rgb(255, 255, 255)\n"
"}")
        self.LiveryTagLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.LiveryGroup.addWidget(self.LiveryTagLabel)

        self.LiveryTextLabel = QLabel(self.ColorDetailOverlayFrame)
        self.LiveryTextLabel.setObjectName(u"LiveryTextLabel")
        self.LiveryTextLabel.setStyleSheet(u"#LiveryTextLabel{\n"
"color:rgb(255, 255, 255)\n"
"}")

        self.LiveryGroup.addWidget(self.LiveryTextLabel)


        self.verticalLayout.addLayout(self.LiveryGroup)

        self.WheelColorGroup = QHBoxLayout()
        self.WheelColorGroup.setSpacing(0)
        self.WheelColorGroup.setObjectName(u"WheelColorGroup")
        self.WheelTagLabel = QLabel(self.ColorDetailOverlayFrame)
        self.WheelTagLabel.setObjectName(u"WheelTagLabel")
        self.WheelTagLabel.setStyleSheet(u"#WheelTagLabel{\n"
"color:rgb(255, 255, 255)\n"
"}")
        self.WheelTagLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.WheelColorGroup.addWidget(self.WheelTagLabel)

        self.WheelTextLabel = QLabel(self.ColorDetailOverlayFrame)
        self.WheelTextLabel.setObjectName(u"WheelTextLabel")
        self.WheelTextLabel.setStyleSheet(u"#WheelTextLabel{\n"
"color:rgb(255, 255, 255)\n"
"}")

        self.WheelColorGroup.addWidget(self.WheelTextLabel)


        self.verticalLayout.addLayout(self.WheelColorGroup)

        self.DialColorGroup = QHBoxLayout()
        self.DialColorGroup.setSpacing(0)
        self.DialColorGroup.setObjectName(u"DialColorGroup")
        self.DialTagLabel = QLabel(self.ColorDetailOverlayFrame)
        self.DialTagLabel.setObjectName(u"DialTagLabel")
        self.DialTagLabel.setStyleSheet(u"#DialTagLabel{\n"
"color:rgb(255, 255, 255)\n"
"}")
        self.DialTagLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.DialColorGroup.addWidget(self.DialTagLabel)

        self.DialTextLabel = QLabel(self.ColorDetailOverlayFrame)
        self.DialTextLabel.setObjectName(u"DialTextLabel")
        self.DialTextLabel.setStyleSheet(u"#DialTextLabel{\n"
"color:rgb(255, 255, 255)\n"
"}")

        self.DialColorGroup.addWidget(self.DialTextLabel)


        self.verticalLayout.addLayout(self.DialColorGroup)

        self.TrimColorGroup = QHBoxLayout()
        self.TrimColorGroup.setSpacing(0)
        self.TrimColorGroup.setObjectName(u"TrimColorGroup")
        self.TrimTagLabel = QLabel(self.ColorDetailOverlayFrame)
        self.TrimTagLabel.setObjectName(u"TrimTagLabel")
        self.TrimTagLabel.setStyleSheet(u"#TrimTagLabel{\n"
"color:rgb(255, 255, 255)\n"
"}")
        self.TrimTagLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.TrimColorGroup.addWidget(self.TrimTagLabel)

        self.TrimTextLabel = QLabel(self.ColorDetailOverlayFrame)
        self.TrimTextLabel.setObjectName(u"TrimTextLabel")
        self.TrimTextLabel.setStyleSheet(u"#TrimTextLabel{\n"
"color:rgb(255, 255, 255)\n"
"}")

        self.TrimColorGroup.addWidget(self.TrimTextLabel)


        self.verticalLayout.addLayout(self.TrimColorGroup)

        self.NeonLightGroup = QHBoxLayout()
        self.NeonLightGroup.setSpacing(0)
        self.NeonLightGroup.setObjectName(u"NeonLightGroup")
        self.NeonlightTagLabel = QLabel(self.ColorDetailOverlayFrame)
        self.NeonlightTagLabel.setObjectName(u"NeonlightTagLabel")
        self.NeonlightTagLabel.setStyleSheet(u"#NeonlightTagLabel{\n"
"color:rgb(255, 255, 255)\n"
"}")
        self.NeonlightTagLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.NeonLightGroup.addWidget(self.NeonlightTagLabel)

        self.NeonTextLabel = QLabel(self.ColorDetailOverlayFrame)
        self.NeonTextLabel.setObjectName(u"NeonTextLabel")
        self.NeonTextLabel.setStyleSheet(u"#NeonTextLabel{\n"
"color:rgb(255, 255, 255)\n"
"}")

        self.NeonLightGroup.addWidget(self.NeonTextLabel)


        self.verticalLayout.addLayout(self.NeonLightGroup)

        self.HeadlightGroup = QHBoxLayout()
        self.HeadlightGroup.setSpacing(0)
        self.HeadlightGroup.setObjectName(u"HeadlightGroup")
        self.HeadlightTagLabel = QLabel(self.ColorDetailOverlayFrame)
        self.HeadlightTagLabel.setObjectName(u"HeadlightTagLabel")
        self.HeadlightTagLabel.setStyleSheet(u"#HeadlightTagLabel{\n"
"color:rgb(255, 255, 255)\n"
"}")
        self.HeadlightTagLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.HeadlightGroup.addWidget(self.HeadlightTagLabel)

        self.HeadlightTextLabel = QLabel(self.ColorDetailOverlayFrame)
        self.HeadlightTextLabel.setObjectName(u"HeadlightTextLabel")
        self.HeadlightTextLabel.setStyleSheet(u"#HeadlightTextLabel{\n"
"color:rgb(255, 255, 255)\n"
"}")

        self.HeadlightGroup.addWidget(self.HeadlightTextLabel)


        self.verticalLayout.addLayout(self.HeadlightGroup)


        self.horizontalLayout.addWidget(self.ColorCardFrame)


        self.retranslateUi(ColorPresetPreviewWidget)

        QMetaObject.connectSlotsByName(ColorPresetPreviewWidget)
    # setupUi

    def retranslateUi(self, ColorPresetPreviewWidget):
        ColorPresetPreviewWidget.setWindowTitle(QCoreApplication.translate("ColorPresetPreviewWidget", u"Form", None))
        self.LiveryImageLabel.setText(QCoreApplication.translate("ColorPresetPreviewWidget", u"Livery", None))
        self.PresetNameLabel.setText(QCoreApplication.translate("ColorPresetPreviewWidget", u"Preset Name", None))
        self.PColorTagLabel.setText(QCoreApplication.translate("ColorPresetPreviewWidget", u"Primary : ", None))
        self.PcolorTextLabel.setText(QCoreApplication.translate("ColorPresetPreviewWidget", u"Matte Black", None))
        self.ScolorTagLabel.setText(QCoreApplication.translate("ColorPresetPreviewWidget", u"Secondary : ", None))
        self.ScolorTextLabel.setText(QCoreApplication.translate("ColorPresetPreviewWidget", u"Metallic Earth Brown", None))
        self.PearlTagLabel.setText(QCoreApplication.translate("ColorPresetPreviewWidget", u"Pearlescent : ", None))
        self.PearlTextGroup.setText(QCoreApplication.translate("ColorPresetPreviewWidget", u"Ice White", None))
        self.LiveryTagLabel.setText(QCoreApplication.translate("ColorPresetPreviewWidget", u"Livery : ", None))
        self.LiveryTextLabel.setText(QCoreApplication.translate("ColorPresetPreviewWidget", u"Downtown Co. Cap", None))
        self.WheelTagLabel.setText(QCoreApplication.translate("ColorPresetPreviewWidget", u"Wheel : ", None))
        self.WheelTextLabel.setText(QCoreApplication.translate("ColorPresetPreviewWidget", u"Desert Green", None))
        self.DialTagLabel.setText(QCoreApplication.translate("ColorPresetPreviewWidget", u"Dial : ", None))
        self.DialTextLabel.setText(QCoreApplication.translate("ColorPresetPreviewWidget", u"Bronze", None))
        self.TrimTagLabel.setText(QCoreApplication.translate("ColorPresetPreviewWidget", u"Trim : ", None))
        self.TrimTextLabel.setText(QCoreApplication.translate("ColorPresetPreviewWidget", u"Defualt", None))
        self.NeonlightTagLabel.setText(QCoreApplication.translate("ColorPresetPreviewWidget", u"Neon : ", None))
        self.NeonTextLabel.setText(QCoreApplication.translate("ColorPresetPreviewWidget", u"Blacklight", None))
        self.HeadlightTagLabel.setText(QCoreApplication.translate("ColorPresetPreviewWidget", u"Headlight : ", None))
        self.HeadlightTextLabel.setText(QCoreApplication.translate("ColorPresetPreviewWidget", u"Red", None))
    # retranslateUi


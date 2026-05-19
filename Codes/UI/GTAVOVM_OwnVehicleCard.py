# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'GTAVOVM_OwnVCardRWPwRQ.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QHBoxLayout, QLayout, QPushButton, QSizePolicy,
    QSpacerItem, QStackedWidget, QVBoxLayout, QWidget)

from Codes.UI.lib.ImageFittingLabel import ImageFittingLabel
from Codes.UI.lib.NoWheelComboBox import NoWheelComboBox

class Ui_OwnVehicleInfoCardWidget(object):
    def setupUi(self, OwnVehicleInfoCardWidget):
        if not OwnVehicleInfoCardWidget.objectName():
            OwnVehicleInfoCardWidget.setObjectName(u"OwnVehicleInfoCardWidget")
        OwnVehicleInfoCardWidget.resize(350, 150)
        self.verticalLayout = QVBoxLayout(OwnVehicleInfoCardWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.OwnCardFrame = QFrame(OwnVehicleInfoCardWidget)
        self.OwnCardFrame.setObjectName(u"OwnCardFrame")
        self.OwnCardFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.OwnCardFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.GarageImageLabel = ImageFittingLabel(self.OwnCardFrame)
        self.GarageImageLabel.setObjectName(u"GarageImageLabel")
        self.GarageImageLabel.setGeometry(QRect(0, 0, 350, 150))
        self.GarageImageLabel.setPixmap(QPixmap(u":/newPrefix/D:/phs/GTA5/carbooks/BF Weevil/Grand Theft Auto V 2025-07-05 \uc624\ud6c4 3_14_49.png"))
        self.GarageImageLabel.setScaledContents(True)
        self.GarageImageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.OwnCardOverlayWidget = QWidget(self.OwnCardFrame)
        self.OwnCardOverlayWidget.setObjectName(u"OwnCardOverlayWidget")
        self.OwnCardOverlayWidget.setGeometry(QRect(0, 0, 350, 155))
        self.OwnCardOverlayWidget.setStyleSheet(u"#OwnCardOverlayWidget{\n"
"background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.67 rgba(255, 255, 255, 255), stop:1 rgba(255, 255, 255, 160))\n"
"}\n"
"")
        self.horizontalLayout_3 = QHBoxLayout(self.OwnCardOverlayWidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.OwnCardOverallLayout = QVBoxLayout()
        self.OwnCardOverallLayout.setObjectName(u"OwnCardOverallLayout")
        self.OwnCardTopBarFrame = QFrame(self.OwnCardOverlayWidget)
        self.OwnCardTopBarFrame.setObjectName(u"OwnCardTopBarFrame")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.OwnCardTopBarFrame.sizePolicy().hasHeightForWidth())
        self.OwnCardTopBarFrame.setSizePolicy(sizePolicy)
        self.OwnCardTopBarFrame.setMaximumSize(QSize(16777215, 16777206))
        self.OwnCardTopBarLayout = QHBoxLayout(self.OwnCardTopBarFrame)
        self.OwnCardTopBarLayout.setObjectName(u"OwnCardTopBarLayout")
        self.OwnCardTopBarLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.OwnCardTopBarLayout.setContentsMargins(0, 0, 0, 0)
        self.OwnPropertyComboBox = NoWheelComboBox(self.OwnCardTopBarFrame)
        self.OwnPropertyComboBox.setObjectName(u"OwnPropertyComboBox")
        self.OwnPropertyComboBox.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)

        self.OwnCardTopBarLayout.addWidget(self.OwnPropertyComboBox)

        self.horizontalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.OwnCardTopBarLayout.addItem(self.horizontalSpacer_2)

        self.ButtonStackedWidget = QStackedWidget(self.OwnCardTopBarFrame)
        self.ButtonStackedWidget.setObjectName(u"ButtonStackedWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.ButtonStackedWidget.sizePolicy().hasHeightForWidth())
        self.ButtonStackedWidget.setSizePolicy(sizePolicy1)
        self.ButtonStackedWidget.setMinimumSize(QSize(75, 0))
        self.SellButtonPage = QWidget()
        self.SellButtonPage.setObjectName(u"SellButtonPage")
        self.horizontalLayout = QHBoxLayout(self.SellButtonPage)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(10, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.SellButton = QPushButton(self.SellButtonPage)
        self.SellButton.setObjectName(u"SellButton")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.SellButton.sizePolicy().hasHeightForWidth())
        self.SellButton.setSizePolicy(sizePolicy2)
        font = QFont()
        font.setPointSize(7)
        self.SellButton.setFont(font)

        self.horizontalLayout.addWidget(self.SellButton)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)
        self.ButtonStackedWidget.addWidget(self.SellButtonPage)
        self.RestoreButtonPage = QWidget()
        self.RestoreButtonPage.setObjectName(u"RestoreButtonPage")
        self.horizontalLayout_2 = QHBoxLayout(self.RestoreButtonPage)
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.RemoveButton = QPushButton(self.RestoreButtonPage)
        self.RemoveButton.setObjectName(u"RemoveButton")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.RemoveButton.sizePolicy().hasHeightForWidth())
        self.RemoveButton.setSizePolicy(sizePolicy3)
        self.RemoveButton.setFont(font)

        self.horizontalLayout_2.addWidget(self.RemoveButton)

        self.RestoreButton = QPushButton(self.RestoreButtonPage)
        self.RestoreButton.setObjectName(u"RestoreButton")
        sizePolicy3.setHeightForWidth(self.RestoreButton.sizePolicy().hasHeightForWidth())
        self.RestoreButton.setSizePolicy(sizePolicy3)
        self.RestoreButton.setFont(font)

        self.horizontalLayout_2.addWidget(self.RestoreButton)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 1)
        self.ButtonStackedWidget.addWidget(self.RestoreButtonPage)

        self.OwnCardTopBarLayout.addWidget(self.ButtonStackedWidget)

        self.OwnCardTopBarLayout.setStretch(0, 8)
        self.OwnCardTopBarLayout.setStretch(1, 1)
        self.OwnCardTopBarLayout.setStretch(2, 3)

        self.OwnCardOverallLayout.addWidget(self.OwnCardTopBarFrame)

        self.OwnCardBottomBarFrame = QFrame(self.OwnCardOverlayWidget)
        self.OwnCardBottomBarFrame.setObjectName(u"OwnCardBottomBarFrame")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.OwnCardBottomBarFrame.sizePolicy().hasHeightForWidth())
        self.OwnCardBottomBarFrame.setSizePolicy(sizePolicy4)
        self.OwnCardBottomBarLayout = QHBoxLayout(self.OwnCardBottomBarFrame)
        self.OwnCardBottomBarLayout.setObjectName(u"OwnCardBottomBarLayout")
        self.CardPaintPresetPreviewWidget = QWidget(self.OwnCardBottomBarFrame)
        self.CardPaintPresetPreviewWidget.setObjectName(u"CardPaintPresetPreviewWidget")

        self.OwnCardBottomBarLayout.addWidget(self.CardPaintPresetPreviewWidget)

        self.CheckBoxGroup1Layout = QVBoxLayout()
        self.CheckBoxGroup1Layout.setSpacing(0)
        self.CheckBoxGroup1Layout.setObjectName(u"CheckBoxGroup1Layout")
        self.LimitedModCheckBox = QCheckBox(self.OwnCardBottomBarFrame)
        self.LimitedModCheckBox.setObjectName(u"LimitedModCheckBox")

        self.CheckBoxGroup1Layout.addWidget(self.LimitedModCheckBox)

        self.LimitedPlateCheckBox = QCheckBox(self.OwnCardBottomBarFrame)
        self.LimitedPlateCheckBox.setObjectName(u"LimitedPlateCheckBox")

        self.CheckBoxGroup1Layout.addWidget(self.LimitedPlateCheckBox)

        self.LimitedLiveryCheckBox = QCheckBox(self.OwnCardBottomBarFrame)
        self.LimitedLiveryCheckBox.setObjectName(u"LimitedLiveryCheckBox")

        self.CheckBoxGroup1Layout.addWidget(self.LimitedLiveryCheckBox)

        self.LimitedPaintCheckBox = QCheckBox(self.OwnCardBottomBarFrame)
        self.LimitedPaintCheckBox.setObjectName(u"LimitedPaintCheckBox")

        self.CheckBoxGroup1Layout.addWidget(self.LimitedPaintCheckBox)

        self.RewardCheckBox = QCheckBox(self.OwnCardBottomBarFrame)
        self.RewardCheckBox.setObjectName(u"RewardCheckBox")

        self.CheckBoxGroup1Layout.addWidget(self.RewardCheckBox)

        self.CheckBoxGroup1Layout.setStretch(0, 1)
        self.CheckBoxGroup1Layout.setStretch(1, 1)
        self.CheckBoxGroup1Layout.setStretch(2, 1)
        self.CheckBoxGroup1Layout.setStretch(3, 1)
        self.CheckBoxGroup1Layout.setStretch(4, 1)

        self.OwnCardBottomBarLayout.addLayout(self.CheckBoxGroup1Layout)

        self.CheckBoxGroup2Layout = QVBoxLayout()
        self.CheckBoxGroup2Layout.setSpacing(0)
        self.CheckBoxGroup2Layout.setObjectName(u"CheckBoxGroup2Layout")
        self.ModUpgradeCheckBox = QCheckBox(self.OwnCardBottomBarFrame)
        self.ModUpgradeCheckBox.setObjectName(u"ModUpgradeCheckBox")

        self.CheckBoxGroup2Layout.addWidget(self.ModUpgradeCheckBox)

        self.ModCustomCheckBox = QCheckBox(self.OwnCardBottomBarFrame)
        self.ModCustomCheckBox.setObjectName(u"ModCustomCheckBox")

        self.CheckBoxGroup2Layout.addWidget(self.ModCustomCheckBox)

        self.ModImaniCheckBox = QCheckBox(self.OwnCardBottomBarFrame)
        self.ModImaniCheckBox.setObjectName(u"ModImaniCheckBox")

        self.CheckBoxGroup2Layout.addWidget(self.ModImaniCheckBox)

        self.ModHSWCheckBox = QCheckBox(self.OwnCardBottomBarFrame)
        self.ModHSWCheckBox.setObjectName(u"ModHSWCheckBox")

        self.CheckBoxGroup2Layout.addWidget(self.ModHSWCheckBox)

        self.ModDriftCheckBox = QCheckBox(self.OwnCardBottomBarFrame)
        self.ModDriftCheckBox.setObjectName(u"ModDriftCheckBox")

        self.CheckBoxGroup2Layout.addWidget(self.ModDriftCheckBox)

        self.CheckBoxGroup2Layout.setStretch(0, 1)
        self.CheckBoxGroup2Layout.setStretch(1, 1)
        self.CheckBoxGroup2Layout.setStretch(2, 1)
        self.CheckBoxGroup2Layout.setStretch(3, 1)
        self.CheckBoxGroup2Layout.setStretch(4, 1)

        self.OwnCardBottomBarLayout.addLayout(self.CheckBoxGroup2Layout)

        self.OwnCardBottomBarLayout.setStretch(0, 1)
        self.OwnCardBottomBarLayout.setStretch(1, 1)
        self.OwnCardBottomBarLayout.setStretch(2, 1)

        self.OwnCardOverallLayout.addWidget(self.OwnCardBottomBarFrame)


        self.horizontalLayout_3.addLayout(self.OwnCardOverallLayout)


        self.verticalLayout.addWidget(self.OwnCardFrame)


        self.retranslateUi(OwnVehicleInfoCardWidget)

        self.ButtonStackedWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(OwnVehicleInfoCardWidget)
    # setupUi

    def retranslateUi(self, OwnVehicleInfoCardWidget):
        OwnVehicleInfoCardWidget.setWindowTitle(QCoreApplication.translate("OwnVehicleInfoCardWidget", u"Form", None))
        self.GarageImageLabel.setText("")
        self.SellButton.setText(QCoreApplication.translate("OwnVehicleInfoCardWidget", u"Sell", None))
        self.RemoveButton.setText(QCoreApplication.translate("OwnVehicleInfoCardWidget", u"Remove", None))
        self.RestoreButton.setText(QCoreApplication.translate("OwnVehicleInfoCardWidget", u"Restore", None))
        self.LimitedModCheckBox.setText(QCoreApplication.translate("OwnVehicleInfoCardWidget", u"Limited Mod", None))
        self.LimitedPlateCheckBox.setText(QCoreApplication.translate("OwnVehicleInfoCardWidget", u"Limited Plate", None))
        self.LimitedLiveryCheckBox.setText(QCoreApplication.translate("OwnVehicleInfoCardWidget", u"Limited Livery", None))
        self.LimitedPaintCheckBox.setText(QCoreApplication.translate("OwnVehicleInfoCardWidget", u"Limited Paint", None))
        self.RewardCheckBox.setText(QCoreApplication.translate("OwnVehicleInfoCardWidget", u"Reward", None))
        self.ModUpgradeCheckBox.setText(QCoreApplication.translate("OwnVehicleInfoCardWidget", u"Upgraded", None))
        self.ModCustomCheckBox.setText(QCoreApplication.translate("OwnVehicleInfoCardWidget", u"Customized", None))
        self.ModImaniCheckBox.setText(QCoreApplication.translate("OwnVehicleInfoCardWidget", u"Imani", None))
        self.ModHSWCheckBox.setText(QCoreApplication.translate("OwnVehicleInfoCardWidget", u"HSW", None))
        self.ModDriftCheckBox.setText(QCoreApplication.translate("OwnVehicleInfoCardWidget", u"Drift Mod", None))
    # retranslateUi


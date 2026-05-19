# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'GTAVOVM_GarageVCardZCzxxl.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QStackedWidget, QVBoxLayout, QWidget)

from Codes.UI.lib.ImageFittingLabel import ImageFittingLabel

class Ui_GarageVehicleCardWidget(object):
    def setupUi(self, GarageVehicleCardWidget):
        if not GarageVehicleCardWidget.objectName():
            GarageVehicleCardWidget.setObjectName(u"GarageVehicleCardWidget")
        GarageVehicleCardWidget.resize(320, 120)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(GarageVehicleCardWidget.sizePolicy().hasHeightForWidth())
        GarageVehicleCardWidget.setSizePolicy(sizePolicy)
        self.horizontalLayout_3 = QHBoxLayout(GarageVehicleCardWidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.GarageVehicleStackedWidget = QStackedWidget(GarageVehicleCardWidget)
        self.GarageVehicleStackedWidget.setObjectName(u"GarageVehicleStackedWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.GarageVehicleStackedWidget.sizePolicy().hasHeightForWidth())
        self.GarageVehicleStackedWidget.setSizePolicy(sizePolicy1)
        self.GarageVehicleStackedWidget.setFrameShape(QFrame.Shape.NoFrame)
        self.GarageVehicleDefaultPage = QWidget()
        self.GarageVehicleDefaultPage.setObjectName(u"GarageVehicleDefaultPage")
        self.horizontalLayout = QHBoxLayout(self.GarageVehicleDefaultPage)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, -1, 0, -1)
        self.VehicleImageLabel = ImageFittingLabel(self.GarageVehicleDefaultPage)
        self.VehicleImageLabel.setObjectName(u"VehicleImageLabel")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.VehicleImageLabel.sizePolicy().hasHeightForWidth())
        self.VehicleImageLabel.setSizePolicy(sizePolicy2)
        self.VehicleImageLabel.setPixmap(QPixmap(u":/newPrefix/D:/phs/GTA5/carbooks/BF Weevil/Grand Theft Auto V 2025-07-05 \uc624\ud6c4 3_14_49.png"))
        self.VehicleImageLabel.setScaledContents(False)

        self.horizontalLayout.addWidget(self.VehicleImageLabel)

        self.VehicleDataGroupLayout = QVBoxLayout()
        self.VehicleDataGroupLayout.setSpacing(0)
        self.VehicleDataGroupLayout.setObjectName(u"VehicleDataGroupLayout")
        self.ManufacturerLabel = QLabel(self.GarageVehicleDefaultPage)
        self.ManufacturerLabel.setObjectName(u"ManufacturerLabel")
        self.ManufacturerLabel.setStyleSheet(u"")
        self.ManufacturerLabel.setAlignment(Qt.AlignmentFlag.AlignBottom|Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft)
        self.ManufacturerLabel.setMargin(-3)
        self.ManufacturerLabel.setIndent(-1)

        self.VehicleDataGroupLayout.addWidget(self.ManufacturerLabel)

        self.VehicleNameLabel = QLabel(self.GarageVehicleDefaultPage)
        self.VehicleNameLabel.setObjectName(u"VehicleNameLabel")
        font = QFont()
        font.setPointSize(15)
        self.VehicleNameLabel.setFont(font)
        self.VehicleNameLabel.setStyleSheet(u"")
        self.VehicleNameLabel.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.VehicleNameLabel.setMargin(-3)

        self.VehicleDataGroupLayout.addWidget(self.VehicleNameLabel)

        self.GarageDefaultBottomBarLayout = QHBoxLayout()
        self.GarageDefaultBottomBarLayout.setObjectName(u"GarageDefaultBottomBarLayout")
        self.CardPaintPresetPreviewWidget = QWidget(self.GarageVehicleDefaultPage)
        self.CardPaintPresetPreviewWidget.setObjectName(u"CardPaintPresetPreviewWidget")

        self.GarageDefaultBottomBarLayout.addWidget(self.CardPaintPresetPreviewWidget)

        self.InfoGroupLayout = QVBoxLayout()
        self.InfoGroupLayout.setSpacing(0)
        self.InfoGroupLayout.setObjectName(u"InfoGroupLayout")
        self.ClassLabel = QLabel(self.GarageVehicleDefaultPage)
        self.ClassLabel.setObjectName(u"ClassLabel")
        self.ClassLabel.setStyleSheet(u"")

        self.InfoGroupLayout.addWidget(self.ClassLabel)

        self.PriceLabel = QLabel(self.GarageVehicleDefaultPage)
        self.PriceLabel.setObjectName(u"PriceLabel")
        self.PriceLabel.setStyleSheet(u"")

        self.InfoGroupLayout.addWidget(self.PriceLabel)


        self.GarageDefaultBottomBarLayout.addLayout(self.InfoGroupLayout)

        self.GarageDefaultBottomBarLayout.setStretch(0, 1)
        self.GarageDefaultBottomBarLayout.setStretch(1, 2)

        self.VehicleDataGroupLayout.addLayout(self.GarageDefaultBottomBarLayout)

        self.VehicleDataGroupLayout.setStretch(0, 1)
        self.VehicleDataGroupLayout.setStretch(1, 2)
        self.VehicleDataGroupLayout.setStretch(2, 4)

        self.horizontalLayout.addLayout(self.VehicleDataGroupLayout)

        self.PageButton = QPushButton(self.GarageVehicleDefaultPage)
        self.PageButton.setObjectName(u"PageButton")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.PageButton.sizePolicy().hasHeightForWidth())
        self.PageButton.setSizePolicy(sizePolicy3)

        self.horizontalLayout.addWidget(self.PageButton)

        self.horizontalLayout.setStretch(0, 3)
        self.horizontalLayout.setStretch(1, 5)
        self.horizontalLayout.setStretch(2, 1)
        self.GarageVehicleStackedWidget.addWidget(self.GarageVehicleDefaultPage)
        self.GarageVehicleDetailsPage = QWidget()
        self.GarageVehicleDetailsPage.setObjectName(u"GarageVehicleDetailsPage")
        self.horizontalLayout_2 = QHBoxLayout(self.GarageVehicleDetailsPage)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, -1, 0, -1)
        self.SellButton = QPushButton(self.GarageVehicleDetailsPage)
        self.SellButton.setObjectName(u"SellButton")
        sizePolicy3.setHeightForWidth(self.SellButton.sizePolicy().hasHeightForWidth())
        self.SellButton.setSizePolicy(sizePolicy3)
        self.SellButton.setIconSize(QSize(16, 16))
        self.SellButton.setAutoDefault(False)

        self.horizontalLayout_2.addWidget(self.SellButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.CheckBoxGroup1Layout = QVBoxLayout()
        self.CheckBoxGroup1Layout.setSpacing(0)
        self.CheckBoxGroup1Layout.setObjectName(u"CheckBoxGroup1Layout")
        self.LimitedModCheckBox = QCheckBox(self.GarageVehicleDetailsPage)
        self.LimitedModCheckBox.setObjectName(u"LimitedModCheckBox")

        self.CheckBoxGroup1Layout.addWidget(self.LimitedModCheckBox)

        self.LimitedPlateCheckBox = QCheckBox(self.GarageVehicleDetailsPage)
        self.LimitedPlateCheckBox.setObjectName(u"LimitedPlateCheckBox")

        self.CheckBoxGroup1Layout.addWidget(self.LimitedPlateCheckBox)

        self.LimitedLiveryCheckBox = QCheckBox(self.GarageVehicleDetailsPage)
        self.LimitedLiveryCheckBox.setObjectName(u"LimitedLiveryCheckBox")

        self.CheckBoxGroup1Layout.addWidget(self.LimitedLiveryCheckBox)

        self.LimitedPaintCheckBox = QCheckBox(self.GarageVehicleDetailsPage)
        self.LimitedPaintCheckBox.setObjectName(u"LimitedPaintCheckBox")

        self.CheckBoxGroup1Layout.addWidget(self.LimitedPaintCheckBox)

        self.RewardCheckBox = QCheckBox(self.GarageVehicleDetailsPage)
        self.RewardCheckBox.setObjectName(u"RewardCheckBox")

        self.CheckBoxGroup1Layout.addWidget(self.RewardCheckBox)

        self.CheckBoxGroup1Layout.setStretch(0, 1)
        self.CheckBoxGroup1Layout.setStretch(1, 1)
        self.CheckBoxGroup1Layout.setStretch(2, 1)
        self.CheckBoxGroup1Layout.setStretch(3, 1)
        self.CheckBoxGroup1Layout.setStretch(4, 1)

        self.horizontalLayout_2.addLayout(self.CheckBoxGroup1Layout)

        self.CheckBoxGroup2Layout = QVBoxLayout()
        self.CheckBoxGroup2Layout.setSpacing(0)
        self.CheckBoxGroup2Layout.setObjectName(u"CheckBoxGroup2Layout")
        self.ModUpgradeCheckBox = QCheckBox(self.GarageVehicleDetailsPage)
        self.ModUpgradeCheckBox.setObjectName(u"ModUpgradeCheckBox")

        self.CheckBoxGroup2Layout.addWidget(self.ModUpgradeCheckBox)

        self.ModCustomCheckBox = QCheckBox(self.GarageVehicleDetailsPage)
        self.ModCustomCheckBox.setObjectName(u"ModCustomCheckBox")

        self.CheckBoxGroup2Layout.addWidget(self.ModCustomCheckBox)

        self.ModImaniCheckBox = QCheckBox(self.GarageVehicleDetailsPage)
        self.ModImaniCheckBox.setObjectName(u"ModImaniCheckBox")

        self.CheckBoxGroup2Layout.addWidget(self.ModImaniCheckBox)

        self.ModHSWCheckBox = QCheckBox(self.GarageVehicleDetailsPage)
        self.ModHSWCheckBox.setObjectName(u"ModHSWCheckBox")

        self.CheckBoxGroup2Layout.addWidget(self.ModHSWCheckBox)

        self.ModDriftCheckBox = QCheckBox(self.GarageVehicleDetailsPage)
        self.ModDriftCheckBox.setObjectName(u"ModDriftCheckBox")

        self.CheckBoxGroup2Layout.addWidget(self.ModDriftCheckBox)

        self.CheckBoxGroup2Layout.setStretch(0, 1)
        self.CheckBoxGroup2Layout.setStretch(1, 1)
        self.CheckBoxGroup2Layout.setStretch(2, 1)
        self.CheckBoxGroup2Layout.setStretch(3, 1)
        self.CheckBoxGroup2Layout.setStretch(4, 1)

        self.horizontalLayout_2.addLayout(self.CheckBoxGroup2Layout)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.PageButton2 = QPushButton(self.GarageVehicleDetailsPage)
        self.PageButton2.setObjectName(u"PageButton2")
        sizePolicy2.setHeightForWidth(self.PageButton2.sizePolicy().hasHeightForWidth())
        self.PageButton2.setSizePolicy(sizePolicy2)

        self.horizontalLayout_2.addWidget(self.PageButton2)

        self.horizontalLayout_2.setStretch(0, 3)
        self.horizontalLayout_2.setStretch(1, 1)
        self.horizontalLayout_2.setStretch(2, 6)
        self.horizontalLayout_2.setStretch(3, 6)
        self.horizontalLayout_2.setStretch(4, 1)
        self.horizontalLayout_2.setStretch(5, 3)
        self.GarageVehicleStackedWidget.addWidget(self.GarageVehicleDetailsPage)

        self.horizontalLayout_3.addWidget(self.GarageVehicleStackedWidget)


        self.retranslateUi(GarageVehicleCardWidget)

        self.GarageVehicleStackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(GarageVehicleCardWidget)
    # setupUi

    def retranslateUi(self, GarageVehicleCardWidget):
        GarageVehicleCardWidget.setWindowTitle(QCoreApplication.translate("GarageVehicleCardWidget", u"Form", None))
        self.VehicleImageLabel.setText("")
        self.ManufacturerLabel.setText(QCoreApplication.translate("GarageVehicleCardWidget", u"  Manufacturer", None))
        self.VehicleNameLabel.setText(QCoreApplication.translate("GarageVehicleCardWidget", u" Vehicle Name", None))
        self.ClassLabel.setText(QCoreApplication.translate("GarageVehicleCardWidget", u"Class", None))
        self.PriceLabel.setText(QCoreApplication.translate("GarageVehicleCardWidget", u"Price", None))
        self.PageButton.setText(QCoreApplication.translate("GarageVehicleCardWidget", u"Page", None))
        self.SellButton.setText(QCoreApplication.translate("GarageVehicleCardWidget", u"Sell", None))
        self.LimitedModCheckBox.setText(QCoreApplication.translate("GarageVehicleCardWidget", u"Limited Mod", None))
        self.LimitedPlateCheckBox.setText(QCoreApplication.translate("GarageVehicleCardWidget", u"Limited Plate", None))
        self.LimitedLiveryCheckBox.setText(QCoreApplication.translate("GarageVehicleCardWidget", u"Limited Livery", None))
        self.LimitedPaintCheckBox.setText(QCoreApplication.translate("GarageVehicleCardWidget", u"Limited Paint", None))
        self.RewardCheckBox.setText(QCoreApplication.translate("GarageVehicleCardWidget", u"Reward", None))
        self.ModUpgradeCheckBox.setText(QCoreApplication.translate("GarageVehicleCardWidget", u"Upgraded", None))
        self.ModCustomCheckBox.setText(QCoreApplication.translate("GarageVehicleCardWidget", u"Customized", None))
        self.ModImaniCheckBox.setText(QCoreApplication.translate("GarageVehicleCardWidget", u"Imani", None))
        self.ModHSWCheckBox.setText(QCoreApplication.translate("GarageVehicleCardWidget", u"HSW", None))
        self.ModDriftCheckBox.setText(QCoreApplication.translate("GarageVehicleCardWidget", u"Drift Mod", None))
        self.PageButton2.setText(QCoreApplication.translate("GarageVehicleCardWidget", u"Page", None))
    # retranslateUi


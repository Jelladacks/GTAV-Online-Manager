# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'GTAVOVM_VehicleCardNQpMMR.ui'
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
    QSizePolicy, QSpacerItem, QStackedWidget, QVBoxLayout,
    QWidget)

from Codes.UI.lib.ImageFittingLabel import ImageFittingLabel
from Codes.UI.lib.ImageMinLabel import ImageMinLabel

class Ui_VehicleCardWidget(object):
    def setupUi(self, VehicleCardWidget):
        if not VehicleCardWidget.objectName():
            VehicleCardWidget.setObjectName(u"VehicleCardWidget")
        VehicleCardWidget.resize(400, 300)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(VehicleCardWidget.sizePolicy().hasHeightForWidth())
        VehicleCardWidget.setSizePolicy(sizePolicy)
        VehicleCardWidget.setMinimumSize(QSize(400, 300))
        VehicleCardWidget.setMaximumSize(QSize(400, 300))
        self.horizontalLayout = QHBoxLayout(VehicleCardWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.VehicleCardFrame = QFrame(VehicleCardWidget)
        self.VehicleCardFrame.setObjectName(u"VehicleCardFrame")
        self.VehicleCardFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.VehicleCardFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.VehicleImageLabel = ImageFittingLabel(self.VehicleCardFrame)
        self.VehicleImageLabel.setObjectName(u"VehicleImageLabel")
        self.VehicleImageLabel.setGeometry(QRect(0, 0, 400, 300))
        self.VehicleImageLabel.setPixmap(QPixmap(u":/newPrefix/D:/phs/GTA5/carbooks/BF Weevil/Grand Theft Auto V 2025-07-05 \uc624\ud6c4 3_14_49.png"))
        self.VehicleImageLabel.setScaledContents(False)
        self.VehicleImageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.VehicleCardStackedWidget = QStackedWidget(self.VehicleCardFrame)
        self.VehicleCardStackedWidget.setObjectName(u"VehicleCardStackedWidget")
        self.VehicleCardStackedWidget.setGeometry(QRect(-1, 0, 400, 300))
        self.VehicleCardStackedWidget.setStyleSheet(u"")
        self.CardDefault = QWidget()
        self.CardDefault.setObjectName(u"CardDefault")
        self.CardDefault.setStyleSheet(u"#CardDefault{\n"
"background-color:rgba(0,0,0,0)\n"
"}")
        self.verticalLayout = QVBoxLayout(self.CardDefault)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.CardTextGroupWidget = QWidget(self.CardDefault)
        self.CardTextGroupWidget.setObjectName(u"CardTextGroupWidget")
        self.CardTextGroupWidget.setStyleSheet(u"#CardTextGroupWidget {\n"
"    background-color: rgba(0, 0, 0, 160); \n"
"    color: white;\n"
"}")
        self.CardDefaultTextLayout = QVBoxLayout(self.CardTextGroupWidget)
        self.CardDefaultTextLayout.setSpacing(1)
        self.CardDefaultTextLayout.setObjectName(u"CardDefaultTextLayout")
        self.CardDefaultTextLayout.setContentsMargins(25, 10, 0, 13)
        self.ManufacturerLabel = QLabel(self.CardTextGroupWidget)
        self.ManufacturerLabel.setObjectName(u"ManufacturerLabel")
        self.ManufacturerLabel.setStyleSheet(u"#ManufacturerLabel{\n"
"color:rgb(255, 255, 255);\n"
"}")

        self.CardDefaultTextLayout.addWidget(self.ManufacturerLabel)

        self.VehicleNameLabel = QLabel(self.CardTextGroupWidget)
        self.VehicleNameLabel.setObjectName(u"VehicleNameLabel")
        font = QFont()
        font.setPointSize(15)
        self.VehicleNameLabel.setFont(font)
        self.VehicleNameLabel.setStyleSheet(u"#VehicleNameLabel{\n"
"color:rgb(255, 255, 255);\n"
"}")

        self.CardDefaultTextLayout.addWidget(self.VehicleNameLabel)

        self.AdditionalInfoLabel = QLabel(self.CardTextGroupWidget)
        self.AdditionalInfoLabel.setObjectName(u"AdditionalInfoLabel")
        self.AdditionalInfoLabel.setStyleSheet(u"#AdditionalInfoLabel{\n"
"color:rgb(255, 170, 0);\n"
"}")

        self.CardDefaultTextLayout.addWidget(self.AdditionalInfoLabel)


        self.verticalLayout.addWidget(self.CardTextGroupWidget)

        self.VehicleCardStackedWidget.addWidget(self.CardDefault)
        self.CardOverlay = QWidget()
        self.CardOverlay.setObjectName(u"CardOverlay")
        self.CardOverlay.setStyleSheet(u"#CardOverlay{\n"
"background-color:rgba(0, 0, 0, 160)\n"
"}")
        self.verticalLayout_2 = QVBoxLayout(self.CardOverlay)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(80, 40, 80, 40)
        self.CardManufacturerLogo = ImageMinLabel(self.CardOverlay)
        self.CardManufacturerLogo.setObjectName(u"CardManufacturerLogo")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.CardManufacturerLogo.sizePolicy().hasHeightForWidth())
        self.CardManufacturerLogo.setSizePolicy(sizePolicy1)
        self.CardManufacturerLogo.setMinimumSize(QSize(100, 100))
        self.CardManufacturerLogo.setStyleSheet(u"#CardManufacturerLogo{\n"
"color:rgb(255, 255, 255);\n"
"}")
        self.CardManufacturerLogo.setFrameShape(QFrame.Shape.NoFrame)
        self.CardManufacturerLogo.setLineWidth(3)
        self.CardManufacturerLogo.setMidLineWidth(0)
        self.CardManufacturerLogo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.CardManufacturerLogo.setMargin(0)

        self.verticalLayout_2.addWidget(self.CardManufacturerLogo)

        self.BackVehicleNameLabel = QLabel(self.CardOverlay)
        self.BackVehicleNameLabel.setObjectName(u"BackVehicleNameLabel")
        sizePolicy1.setHeightForWidth(self.BackVehicleNameLabel.sizePolicy().hasHeightForWidth())
        self.BackVehicleNameLabel.setSizePolicy(sizePolicy1)
        self.BackVehicleNameLabel.setFont(font)
        self.BackVehicleNameLabel.setStyleSheet(u"#BackVehicleNameLabel{\n"
"color:rgb(255, 255, 255);\n"
"}")
        self.BackVehicleNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.BackVehicleNameLabel)

        self.BackVehicleClassLabel = QLabel(self.CardOverlay)
        self.BackVehicleClassLabel.setObjectName(u"BackVehicleClassLabel")
        sizePolicy1.setHeightForWidth(self.BackVehicleClassLabel.sizePolicy().hasHeightForWidth())
        self.BackVehicleClassLabel.setSizePolicy(sizePolicy1)
        self.BackVehicleClassLabel.setStyleSheet(u"#BackVehicleClassLabel{\n"
"color:rgb(255, 255, 255);\n"
"}")
        self.BackVehicleClassLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.BackVehicleClassLabel)

        self.BackSpeedLayoutWidget = QWidget(self.CardOverlay)
        self.BackSpeedLayoutWidget.setObjectName(u"BackSpeedLayoutWidget")
        sizePolicy1.setHeightForWidth(self.BackSpeedLayoutWidget.sizePolicy().hasHeightForWidth())
        self.BackSpeedLayoutWidget.setSizePolicy(sizePolicy1)
        self.BackSpeedDataLayout = QHBoxLayout(self.BackSpeedLayoutWidget)
        self.BackSpeedDataLayout.setObjectName(u"BackSpeedDataLayout")
        self.BackSpeedDataLayout.setContentsMargins(0, 0, 0, 0)
        self.BackLaptimeLabel = QLabel(self.BackSpeedLayoutWidget)
        self.BackLaptimeLabel.setObjectName(u"BackLaptimeLabel")
        sizePolicy1.setHeightForWidth(self.BackLaptimeLabel.sizePolicy().hasHeightForWidth())
        self.BackLaptimeLabel.setSizePolicy(sizePolicy1)
        self.BackLaptimeLabel.setStyleSheet(u"#BackLaptimeLabel{\n"
"color:rgb(255, 255, 255);\n"
"}")
        self.BackLaptimeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.BackSpeedDataLayout.addWidget(self.BackLaptimeLabel)

        self.BackTopspeedLabel = QLabel(self.BackSpeedLayoutWidget)
        self.BackTopspeedLabel.setObjectName(u"BackTopspeedLabel")
        sizePolicy1.setHeightForWidth(self.BackTopspeedLabel.sizePolicy().hasHeightForWidth())
        self.BackTopspeedLabel.setSizePolicy(sizePolicy1)
        self.BackTopspeedLabel.setStyleSheet(u"#BackTopspeedLabel{\n"
"color:rgb(255, 255, 255);\n"
"}")
        self.BackTopspeedLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.BackSpeedDataLayout.addWidget(self.BackTopspeedLabel)


        self.verticalLayout_2.addWidget(self.BackSpeedLayoutWidget)

        self.BackPriceLabel = QLabel(self.CardOverlay)
        self.BackPriceLabel.setObjectName(u"BackPriceLabel")
        sizePolicy1.setHeightForWidth(self.BackPriceLabel.sizePolicy().hasHeightForWidth())
        self.BackPriceLabel.setSizePolicy(sizePolicy1)
        self.BackPriceLabel.setStyleSheet(u"#BackPriceLabel{\n"
"color:rgb(255, 255, 255);\n"
"}")
        self.BackPriceLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.BackPriceLabel)

        self.VehicleCardStackedWidget.addWidget(self.CardOverlay)

        self.horizontalLayout.addWidget(self.VehicleCardFrame)


        self.retranslateUi(VehicleCardWidget)

        self.VehicleCardStackedWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(VehicleCardWidget)
    # setupUi

    def retranslateUi(self, VehicleCardWidget):
        VehicleCardWidget.setWindowTitle(QCoreApplication.translate("VehicleCardWidget", u"Form", None))
        self.VehicleImageLabel.setText("")
        self.ManufacturerLabel.setText(QCoreApplication.translate("VehicleCardWidget", u"Manufacturer", None))
        self.VehicleNameLabel.setText(QCoreApplication.translate("VehicleCardWidget", u"Vehicle Name", None))
        self.AdditionalInfoLabel.setText(QCoreApplication.translate("VehicleCardWidget", u"TextLabel", None))
        self.CardManufacturerLogo.setText(QCoreApplication.translate("VehicleCardWidget", u"LOGO", None))
        self.BackVehicleNameLabel.setText(QCoreApplication.translate("VehicleCardWidget", u"Vehicle Name", None))
        self.BackVehicleClassLabel.setText(QCoreApplication.translate("VehicleCardWidget", u"Vehicle Class", None))
        self.BackLaptimeLabel.setText(QCoreApplication.translate("VehicleCardWidget", u"Laptime", None))
        self.BackTopspeedLabel.setText(QCoreApplication.translate("VehicleCardWidget", u"Topspeed", None))
        self.BackPriceLabel.setText(QCoreApplication.translate("VehicleCardWidget", u"Price", None))
    # retranslateUi


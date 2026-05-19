# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'GTAVOVM_PropertyCardBUhiyE.ui'
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

class Ui_PropertyCardWidget(object):
    def setupUi(self, PropertyCardWidget):
        if not PropertyCardWidget.objectName():
            PropertyCardWidget.setObjectName(u"PropertyCardWidget")
        PropertyCardWidget.resize(400, 300)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PropertyCardWidget.sizePolicy().hasHeightForWidth())
        PropertyCardWidget.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(PropertyCardWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.CardMainFrame = QFrame(PropertyCardWidget)
        self.CardMainFrame.setObjectName(u"CardMainFrame")
        self.CardMainFrame.setFrameShape(QFrame.Shape.Box)
        self.CardMainFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.CardMainFrame)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.lbl_image = ImageFittingLabel(self.CardMainFrame)
        self.lbl_image.setObjectName(u"lbl_image")
        self.lbl_image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.lbl_image)

        self.lbl_name = QLabel(self.CardMainFrame)
        self.lbl_name.setObjectName(u"lbl_name")
        self.lbl_name.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.lbl_name)

        self.lbl_price = QLabel(self.CardMainFrame)
        self.lbl_price.setObjectName(u"lbl_price")
        self.lbl_price.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.lbl_price)

        self.SelectionContainer = QFrame(self.CardMainFrame)
        self.SelectionContainer.setObjectName(u"SelectionContainer")
        self.SelectionContainer.setFrameShape(QFrame.Shape.StyledPanel)
        self.SelectionContainer.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.SelectionContainer)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")

        self.verticalLayout.addWidget(self.SelectionContainer)

        self.verticalLayout.setStretch(0, 15)
        self.verticalLayout.setStretch(1, 2)
        self.verticalLayout.setStretch(3, 2)

        self.horizontalLayout.addWidget(self.CardMainFrame)


        self.retranslateUi(PropertyCardWidget)

        QMetaObject.connectSlotsByName(PropertyCardWidget)
    # setupUi

    def retranslateUi(self, PropertyCardWidget):
        PropertyCardWidget.setWindowTitle(QCoreApplication.translate("PropertyCardWidget", u"Form", None))
        self.lbl_image.setText(QCoreApplication.translate("PropertyCardWidget", u"PropertyImage", None))
        self.lbl_name.setText(QCoreApplication.translate("PropertyCardWidget", u"Property Name", None))
        self.lbl_price.setText(QCoreApplication.translate("PropertyCardWidget", u"Property Price", None))
    # retranslateUi


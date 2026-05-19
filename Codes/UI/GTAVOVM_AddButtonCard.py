# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'GTAVOVM_AddButtonCarduVaghi.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QLabel,
    QSizePolicy, QWidget)

class Ui_AddButtonCardWidget(object):
    def setupUi(self, AddButtonCardWidget):
        if not AddButtonCardWidget.objectName():
            AddButtonCardWidget.setObjectName(u"AddButtonCardWidget")
        AddButtonCardWidget.resize(250, 250)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AddButtonCardWidget.sizePolicy().hasHeightForWidth())
        AddButtonCardWidget.setSizePolicy(sizePolicy)
        AddButtonCardWidget.setStyleSheet(u"")
        self.gridLayout_2 = QGridLayout(AddButtonCardWidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.MainFrame = QFrame(AddButtonCardWidget)
        self.MainFrame.setObjectName(u"MainFrame")
        self.MainFrame.setStyleSheet(u"#MainFrame {\n"
"    border: 3px dashed #D1D1D1;    /* \ub450\uaed8 3px, \uc810\uc120(dashed), \uc5f0\ud68c\uc0c9 */\n"
"    border-radius: 20px;           /* \ubaa8\uc11c\ub9ac\ub97c \ub465\uae00\uac8c */\n"
"    /*background-color: #F9F9F9;      \uc544\uc8fc \uc5f0\ud55c \ud68c\uc0c9 \ubc30\uacbd */\n"
"}\n"
"\n"
"#MainFrame:hover {\n"
"    border: 3px dashed #3498DB;    /* \ud14c\ub450\ub9ac\ub97c \ud30c\ub780\uc0c9\uc73c\ub85c \ubcc0\uacbd */\n"
"    /*background-color: #F0F7FF;      \ubc30\uacbd\uc744 \uc544\uc8fc \uc5f0\ud55c \ud30c\ub780\uc0c9\uc73c\ub85c */\n"
"}")
        self.MainFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.MainFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.MainFrame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.PlusLabel = QLabel(self.MainFrame)
        self.PlusLabel.setObjectName(u"PlusLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.PlusLabel.sizePolicy().hasHeightForWidth())
        self.PlusLabel.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setPointSize(50)
        self.PlusLabel.setFont(font)
        self.PlusLabel.setStyleSheet(u"#PlusLabel{\n"
"color:rgb(130, 200, 120)\n"
"}")
        self.PlusLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.PlusLabel.setMargin(-5)

        self.gridLayout.addWidget(self.PlusLabel, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.MainFrame, 0, 0, 1, 1)


        self.retranslateUi(AddButtonCardWidget)

        QMetaObject.connectSlotsByName(AddButtonCardWidget)
    # setupUi

    def retranslateUi(self, AddButtonCardWidget):
        AddButtonCardWidget.setWindowTitle(QCoreApplication.translate("AddButtonCardWidget", u"Form", None))
        self.PlusLabel.setText(QCoreApplication.translate("AddButtonCardWidget", u"+", None))
    # retranslateUi


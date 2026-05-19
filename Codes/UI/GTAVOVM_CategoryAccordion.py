# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'GTAVOVM_CategoryAccordionjgiUNm.ui'
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

class Ui_CategoryAccordianWidget(object):
    def setupUi(self, CategoryAccordianWidget):
        if not CategoryAccordianWidget.objectName():
            CategoryAccordianWidget.setObjectName(u"CategoryAccordianWidget")
        CategoryAccordianWidget.resize(291, 154)
        self.verticalLayout = QVBoxLayout(CategoryAccordianWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.HeaderFrame = QFrame(CategoryAccordianWidget)
        self.HeaderFrame.setObjectName(u"HeaderFrame")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.HeaderFrame.sizePolicy().hasHeightForWidth())
        self.HeaderFrame.setSizePolicy(sizePolicy)
        self.HeaderFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.HeaderFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.HeaderFrame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lbl_arrow = QLabel(self.HeaderFrame)
        self.lbl_arrow.setObjectName(u"lbl_arrow")
        sizePolicy.setHeightForWidth(self.lbl_arrow.sizePolicy().hasHeightForWidth())
        self.lbl_arrow.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.lbl_arrow)

        self.lbl_title = QLabel(self.HeaderFrame)
        self.lbl_title.setObjectName(u"lbl_title")
        font = QFont()
        font.setPointSize(12)
        self.lbl_title.setFont(font)

        self.horizontalLayout.addWidget(self.lbl_title)


        self.verticalLayout.addWidget(self.HeaderFrame)

        self.ContentFrame = QFrame(CategoryAccordianWidget)
        self.ContentFrame.setObjectName(u"ContentFrame")
        self.ContentFrame.setFrameShape(QFrame.Shape.Box)
        self.ContentFrame.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout.addWidget(self.ContentFrame)


        self.retranslateUi(CategoryAccordianWidget)

        QMetaObject.connectSlotsByName(CategoryAccordianWidget)
    # setupUi

    def retranslateUi(self, CategoryAccordianWidget):
        CategoryAccordianWidget.setWindowTitle(QCoreApplication.translate("CategoryAccordianWidget", u"Form", None))
        self.lbl_arrow.setText(QCoreApplication.translate("CategoryAccordianWidget", u"\u25b6", None))
        self.lbl_title.setText(QCoreApplication.translate("CategoryAccordianWidget", u"Category Name", None))
    # retranslateUi


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'GTAVOVM_ACQcardqNNalm.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QSizePolicy, QWidget)

from Codes.UI.lib.ImageFittingLabel import ImageFittingLabel

class Ui_ACQWidget(object):
    def setupUi(self, ACQWidget):
        if not ACQWidget.objectName():
            ACQWidget.setObjectName(u"ACQWidget")
        ACQWidget.resize(400, 40)
        self.ACQTextLabel = QLabel(ACQWidget)
        self.ACQTextLabel.setObjectName(u"ACQTextLabel")
        self.ACQTextLabel.setGeometry(QRect(0, 0, 400, 40))
        self.ACQTextLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ACQImageLabel = ImageFittingLabel(ACQWidget)
        self.ACQImageLabel.setObjectName(u"ACQImageLabel")
        self.ACQImageLabel.setGeometry(QRect(0, 0, 400, 40))
        self.ACQImageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ACQImageLabel.raise_()
        self.ACQTextLabel.raise_()

        self.retranslateUi(ACQWidget)

        QMetaObject.connectSlotsByName(ACQWidget)
    # setupUi

    def retranslateUi(self, ACQWidget):
        ACQWidget.setWindowTitle(QCoreApplication.translate("ACQWidget", u"Form", None))
        self.ACQTextLabel.setText(QCoreApplication.translate("ACQWidget", u"TextLabel", None))
        self.ACQImageLabel.setText(QCoreApplication.translate("ACQWidget", u"Imaeg", None))
    # retranslateUi


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'GTAVOVM_ColorRefWidgetfXMPQb.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QSizePolicy,
    QWidget)

class Ui_ColorRefWidget(object):
    def setupUi(self, ColorRefWidget):
        if not ColorRefWidget.objectName():
            ColorRefWidget.setObjectName(u"ColorRefWidget")
        ColorRefWidget.resize(400, 30)
        ColorRefWidget.setMinimumSize(QSize(0, 30))
        ColorRefWidget.setMaximumSize(QSize(16777215, 30))
        self.horizontalLayout = QHBoxLayout(ColorRefWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.ColorTextLabel = QLabel(ColorRefWidget)
        self.ColorTextLabel.setObjectName(u"ColorTextLabel")
        self.ColorTextLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.ColorTextLabel)


        self.retranslateUi(ColorRefWidget)

        QMetaObject.connectSlotsByName(ColorRefWidget)
    # setupUi

    def retranslateUi(self, ColorRefWidget):
        ColorRefWidget.setWindowTitle(QCoreApplication.translate("ColorRefWidget", u"Form", None))
        self.ColorTextLabel.setText(QCoreApplication.translate("ColorRefWidget", u"Unknown", None))
    # retranslateUi


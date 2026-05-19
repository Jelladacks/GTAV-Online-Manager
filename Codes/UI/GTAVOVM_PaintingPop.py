# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'GTAVOVM_PaintingPoprShsNK.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QTreeView,
    QVBoxLayout, QWidget)

class Ui_PaintManager(object):
    def setupUi(self, PaintManager):
        if not PaintManager.objectName():
            PaintManager.setObjectName(u"PaintManager")
        PaintManager.resize(750, 601)
        self.horizontalLayout_8 = QHBoxLayout(PaintManager)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.PaintManagerGlobal = QVBoxLayout()
        self.PaintManagerGlobal.setObjectName(u"PaintManagerGlobal")
        self.PaintManagerMainWidget = QWidget(PaintManager)
        self.PaintManagerMainWidget.setObjectName(u"PaintManagerMainWidget")
        self.verticalLayout = QVBoxLayout(self.PaintManagerMainWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.PaintManagerOverallLayout = QHBoxLayout()
        self.PaintManagerOverallLayout.setObjectName(u"PaintManagerOverallLayout")
        self.treeView = QTreeView(self.PaintManagerMainWidget)
        self.treeView.setObjectName(u"treeView")

        self.PaintManagerOverallLayout.addWidget(self.treeView)

        self.ColorPanelRightLayout = QVBoxLayout()
        self.ColorPanelRightLayout.setObjectName(u"ColorPanelRightLayout")
        self.ColorPreview = QWidget(self.PaintManagerMainWidget)
        self.ColorPreview.setObjectName(u"ColorPreview")

        self.ColorPanelRightLayout.addWidget(self.ColorPreview)

        self.ColorInfoLayout = QVBoxLayout()
        self.ColorInfoLayout.setObjectName(u"ColorInfoLayout")
        self.ColorInfoLayout.setContentsMargins(-1, -1, -1, 0)
        self.PresetNameBarLayout = QHBoxLayout()
        self.PresetNameBarLayout.setObjectName(u"PresetNameBarLayout")
        self.PresetNameBarLayout.setContentsMargins(-1, 0, -1, -1)
        self.PresetNameLabel = QLabel(self.PaintManagerMainWidget)
        self.PresetNameLabel.setObjectName(u"PresetNameLabel")

        self.PresetNameBarLayout.addWidget(self.PresetNameLabel)

        self.PresetNameEditor = QLineEdit(self.PaintManagerMainWidget)
        self.PresetNameEditor.setObjectName(u"PresetNameEditor")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PresetNameEditor.sizePolicy().hasHeightForWidth())
        self.PresetNameEditor.setSizePolicy(sizePolicy)

        self.PresetNameBarLayout.addWidget(self.PresetNameEditor)

        self.PresetNameBarLayout.setStretch(0, 1)
        self.PresetNameBarLayout.setStretch(1, 2)

        self.ColorInfoLayout.addLayout(self.PresetNameBarLayout)

        self.PrimaryPaintBarLayout = QHBoxLayout()
        self.PrimaryPaintBarLayout.setObjectName(u"PrimaryPaintBarLayout")
        self.PrimaryColorLabel = QLabel(self.PaintManagerMainWidget)
        self.PrimaryColorLabel.setObjectName(u"PrimaryColorLabel")

        self.PrimaryPaintBarLayout.addWidget(self.PrimaryColorLabel)

        self.PrimaryColorFrame = QWidget(self.PaintManagerMainWidget)
        self.PrimaryColorFrame.setObjectName(u"PrimaryColorFrame")

        self.PrimaryPaintBarLayout.addWidget(self.PrimaryColorFrame)

        self.PrimaryComboBox = QComboBox(self.PaintManagerMainWidget)
        self.PrimaryComboBox.setObjectName(u"PrimaryComboBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.PrimaryComboBox.sizePolicy().hasHeightForWidth())
        self.PrimaryComboBox.setSizePolicy(sizePolicy1)

        self.PrimaryPaintBarLayout.addWidget(self.PrimaryComboBox)


        self.ColorInfoLayout.addLayout(self.PrimaryPaintBarLayout)

        self.SecondaryPaintBarLayout = QHBoxLayout()
        self.SecondaryPaintBarLayout.setObjectName(u"SecondaryPaintBarLayout")
        self.SecondaryColorLabel = QLabel(self.PaintManagerMainWidget)
        self.SecondaryColorLabel.setObjectName(u"SecondaryColorLabel")
        self.SecondaryColorLabel.setScaledContents(False)

        self.SecondaryPaintBarLayout.addWidget(self.SecondaryColorLabel)

        self.SecondaryColorFrame = QWidget(self.PaintManagerMainWidget)
        self.SecondaryColorFrame.setObjectName(u"SecondaryColorFrame")

        self.SecondaryPaintBarLayout.addWidget(self.SecondaryColorFrame)

        self.SecondaryComboBox = QComboBox(self.PaintManagerMainWidget)
        self.SecondaryComboBox.setObjectName(u"SecondaryComboBox")
        sizePolicy1.setHeightForWidth(self.SecondaryComboBox.sizePolicy().hasHeightForWidth())
        self.SecondaryComboBox.setSizePolicy(sizePolicy1)

        self.SecondaryPaintBarLayout.addWidget(self.SecondaryComboBox)


        self.ColorInfoLayout.addLayout(self.SecondaryPaintBarLayout)

        self.SubColorPaintBarLayout = QHBoxLayout()
        self.SubColorPaintBarLayout.setSpacing(5)
        self.SubColorPaintBarLayout.setObjectName(u"SubColorPaintBarLayout")
        self.PearlAndLiveryBarLayout = QVBoxLayout()
        self.PearlAndLiveryBarLayout.setObjectName(u"PearlAndLiveryBarLayout")
        self.PearlPaintBarLayout = QHBoxLayout()
        self.PearlPaintBarLayout.setObjectName(u"PearlPaintBarLayout")
        self.PearlLabel = QLabel(self.PaintManagerMainWidget)
        self.PearlLabel.setObjectName(u"PearlLabel")

        self.PearlPaintBarLayout.addWidget(self.PearlLabel)

        self.PearlColorFrame = QWidget(self.PaintManagerMainWidget)
        self.PearlColorFrame.setObjectName(u"PearlColorFrame")

        self.PearlPaintBarLayout.addWidget(self.PearlColorFrame)


        self.PearlAndLiveryBarLayout.addLayout(self.PearlPaintBarLayout)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.LiveryColorLabel = QLabel(self.PaintManagerMainWidget)
        self.LiveryColorLabel.setObjectName(u"LiveryColorLabel")
        self.LiveryColorLabel.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_9.addWidget(self.LiveryColorLabel)

        self.LiveryColorFrame = QWidget(self.PaintManagerMainWidget)
        self.LiveryColorFrame.setObjectName(u"LiveryColorFrame")

        self.horizontalLayout_9.addWidget(self.LiveryColorFrame)

        self.horizontalLayout_9.setStretch(0, 1)
        self.horizontalLayout_9.setStretch(1, 2)

        self.PearlAndLiveryBarLayout.addLayout(self.horizontalLayout_9)

        self.PearlAndLiveryBarLayout.setStretch(0, 1)
        self.PearlAndLiveryBarLayout.setStretch(1, 4)

        self.SubColorPaintBarLayout.addLayout(self.PearlAndLiveryBarLayout)

        self.AdditionalPaintOptionLayout = QVBoxLayout()
        self.AdditionalPaintOptionLayout.setObjectName(u"AdditionalPaintOptionLayout")
        self.AdditionalPaintOptionLayout.setContentsMargins(-1, -1, -1, 0)
        self.WheelLabelLayout = QHBoxLayout()
        self.WheelLabelLayout.setObjectName(u"WheelLabelLayout")
        self.WheelLabel = QLabel(self.PaintManagerMainWidget)
        self.WheelLabel.setObjectName(u"WheelLabel")

        self.WheelLabelLayout.addWidget(self.WheelLabel)

        self.WheelColorFrame = QWidget(self.PaintManagerMainWidget)
        self.WheelColorFrame.setObjectName(u"WheelColorFrame")

        self.WheelLabelLayout.addWidget(self.WheelColorFrame)

        self.WheelLabelLayout.setStretch(0, 1)
        self.WheelLabelLayout.setStretch(1, 1)

        self.AdditionalPaintOptionLayout.addLayout(self.WheelLabelLayout)

        self.DialLabelLayout = QHBoxLayout()
        self.DialLabelLayout.setObjectName(u"DialLabelLayout")
        self.DialLabel = QLabel(self.PaintManagerMainWidget)
        self.DialLabel.setObjectName(u"DialLabel")

        self.DialLabelLayout.addWidget(self.DialLabel)

        self.DialColorFrame = QWidget(self.PaintManagerMainWidget)
        self.DialColorFrame.setObjectName(u"DialColorFrame")

        self.DialLabelLayout.addWidget(self.DialColorFrame)

        self.DialLabelLayout.setStretch(0, 1)
        self.DialLabelLayout.setStretch(1, 1)

        self.AdditionalPaintOptionLayout.addLayout(self.DialLabelLayout)

        self.TrimLabelLayout = QHBoxLayout()
        self.TrimLabelLayout.setObjectName(u"TrimLabelLayout")
        self.TrimLabel = QLabel(self.PaintManagerMainWidget)
        self.TrimLabel.setObjectName(u"TrimLabel")

        self.TrimLabelLayout.addWidget(self.TrimLabel)

        self.TrimColorFrame = QWidget(self.PaintManagerMainWidget)
        self.TrimColorFrame.setObjectName(u"TrimColorFrame")

        self.TrimLabelLayout.addWidget(self.TrimColorFrame)

        self.TrimLabelLayout.setStretch(0, 1)
        self.TrimLabelLayout.setStretch(1, 1)

        self.AdditionalPaintOptionLayout.addLayout(self.TrimLabelLayout)

        self.NeonLabelLayout = QHBoxLayout()
        self.NeonLabelLayout.setObjectName(u"NeonLabelLayout")
        self.NeonLightLabel = QLabel(self.PaintManagerMainWidget)
        self.NeonLightLabel.setObjectName(u"NeonLightLabel")

        self.NeonLabelLayout.addWidget(self.NeonLightLabel)

        self.NeonColorFrame = QWidget(self.PaintManagerMainWidget)
        self.NeonColorFrame.setObjectName(u"NeonColorFrame")

        self.NeonLabelLayout.addWidget(self.NeonColorFrame)

        self.NeonLabelLayout.setStretch(0, 1)
        self.NeonLabelLayout.setStretch(1, 1)

        self.AdditionalPaintOptionLayout.addLayout(self.NeonLabelLayout)

        self.HeadlightLabelLayout = QHBoxLayout()
        self.HeadlightLabelLayout.setObjectName(u"HeadlightLabelLayout")
        self.HeadlightLabel = QLabel(self.PaintManagerMainWidget)
        self.HeadlightLabel.setObjectName(u"HeadlightLabel")

        self.HeadlightLabelLayout.addWidget(self.HeadlightLabel)

        self.HeadLightColorFrame = QWidget(self.PaintManagerMainWidget)
        self.HeadLightColorFrame.setObjectName(u"HeadLightColorFrame")

        self.HeadlightLabelLayout.addWidget(self.HeadLightColorFrame)

        self.HeadlightLabelLayout.setStretch(0, 1)
        self.HeadlightLabelLayout.setStretch(1, 1)

        self.AdditionalPaintOptionLayout.addLayout(self.HeadlightLabelLayout)


        self.SubColorPaintBarLayout.addLayout(self.AdditionalPaintOptionLayout)

        self.SubColorPaintBarLayout.setStretch(0, 2)
        self.SubColorPaintBarLayout.setStretch(1, 1)

        self.ColorInfoLayout.addLayout(self.SubColorPaintBarLayout)

        self.ColorInfoLayout.setStretch(0, 1)
        self.ColorInfoLayout.setStretch(1, 1)
        self.ColorInfoLayout.setStretch(2, 1)
        self.ColorInfoLayout.setStretch(3, 5)

        self.ColorPanelRightLayout.addLayout(self.ColorInfoLayout)

        self.ColorPanelRightLayout.setStretch(0, 1)
        self.ColorPanelRightLayout.setStretch(1, 1)

        self.PaintManagerOverallLayout.addLayout(self.ColorPanelRightLayout)

        self.PaintManagerOverallLayout.setStretch(0, 5)
        self.PaintManagerOverallLayout.setStretch(1, 3)

        self.verticalLayout.addLayout(self.PaintManagerOverallLayout)

        self.ButtonsBarLayout = QHBoxLayout()
        self.ButtonsBarLayout.setObjectName(u"ButtonsBarLayout")
        self.PaintPopNewCrewColorButton = QPushButton(self.PaintManagerMainWidget)
        self.PaintPopNewCrewColorButton.setObjectName(u"PaintPopNewCrewColorButton")

        self.ButtonsBarLayout.addWidget(self.PaintPopNewCrewColorButton)

        self.PaintManagerButtonBox = QDialogButtonBox(self.PaintManagerMainWidget)
        self.PaintManagerButtonBox.setObjectName(u"PaintManagerButtonBox")
        self.PaintManagerButtonBox.setOrientation(Qt.Orientation.Horizontal)
        self.PaintManagerButtonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Save)

        self.ButtonsBarLayout.addWidget(self.PaintManagerButtonBox)


        self.verticalLayout.addLayout(self.ButtonsBarLayout)


        self.PaintManagerGlobal.addWidget(self.PaintManagerMainWidget)


        self.horizontalLayout_8.addLayout(self.PaintManagerGlobal)


        self.retranslateUi(PaintManager)

        QMetaObject.connectSlotsByName(PaintManager)
    # setupUi

    def retranslateUi(self, PaintManager):
        PaintManager.setWindowTitle(QCoreApplication.translate("PaintManager", u"Dialog", None))
        self.PresetNameLabel.setText(QCoreApplication.translate("PaintManager", u"Preset Name", None))
        self.PrimaryColorLabel.setText(QCoreApplication.translate("PaintManager", u"Primary", None))
        self.SecondaryColorLabel.setText(QCoreApplication.translate("PaintManager", u"Secondary", None))
        self.PearlLabel.setText(QCoreApplication.translate("PaintManager", u"Pearlescent", None))
        self.LiveryColorLabel.setText(QCoreApplication.translate("PaintManager", u"Livery", None))
        self.WheelLabel.setText(QCoreApplication.translate("PaintManager", u"Wheel", None))
        self.DialLabel.setText(QCoreApplication.translate("PaintManager", u"Dial  ", None))
        self.TrimLabel.setText(QCoreApplication.translate("PaintManager", u"Trim ", None))
        self.NeonLightLabel.setText(QCoreApplication.translate("PaintManager", u"Neon", None))
        self.HeadlightLabel.setText(QCoreApplication.translate("PaintManager", u"Light", None))
        self.PaintPopNewCrewColorButton.setText(QCoreApplication.translate("PaintManager", u"Add Crew Color", None))
    # retranslateUi


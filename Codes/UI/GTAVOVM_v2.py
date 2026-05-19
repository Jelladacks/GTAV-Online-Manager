# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'GTAVOVM_v2NqNaPw.ui'
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
    QHBoxLayout, QHeaderView, QLabel, QLayout,
    QLineEdit, QListView, QMainWindow, QProgressBar,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QTabWidget, QTableView, QVBoxLayout, QWidget)

from Codes.UI.lib.ImageFittingLabel import ImageFittingLabel
from Codes.UI.lib.ImageMinLabel import ImageMinLabel

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1080, 668)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.GlobalLayout = QVBoxLayout()
        self.GlobalLayout.setObjectName(u"GlobalLayout")
        self.GlobalLayout.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.MenuSelect = QTabWidget(self.centralwidget)
        self.MenuSelect.setObjectName(u"MenuSelect")
        self.Search = QWidget()
        self.Search.setObjectName(u"Search")
        self.verticalLayout_8 = QVBoxLayout(self.Search)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.SearchBarTab = QHBoxLayout()
        self.SearchBarTab.setObjectName(u"SearchBarTab")
        self.NameSearcher = QLineEdit(self.Search)
        self.NameSearcher.setObjectName(u"NameSearcher")

        self.SearchBarTab.addWidget(self.NameSearcher)

        self.ClassSearcher = QComboBox(self.Search)
        self.ClassSearcher.setObjectName(u"ClassSearcher")

        self.SearchBarTab.addWidget(self.ClassSearcher)

        self.ManufacturerSearcher = QComboBox(self.Search)
        self.ManufacturerSearcher.setObjectName(u"ManufacturerSearcher")

        self.SearchBarTab.addWidget(self.ManufacturerSearcher)

        self.AcquisitionSearcher = QComboBox(self.Search)
        self.AcquisitionSearcher.setObjectName(u"AcquisitionSearcher")

        self.SearchBarTab.addWidget(self.AcquisitionSearcher)

        self.SeatInput = QLineEdit(self.Search)
        self.SeatInput.setObjectName(u"SeatInput")

        self.SearchBarTab.addWidget(self.SeatInput)

        self.SeatSearcher = QComboBox(self.Search)
        self.SeatSearcher.setObjectName(u"SeatSearcher")

        self.SearchBarTab.addWidget(self.SeatSearcher)

        self.horizontalSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.SearchBarTab.addItem(self.horizontalSpacer)

        self.ReverseSortCheck = QCheckBox(self.Search)
        self.ReverseSortCheck.setObjectName(u"ReverseSortCheck")

        self.SearchBarTab.addWidget(self.ReverseSortCheck)

        self.SortingOrder = QComboBox(self.Search)
        self.SortingOrder.setObjectName(u"SortingOrder")

        self.SearchBarTab.addWidget(self.SortingOrder)

        self.SearchBarTab.setStretch(0, 6)
        self.SearchBarTab.setStretch(1, 2)
        self.SearchBarTab.setStretch(2, 2)
        self.SearchBarTab.setStretch(3, 3)
        self.SearchBarTab.setStretch(4, 1)
        self.SearchBarTab.setStretch(5, 1)
        self.SearchBarTab.setStretch(7, 1)
        self.SearchBarTab.setStretch(8, 1)

        self.verticalLayout_8.addLayout(self.SearchBarTab)

        self.SearchResultScrollArea = QScrollArea(self.Search)
        self.SearchResultScrollArea.setObjectName(u"SearchResultScrollArea")
        self.SearchResultScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.SearchResultScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.SearchResultScrollArea.setWidgetResizable(True)
        self.SearchResultScrollGridContainer = QWidget()
        self.SearchResultScrollGridContainer.setObjectName(u"SearchResultScrollGridContainer")
        self.SearchResultScrollGridContainer.setGeometry(QRect(0, 0, 1017, 569))
        self.SearchResultScrollArea.setWidget(self.SearchResultScrollGridContainer)

        self.verticalLayout_8.addWidget(self.SearchResultScrollArea)

        self.MenuSelect.addTab(self.Search, "")
        self.VehicleViewer = QWidget()
        self.VehicleViewer.setObjectName(u"VehicleViewer")
        self.VehicleViewer.setEnabled(True)
        self.horizontalLayout_6 = QHBoxLayout(self.VehicleViewer)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.VehicleViewerTotalLayout = QVBoxLayout()
        self.VehicleViewerTotalLayout.setObjectName(u"VehicleViewerTotalLayout")
        self.VehicleSearchBarComboBox = QComboBox(self.VehicleViewer)
        self.VehicleSearchBarComboBox.setObjectName(u"VehicleSearchBarComboBox")

        self.VehicleViewerTotalLayout.addWidget(self.VehicleSearchBarComboBox)

        self.TopVehicleImageAndInfoLayout = QHBoxLayout()
        self.TopVehicleImageAndInfoLayout.setObjectName(u"TopVehicleImageAndInfoLayout")
        self.VehicleImageLabel = ImageFittingLabel(self.VehicleViewer)
        self.VehicleImageLabel.setObjectName(u"VehicleImageLabel")
        self.VehicleImageLabel.setAutoFillBackground(False)
        self.VehicleImageLabel.setFrameShape(QFrame.Shape.Box)
        self.VehicleImageLabel.setFrameShadow(QFrame.Shadow.Plain)
        self.VehicleImageLabel.setLineWidth(2)
        self.VehicleImageLabel.setMidLineWidth(0)
        self.VehicleImageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.TopVehicleImageAndInfoLayout.addWidget(self.VehicleImageLabel)

        self.TotalVehicleInfoTextLayout = QVBoxLayout()
        self.TotalVehicleInfoTextLayout.setObjectName(u"TotalVehicleInfoTextLayout")
        self.TotalVehicleInfoTextLayout.setContentsMargins(-1, -1, -1, 0)
        self.VehicleNameLayout = QHBoxLayout()
        self.VehicleNameLayout.setObjectName(u"VehicleNameLayout")
        self.VehicleNameLayout.setContentsMargins(-1, -1, 0, -1)
        self.VehicleNameBarLeftLayout = QHBoxLayout()
        self.VehicleNameBarLeftLayout.setObjectName(u"VehicleNameBarLeftLayout")
        self.ManufacturerImageLabel = ImageMinLabel(self.VehicleViewer)
        self.ManufacturerImageLabel.setObjectName(u"ManufacturerImageLabel")
        self.ManufacturerImageLabel.setFrameShape(QFrame.Shape.Box)
        self.ManufacturerImageLabel.setLineWidth(2)
        self.ManufacturerImageLabel.setMargin(5)

        self.VehicleNameBarLeftLayout.addWidget(self.ManufacturerImageLabel)

        self.ManufacturerGroupLayout = QVBoxLayout()
        self.ManufacturerGroupLayout.setSpacing(0)
        self.ManufacturerGroupLayout.setObjectName(u"ManufacturerGroupLayout")
        self.ManufacturerNameLabel = QLabel(self.VehicleViewer)
        self.ManufacturerNameLabel.setObjectName(u"ManufacturerNameLabel")
        self.ManufacturerNameLabel.setFrameShape(QFrame.Shape.Box)
        self.ManufacturerNameLabel.setLineWidth(2)
        self.ManufacturerNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.ManufacturerGroupLayout.addWidget(self.ManufacturerNameLabel)

        self.ManuKORnameLabel = QLabel(self.VehicleViewer)
        self.ManuKORnameLabel.setObjectName(u"ManuKORnameLabel")
        self.ManuKORnameLabel.setFrameShape(QFrame.Shape.Box)
        self.ManuKORnameLabel.setLineWidth(2)
        self.ManuKORnameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.ManufacturerGroupLayout.addWidget(self.ManuKORnameLabel)


        self.VehicleNameBarLeftLayout.addLayout(self.ManufacturerGroupLayout)

        self.VehicleNameBarLeftLayout.setStretch(0, 1)
        self.VehicleNameBarLeftLayout.setStretch(1, 1)

        self.VehicleNameLayout.addLayout(self.VehicleNameBarLeftLayout)

        self.VehicleNameGroupLayout = QVBoxLayout()
        self.VehicleNameGroupLayout.setSpacing(0)
        self.VehicleNameGroupLayout.setObjectName(u"VehicleNameGroupLayout")
        self.VehicleNameLabel = QLabel(self.VehicleViewer)
        self.VehicleNameLabel.setObjectName(u"VehicleNameLabel")
        self.VehicleNameLabel.setFrameShape(QFrame.Shape.Box)
        self.VehicleNameLabel.setLineWidth(2)
        self.VehicleNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.VehicleNameGroupLayout.addWidget(self.VehicleNameLabel)

        self.VehicleKORnameLabel = QLabel(self.VehicleViewer)
        self.VehicleKORnameLabel.setObjectName(u"VehicleKORnameLabel")
        self.VehicleKORnameLabel.setFrameShape(QFrame.Shape.Box)
        self.VehicleKORnameLabel.setLineWidth(2)
        self.VehicleKORnameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.VehicleNameGroupLayout.addWidget(self.VehicleKORnameLabel)


        self.VehicleNameLayout.addLayout(self.VehicleNameGroupLayout)

        self.VehicleNameLayout.setStretch(0, 11)
        self.VehicleNameLayout.setStretch(1, 9)

        self.TotalVehicleInfoTextLayout.addLayout(self.VehicleNameLayout)

        self.VehicleInfoLayout = QHBoxLayout()
        self.VehicleInfoLayout.setObjectName(u"VehicleInfoLayout")
        self.VehicleTypeLabel = QLabel(self.VehicleViewer)
        self.VehicleTypeLabel.setObjectName(u"VehicleTypeLabel")
        self.VehicleTypeLabel.setFrameShape(QFrame.Shape.Box)
        self.VehicleTypeLabel.setLineWidth(2)
        self.VehicleTypeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.VehicleInfoLayout.addWidget(self.VehicleTypeLabel)

        self.PriceLabel = QLabel(self.VehicleViewer)
        self.PriceLabel.setObjectName(u"PriceLabel")
        self.PriceLabel.setFrameShape(QFrame.Shape.Box)
        self.PriceLabel.setLineWidth(2)
        self.PriceLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.VehicleInfoLayout.addWidget(self.PriceLabel)

        self.VehicleInfoLayout.setStretch(0, 11)
        self.VehicleInfoLayout.setStretch(1, 9)

        self.TotalVehicleInfoTextLayout.addLayout(self.VehicleInfoLayout)

        self.AcquisitionScrollArea = QScrollArea(self.VehicleViewer)
        self.AcquisitionScrollArea.setObjectName(u"AcquisitionScrollArea")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AcquisitionScrollArea.sizePolicy().hasHeightForWidth())
        self.AcquisitionScrollArea.setSizePolicy(sizePolicy)
        self.AcquisitionScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.AcquisitionScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.AcquisitionScrollArea.setWidgetResizable(True)
        self.AcquisitionScrollAreaContents = QWidget()
        self.AcquisitionScrollAreaContents.setObjectName(u"AcquisitionScrollAreaContents")
        self.AcquisitionScrollAreaContents.setEnabled(True)
        self.AcquisitionScrollAreaContents.setGeometry(QRect(0, 0, 98, 28))
        self.horizontalLayout_4 = QHBoxLayout(self.AcquisitionScrollAreaContents)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.AcquisitionScrollArea.setWidget(self.AcquisitionScrollAreaContents)

        self.TotalVehicleInfoTextLayout.addWidget(self.AcquisitionScrollArea)

        self.VehicleDetailsBarLayout = QHBoxLayout()
        self.VehicleDetailsBarLayout.setSpacing(6)
        self.VehicleDetailsBarLayout.setObjectName(u"VehicleDetailsBarLayout")
        self.VehicleDetailsBarLayout.setContentsMargins(-1, -1, 0, -1)
        self.DetailBarLeftLayout = QHBoxLayout()
        self.DetailBarLeftLayout.setObjectName(u"DetailBarLeftLayout")
        self.DetailBarLeftLayout.setContentsMargins(-1, -1, 0, -1)
        self.SeatsLabel = QLabel(self.VehicleViewer)
        self.SeatsLabel.setObjectName(u"SeatsLabel")
        self.SeatsLabel.setFrameShape(QFrame.Shape.Box)
        self.SeatsLabel.setLineWidth(2)
        self.SeatsLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.DetailBarLeftLayout.addWidget(self.SeatsLabel)

        self.DrivetrainLabel = QLabel(self.VehicleViewer)
        self.DrivetrainLabel.setObjectName(u"DrivetrainLabel")
        self.DrivetrainLabel.setFrameShape(QFrame.Shape.Box)
        self.DrivetrainLabel.setLineWidth(2)
        self.DrivetrainLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.DetailBarLeftLayout.addWidget(self.DrivetrainLabel)

        self.MassLabel = QLabel(self.VehicleViewer)
        self.MassLabel.setObjectName(u"MassLabel")
        self.MassLabel.setFrameShape(QFrame.Shape.Box)
        self.MassLabel.setLineWidth(2)
        self.MassLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.DetailBarLeftLayout.addWidget(self.MassLabel)


        self.VehicleDetailsBarLayout.addLayout(self.DetailBarLeftLayout)

        self.DetailBarRightLayout = QHBoxLayout()
        self.DetailBarRightLayout.setObjectName(u"DetailBarRightLayout")
        self.GearLabel = QLabel(self.VehicleViewer)
        self.GearLabel.setObjectName(u"GearLabel")
        self.GearLabel.setFrameShape(QFrame.Shape.Box)
        self.GearLabel.setLineWidth(2)
        self.GearLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.DetailBarRightLayout.addWidget(self.GearLabel)

        self.SizeLabel = QLabel(self.VehicleViewer)
        self.SizeLabel.setObjectName(u"SizeLabel")
        self.SizeLabel.setFrameShape(QFrame.Shape.Box)
        self.SizeLabel.setLineWidth(2)
        self.SizeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.DetailBarRightLayout.addWidget(self.SizeLabel)

        self.DetailBarRightLayout.setStretch(0, 2)
        self.DetailBarRightLayout.setStretch(1, 3)

        self.VehicleDetailsBarLayout.addLayout(self.DetailBarRightLayout)

        self.VehicleDetailsBarLayout.setStretch(0, 11)
        self.VehicleDetailsBarLayout.setStretch(1, 9)

        self.TotalVehicleInfoTextLayout.addLayout(self.VehicleDetailsBarLayout)

        self.VehicleLaptimeBarLayout = QHBoxLayout()
        self.VehicleLaptimeBarLayout.setSpacing(6)
        self.VehicleLaptimeBarLayout.setObjectName(u"VehicleLaptimeBarLayout")
        self.VehicleLaptimeBarLayout.setContentsMargins(0, -1, 0, -1)
        self.LaptimeLabelLayout = QHBoxLayout()
        self.LaptimeLabelLayout.setObjectName(u"LaptimeLabelLayout")
        self.LapTimeNameLabel = QLabel(self.VehicleViewer)
        self.LapTimeNameLabel.setObjectName(u"LapTimeNameLabel")
        self.LapTimeNameLabel.setFrameShape(QFrame.Shape.NoFrame)
        self.LapTimeNameLabel.setLineWidth(2)
        self.LapTimeNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.LaptimeLabelLayout.addWidget(self.LapTimeNameLabel)

        self.LaptimeLabel = QLabel(self.VehicleViewer)
        self.LaptimeLabel.setObjectName(u"LaptimeLabel")
        self.LaptimeLabel.setFrameShape(QFrame.Shape.Box)
        self.LaptimeLabel.setLineWidth(2)
        self.LaptimeLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.LaptimeLabel.setMargin(0)

        self.LaptimeLabelLayout.addWidget(self.LaptimeLabel)

        self.LaptimeLabelLayout.setStretch(0, 1)
        self.LaptimeLabelLayout.setStretch(1, 2)

        self.VehicleLaptimeBarLayout.addLayout(self.LaptimeLabelLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.TopSpeedNameLabel = QLabel(self.VehicleViewer)
        self.TopSpeedNameLabel.setObjectName(u"TopSpeedNameLabel")
        self.TopSpeedNameLabel.setFrameShape(QFrame.Shape.NoFrame)
        self.TopSpeedNameLabel.setLineWidth(2)
        self.TopSpeedNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.TopSpeedNameLabel)

        self.TopspeedLabel = QLabel(self.VehicleViewer)
        self.TopspeedLabel.setObjectName(u"TopspeedLabel")
        self.TopspeedLabel.setFrameShape(QFrame.Shape.Box)
        self.TopspeedLabel.setLineWidth(2)
        self.TopspeedLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.TopspeedLabel)

        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 3)

        self.VehicleLaptimeBarLayout.addLayout(self.horizontalLayout)

        self.VehicleLaptimeBarLayout.setStretch(0, 11)
        self.VehicleLaptimeBarLayout.setStretch(1, 9)

        self.TotalVehicleInfoTextLayout.addLayout(self.VehicleLaptimeBarLayout)

        self.GraphBarGroupLayout = QVBoxLayout()
        self.GraphBarGroupLayout.setSpacing(0)
        self.GraphBarGroupLayout.setObjectName(u"GraphBarGroupLayout")
        self.GraphBarGroupLayout.setContentsMargins(-1, -1, -1, 0)
        self.AccGraphBarLayout_2 = QHBoxLayout()
        self.AccGraphBarLayout_2.setObjectName(u"AccGraphBarLayout_2")
        self.SpeedGraphNameTag = QLabel(self.VehicleViewer)
        self.SpeedGraphNameTag.setObjectName(u"SpeedGraphNameTag")
        self.SpeedGraphNameTag.setFrameShape(QFrame.Shape.NoFrame)
        self.SpeedGraphNameTag.setLineWidth(2)
        self.SpeedGraphNameTag.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.AccGraphBarLayout_2.addWidget(self.SpeedGraphNameTag)

        self.SpeedProgressBar = QProgressBar(self.VehicleViewer)
        self.SpeedProgressBar.setObjectName(u"SpeedProgressBar")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.SpeedProgressBar.sizePolicy().hasHeightForWidth())
        self.SpeedProgressBar.setSizePolicy(sizePolicy1)
        self.SpeedProgressBar.setValue(24)
        self.SpeedProgressBar.setTextVisible(False)
        self.SpeedProgressBar.setInvertedAppearance(False)

        self.AccGraphBarLayout_2.addWidget(self.SpeedProgressBar)

        self.SpeedInputLabel = QLabel(self.VehicleViewer)
        self.SpeedInputLabel.setObjectName(u"SpeedInputLabel")
        self.SpeedInputLabel.setFrameShape(QFrame.Shape.Box)
        self.SpeedInputLabel.setLineWidth(2)
        self.SpeedInputLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.AccGraphBarLayout_2.addWidget(self.SpeedInputLabel)

        self.AccGraphBarLayout_2.setStretch(0, 5)
        self.AccGraphBarLayout_2.setStretch(1, 16)
        self.AccGraphBarLayout_2.setStretch(2, 4)

        self.GraphBarGroupLayout.addLayout(self.AccGraphBarLayout_2)

        self.AccGraphBarLayout = QHBoxLayout()
        self.AccGraphBarLayout.setObjectName(u"AccGraphBarLayout")
        self.AccGraphNameTag = QLabel(self.VehicleViewer)
        self.AccGraphNameTag.setObjectName(u"AccGraphNameTag")
        self.AccGraphNameTag.setFrameShape(QFrame.Shape.NoFrame)
        self.AccGraphNameTag.setLineWidth(2)
        self.AccGraphNameTag.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.AccGraphBarLayout.addWidget(self.AccGraphNameTag)

        self.ACCProgressBar = QProgressBar(self.VehicleViewer)
        self.ACCProgressBar.setObjectName(u"ACCProgressBar")
        sizePolicy1.setHeightForWidth(self.ACCProgressBar.sizePolicy().hasHeightForWidth())
        self.ACCProgressBar.setSizePolicy(sizePolicy1)
        self.ACCProgressBar.setValue(24)
        self.ACCProgressBar.setTextVisible(False)

        self.AccGraphBarLayout.addWidget(self.ACCProgressBar)

        self.AccInputLabel = QLabel(self.VehicleViewer)
        self.AccInputLabel.setObjectName(u"AccInputLabel")
        self.AccInputLabel.setFrameShape(QFrame.Shape.Box)
        self.AccInputLabel.setLineWidth(2)
        self.AccInputLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.AccGraphBarLayout.addWidget(self.AccInputLabel)

        self.AccGraphBarLayout.setStretch(0, 5)
        self.AccGraphBarLayout.setStretch(1, 16)
        self.AccGraphBarLayout.setStretch(2, 4)

        self.GraphBarGroupLayout.addLayout(self.AccGraphBarLayout)

        self.BrakeGraphBarLayout = QHBoxLayout()
        self.BrakeGraphBarLayout.setObjectName(u"BrakeGraphBarLayout")
        self.BrakeGraphNameTag = QLabel(self.VehicleViewer)
        self.BrakeGraphNameTag.setObjectName(u"BrakeGraphNameTag")
        self.BrakeGraphNameTag.setFrameShape(QFrame.Shape.NoFrame)
        self.BrakeGraphNameTag.setLineWidth(2)
        self.BrakeGraphNameTag.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.BrakeGraphBarLayout.addWidget(self.BrakeGraphNameTag)

        self.BrakeProgressBar = QProgressBar(self.VehicleViewer)
        self.BrakeProgressBar.setObjectName(u"BrakeProgressBar")
        sizePolicy1.setHeightForWidth(self.BrakeProgressBar.sizePolicy().hasHeightForWidth())
        self.BrakeProgressBar.setSizePolicy(sizePolicy1)
        self.BrakeProgressBar.setValue(24)
        self.BrakeProgressBar.setTextVisible(False)

        self.BrakeGraphBarLayout.addWidget(self.BrakeProgressBar)

        self.BrakeInputLabel = QLabel(self.VehicleViewer)
        self.BrakeInputLabel.setObjectName(u"BrakeInputLabel")
        self.BrakeInputLabel.setFrameShape(QFrame.Shape.Box)
        self.BrakeInputLabel.setLineWidth(2)
        self.BrakeInputLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.BrakeGraphBarLayout.addWidget(self.BrakeInputLabel)

        self.BrakeGraphBarLayout.setStretch(0, 5)
        self.BrakeGraphBarLayout.setStretch(1, 16)
        self.BrakeGraphBarLayout.setStretch(2, 4)

        self.GraphBarGroupLayout.addLayout(self.BrakeGraphBarLayout)

        self.HandlingGraphBarLayout = QHBoxLayout()
        self.HandlingGraphBarLayout.setObjectName(u"HandlingGraphBarLayout")
        self.HandleGraphNameTag = QLabel(self.VehicleViewer)
        self.HandleGraphNameTag.setObjectName(u"HandleGraphNameTag")
        self.HandleGraphNameTag.setFrameShape(QFrame.Shape.NoFrame)
        self.HandleGraphNameTag.setLineWidth(2)
        self.HandleGraphNameTag.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.HandlingGraphBarLayout.addWidget(self.HandleGraphNameTag)

        self.HandleProgressBar = QProgressBar(self.VehicleViewer)
        self.HandleProgressBar.setObjectName(u"HandleProgressBar")
        sizePolicy1.setHeightForWidth(self.HandleProgressBar.sizePolicy().hasHeightForWidth())
        self.HandleProgressBar.setSizePolicy(sizePolicy1)
        self.HandleProgressBar.setValue(24)
        self.HandleProgressBar.setTextVisible(False)

        self.HandlingGraphBarLayout.addWidget(self.HandleProgressBar)

        self.HandleInputLabel = QLabel(self.VehicleViewer)
        self.HandleInputLabel.setObjectName(u"HandleInputLabel")
        self.HandleInputLabel.setFrameShape(QFrame.Shape.Box)
        self.HandleInputLabel.setLineWidth(2)
        self.HandleInputLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.HandlingGraphBarLayout.addWidget(self.HandleInputLabel)

        self.HandlingGraphBarLayout.setStretch(0, 5)
        self.HandlingGraphBarLayout.setStretch(1, 16)
        self.HandlingGraphBarLayout.setStretch(2, 4)

        self.GraphBarGroupLayout.addLayout(self.HandlingGraphBarLayout)


        self.TotalVehicleInfoTextLayout.addLayout(self.GraphBarGroupLayout)

        self.TotalVehicleInfoTextLayout.setStretch(0, 8)
        self.TotalVehicleInfoTextLayout.setStretch(1, 4)
        self.TotalVehicleInfoTextLayout.setStretch(2, 4)
        self.TotalVehicleInfoTextLayout.setStretch(3, 3)
        self.TotalVehicleInfoTextLayout.setStretch(4, 3)
        self.TotalVehicleInfoTextLayout.setStretch(5, 9)

        self.TopVehicleImageAndInfoLayout.addLayout(self.TotalVehicleInfoTextLayout)

        self.TopVehicleImageAndInfoLayout.setStretch(0, 11)
        self.TopVehicleImageAndInfoLayout.setStretch(1, 9)

        self.VehicleViewerTotalLayout.addLayout(self.TopVehicleImageAndInfoLayout)

        self.VehicleViewerBottomLayout = QHBoxLayout()
        self.VehicleViewerBottomLayout.setObjectName(u"VehicleViewerBottomLayout")
        self.CustomPaintGroupLayout = QVBoxLayout()
        self.CustomPaintGroupLayout.setObjectName(u"CustomPaintGroupLayout")
        self.CustomPaintGroupLayout.setContentsMargins(-1, -1, -1, 0)
        self.CustomPaintLabelLayout = QHBoxLayout()
        self.CustomPaintLabelLayout.setObjectName(u"CustomPaintLabelLayout")
        self.customPaintTag = QLabel(self.VehicleViewer)
        self.customPaintTag.setObjectName(u"customPaintTag")

        self.CustomPaintLabelLayout.addWidget(self.customPaintTag)

        self.horizontalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.CustomPaintLabelLayout.addItem(self.horizontalSpacer_2)

        self.VanilaPaintCheckBox = QCheckBox(self.VehicleViewer)
        self.VanilaPaintCheckBox.setObjectName(u"VanilaPaintCheckBox")

        self.CustomPaintLabelLayout.addWidget(self.VanilaPaintCheckBox)


        self.CustomPaintGroupLayout.addLayout(self.CustomPaintLabelLayout)

        self.CustomPaintScrollArea = QScrollArea(self.VehicleViewer)
        self.CustomPaintScrollArea.setObjectName(u"CustomPaintScrollArea")
        self.CustomPaintScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.CustomPaintScrollArea.setWidgetResizable(True)
        self.CustomPaintScrollAreaWidgetContents = QWidget()
        self.CustomPaintScrollAreaWidgetContents.setObjectName(u"CustomPaintScrollAreaWidgetContents")
        self.CustomPaintScrollAreaWidgetContents.setGeometry(QRect(0, 0, 98, 28))
        self.CustomPaintScrollArea.setWidget(self.CustomPaintScrollAreaWidgetContents)

        self.CustomPaintGroupLayout.addWidget(self.CustomPaintScrollArea)


        self.VehicleViewerBottomLayout.addLayout(self.CustomPaintGroupLayout)

        self.OwnedVehicleGroupLayout = QVBoxLayout()
        self.OwnedVehicleGroupLayout.setSpacing(9)
        self.OwnedVehicleGroupLayout.setObjectName(u"OwnedVehicleGroupLayout")
        self.OwnedVehicleGroupLayout.setContentsMargins(-1, 4, -1, -1)
        self.OwnedVehicleInGarageTag = QLabel(self.VehicleViewer)
        self.OwnedVehicleInGarageTag.setObjectName(u"OwnedVehicleInGarageTag")

        self.OwnedVehicleGroupLayout.addWidget(self.OwnedVehicleInGarageTag)

        self.OwnedVehicleScrollArea = QScrollArea(self.VehicleViewer)
        self.OwnedVehicleScrollArea.setObjectName(u"OwnedVehicleScrollArea")
        self.OwnedVehicleScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.OwnedVehicleScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.OwnedVehicleScrollArea.setWidgetResizable(True)
        self.OwnedVehicleScrollAreaWidgetContents = QWidget()
        self.OwnedVehicleScrollAreaWidgetContents.setObjectName(u"OwnedVehicleScrollAreaWidgetContents")
        self.OwnedVehicleScrollAreaWidgetContents.setGeometry(QRect(0, 0, 98, 28))
        self.OwnedVehicleScrollAreaWidgetContents.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.horizontalLayout_2 = QHBoxLayout(self.OwnedVehicleScrollAreaWidgetContents)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.OwnedVehicleScrollArea.setWidget(self.OwnedVehicleScrollAreaWidgetContents)

        self.OwnedVehicleGroupLayout.addWidget(self.OwnedVehicleScrollArea)


        self.VehicleViewerBottomLayout.addLayout(self.OwnedVehicleGroupLayout)

        self.VehicleViewerBottomLayout.setStretch(0, 3)
        self.VehicleViewerBottomLayout.setStretch(1, 7)

        self.VehicleViewerTotalLayout.addLayout(self.VehicleViewerBottomLayout)

        self.VehicleViewerTotalLayout.setStretch(0, 1)
        self.VehicleViewerTotalLayout.setStretch(1, 13)
        self.VehicleViewerTotalLayout.setStretch(2, 7)

        self.horizontalLayout_6.addLayout(self.VehicleViewerTotalLayout)

        self.MenuSelect.addTab(self.VehicleViewer, "")
        self.GarageViewer = QWidget()
        self.GarageViewer.setObjectName(u"GarageViewer")
        self.verticalLayout_4 = QVBoxLayout(self.GarageViewer)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.GarageViewerWidget = QWidget(self.GarageViewer)
        self.GarageViewerWidget.setObjectName(u"GarageViewerWidget")
        self.verticalLayout_6 = QVBoxLayout(self.GarageViewerWidget)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.GarageHorizontalViewLayout = QHBoxLayout()
        self.GarageHorizontalViewLayout.setObjectName(u"GarageHorizontalViewLayout")
        self.GarageImageLabel = ImageFittingLabel(self.GarageViewerWidget)
        self.GarageImageLabel.setObjectName(u"GarageImageLabel")
        self.GarageImageLabel.setFrameShape(QFrame.Shape.Box)
        self.GarageImageLabel.setScaledContents(True)

        self.GarageHorizontalViewLayout.addWidget(self.GarageImageLabel)

        self.GarageCardListView = QListView(self.GarageViewerWidget)
        self.GarageCardListView.setObjectName(u"GarageCardListView")

        self.GarageHorizontalViewLayout.addWidget(self.GarageCardListView)

        self.GarageHorizontalViewLayout.setStretch(0, 2)
        self.GarageHorizontalViewLayout.setStretch(1, 1)

        self.verticalLayout_6.addLayout(self.GarageHorizontalViewLayout)

        self.GarageMemoTextLabel = QLabel(self.GarageViewerWidget)
        self.GarageMemoTextLabel.setObjectName(u"GarageMemoTextLabel")
        self.GarageMemoTextLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_6.addWidget(self.GarageMemoTextLabel)

        self.GarageSelectBox = QComboBox(self.GarageViewerWidget)
        self.GarageSelectBox.setObjectName(u"GarageSelectBox")

        self.verticalLayout_6.addWidget(self.GarageSelectBox)


        self.verticalLayout_4.addWidget(self.GarageViewerWidget)

        self.MenuSelect.addTab(self.GarageViewer, "")
        self.VehicleList = QWidget()
        self.VehicleList.setObjectName(u"VehicleList")
        self.verticalLayout_7 = QVBoxLayout(self.VehicleList)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.VehicleListWidget = QWidget(self.VehicleList)
        self.VehicleListWidget.setObjectName(u"VehicleListWidget")
        self.verticalLayout_2 = QVBoxLayout(self.VehicleListWidget)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.VehicleListTable = QTableView(self.VehicleListWidget)
        self.VehicleListTable.setObjectName(u"VehicleListTable")

        self.verticalLayout_2.addWidget(self.VehicleListTable)


        self.verticalLayout_7.addWidget(self.VehicleListWidget)

        self.MenuSelect.addTab(self.VehicleList, "")
        self.GarageList = QWidget()
        self.GarageList.setObjectName(u"GarageList")
        self.verticalLayout_3 = QVBoxLayout(self.GarageList)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.GarageListTable = QTableView(self.GarageList)
        self.GarageListTable.setObjectName(u"GarageListTable")

        self.verticalLayout_3.addWidget(self.GarageListTable)

        self.MenuSelect.addTab(self.GarageList, "")
        self.PaintListTab = QWidget()
        self.PaintListTab.setObjectName(u"PaintListTab")
        self.horizontalLayout_8 = QHBoxLayout(self.PaintListTab)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.PaintPresetScrollArea = QScrollArea(self.PaintListTab)
        self.PaintPresetScrollArea.setObjectName(u"PaintPresetScrollArea")
        self.PaintPresetScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.PaintPresetScrollArea.setWidgetResizable(True)
        self.PaintPresetScrollAreaWidgetContents = QWidget()
        self.PaintPresetScrollAreaWidgetContents.setObjectName(u"PaintPresetScrollAreaWidgetContents")
        self.PaintPresetScrollAreaWidgetContents.setGeometry(QRect(0, 0, 81, 28))
        self.PaintPresetScrollArea.setWidget(self.PaintPresetScrollAreaWidgetContents)

        self.horizontalLayout_8.addWidget(self.PaintPresetScrollArea)

        self.PaintTabRightBarLayout = QVBoxLayout()
        self.PaintTabRightBarLayout.setObjectName(u"PaintTabRightBarLayout")
        self.PaintTabRightBarLayout.setContentsMargins(-1, -1, -1, 0)
        self.ColorViewCheckBoxes = QVBoxLayout()
        self.ColorViewCheckBoxes.setSpacing(3)
        self.ColorViewCheckBoxes.setObjectName(u"ColorViewCheckBoxes")
        self.CheckVanillaPreset = QCheckBox(self.PaintListTab)
        self.CheckVanillaPreset.setObjectName(u"CheckVanillaPreset")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Ignored)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.CheckVanillaPreset.sizePolicy().hasHeightForWidth())
        self.CheckVanillaPreset.setSizePolicy(sizePolicy2)

        self.ColorViewCheckBoxes.addWidget(self.CheckVanillaPreset)

        self.CheckWheelColor = QCheckBox(self.PaintListTab)
        self.CheckWheelColor.setObjectName(u"CheckWheelColor")
        sizePolicy2.setHeightForWidth(self.CheckWheelColor.sizePolicy().hasHeightForWidth())
        self.CheckWheelColor.setSizePolicy(sizePolicy2)

        self.ColorViewCheckBoxes.addWidget(self.CheckWheelColor)

        self.CheckDialColor = QCheckBox(self.PaintListTab)
        self.CheckDialColor.setObjectName(u"CheckDialColor")
        sizePolicy2.setHeightForWidth(self.CheckDialColor.sizePolicy().hasHeightForWidth())
        self.CheckDialColor.setSizePolicy(sizePolicy2)

        self.ColorViewCheckBoxes.addWidget(self.CheckDialColor)

        self.CheckTrimColor = QCheckBox(self.PaintListTab)
        self.CheckTrimColor.setObjectName(u"CheckTrimColor")
        sizePolicy2.setHeightForWidth(self.CheckTrimColor.sizePolicy().hasHeightForWidth())
        self.CheckTrimColor.setSizePolicy(sizePolicy2)

        self.ColorViewCheckBoxes.addWidget(self.CheckTrimColor)

        self.CheckLivery = QCheckBox(self.PaintListTab)
        self.CheckLivery.setObjectName(u"CheckLivery")
        sizePolicy2.setHeightForWidth(self.CheckLivery.sizePolicy().hasHeightForWidth())
        self.CheckLivery.setSizePolicy(sizePolicy2)

        self.ColorViewCheckBoxes.addWidget(self.CheckLivery)

        self.CheckNeonLights = QCheckBox(self.PaintListTab)
        self.CheckNeonLights.setObjectName(u"CheckNeonLights")
        sizePolicy2.setHeightForWidth(self.CheckNeonLights.sizePolicy().hasHeightForWidth())
        self.CheckNeonLights.setSizePolicy(sizePolicy2)

        self.ColorViewCheckBoxes.addWidget(self.CheckNeonLights)

        self.CheckHeadlights = QCheckBox(self.PaintListTab)
        self.CheckHeadlights.setObjectName(u"CheckHeadlights")
        sizePolicy2.setHeightForWidth(self.CheckHeadlights.sizePolicy().hasHeightForWidth())
        self.CheckHeadlights.setSizePolicy(sizePolicy2)

        self.ColorViewCheckBoxes.addWidget(self.CheckHeadlights)

        self.ColorViewCheckBoxes.setStretch(0, 1)
        self.ColorViewCheckBoxes.setStretch(1, 1)
        self.ColorViewCheckBoxes.setStretch(2, 1)
        self.ColorViewCheckBoxes.setStretch(3, 1)
        self.ColorViewCheckBoxes.setStretch(4, 1)
        self.ColorViewCheckBoxes.setStretch(5, 1)
        self.ColorViewCheckBoxes.setStretch(6, 1)

        self.PaintTabRightBarLayout.addLayout(self.ColorViewCheckBoxes)

        self.colorIndexListScrollArea = QScrollArea(self.PaintListTab)
        self.colorIndexListScrollArea.setObjectName(u"colorIndexListScrollArea")
        self.colorIndexListScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.colorIndexListScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.colorIndexListScrollArea.setWidgetResizable(True)
        self.colorIndexListScrollContents = QWidget()
        self.colorIndexListScrollContents.setObjectName(u"colorIndexListScrollContents")
        self.colorIndexListScrollContents.setGeometry(QRect(0, 0, 98, 28))
        self.verticalLayout_12 = QVBoxLayout(self.colorIndexListScrollContents)
        self.verticalLayout_12.setSpacing(1)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(1, 1, 1, 1)
        self.colorIndexListScrollArea.setWidget(self.colorIndexListScrollContents)

        self.PaintTabRightBarLayout.addWidget(self.colorIndexListScrollArea)

        self.CrewColorListScrollArea = QScrollArea(self.PaintListTab)
        self.CrewColorListScrollArea.setObjectName(u"CrewColorListScrollArea")
        self.CrewColorListScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.CrewColorListScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.CrewColorListScrollArea.setWidgetResizable(True)
        self.CrewColorListScrollContents = QWidget()
        self.CrewColorListScrollContents.setObjectName(u"CrewColorListScrollContents")
        self.CrewColorListScrollContents.setGeometry(QRect(0, 0, 98, 28))
        self.verticalLayout_11 = QVBoxLayout(self.CrewColorListScrollContents)
        self.verticalLayout_11.setSpacing(1)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(1, 1, 1, 1)
        self.CrewColorListScrollArea.setWidget(self.CrewColorListScrollContents)

        self.PaintTabRightBarLayout.addWidget(self.CrewColorListScrollArea)

        self.NewCrewColorButton = QPushButton(self.PaintListTab)
        self.NewCrewColorButton.setObjectName(u"NewCrewColorButton")

        self.PaintTabRightBarLayout.addWidget(self.NewCrewColorButton)

        self.PaintTabRightBarLayout.setStretch(0, 4)
        self.PaintTabRightBarLayout.setStretch(1, 10)
        self.PaintTabRightBarLayout.setStretch(2, 3)
        self.PaintTabRightBarLayout.setStretch(3, 1)

        self.horizontalLayout_8.addLayout(self.PaintTabRightBarLayout)

        self.horizontalLayout_8.setStretch(0, 10)
        self.horizontalLayout_8.setStretch(1, 1)
        self.MenuSelect.addTab(self.PaintListTab, "")
        self.Properties = QWidget()
        self.Properties.setObjectName(u"Properties")
        self.horizontalLayout_9 = QHBoxLayout(self.Properties)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.PropertiesScrollArea = QScrollArea(self.Properties)
        self.PropertiesScrollArea.setObjectName(u"PropertiesScrollArea")
        self.PropertiesScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.PropertiesScrollArea.setWidgetResizable(True)
        self.PropertiesScrollAreaWidgetContents = QWidget()
        self.PropertiesScrollAreaWidgetContents.setObjectName(u"PropertiesScrollAreaWidgetContents")
        self.PropertiesScrollAreaWidgetContents.setGeometry(QRect(0, 0, 81, 28))
        self.verticalLayout_13 = QVBoxLayout(self.PropertiesScrollAreaWidgetContents)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.PropertiesScrollArea.setWidget(self.PropertiesScrollAreaWidgetContents)

        self.horizontalLayout_9.addWidget(self.PropertiesScrollArea)

        self.PropertyDetailFrame = QFrame(self.Properties)
        self.PropertyDetailFrame.setObjectName(u"PropertyDetailFrame")
        self.PropertyDetailLayout = QVBoxLayout(self.PropertyDetailFrame)
        self.PropertyDetailLayout.setObjectName(u"PropertyDetailLayout")
        self.PropertyDetailLayout.setContentsMargins(0, 0, 0, 0)
        self.PropertyImageLabel = QLabel(self.PropertyDetailFrame)
        self.PropertyImageLabel.setObjectName(u"PropertyImageLabel")
        self.PropertyImageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.PropertyDetailLayout.addWidget(self.PropertyImageLabel)

        self.PropertyDetailScrollArea = QScrollArea(self.PropertyDetailFrame)
        self.PropertyDetailScrollArea.setObjectName(u"PropertyDetailScrollArea")
        self.PropertyDetailScrollArea.setWidgetResizable(True)
        self.PropertyDetailScrollAreaWidgetContents = QWidget()
        self.PropertyDetailScrollAreaWidgetContents.setObjectName(u"PropertyDetailScrollAreaWidgetContents")
        self.PropertyDetailScrollAreaWidgetContents.setGeometry(QRect(0, 0, 98, 28))
        self.verticalLayout_14 = QVBoxLayout(self.PropertyDetailScrollAreaWidgetContents)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.PropertyDetailVerticalLayout = QVBoxLayout()
        self.PropertyDetailVerticalLayout.setObjectName(u"PropertyDetailVerticalLayout")

        self.verticalLayout_14.addLayout(self.PropertyDetailVerticalLayout)

        self.PropertyDetailScrollArea.setWidget(self.PropertyDetailScrollAreaWidgetContents)

        self.PropertyDetailLayout.addWidget(self.PropertyDetailScrollArea)

        self.PropertyDetailLayout.setStretch(0, 3)
        self.PropertyDetailLayout.setStretch(1, 7)

        self.horizontalLayout_9.addWidget(self.PropertyDetailFrame)

        self.horizontalLayout_9.setStretch(0, 7)
        self.horizontalLayout_9.setStretch(1, 3)
        self.MenuSelect.addTab(self.Properties, "")
        self.Stats = QWidget()
        self.Stats.setObjectName(u"Stats")
        self.horizontalLayout_7 = QHBoxLayout(self.Stats)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.VehicleStatTable = QTableView(self.Stats)
        self.VehicleStatTable.setObjectName(u"VehicleStatTable")

        self.horizontalLayout_7.addWidget(self.VehicleStatTable)

        self.MenuSelect.addTab(self.Stats, "")

        self.GlobalLayout.addWidget(self.MenuSelect)


        self.verticalLayout.addLayout(self.GlobalLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.MenuSelect.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.ReverseSortCheck.setText(QCoreApplication.translate("MainWindow", u"Reverse", None))
        self.MenuSelect.setTabText(self.MenuSelect.indexOf(self.Search), QCoreApplication.translate("MainWindow", u"Vehicle Searcher", None))
        self.VehicleImageLabel.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;\">Select Vehicle to view details</span></p><p align=\"center\"><span style=\" font-size:11pt;\">And Click the image appears here to change it</span></p></body></html>", None))
        self.ManufacturerImageLabel.setText(QCoreApplication.translate("MainWindow", u"ManufacturerImage", None))
        self.ManufacturerNameLabel.setText(QCoreApplication.translate("MainWindow", u"ManufacturerName", None))
        self.ManuKORnameLabel.setText(QCoreApplication.translate("MainWindow", u"\uc81c\uc870\uc0ac\uc774\ub984", None))
        self.VehicleNameLabel.setText(QCoreApplication.translate("MainWindow", u"VehicleName", None))
        self.VehicleKORnameLabel.setText(QCoreApplication.translate("MainWindow", u"\uc774\ub3d9\uc218\ub2e8 \uc774\ub984", None))
        self.VehicleTypeLabel.setText(QCoreApplication.translate("MainWindow", u"VehicleTypeName", None))
        self.PriceLabel.setText(QCoreApplication.translate("MainWindow", u"VehiclePrice", None))
        self.SeatsLabel.setText(QCoreApplication.translate("MainWindow", u"Seats", None))
        self.DrivetrainLabel.setText(QCoreApplication.translate("MainWindow", u"DriveTrain", None))
        self.MassLabel.setText(QCoreApplication.translate("MainWindow", u"Mass", None))
        self.GearLabel.setText(QCoreApplication.translate("MainWindow", u"Gears", None))
        self.SizeLabel.setText(QCoreApplication.translate("MainWindow", u"Size * Size * Size", None))
        self.LapTimeNameLabel.setText(QCoreApplication.translate("MainWindow", u"Lap Time :", None))
        self.LaptimeLabel.setText(QCoreApplication.translate("MainWindow", u"LapTime", None))
        self.TopSpeedNameLabel.setText(QCoreApplication.translate("MainWindow", u"Top Speed :", None))
        self.TopspeedLabel.setText(QCoreApplication.translate("MainWindow", u"TopSpeed", None))
        self.SpeedGraphNameTag.setText(QCoreApplication.translate("MainWindow", u"SPEED", None))
        self.SpeedInputLabel.setText(QCoreApplication.translate("MainWindow", u"speed", None))
        self.AccGraphNameTag.setText(QCoreApplication.translate("MainWindow", u"ACCELERATION", None))
        self.AccInputLabel.setText(QCoreApplication.translate("MainWindow", u"acc", None))
        self.BrakeGraphNameTag.setText(QCoreApplication.translate("MainWindow", u"BRAKING", None))
        self.BrakeInputLabel.setText(QCoreApplication.translate("MainWindow", u"brake", None))
        self.HandleGraphNameTag.setText(QCoreApplication.translate("MainWindow", u"HANDLING", None))
        self.HandleInputLabel.setText(QCoreApplication.translate("MainWindow", u"handle", None))
        self.customPaintTag.setText(QCoreApplication.translate("MainWindow", u"Custom Paint List", None))
        self.VanilaPaintCheckBox.setText(QCoreApplication.translate("MainWindow", u"Vanilla", None))
        self.OwnedVehicleInGarageTag.setText(QCoreApplication.translate("MainWindow", u"Storaged At :", None))
        self.MenuSelect.setTabText(self.MenuSelect.indexOf(self.VehicleViewer), QCoreApplication.translate("MainWindow", u"Vehicle Viewer", None))
        self.GarageImageLabel.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;\">Select Garage To View Vehicles</span></p><p align=\"center\"><span style=\" font-size:11pt;\">And Click the image appears here to change it</span></p></body></html>", None))
        self.GarageMemoTextLabel.setText(QCoreApplication.translate("MainWindow", u"Garage Info", None))
        self.MenuSelect.setTabText(self.MenuSelect.indexOf(self.GarageViewer), QCoreApplication.translate("MainWindow", u"Garage Viewer", None))
        self.MenuSelect.setTabText(self.MenuSelect.indexOf(self.VehicleList), QCoreApplication.translate("MainWindow", u"Vehicle List", None))
        self.MenuSelect.setTabText(self.MenuSelect.indexOf(self.GarageList), QCoreApplication.translate("MainWindow", u"Garage List", None))
        self.CheckVanillaPreset.setText(QCoreApplication.translate("MainWindow", u"Vanilla Only", None))
        self.CheckWheelColor.setText(QCoreApplication.translate("MainWindow", u"Wheel Color", None))
        self.CheckDialColor.setText(QCoreApplication.translate("MainWindow", u"Dial Color", None))
        self.CheckTrimColor.setText(QCoreApplication.translate("MainWindow", u"Trim Color", None))
        self.CheckLivery.setText(QCoreApplication.translate("MainWindow", u"Liveries", None))
        self.CheckNeonLights.setText(QCoreApplication.translate("MainWindow", u"Neon Lights", None))
        self.CheckHeadlights.setText(QCoreApplication.translate("MainWindow", u"Headlights", None))
        self.NewCrewColorButton.setText(QCoreApplication.translate("MainWindow", u"Add Crew Color", None))
        self.MenuSelect.setTabText(self.MenuSelect.indexOf(self.PaintListTab), QCoreApplication.translate("MainWindow", u"Paint List", None))
        self.PropertyImageLabel.setText(QCoreApplication.translate("MainWindow", u"Property Image", None))
        self.MenuSelect.setTabText(self.MenuSelect.indexOf(self.Properties), QCoreApplication.translate("MainWindow", u"Properties", None))
        self.MenuSelect.setTabText(self.MenuSelect.indexOf(self.Stats), QCoreApplication.translate("MainWindow", u"Statistics", None))
    # retranslateUi


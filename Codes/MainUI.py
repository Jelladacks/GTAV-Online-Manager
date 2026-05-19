import os

from PySide6.QtWidgets import QAbstractItemView, QApplication, QButtonGroup, QDialog, QFrame, QLabel, QListView, QMainWindow, QHeaderView, QMessageBox, QVBoxLayout, QWidget, QCheckBox, QRadioButton, QSizePolicy
from PySide6.QtGui import QDrag, QIcon, QPixmap, QStandardItemModel, QStandardItem, QIntValidator, QPalette, QColor
from PySide6.QtCore import QCoreApplication, QEvent, QMimeData, QSize, QSortFilterProxyModel, Qt, QTimer, Signal
import sys
import sqlite3
from Datas.Database.init.SmartSeeder import SmartSeeder
from Codes.UI.ImageManagerDialog import ImageManagerDialog
from Codes.UI.PropertyCustomDialong import PropertyCustomDialog
from Codes.UI.lib.SortingProxyModel import SortingProxyModel
from Codes.UI.lib.LoadingOverlay import LoadingOverlay
from Codes.config import AppConfig
from Codes.UI.GTAVOVM_v2 import Ui_MainWindow
from Codes.UI.GTAVOVM_PropertyCard import Ui_PropertyCardWidget
from Codes.UI.GTAVOVM_CategoryAccordion import Ui_CategoryAccordianWidget
from Codes.UI.GTAVOVM_VehicleCard import Ui_VehicleCardWidget
from Codes.UI.GTAVOVM_ColorCard import Ui_ColorPresetPreviewWidget
from Codes.UI.GTAVOVM_AddButtonCard import Ui_AddButtonCardWidget
from Codes.UI.GTAVOVM_OwnVehicleCard import Ui_OwnVehicleInfoCardWidget
from Codes.UI.GTAVOVM_ACQcard import Ui_ACQWidget
from Codes.UI.GTAVOVM_GarageVehicleCard import Ui_GarageVehicleCardWidget
from Codes.UI.GTAVOVM_ColorRefWidget import Ui_ColorRefWidget
from Codes.Service.MainFunctions import *
from Codes.Service.loadGTAData import DBLoader_GTA
from Codes.Service.ImageManager import ImageManager
from Codes.Library.DataToView import *
from Codes.UI.PaintPopDialog import PaintEditDialog
from Codes.UI.lib.FlowLayout import FlowLayout
from Codes.UI.lib.colorpicker.colorpicker import ColorPicker
from Codes.UI.lib.GarageList.GarageCarModel import GarageCarModel
from Codes.UI.lib.GarageList.GarageCardDelegate import CarCardDelegate
from collections import Counter
import json
import weakref

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        ### Init Main UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(u"GTA V & Online Vehicle Manager")
        icon_path = IMAGE_DIR = os.path.join(AppConfig.BASE_DIR, "Datas", "icon.png")
        self.setWindowIcon(QIcon(icon_path))

        ### Init Model For Vehicle List and Garage List
        self.vehicle_list_model = QStandardItemModel()
        self.veh_proxy_model = SortingProxyModel()
        header = self.ui.VehicleListTable.horizontalHeader()
        # header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)

        self.garage_list_model = QStandardItemModel()
        self.gar_proxy_model = SortingProxyModel() 
        self._is_loading_garage_model = False

        ### Garage Viewer Card Painter
        self.garage_card_model = GarageCarModel()
        self.garage_card_model.orderChanged.connect(self.save_garage_order)
        self.carCardDelegate = None

        ### Current Data
        self.selected_garage_info = None
        self.current_veiwer_veicle_id = None

        ### Connect Table Signal 
        # self.ui.mainTabWidget.currentChanged.connect(self.on_tab_changed)
        self.ui.VehicleListTable.doubleClicked.connect(self.on_vehicle_doubleclicked)
        self.ui.GarageListTable.doubleClicked.connect(self.on_garage_doubleclicked)

        # Statistics Table
        self.statistics_model = QStandardItemModel()
        self.ui.VehicleStatTable.setModel(self.statistics_model)

        ### Vehicle Searcher Init
        self.vehicle_card_dict = dict()
        self.vehicle_search_column_count = 4

        ### Garage Viewer Edit
        self.garage_own_card_dict = dict()

        ### Property Tab Init
        self.property_category_dict = dict() 
        """To Find Category Widget"""
        self.property_card_dict = dict()
        """To Find Property Widget"""
        self.property_btgroup_dict = dict()
        self.current_selected_own_property_id = None
        self.need_refresh_garage = False

        self.custom_category_dict = dict()
        self.custom_card_dict = dict()
        self.btn_group_dict = dict()

        ### Vehicle Viewer Init
        self.own_vehicle_dict = dict()
        self.own_inactive_vehicle_dict = dict()
        self.own_index = 0
        self.acq_card_dict = dict()
        self.ownv_selectable_garage_dict = dict()
        
        ### Flow Layouts for Vehicle Searcher, Paint Viewer
        self.flow_layout = FlowLayout(self.ui.SearchResultScrollGridContainer)
        self.flow_layout_paint = FlowLayout(self.ui.PaintPresetScrollAreaWidgetContents)
        self.flow_vehicle_paint = FlowLayout(self.ui.CustomPaintScrollAreaWidgetContents)
        self.last_size = QSize(0, 0)

        ### Init Card Sizes
        self.vehicle_card_width = 249
        self.paint_card_width = 250
        self.paint_subcard_width = 250
        self.own_card_height = 150
        self.acq_card_height = 40
        self.property_card_width = 400
        self.garage_card_width = 320

        ### Init padding
        self.ui.LaptimeLabel.setStyleSheet("padding-right: 15px;")
        self.ui.SpeedInputLabel.setStyleSheet("padding-right: 10px;")
        self.ui.AccInputLabel.setStyleSheet("padding-right: 10px;")
        self.ui.BrakeInputLabel.setStyleSheet("padding-right: 10px;")
        self.ui.HandleInputLabel.setStyleSheet("padding-right: 10px;")

        self.ui.SpeedGraphNameTag.setStyleSheet("padding-right: 3px;")
        self.ui.AccGraphNameTag.setStyleSheet("padding-right: 3px;")
        self.ui.BrakeGraphNameTag.setStyleSheet("padding-right: 3px;")
        self.ui.HandleGraphNameTag.setStyleSheet("padding-right: 3px;")

        ### Connect Tab Changed Function
        self.ui.MenuSelect.currentChanged.connect(self.handle_tab_changed)

        ### Timer Setting
        self.resize_timer = QTimer()
        self.resize_timer.setSingleShot(True) # 한 번만 실행되도록
        self.resize_timer.timeout.connect(self.update_card_sizes)

        self.searcher_image_timer = QTimer()
        self.searcher_image_timer.setSingleShot(True) # 한 번만 실행되도록
        self.searcher_image_timer.timeout.connect(self.check_lazy_vehicle_loading)

        self.property_image_timer = QTimer()
        self.property_image_timer.setSingleShot(True) # 한 번만 실행되도록
        self.property_image_timer.timeout.connect(self.check_lazy_property_loading)

        self.searcher_filter_timer = QTimer()
        self.searcher_filter_timer.setSingleShot(True) # 한 번만 실행되도록
        self.searcher_filter_timer.timeout.connect(self.search_filter_changed)

        ### Paint Viewer Init
        self.paint_card_dict = dict()
        self.paint_subcard_dict = dict()
        self.crew_color_dict = dict()

        self.ui.NewCrewColorButton.clicked.connect(self.handle_new_crew_color)

        self.preset_filter_status = {
            "CheckVanillaPreset" : False,
            "CheckWheelColor": False,
            "CheckDialColor": False,
            "CheckTrimColor": False,
            "CheckLivery": False,
            "CheckNeonLights": False,
            "CheckHeadlights": False
        }

        self.init_main_load_app_datas()

    def init_main_load_app_datas(self):
        """
        Init DB and Tab UIs
        """
        print("Loading Managers")
        self.all_managers = Managers()
        self.func_lib = MainFundamentalFunc(self.all_managers)
        self.func_lib.load_all_services()
        print("load_all_services Done")

        self.init_vehicle_model()
        print("init_vehicle_model Done")
        self.init_garage_model()
        print("init_garage_model Done")
        self.init_property_tab()
        print("init_property_tab Done")
        self.init_vehicle_searcher()
        print("init_vehicle_searcher Done")
        self.init_vehicle_viewer()
        print("init_vehicle_viewer Done")
        self.init_garage_viewer()
        print("init_garage_viewer Done")
        self.init_paint_viewer()
        print("init_paint_viewer Done")
        self.init_stat_viewer()
        print("init_stat_viewer Done")

        self.init_scroll_design(self.ui.PaintPresetScrollArea)
        self.init_scroll_design(self.ui.PropertiesScrollArea)
        self.init_scroll_design(self.ui.CrewColorListScrollArea)
        self.init_scroll_design(self.ui.colorIndexListScrollArea)
        self.init_scroll_design(self.ui.CustomPaintScrollArea)
        self.init_scroll_design(self.ui.AcquisitionScrollArea)
        self.init_scroll_design(self.ui.SearchResultScrollArea)
        # self.init_scroll_design(self.ui.OwnedVehicleScrollArea)
        print("init_main_load_app_datas Done")

        
    def init_vehicle_model(self):
        """
        Setting Vehicle List Tab
        """
        self.veh_proxy_model.setSourceModel(self.vehicle_list_model)
        self.veh_proxy_model.setDynamicSortFilter(True)

        self.ui.VehicleListTable.setModel(self.veh_proxy_model)
        self.ui.VehicleListTable.setSortingEnabled(True)

        ### Table Header Setting
        self.vehicle_list_model.setHorizontalHeaderLabels(['ID', 'name', 'manufacturer', 'class', 'price', 'laptime_ms', 'topspeed_10mtph', 'is_owned', 'mass', 'gears', 'seats', 'drivetrain', 'graph_speed', 'graph_acc', 'graph_brake', 'graph_handle', 'sizecm_x', 'sizecm_y', 'sizecm_z', 'is_pegasus', 'is_unique'])
        
        self.ui.VehicleListTable.setColumnWidth(0, 1)
        self.ui.VehicleListTable.setColumnWidth(1, 130)
        self.ui.VehicleListTable.setColumnWidth(2, 90)
        self.ui.VehicleListTable.setColumnWidth(3, 80)
        self.ui.VehicleListTable.setColumnWidth(4, 70)
        self.ui.VehicleListTable.setColumnWidth(5, 50)
        self.ui.VehicleListTable.setColumnWidth(6, 50)
        self.ui.VehicleListTable.setColumnWidth(7, 40)
        self.ui.VehicleListTable.setColumnWidth(8, 50)
        self.ui.VehicleListTable.setColumnWidth(9, 30)
        self.ui.VehicleListTable.setColumnWidth(10, 30)
        self.ui.VehicleListTable.setColumnWidth(11, 40)
        self.ui.VehicleListTable.setColumnWidth(12, 45)
        self.ui.VehicleListTable.setColumnWidth(13, 45)
        self.ui.VehicleListTable.setColumnWidth(14, 45)
        self.ui.VehicleListTable.setColumnWidth(15, 45)
        self.ui.VehicleListTable.setColumnWidth(16, 45)
        self.ui.VehicleListTable.setColumnWidth(17, 45)
        self.ui.VehicleListTable.setColumnWidth(18, 45)
        self.ui.VehicleListTable.setColumnWidth(19, 10)
        self.ui.VehicleListTable.setColumnWidth(20, 10)

        self.fill_vehicle_table()

        self.ui.VehicleListTable.sortByColumn(0, Qt.DescendingOrder)
        

    def fill_vehicle_table(self):
        """
            Filling Vehicle List
        """
        self.vehicle_list_model.removeRows(0, self.vehicle_list_model.rowCount())

        vehicles = self.func_lib.get_vehicle_list(1)

        def create_numeric_item(value, display_text=None):
            """
                Create QStandardItem that can be Sorted by Value
            """
            item = QStandardItem()
            # 숫자로 변환 시도 (비어있을 경우 0)
            try:
                num_value = float(value) if value != '' else 0
            except:
                num_value = 0
                
            # EditRole에 숫자를 넣어야 ProxyModel이 숫자로 정렬함
            item.setData(num_value, Qt.EditRole) 
            item.setData(display_text if display_text is not None else str(value), Qt.DisplayRole)
            return item

        ### Looping All Vehicles To Add Items
        for row_data in vehicles:
            raw_laptime = row_data.get('laptime_ms', 0)
            laptime_str = format_lap_time(raw_laptime)
            topspeed = value_to_percentage(row_data.get('topspeed_10mtph', ''))

            graph_speed = value_to_percentage(row_data.get('graph_speed', ''))
            graph_acc = value_to_percentage(row_data.get('graph_acc', ''))
            graph_brake = value_to_percentage(row_data.get('graph_brake', ''))
            graph_handle = value_to_percentage(row_data.get('graph_handle', ''))

            sizecm_x = value_to_percentage(row_data.get('sizecm_x', ''))
            sizecm_y = value_to_percentage(row_data.get('sizecm_y', ''))
            sizecm_z = value_to_percentage(row_data.get('sizecm_z', ''))

            items = [
                create_numeric_item(row_data.get('id', 0)),               # id
                QStandardItem(str(row_data.get('name', ''))),
                QStandardItem(str(row_data.get('manufacturer', ''))),
                QStandardItem(str(row_data.get('vehicle_class', ''))),
                create_numeric_item(row_data.get('price', 0)),           # price
                create_numeric_item(raw_laptime, laptime_str),           # laptime (정렬은 ms, 표시는 포맷팅된 문자열)
                create_numeric_item(topspeed),                           # topspeed
                QStandardItem(str(row_data.get('is_owned', ''))),
                create_numeric_item(row_data.get('mass', 0)),            # mass
                create_numeric_item(row_data.get('gears', 0)),           # gears
                create_numeric_item(row_data.get('seats', 0)),           # seats
                QStandardItem(str(row_data.get('drivetrain', ''))),
                create_numeric_item(graph_speed),                        # graph_speed
                create_numeric_item(graph_acc),                          # graph_acc
                create_numeric_item(graph_brake),                        # graph_brake
                create_numeric_item(graph_handle),                       # graph_handle
                create_numeric_item(sizecm_x),                           # sizecm_x
                create_numeric_item(sizecm_y),                           # sizecm_y
                create_numeric_item(sizecm_z),                           # sizecm_z
                QStandardItem(str(row_data.get('is_pegasus', ''))),
                QStandardItem(str(row_data.get('is_unique', '')))
            ]

            ### Block Typing Cells in Table
            for item in items:
                item.setEditable(False)
            self.vehicle_list_model.appendRow(items)


    def init_garage_model(self):       
        """
            Setting Garage List Tab
        """
        self.gar_proxy_model.setSourceModel(self.garage_list_model)
        self.gar_proxy_model.setDynamicSortFilter(True)

        self.ui.GarageListTable.setModel(self.gar_proxy_model)
        self.ui.GarageListTable.setSortingEnabled(True)

        ### Setting Header
        self.garage_list_model.setHorizontalHeaderLabels(['ID', 'property', 'property_type', 'slot_type', 'memo', 'total_slot', 'filled_slot'])

        self.ui.GarageListTable.setColumnWidth(0, 1)
        self.ui.GarageListTable.setColumnWidth(1, 180)
        self.ui.GarageListTable.setColumnWidth(2, 180)
        self.ui.GarageListTable.setColumnWidth(3, 140)
        self.ui.GarageListTable.setColumnWidth(4, 250)
        self.ui.GarageListTable.setColumnWidth(5, 100)
        self.ui.GarageListTable.setColumnWidth(6, 100)

        self.fill_garage_table()
        self.ui.GarageListTable.sortByColumn(0, Qt.AscendingOrder)
        
    
    def fill_garage_table(self):
        """
            Filling Garage List
        """

        ### Prevent to Call Several Filling Function
        if self._is_loading_garage_model:
            return
        
        self._is_loading_garage_model = True
        self.garage_list_model.beginResetModel()


        try:
            ### Remove All Items
            self.garage_list_model.removeRows(0, self.garage_list_model.rowCount())

            garages = self.func_lib.get_garage_list()

            if garages is None:
                return

            ### Loop Garages To Add Items
            for row_data in garages:
                memotext = row_data.get('memo', '')
                if (memotext is None) or (memotext == ''):
                    memotext = 'Type Memo Here'

                pdata = self.all_managers.property.property_map.get(row_data.get('property_id', 0), {})
                ptypedata = self.all_managers.property.property_type_map.get(row_data.get('property_type_id', 0), {})
                stypename = self.all_managers.storage.slot_type_map.get(row_data.get('slot_type_id', 0), 'Unknown')

                memo_item = QStandardItem(str(memotext))
                memo_item.setData(row_data.get('id'), Qt.UserRole)

                ptype_item = QStandardItem(str(ptypedata.get('key_name', 'Unknown')))
                ptype_item.setData(ptypedata.get('id'), Qt.UserRole)

                stype_item = QStandardItem(str(stypename))
                stype_item.setData(row_data.get('slot_type_id', 0), Qt.UserRole)

                items = [
                    QStandardItem(str(row_data.get('ui_garage_id', ''))),
                    QStandardItem(str(pdata.get('key_name', "Unknown"))),
                    ptype_item,
                    stype_item,
                    memo_item,
                    QStandardItem(str(row_data.get('total_slot', ''))),
                    QStandardItem(str(row_data.get('filled_slot', '')))
                ]
                for i, item in enumerate(items):
                    item.setEditable(False)

                ### Memo Needs To Edit
                memo_item.setEditable(True)
                self.garage_list_model.appendRow(items)

            ### Save DB Event After Editing Memo
            self.garage_list_model.layoutChanged.emit()
            self.garage_list_model.itemChanged.connect(self.on_edit_property_memo)

        finally:
            self.garage_list_model.endResetModel()
            self._is_loading_garage_model = False



    def init_property_tab(self):
        """
            Initial Property Widgets Setting
            Pre Build Categories and Properties
        """
        self.ui.PropertyDetailFrame.hide()
        pdict = self.func_lib.get_property_dict()
        total_width = self.ui.PropertiesScrollArea.viewport().width() - 5
        
        """
            You will need Category Parent, Category Child and Property Cards
            This will make all Categories and Property Cards First,
            Then Connect All of them with Property Map
        """

        ### Loop Property Types To make Category Widget
        should_set_parent_category_list = defaultdict(list)
        for ptype_id, ptype_data in self.all_managers.property.property_type_map.items():

            if ptype_data.get('is_hidden', None) == 1:
                ### Skipping Hidden Category
                # print(f"Skip Generating Hidden Property Type : {ptype_data.get('key_name', None)}")
                continue

            property_category = CategoryWidget(ptype_data)
            property_category.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
            property_category.toggled_category.connect(self.property_image_timer_starts)
            self.property_category_dict[ptype_id] = property_category

            ### If property_type has parent_id, Put it in a temporary dict (list).
            if ptype_data.get('parent_id', None) is not None:
                should_set_parent_category_list[ ptype_data.get('parent_id') ].append(property_category)
            
            ### Else, Add widget to Property UI and set ButtonGroup.
            else:
                self.ui.PropertiesScrollAreaWidgetContents.layout().addWidget(property_category, alignment=Qt.AlignmentFlag.AlignTop)
                new_buttongroup = QButtonGroup(self)
                if (ptype_data.get('max_owned') > 1):
                    new_buttongroup.setExclusive(False)
                else:
                    new_buttongroup.setExclusive(True)
                self.property_btgroup_dict[ptype_id] = new_buttongroup

        ### Loop Properties To make PropertyCard
        for pid, property_data in self.all_managers.property.property_map.items():
            type_id = property_data.get('type_id')
            type_data = self.all_managers.property.property_type_map.get(type_id)
            is_unchangeable = type_data.get('is_unchangeable', False)
            is_owned = self.all_managers.property.is_owned_property(pid)
            is_radio = False

            ### Determine whether to use radio checkboxes based on the Max_owned value
            if (type_data.get('max_owned') == 1) and (len(self.all_managers.property.ptype_map.get(type_id)) != 1):
                is_radio = True
            elif (type_data.get('max_owned') is None) and \
                  (self.all_managers.property.property_type_map\
                   [ self.all_managers.property.property_type_map[type_id]['parent_id'] ]['max_owned'] == 1):
                is_radio = True

            ### Creating Property Cards
            target_category = self.property_category_dict.get(type_id, None)
            if target_category is not None:
                property_card = PropertyCard(property_data)
                property_card.init_selector_button( is_radio, is_owned, is_unchangeable)
                property_card.property_changed.connect(self.handle_property_checked)
                property_card.image_clicked.connect(self.handle_property_details)
                self.property_card_dict[pid] = property_card
                target_category.add_child(property_card)

                ### Connecting Button in PropertyCard To ButtonGroup
                target_buttongroup = self.property_btgroup_dict.get(type_id, None)
                if target_buttongroup is not None:
                    if property_card.is_ready_to_use():
                        target_buttongroup.addButton(property_card.selector)
                
        ### Loop temporary dict created above to connect the parents.
        for parent_id , category_list in should_set_parent_category_list.items():
            target_buttongroup = self.property_btgroup_dict.get(parent_id, None)

            """
                The Merge Flag merges
                    multiple Child Categories within a
                    Parent Category that have only a single PropertyCard,
                    allowing the PropertyCard to be displayed directly within the Parent Category.
            """
            merge_flag = False
            for categet in category_list:
                if categet.get_child_count() > 1:
                    merge_flag = False
                    break
                merge_flag = True
            
            if merge_flag:
                for categet in category_list:    
                    for child_property in categet.child_dict.values():
                        self.property_category_dict.get(parent_id).add_child(child_property)
                        
                        if target_buttongroup is not None:
                            if child_property.is_ready_to_use():
                                target_buttongroup.addButton(child_property.selector)

            else:
                for categet in category_list:
                    self.property_category_dict.get(parent_id).add_child(categet)

                    for child_property in categet.child_dict.values():
                        if target_buttongroup is not None:
                            if child_property.is_ready_to_use():
                                target_buttongroup.addButton(child_property.selector)
  
        ### Connect Image Loader
        self.ui.PropertiesScrollArea.verticalScrollBar().valueChanged.connect(self.property_image_timer_starts)

        """
        ### Legacy Category Builder
        for ptype_id, plist in pdict.items():
            type_data = self.all_managers.property.property_type_map.get(ptype_id)
            property_category = CategoryWidget(plist, type_data)
            property_category.relay_property_clicked.connect(self.handle_property_checked)
            self.property_category_dict[ptype_id] = property_category
            self.ui.PropertiesScrollAreaWidgetContents.layout().addWidget(property_category, alignment=Qt.AlignmentFlag.AlignTop)
        """
        
    def init_vehicle_searcher(self):
        """
            Init Vehicle Search Tab And Pre Build Vehicle Cards
        """
        classes = [''] + self.func_lib.get_vehicle_classes()
        self.ui.ClassSearcher.addItems( classes )
        self.ui.ClassSearcher.setPlaceholderText("Class Filter")
        manus = [''] + self.func_lib.get_vehicle_manufacturers()
        self.ui.ManufacturerSearcher.addItems( manus )
        self.ui.ManufacturerSearcher.setPlaceholderText("Manufacturer Filter")
        acqs = [''] + sorted(list(self.all_managers.vehicle.acq_set))
        self.ui.AcquisitionSearcher.addItems( acqs )
        self.ui.AcquisitionSearcher.setPlaceholderText("Acquisition Filter")
        self.ui.SeatSearcher.addItems(['==', '<', '>', '<=', '>='])
        self.ui.SortingOrder.addItems(['ID', 'Name', 'Price', 'Laptime', 'Topspeed', 'Mass'])

        validator = QIntValidator(0, 30, self)
        self.ui.SeatInput.setValidator(validator)

        ### Connect Search Bar To Relocating Cards Function
        self.ui.NameSearcher.textEdited.connect(self.on_filter_changed)
        self.ui.ClassSearcher.currentTextChanged.connect(self.on_filter_changed)
        self.ui.ManufacturerSearcher.currentTextChanged.connect(self.on_filter_changed)
        self.ui.AcquisitionSearcher.currentTextChanged.connect(self.on_filter_changed)
        self.ui.SeatInput.textChanged.connect(self.on_filter_changed)
        self.ui.SeatSearcher.currentTextChanged.connect(self.on_filter_changed)
        self.ui.SortingOrder.currentIndexChanged.connect(self.on_filter_changed)
        self.ui.ReverseSortCheck.checkStateChanged.connect(self.on_filter_changed)

        

        
        ### Connect Image Loader
        self.ui.SearchResultScrollArea.verticalScrollBar().valueChanged.connect(self.searcher_image_timer_starts)

        ### Load All Vehicle Cards
        temp_list = self.func_lib.get_vehicle_list(1, True)
        self.vehicle_card_dict.clear()
        for vehicle in temp_list:
            # 차량 위젯 만들고 vehicle_id 기준으로 잡는 dict 생성
            vehicle_card = VehicleSearchCardWidget(vehicle)
            self.vehicle_card_dict[vehicle['id']] = vehicle_card
            self.flow_layout.addWidget(vehicle_card)
            vehicle_card.double_clicked.connect(self.handle_vcard_double_click)

    def init_vehicle_viewer(self):
        """
            Install Events, Style UI and Load All Acquisition Cards
        """

        ### Set Upper Combo Box
        self.ui.VehicleSearchBarComboBox.clear()
        vehicles = self.func_lib.get_vehicle_list(1, True)
        for vehicle in vehicles:
            display_text = f"{vehicle['vehicle_class']} | {vehicle['manufacturer']} {vehicle['name']}"
            self.ui.VehicleSearchBarComboBox.addItem( display_text, vehicle['id'] )
        
        self.ui.VehicleSearchBarComboBox.setPlaceholderText("Choose Vehicle")
        self.ui.VehicleSearchBarComboBox.currentIndexChanged.connect(self.on_vehicle_selected)
        self.ui.VehicleSearchBarComboBox.setCurrentIndex(-1)

        ### UI Making
        self.ui.OwnedVehicleScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.ui.OwnedVehicleScrollAreaWidgetContents.layout().setAlignment(Qt.AlignLeft)
        self.ui.AcquisitionScrollAreaContents.layout().setAlignment(Qt.AlignLeft)

        ProgressBarStyle = """
            QProgressBar {
                border: 1px solid white;
                /*border-radius: 5px;*/
                background-color: #FFFFFF;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #AAAAAA;
                /*width: 20px;*/
            }
        """
        self.ui.SpeedProgressBar.setStyleSheet(ProgressBarStyle)
        self.ui.BrakeProgressBar.setStyleSheet(ProgressBarStyle)
        self.ui.HandleProgressBar.setStyleSheet(ProgressBarStyle)
        self.ui.ACCProgressBar.setStyleSheet(ProgressBarStyle)

        self.ui.OwnedVehicleScrollArea.viewport().installEventFilter(self)
        self.ui.AcquisitionScrollArea.viewport().installEventFilter(self)
        self.ui.VehicleImageLabel.installEventFilter(self)

        self.add_vehicle_btn = AddButtonCard()
        """
            Common AddButton to be used for all vehicle addition logic
        """

        """
            Create all AcquisitionCards here, Hide them later depending on the vehicle type.
        """
        acq_list = self.all_managers.vehicle.acquisition_table
        for acq in acq_list:
            acq_card = AcquisitionCard(acq['source'])
            acq_card.adjust_content_size(self.acq_card_height)
            self.acq_card_dict[acq['source']] = acq_card
       
    def eventFilter(self, obj, event):
        """
            Overrides EventFilter To Apply Wheel And DoubleClick Event
        """
        ### Changed vertical wheel movement to apply to the horizontal scrollbar.
        if obj == self.ui.OwnedVehicleScrollArea.viewport() and event.type() == QEvent.Type.Wheel:
            # 수직 휠 이동량을 수평 스크롤바에 적용
            delta = event.angleDelta().y()
            scrollbar = self.ui.OwnedVehicleScrollArea.horizontalScrollBar()
            scrollbar.setValue(scrollbar.value() - delta)
            return True 
        if obj == self.ui.AcquisitionScrollArea.viewport() and event.type() == QEvent.Type.Wheel:
            # 수직 휠 이동량을 수평 스크롤바에 적용
            delta = event.angleDelta().y()
            scrollbar = self.ui.AcquisitionScrollArea.horizontalScrollBar()
            scrollbar.setValue(scrollbar.value() - delta)
            return True
        
        ### Display a dialog to change the photo when an image is DoubleClicked
        if obj == self.ui.VehicleImageLabel and event.type() == QEvent.MouseButtonDblClick:
            if event.button() == Qt.MouseButton.LeftButton:
                self.open_image_manager_dialog('Vehicle')
                return True
        if obj == self.ui.GarageImageLabel and event.type() == QEvent.MouseButtonDblClick:
            if event.button() == Qt.MouseButton.LeftButton:
                self.open_image_manager_dialog('Garage')
                return True

        return super().eventFilter(obj, event)
    
    def open_image_manager_dialog(self, category):
        """
            Display a Dialog To Change Vehicle and Garage Images in Viewer
        """
        
        if category == 'Vehicle':
            if self.current_veiwer_veicle_id is None:
                return
            dialog = ImageManagerDialog('Vehicle', self.current_veiwer_veicle_id, self)
        elif category == 'Garage':
            if self.selected_garage_info is None:
                return
            dialog = ImageManagerDialog('Garage', self.selected_garage_info, self)

        if dialog:
            dialog.image_updated.connect(self.handle_image_update)
            dialog.exec()

    def init_garage_viewer(self):
        """
            Add Items In Garage Select comboBox, and Connect Event | 
            Garage Display Text Must Be 'Name [Type] (Slot)'
        """
        self.ui.GarageSelectBox.clear()
        garages = self.func_lib.get_garage_list()
        for gar in garages:
            pdata = self.all_managers.property.property_map.get(gar.get('property_id', 0), {})
            ptypedata = self.all_managers.property.property_type_map.get(gar.get('property_type_id', 0), {})
            stypename = self.all_managers.storage.slot_type_map.get(gar.get('slot_type_id', 0), 'Unknown')
            display_text = f"{pdata.get('key_name', "Unknown")} [{ptypedata.get('key_name', 'Unknown')}] ({stypename})"
            info = (gar['own_property_id'], gar['slot_type_id'], gar['property_type_id'])
            self.ui.GarageSelectBox.addItem(display_text, info)
        
        self.ui.GarageSelectBox.setPlaceholderText("Choose Garage")
        self.ui.GarageSelectBox.currentIndexChanged.connect(self.on_garage_selected)
        self.ui.GarageSelectBox.setCurrentIndex(-1)

        self.ui.GarageImageLabel.installEventFilter(self)
        print("init_garage_viewer Done")

    def set_garage_select_box(self):
        """
            Add Items In Garage Select comboBox in Garage Viewer | 
            Garage Display Text Must Be 'Name [Type] (Slot)'
        """

        ### Check existing items with tuple set
        current_ids = set()
        for i in range(self.ui.GarageSelectBox.count()):
            data = self.ui.GarageSelectBox.itemData(i)
            # print(f"Original data: {data}, Type: {type(data)}")

            if data:
                clean_data = tuple(data) if isinstance(data, list) else data
                current_ids.add(clean_data)

        garagelist = self.func_lib.get_garage_list()

        ### Prevent Sending Signals from This changes
        self.ui.GarageSelectBox.blockSignals(True)

        ### Add Garage Items Not In Currenly Exist Items
        for gar in garagelist:
            info = (gar['own_property_id'], gar['slot_type_id'], gar['property_type_id'])
            if info not in current_ids:
                
                pdata = self.all_managers.property.property_map.get(gar.get('property_id', 0), {})
                ptypedata = self.all_managers.property.property_type_map.get(gar.get('property_type_id', 0), {})
                stypename = self.all_managers.storage.slot_type_map.get(gar.get('slot_type_id', 0), 'Unknown')
                display_text = f"{pdata.get('key_name', "Unknown")} [{ptypedata.get('key_name', 'Unknown')}] ({stypename})"
                self.ui.GarageSelectBox.addItem(display_text, info)

        self.ui.GarageSelectBox.blockSignals(False)


    def init_paint_viewer(self):
        """
            Add Paint Widgets, Sidebar References, and Connect Checkbox Event At Sidebar | 
            There will be some categories

            1. Custom : Custom User Paint Presets
            2. Index : Color References
            3. and.. GTA Default categories
                └ Classic, Metallic, Matte...
        """
        total_paint_list = self.func_lib.get_paint_list()        
        self.paint_card_dict.clear()

        custom_data = total_paint_list.get('Custom', {})
        index_data = total_paint_list.get('Index', {})

        # 딕셔너리일 때만
        if (isinstance(custom_data, dict)) and (isinstance(index_data, dict)):
         
            ### Add Paint Preset Cards
            for key, preset in custom_data.items():
                self.add_paint_widget(preset)

            ### Add Color References at Sidebar
            for color_ref in index_data.values():
                color_widget = ColorReferenceWidget(color_ref)

                if color_ref.get('gta_color_id') is None:
                    crid = color_ref.get('id', -1)
                    color_widget.double_clicked.connect(self.handle_edit_crew_color)
                    
                    self.crew_color_dict[crid] = color_widget
                    color_widget.fillWidget()
                    
                    self.ui.CrewColorListScrollContents.layout().addWidget(color_widget)
                else:
                    self.ui.colorIndexListScrollContents.layout().addWidget(color_widget)
            
        ### Need Add Preset Button
        self.add_paint_btn = AddButtonCard()
        self.add_paint_btn.clicked.connect(self.add_new_preset)
        self.flow_layout_paint.addWidget(self.add_paint_btn)
        self.ui.CrewColorListScrollContents.layout().setAlignment(Qt.AlignmentFlag.AlignTop)


        ### Connect Filters to Signal
        self.filter_checkboxes = [
            self.ui.CheckVanillaPreset, self.ui.CheckWheelColor, self.ui.CheckDialColor, 
            self.ui.CheckTrimColor, self.ui.CheckLivery, self.ui.CheckNeonLights, 
            self.ui.CheckHeadlights
        ]
        
        for cb in self.filter_checkboxes:
            cb.checkStateChanged.connect(self.handle_paint_color_filter)
        
        # Checkbox from Vehicle Viewer Paint Layout
        self.ui.VanilaPaintCheckBox.checkStateChanged.connect(self.handle_paint_color_filter)

    def init_stat_viewer(self):
        """
            I got some Vehicle Statistics for You
        """
        self.statistics_model.clear()
        self.statistics_model.setHorizontalHeaderLabels(['Tag', 'GTA Total', 'Own Count'])
        stat_data = self.func_lib.get_stat_data()

        self.ui.VehicleStatTable.setColumnWidth(0, 200)
        self.ui.VehicleStatTable.setColumnWidth(1, 200)
        self.ui.VehicleStatTable.setColumnWidth(2, 200)

        total_value = [
                QStandardItem( "Total Value" ),
                QStandardItem(str(stat_data["total_price"])),
                QStandardItem(str(stat_data["own_price"]))
            ]
        self.statistics_model.appendRow(total_value)

        total_count = [
                QStandardItem( "Number of Vehicle" ),
                QStandardItem(str(stat_data["total_count"])),
                QStandardItem(str(stat_data["own_count"]))
            ]
        self.statistics_model.appendRow(total_count)

        total_slot = [
                QStandardItem( "Garage Capacity" ),
                QStandardItem(str(stat_data["total_slot"])),
                QStandardItem(str(stat_data["slot_count"]))
            ]
        self.statistics_model.appendRow(total_slot)

        current_slot = [
                QStandardItem( "Filled Total Slots" ),
                QStandardItem(str(stat_data["slot_count"])),
                QStandardItem(str(stat_data["slot_filled"]))
            ]
        self.statistics_model.appendRow(current_slot)

        current_slot = [
                QStandardItem( "Filled Garage Slots" ),
                QStandardItem(str(stat_data["car_slot_count"])),
                QStandardItem(str(stat_data["car_filled"]))
            ]
        self.statistics_model.appendRow(current_slot)

        ### Make Stats for Each Vehicle Class
        all_vehicle_list = self.all_managers.vehicle.vehicle_table
        owned_vehicle_list = self.all_managers.vehicle.own_table.values()
        all_counts = Counter(v['vehicle_class'] for v in all_vehicle_list)
        owned_counts = Counter(v['vehicle_class'] for v in all_vehicle_list if v.get('is_owned'))

        for v_class in all_counts:
            v_class_item = [
                QStandardItem(str(v_class)),
                QStandardItem(str(all_counts[v_class])),
                QStandardItem(str(owned_counts[v_class]))
            ]
            self.statistics_model.appendRow(v_class_item)

    def on_edit_property_memo(self, item):
        """
            If memo is edited from Garage List Tab,
            Save it to DB and Modify all memos of items in the same category within the table.
        """
        new_memo = item.text()
        own_property_id = item.data(Qt.UserRole)
        self.all_managers.property.edit_memo_own_property(own_property_id, new_memo)

        matches = self.garage_list_model.match(
            self.garage_list_model.index(0, 4), # 시작 위치 (0행 0열)
            Qt.UserRole,                        # 찾을 데이터가 저장된 Role
            own_property_id,                    # 찾으려는 ID 값
            hits = -1,                          # 찾을 개수 (-1은 '모두')
            flags = Qt.MatchExactly             # 매칭 옵션
        )

        self.garage_list_model.blockSignals(True)

        for index in matches:
            item = self.garage_list_model.itemFromIndex(index)
            if item:
                item.setText(str(new_memo))

        self.garage_list_model.blockSignals(False)


    def add_own_vehicle_widget(self, own_data):
        """
            This Adds Perfect OwnVehicleCard to Vehicle FlowLayout
        """

        color_data = self.all_managers.color.paint_presets.get(own_data.get('paint_preset_id'), None)
        color_card = self.make_color_preset_card(color_data, True, False)
        if color_card is not None:
            color_card.double_clicked.connect(self.handle_paint_double_click)
        
        owncard = OwnVehicleCard(own_data, self.ownv_selectable_garage_dict, color_card, self.all_managers.color.what_gradient_preview)
        owncard.data_changed.connect(self.handle_own_vehicle_update)
        owncard.vehicle_removed.connect(self.handle_remove_own_vehicle)
        owncard.paint_added.connect(self.add_new_preset_in_vehicle_card)
        owncard.adjust_content_size(self.own_card_height)
        self.own_vehicle_dict[own_data['id']] = owncard
        self.own_index += 1
        if own_data['is_sold'] == True:
            self.own_inactive_vehicle_dict[own_data['id']] = owncard
            self.own_index -= 1
        self.ui.OwnedVehicleScrollAreaWidgetContents.layout().addWidget(owncard)
        # print(f"Added Own Vehicle Widget [own_index : {self.own_index}] >>>> {own_data['id']}")

    def add_new_own_card(self, vehicle_id):
        """
            This will add a new own_vehicle to DB, and Generates OwnVehicleCard
            Then, reposition the Add Button.
        """
        result = self.func_lib.add_own_vehicle(vehicle_id)
        if (result['success'] == False) or (result['category'] != 'vehicle'):
            return False
        
        target = self.all_managers.vehicle.own_table.get(result['own_vid'])

        self.add_own_vehicle_widget(target)
        
        self.ui.OwnedVehicleScrollAreaWidgetContents.layout().removeWidget(self.add_vehicle_btn)
        self.ui.OwnedVehicleScrollAreaWidgetContents.layout().addWidget(self.add_vehicle_btn)
        
        for solds in self.own_inactive_vehicle_dict.values():
            self.ui.OwnedVehicleScrollAreaWidgetContents.layout().removeWidget(solds)
            self.ui.OwnedVehicleScrollAreaWidgetContents.layout().addWidget(solds)
    
    def handle_own_vehicle_update(self, own_vehicle_id, value_dict):
        """
            This is a function that saves changes to the DB
            And Modify the Garage-related data currently in memory
            When OwnVehicleCard has modified
        """


        """
            If Vehicle is Unique Type and User Owned It, 
            Add button will Disappear from Layout
            That is shown in the code below.
        """
        own_vehicle_data = self.all_managers.vehicle.own_table.get(own_vehicle_id)
        # print(f"Editing Own Vehicle >> {own_vehicle_data}")
        own_property_id = own_vehicle_data.get('owned_property_id')
        bef_slot_type_id = own_vehicle_data.get('slot_type_id')
        bef_ptype_id = self.all_managers.property.owned_property.get(own_property_id, {}).get('property_type_id', None)
        before_tuple = (own_property_id, bef_slot_type_id, bef_ptype_id)

        ### If Own Vehicle has Sold, remove from garage data and edit DB
        ###                     (move to default garage (TEMPORARY SLOT) )
        ### AAAAnd It Must be Returned
        if value_dict.get('is_sold') is True:
            self.func_lib.edit_own_vehicle(own_vehicle_id, **value_dict)
            #self.garage_own_card_dict.pop(own_vehicle_id, None)

            garagedict_data = self.ownv_selectable_garage_dict.get(before_tuple)
            garagedict_data['slot_left'] += 1
            print(f"Vehicle {own_vehicle_id} sold and removed.")

            target_card = self.own_vehicle_dict.get(own_vehicle_id, None)
            if target_card is not None:
                self.own_inactive_vehicle_dict[own_vehicle_id] = target_card

                ### Add 'Add Button' to Layout
                if self.func_lib.is_unique_own_vehicle(own_vehicle_id):
                    self.ui.OwnedVehicleScrollAreaWidgetContents.layout().addWidget(self.add_vehicle_btn)
                    self.add_vehicle_btn.show()

                self.ui.OwnedVehicleScrollAreaWidgetContents.layout().removeWidget(target_card)
                self.ui.OwnedVehicleScrollAreaWidgetContents.layout().addWidget(target_card)
                self.own_index -= 1
                ### OwnVehicleCard needs to update Edited Data
                target_card.set_data_refresh( self.all_managers.vehicle.own_table.get(own_vehicle_id) )

            ### Remove 'is_owned' flag if there is no more same vehicle
            self.refresh_vehicle_owned_flag(own_vehicle_id)
            return
        

        
        ### If Own Vehicle has Restored, Add to default garage (TEMPORARY SLOT)
        elif (value_dict.get('is_sold', None) is not None) and value_dict.get('is_sold') is False:
            self.own_inactive_vehicle_dict.pop(own_vehicle_id)

            garagedict_data = self.ownv_selectable_garage_dict.get(before_tuple)
            garagedict_data['slot_left'] -= 1
            print(f"Vehicle {own_vehicle_id} restoring.")

            target_card = self.own_vehicle_dict.get(own_vehicle_id, None)
            if target_card is not None:
                ### Remove 'Add Button' from Layout, If It is Unique
                if self.func_lib.is_unique_own_vehicle(own_vehicle_id):
                    self.ui.OwnedVehicleScrollAreaWidgetContents.layout().removeWidget(self.add_vehicle_btn)
                    self.add_vehicle_btn.hide()

                self.ui.OwnedVehicleScrollAreaWidgetContents.layout().insertWidget(self.own_index, target_card)
                self.own_index += 1
                
                

        if 'owned_property_id' in value_dict:
            """
                If owned_property_id changes, slot_type_id must be updated and passed
                to this function as well.
                An appropriate slot_index is then determined and stored in the data,
                and the garage data is updated accordingly.
            """
            bef_garagedict_data = self.ownv_selectable_garage_dict.get(before_tuple)
            bef_garagedict_data['slot_left'] += 1

            prop_id = value_dict['owned_property_id']
            slot_type_id = value_dict.get('slot_type_id')
            own_property_data = self.all_managers.property.owned_property.get(prop_id, {})
            property_type_id = own_property_data.get('property_type_id')

            if (prop_id is not None) and (prop_id == 0):
                return
            if (slot_type_id is not None) and (slot_type_id == 0):
                return

            value_dict['slot_index'] = self.func_lib.strg_svc.get_available_slotindex(prop_id, slot_type_id)
            after_tuple = (prop_id, slot_type_id, property_type_id)
            aft_garagedict_data = self.ownv_selectable_garage_dict.get(after_tuple)
            aft_garagedict_data['slot_left'] -= 1

            print(f"Moving vehicle to Property:{prop_id}, SlotType:{slot_type_id}, Index:{value_dict['slot_index']}")
        

        ### Edit DB, Apply data to OwnVehicleCard, Garage Combobox, Ownflag
        self.func_lib.edit_own_vehicle(own_vehicle_id, **value_dict)
        
        updated_card = self.own_vehicle_dict.get(own_vehicle_id, None)
        if updated_card is not None:
            updated_card.set_data_refresh( self.all_managers.vehicle.own_table.get(own_vehicle_id) )
        
        for ovdcid, upcards in self.own_vehicle_dict.items():
            upcards.refresh_garage_combobox()

        self.refresh_vehicle_owned_flag(own_vehicle_id)
        self.need_refresh_garage = True # determines whether the garage data needs to be refreshed.
        # print(f"Updated params for {own_vehicle_id}: {value_dict}")

    def refresh_vehicle_owned_flag(self, own_vehicle_id):
        """
            This will be Edit 'is_owned' flag in Vehicle List Tab
        """
        target_data = self.all_managers.vehicle.own_table.get(own_vehicle_id)
        vehicle_id = target_data['vehicle_id']
        own_flag = self.all_managers.vehicle.vehicle_map[vehicle_id]['is_owned']

        matches = self.vehicle_list_model.match(
            self.vehicle_list_model.index(0, 0),    # 0행 0열부터 검색 시작
            Qt.EditRole,       # 모델의 표시 데이터(text)를 기준으로 검색
            vehicle_id,       # ID값을 문자열로 변환하여 검색
            hits = 1,                    # 1개만 찾음
            flags = Qt.MatchExactly
        )
        if matches:
            row = matches[0].row()
            item = self.vehicle_list_model.item(row, 7)

        if item:
            item.setText(str(own_flag))

    def handle_remove_own_vehicle(self, own_vehicle_id):
        """
            Simply Remove Owned Vehicle from Data, DB
        """
        self.func_lib.remove_own_vehicle(own_vehicle_id)
        card = self.own_vehicle_dict.pop(own_vehicle_id, None)
        self.own_inactive_vehicle_dict.pop(own_vehicle_id, None)

        if card:
            self.ui.OwnedVehicleScrollAreaWidgetContents.layout().removeWidget(card)
            card.deleteLater()

        if self.ui.OwnedVehicleScrollAreaWidgetContents.layout().count() == 0:
            self.ui.OwnedVehicleScrollAreaWidgetContents.layout().addWidget(self.add_vehicle_btn)
            self.add_vehicle_btn.show()

    def searcher_image_timer_starts(self):
        """
            Image Timer will load images on the screen
            using an optimized image loading method.
        """
        self.searcher_image_timer.stop()
        self.searcher_image_timer.start(100)

    def check_lazy_vehicle_loading(self):
        """
            Iterates through vehicle_card_dict to determine
            which Vehicle Card is currently displayed on screen,
            then renders the corresponding image.
        """
        for vid, widget in self.vehicle_card_dict.items():
            if isinstance(widget, VehicleSearchCardWidget):
                widget.update_visibility_logic(self.ui.SearchResultScrollArea)

    def property_image_timer_starts(self):
        """
            Image Timer will load images on the screen
            using an optimized image loading method.
        """
        self.property_image_timer.stop()
        self.property_image_timer.start(100)

    def check_lazy_property_loading(self):
        """
            Iterates through property_card_dict to determine
            which Property Card is currently displayed on screen,
            then renders the corresponding image.
        """
        for ptid, prop_widget in self.property_card_dict.items():
            prop_widget.update_visibility_logic(self.ui.PropertiesScrollArea)
        
        """
        ### LEGACY VERSION
        for ptid, cat_widget in self.property_category_dict.items():
            if isinstance(cat_widget, CategoryWidget):
                for pid, p_widget in cat_widget.pcard_dict.items():
                    p_widget.update_visibility_logic(self.ui.PropertiesScrollArea)
        """
                    

    def make_color_preset_card(self, preset, mini_sized=False, drag_available=False):
        """
            Simply Returns a Paint Preset Card || 
            Setting some Datas That Preset Cards Needs\n
            Mini will be used for 'subcard' from Vehicle Viewer,
            Drag will be used for Apply Preset To OwnVehicleCard
        """

        if preset is None:
            return None
        
        color_keys = [
            'primary', 'secondary', 'pearl', 'wheel', 
            'dial', 'trim', 'neon', 'headlight'
        ]
        index_data = self.func_lib.get_color_ref_list()
        new_data = preset.copy()

        prender_id = preset.get("primary_render_id")
        srender_id = preset.get("secondary_render_id")
        new_data['prender'] = self.all_managers.color.render_material.get(prender_id, 'Unknown')
        new_data['srender'] = self.all_managers.color.render_material.get(srender_id, 'Unknown')
        for ck in color_keys:
            color_id = preset.get(f"{ck}_color_id")
            new_data[ck] = index_data.get(color_id, {"hex_color": None, "name": "Unknown"})
        
        livery_type_id = preset.get("livery_type_id")
        new_data['livery_name'] = (self.all_managers.color.livery_type.get(livery_type_id) or {}).get('name', 'Unknown')

        new_data['is_modded'] = self.all_managers.color.is_preset_modded( new_data['id'] )

        return ColorPresetCard(new_data, self.all_managers.color.what_gradient_preview, mini_sized, drag_available, self.preset_filter_status)

    def add_paint_widget(self, preset):
        """
            This will Add Paint Preset Card to Paint Tab Layout and Vehicle Viewer\n
            Connects Proper Signals for them            
        """
        key = preset['id']
        paint_card = self.make_color_preset_card(preset)
        paint_sub_card = self.make_color_preset_card(preset, True, True)
        paint_card.adjust_content_size(self.paint_card_width)
        paint_sub_card.adjust_content_size(self.paint_subcard_width)
        self.paint_card_dict[key] = paint_card
        self.paint_subcard_dict[key] = paint_sub_card
        self.flow_layout_paint.addWidget(paint_card)
        self.flow_vehicle_paint.addWidget(paint_sub_card)
        paint_card.double_clicked.connect(self.handle_paint_double_click)
        paint_sub_card.double_clicked.connect(self.handle_paint_double_click)
        paint_card.right_clicked.connect(self.handle_paint_right_click)

        self.flow_layout_paint.invalidate()
        
    def add_new_preset(self):
        """
            This will be called when you Clicked Add Button from Paint Tab \n
            'Add Paint Preset Card' to data and DB
        """
        tempid = self.func_lib.add_paint_preset(is_hidden=False)
        target = self.func_lib.color_palette['Custom'][tempid]
        self.add_paint_widget(target)

        self.flow_layout_paint.removeWidget(self.add_paint_btn)
        self.flow_layout_paint.addWidget(self.add_paint_btn)

    def add_new_preset_in_vehicle_card(self, own_vehicle_id):
        """
            Make a Hidden Paint Preset for OwnVehicleCard\n
            This will be called When you Clicked Add Button from OwnVehicleCard \n
            If user Closed Dialog without saving, Paint Preset generated will be removed
        """
        tempid = self.func_lib.add_paint_preset(is_hidden=True)
        target = self.all_managers.color.paint_presets.get(tempid)

        paint_temp_card = self.make_color_preset_card(target, True, True)
        card_data = paint_temp_card.preset_data
        # paint_temp_card.double_clicked.connect(self.handle_paint_double_click)

        paint_list = self.func_lib.get_paint_list()
        render_map = self.all_managers.color.render_material
        livery_map = self.all_managers.color.livery_type
        dialog = PaintEditDialog(paint_list, render_map, livery_map, card_data, paint_temp_card, on_crew_add=self.add_crew_color_overall, parent=self)

        print(f"Adding New Preset with Temp Paint ID : {tempid}")

        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_data = copy.deepcopy(dialog.get_result())
            ### Successfully Saved Preset

            """
            ### Fix To DB From Temporary Added Crew Color
            added_crew_color = dialog.get_added_crew_color()
            for indexes, crew_ref in added_crew_color.items():
                popdata = paint_list['Index'].pop(indexes, None)
                if popdata is not None:
                    new_index = self.add_crew_color_overall(crew_ref['name'], crew_ref['hex_color'])
                    for tags, tag_data in updated_data.items():
                        if (tag_data == indexes) and tags not in {'id', 'name', 'is_hidden', 'primary_render_id', 'secondary_render_id'}:
                            updated_data[tags] = new_index
            """

            preset_id = updated_data.get('id', None)

            """
            if (paint_temp_card is not None):
                card_data = copy.copy(updated_data)
                paint_temp_card.edit_preset(card_data)
            """

            preset_name = updated_data.get('name', None)
            if preset_name is None:
                updated_data['name'] = "Custom Preset"


            ov_paintcard = self.make_color_preset_card(updated_data, True, False)
            ov_paintcard.double_clicked.connect(self.handle_paint_double_click)
            self.own_vehicle_dict.get(own_vehicle_id).set_paintcard_to_vehicle(ov_paintcard)
            
            ### Temporary data must be cleared before saving to the DB.
            preset_id = updated_data.pop('id', None)
            temp = updated_data.pop('primary', None)
            temp = updated_data.pop('secondary', None)
            temp = updated_data.pop('pearl', None)
            temp = updated_data.pop('wheel', None)
            temp = updated_data.pop('dial', None)
            temp = updated_data.pop('trim', None)
            temp = updated_data.pop('headlight', None)
            temp = updated_data.pop('neon', None)
            temp = updated_data.pop('livery', None)
            temp = updated_data.pop('prender', None)
            temp = updated_data.pop('srender', None)
            temp = updated_data.pop('livery_name', None)
            temp = updated_data.pop('is_modded', None)
            
            self.func_lib.edit_paint_preset(preset_id, **updated_data)
            print(f"updated : {preset_id} into {updated_data} ")

        
        ### Remove Preset because the user closed the dialog without saving.
        else:
            """
            added_crew_color = dialog.get_added_crew_color()
            for indexes, crew_ref in added_crew_color.items():
                popdata = paint_list['Index'].pop(indexes, None)
                if popdata is not None:
                    new_index = self.add_crew_color_overall(crew_ref['name'], crew_ref['hex_color'])
            """

            print(f"Removing Temp Paint ID : {tempid}")
            self.func_lib.remove_paint_preset(tempid)
        pass


    def on_vehicle_doubleclicked(self, index):
        """
            Double-click the Vehicle table to display the Vehicle information in the Vehicle Viewer.
        """
        row = index.row()
        vehicle_id = int(self.veh_proxy_model.data(self.veh_proxy_model.index(row, 0)))
        self.fill_vehicle_viewer(vehicle_id)
        self.ui.MenuSelect.setCurrentIndex(1)

    def on_vehicle_selected(self, index):
        """
            Select Vehicle Combobox from Vehicle Viewer Event
        """
        if index == -1:
            return
        
        selected_id = self.ui.VehicleSearchBarComboBox.itemData(index)
        if selected_id:
            self.fill_vehicle_viewer(selected_id)

    def on_garage_selected(self, index):
        """
            Select Garage Combobox from Garage Viewer Event
        """
        if index == -1:
            return
        
        selected_info = self.ui.GarageSelectBox.itemData(index)
        if selected_info:
            if isinstance(selected_info, list):
                selected_info = tuple(selected_info)
            # self.selected_garage_info = selected_info
            self.list_own_garage_vehicle(selected_info)

        self.update_garage_image()
    
    def update_garage_image(self):
        pixmap = ImageManager.get_image("Garage", self.selected_garage_info)
        self.ui.GarageImageLabel.set_image(pixmap)

    def on_garage_doubleclicked(self, index):
        """
            Double-click the Garage table to display 
            the Garage information in the Garage Viewer.\n
            Exclude the fourth column from this event,
            as it is reserved for memo editing.
        """
        col = index.column()
        if col == 4:
            return
        
        row = index.row()
        own_property_id = self.gar_proxy_model.data(self.gar_proxy_model.index(row, 4), Qt.UserRole)
        slot_type_id = self.gar_proxy_model.data(self.gar_proxy_model.index(row, 3), Qt.UserRole)
        ptype_id = self.gar_proxy_model.data(self.gar_proxy_model.index(row, 2), Qt.UserRole)
        garage_tuple = (own_property_id, slot_type_id, ptype_id)

        grg_idx = self.ui.GarageSelectBox.findData(garage_tuple)
        self.ui.GarageSelectBox.setCurrentIndex(grg_idx)
        # self.list_own_garage_vehicle(garage_tuple)
        self.ui.MenuSelect.setCurrentIndex(2)

    def handle_vcard_double_click(self, vehicle_data):
        """
            DoubleClick Vehicle Search Card to View Vehicle Details
        """
        self.fill_vehicle_viewer(vehicle_data['id'])
        self.ui.MenuSelect.setCurrentIndex(1)
        pass

    def handle_paint_right_click(self, preset_data):
        """
            Right Click Paint Preset To Remove It
        """
        preset_id = preset_data.get('id', None)

        paint_card = self.paint_card_dict.pop(preset_id, None)
        paint_sub_card = self.paint_subcard_dict.pop(preset_id, None)

        self.flow_layout_paint.removeWidget(paint_card)
        self.flow_vehicle_paint.removeWidget(paint_sub_card)

        paint_card.deleteLater()
        paint_sub_card.deleteLater()

        self.flow_layout_paint.invalidate()
        self.flow_vehicle_paint.invalidate()

        self.func_lib.remove_paint_preset(preset_id)

    def handle_paint_double_click(self, preset_data, selfcard=None):
        """
            Double Click Paint Preset To Pop up Editor Dialog
        """
        editorpresetcard = self.make_color_preset_card(preset_data)
        paint_list = self.func_lib.get_paint_list()
        render_map = self.all_managers.color.render_material
        livery_map = self.all_managers.color.livery_type
        dialog = PaintEditDialog(paint_list, render_map, livery_map, preset_data, editorpresetcard, on_crew_add=self.add_crew_color_overall, parent=self)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_data = copy.deepcopy(dialog.get_result())
            updb_data = copy.deepcopy(updated_data)
            ### Successfully Saved Preset
            
            preset_name = updated_data.get('name', None)
            if preset_name is None:
                updated_data['name'] = "Custom Preset"
                updb_data['name'] = "Custom Preset"

            ### Temporary data must be cleared before saving to the DB. 
            preset_id = updb_data.pop('id', None)
            temp = updb_data.pop('primary', None)
            temp = updb_data.pop('secondary', None)
            temp = updb_data.pop('pearl', None)
            temp = updb_data.pop('wheel', None)
            temp = updb_data.pop('dial', None)
            temp = updb_data.pop('trim', None)
            temp = updb_data.pop('headlight', None)
            temp = updb_data.pop('neon', None)
            temp = updb_data.pop('livery', None)
            temp = updb_data.pop('prender', None)
            temp = updb_data.pop('srender', None)
            temp = updb_data.pop('livery_name', None)
            temp = updb_data.pop('is_modded', None)
            
            # Update
            self.func_lib.edit_paint_preset(preset_id, **updb_data)
            print(f"updated : {preset_id} into {updb_data} ")
            """
            ### Fix To DB From Temporary Added Crew Color
            added_crew_color = dialog.get_added_crew_color()
            for indexes, crew_ref in added_crew_color.items():
                popdata = paint_list['Index'].pop(indexes, None)
                if popdata is not None:
                    new_index = self.add_crew_color_overall(crew_ref['name'], crew_ref['hex_color'])
                    for tags, tag_data in updated_data.items():
                        if (tag_data == indexes) and tags not in {'id', 'name', 'is_hidden', 'primary_render_id', 'secondary_render_id'}:
                            updated_data[tags] = new_index
            """

            ### Apply Data with Modded check in Preset Cards
            preset_id = updated_data.get('id', None)
            updated_data['is_modded'] = self.all_managers.color.is_preset_modded(preset_id)

            paintcard = self.paint_card_dict.get(preset_id, None)
            subpaintcard = self.paint_subcard_dict.get(preset_id, None)
            if (paintcard is not None) and (subpaintcard is not None):
                card_data = copy.copy(updated_data)
                paintcard.edit_preset(card_data)
                subpaintcard.edit_preset(card_data)
            if selfcard is not None:
                card_data = copy.copy(updated_data)
                selfcard.edit_preset(card_data)

        """
        ### Fix To DB From Temporary Added Crew Color
        else:
            added_crew_color = dialog.get_added_crew_color()
            for indexes, crew_ref in added_crew_color.items():
                popdata = paint_list['Index'].pop(indexes, None)
                if popdata is not None:
                    new_index = self.add_crew_color_overall(crew_ref['name'], crew_ref['hex_color'])
        """
        pass

    def handle_paint_color_filter(self):
        """
            Adjust the Palettes of Paint Presets in memory by checking the Paint Filter Checkbox.
        """
        sender_cb = self.sender()
        cb_name = sender_cb.objectName()
        is_checked = sender_cb.isChecked()

        self.preset_filter_status[cb_name] = is_checked

        ### Vanilla Filter and Synchronize two checkboxes
        if cb_name == "CheckVanillaPreset" or cb_name == "VanilaPaintCheckBox":
            self.ui.CheckVanillaPreset.setChecked(is_checked)
            self.ui.VanilaPaintCheckBox.setChecked(is_checked)
            self.filter_vanilla_color_preset(is_checked)
        else:
            self.apply_filter_to_cards()

    def filter_vanilla_color_preset(self, is_checked):
        """
            Loop paint_card_dict and Check 'is_modded' Flag
        """            
        self.ui.CustomPaintScrollAreaWidgetContents.setUpdatesEnabled(False)
        self.ui.PaintPresetScrollAreaWidgetContents.setUpdatesEnabled(False)

        while self.flow_layout_paint.count():
            item = self.flow_layout_paint.takeAt(0)
            itemsub = self.flow_vehicle_paint.takeAt(0)

        visible_count = 0

        for pkey, pcard in self.paint_card_dict.items():
            pscard = self.paint_subcard_dict.get(pkey, None)
            if not pscard: continue

            if pcard.is_modded() and is_checked:
                pcard.hide()
                pscard.hide()

            else:
                self.flow_layout_paint.addWidget(pcard)
                self.flow_vehicle_paint.addWidget(pscard)

                pcard.show()
                pscard.show()
                visible_count += 1

        self.flow_layout_paint.removeWidget(self.add_paint_btn)
        self.flow_layout_paint.addWidget(self.add_paint_btn)

        self.ui.CustomPaintScrollAreaWidgetContents.setUpdatesEnabled(True)
        self.ui.PaintPresetScrollAreaWidgetContents.setUpdatesEnabled(True)

        self.flow_layout_paint.invalidate()
        self.flow_vehicle_paint.invalidate()

    def apply_filter_to_cards(self):
        """
            Send Filter Value to Preset Cards
        """

        ### Filtering All Presets
        for pkey, pcard in self.paint_card_dict.items():
            pscard = self.paint_subcard_dict.get(pkey, None)
            if not pscard: continue

            pcard.set_hide_parts(self.preset_filter_status.get("CheckVanillaPreset", False),
                                 self.preset_filter_status.get("CheckWheelColor", False),
                                 self.preset_filter_status.get("CheckDialColor", False),
                                 self.preset_filter_status.get("CheckTrimColor", False),
                                 self.preset_filter_status.get("CheckLivery", False),
                                 self.preset_filter_status.get("CheckNeonLights", False),
                                 self.preset_filter_status.get("CheckHeadlights", False),
                                 )
            
            pscard.set_hide_parts(self.preset_filter_status.get("CheckVanillaPreset", False),
                                  self.preset_filter_status.get("CheckWheelColor", False),
                                  self.preset_filter_status.get("CheckDialColor", False),
                                  self.preset_filter_status.get("CheckTrimColor", False),
                                  self.preset_filter_status.get("CheckLivery", False),
                                  self.preset_filter_status.get("CheckNeonLights", False),
                                  self.preset_filter_status.get("CheckHeadlights", False),
                                  )

    def handle_property_checked(self, prop_id, is_checked):
        """
            Uses the Property Card checkbox state
            to determine whether the property is owned or removed.
        """

        ### Property Checked == Purchased It
        if is_checked:
            prop_data = self.all_managers.property.property_map.get(prop_id)
            # print(f"Property Checked :: {prop_data}")
            ptype_id = prop_data.get('type_id')
            own_list = self.all_managers.property.own_map.get(ptype_id)

            ### Check if the user ends up owning more Property than the number permitted.
            addflag = False

            max_count = len(own_list)
            tmp_property = None
            
            for i in range(max_count):
                if own_list[i] is None:
                    addflag = True
                    break
                elif own_list[i]['is_active'] == 0:
                    addflag = True
                    tmp_property = own_list[i]
                    break
                elif (max_count == 1) and (own_list[i]['is_active'] == 1):
                    tmp_property = own_list[i]
                    break

            ### Passed Purchase Condition
            if addflag:
                result = self.func_lib.enable_own_property(prop_id)
                own_pid = result['own_pid']
                if result['success'] == False:
                    QMessageBox.critical(self, "Error", f"{result['msg']}")
                else:
                    # QMessageBox.critical(self, "DEBUG", f"{result['msg']}")
                    pass

                ### Eclipse Blvd 50 Garage Option
                if prop_id in {225, 226, 227, 228, 229}:
                    for ebvd in [225, 226, 227, 228, 229]:
                        self.property_card_dict[ebvd].enable_checkbox()

                """
                    Changes the owned property if the user
                    is limited to owning only one property
                    and already has one.
                """
                
            elif (max_count == 1) and (addflag == False) and (tmp_property is not None):
                own_pid = self.func_lib.change_own_property(tmp_property['property_id'], prop_id)

            ### Cannot Purchase > Disable checkbox
            else:
                QMessageBox.critical(self, "Error", f"You cannot purchase any more of this type")
                self.property_card_dict[prop_id].disable_checkbox()
                return
            
            ### ownv_selectable_garage_dict에 row 추가하기 >> OwnVehicleCard에 동기화됨
            owned_prop = self.all_managers.property.owned_property.get(own_pid, None)
            if (owned_prop is None) or (owned_prop.get('is_active', False) == False):
                print(f"something wrong here : {own_pid}")
            else:
                """
                    Purchased Property Needs to Register Garage Data,
                    Add Garage Key to Garage Dict and Refresh all OwnVehicleCards
                """
                slots_info = self.all_managers.storage.ptype_slot_map.get(ptype_id, {})
                vehicle_row = self.all_managers.vehicle.get_vehicle(self.current_veiwer_veicle_id)

                if vehicle_row is not None:
                    for slottype_id, max_count in slots_info.items():
                        if self.all_managers.storage.is_compatible(vehicle_row, slottype_id):
                            prop_name = self.all_managers.property.property_map.get(prop_id, {}).get('key_name', 'Unknown')
                            prop_entry = copy.copy(owned_prop)
                            prop_entry['property_name'] = prop_name
                            prop_entry['slot_type_id'] = slottype_id
                            prop_entry['slot_type_name'] = self.all_managers.storage.slot_type_map.get(slottype_id, 'Unknown')
                            prop_entry['slot_left'] = self.func_lib.strg_svc.get_number_of_empty_slot(own_pid, slottype_id)

                            key = (prop_entry['id'], prop_entry['slot_type_id'], prop_entry['property_type_id'])
                            self.ownv_selectable_garage_dict[key] = prop_entry

                            for ownid, ovcard in self.own_vehicle_dict.items():
                                ovcard.add_available_garage_dict(key, prop_entry)

            self.set_garage_select_box()        

        ### Yes, Checkbox Disabled. 
        else:
            self.func_lib.disable_own_property(prop_id)

        ### determines whether the garage data needs to be refreshed.
        self.need_refresh_garage = True

    def handle_property_details(self, property_id):
        """
            Opens a dialog for Property Custom
            when the PropertyCard image is clicked.\n
            As with Property, Category and Property widgets are pre-created.\n
            Since there is no parent category in this case,
            the widgets are added directly to the layout.
        """
        property_data = copy.copy(self.all_managers.property.property_map.get(property_id))
        property_type_id = property_data.get('type_id')
        property_data['type_name'] = self.all_managers.property.property_type_map.get(property_type_id, None).get('key_name', 'Unknown')
        
        otmap_list = self.all_managers.property.own_map.get(property_type_id, [])      
        for own_property in otmap_list:           
            if own_property and (own_property.get('property_id', None) == property_id):
                self.current_selected_own_property_id = own_property['id']
                break

        if self.current_selected_own_property_id is None:
            return

        car_slot_count = 0
        plane_slot_count = 0
        bike_slot_count = 0
        ect_slot_count = 0

        for slot_type_id, number_of_slot in self.all_managers.storage.ptype_slot_map[property_type_id].items():
            slot_name = self.all_managers.storage.slot_type_map.get(slot_type_id, None)
            if slot_name == 'Garage':
                car_slot_count = number_of_slot
                continue
            elif slot_name == 'Hangar':
                plane_slot_count = number_of_slot
                continue
            elif slot_name == 'Bike':
                bike_slot_count = number_of_slot
                continue
            else:
                ect_slot_count += number_of_slot\
                
        slot_data = (car_slot_count, plane_slot_count, bike_slot_count, ect_slot_count)

        self.custom_card_dict.clear()
        self.custom_category_dict.clear()
        self.btn_group_dict.clear()
        self.custom_card_dict = dict()
        self.custom_category_dict = dict()
        self.btn_group_dict = dict()

        customs = self.func_lib.get_clicked_property_data(property_id)  
        # print(f"get clicked {property_id} >>> {customs}")
        for ctype_id, custom_list in customs.items():
            ctype_data = self.all_managers.property.property_custom_type_map.get(ctype_id, None)

            ctype_card = CategoryWidget(ctype_data, True)
            ctype_card.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
            self.custom_category_dict[ctype_id] = ctype_card

            ctype_radio = (self.all_managers.property.get_pcustom_max_owned(ctype_id) == 1)

            ctype_button_group = QButtonGroup(self)

            if (ctype_data.get('max_owned') > 1):
                ctype_button_group.setExclusive(False)
            else:
                ctype_button_group.setExclusive(True)
            self.btn_group_dict[ctype_id] = ctype_button_group

            for custom in custom_list:
                custom_card = PropertyCard(custom)
                # print(f"{custom['id']} :: {ctype_radio}, {custom['is_owned']}, {ctype_data.get('is_unchangeable')}")
                custom_card.init_selector_button(ctype_radio, custom['is_owned'], ctype_data.get('is_unchangeable'))
                custom_card.property_changed.connect(self.handle_custom_checked)
                ctype_card.add_child(custom_card)
                self.custom_card_dict[custom['id']] = custom_card

                if custom_card.is_ready_to_use():
                    ctype_button_group.addButton(custom_card.selector)

        dialog = PropertyCustomDialog(property_data, slot_data, self.custom_category_dict, parent=self)
        dialog.exec()   
        self.current_selected_own_property_id = None
        self.need_refresh_garage = True

    def handle_custom_checked(self, custom_id, is_checked):
        """
            Uses the Property Card checkbox state
            to determine whether the PropertyCustom is owned or removed.
        """
        if self.current_selected_own_property_id is None:
            return
            
        # print(f"This is PCustom Handle for {custom_id} is {is_checked}")
        own_custom_list = self.all_managers.property.get_own_custom_list_from_cid(self.current_selected_own_property_id, custom_id)
        # print(own_custom_list)
        max_owned = self.all_managers.property.get_pcustom_max_owned_from_cid(custom_id)
        cur_count = len(own_custom_list)

        # max==1이고 이미 값 있을 경우 edit
        # max보다 소유가 적을 경우 enable
        # max > 1이고 이미 값 있을 경우 취소
        if is_checked:
            if (max_owned - cur_count) > 0:
                result = self.func_lib.enable_own_property_custom(self.current_selected_own_property_id, custom_id)
                if result['success'] == False:
                    QMessageBox.critical(self, "Error", f"{result['msg']}")

            elif (max_owned == 1) and (cur_count == 1):
                bef_custom_data = own_custom_list[0]
                bef_cid = bef_custom_data.get('id')

                result = self.func_lib.change_own_property_custom(self.current_selected_own_property_id, bef_cid, custom_id)
                if result == False:
                    QMessageBox.critical(self, "Error", f"Cannot Find Custom Data Error")
            
            else:
                QMessageBox.critical(self, "Error", f"You cannot purchase any more of this type")
                self.custom_card_dict[custom_id].disable_checkbox()

        else:
            self.func_lib.disable_own_property_custom(self.current_selected_own_property_id, custom_id)
        pass     

        self.need_refresh_garage = True

    def handle_new_crew_color(self):
        """
            Add New Crew Color When Add Button in Paint Tab Sidebar Pressed
        """
        name, hex = show_color_picker_dialog(self, "CREW", "000000")
        if (name is not None) and (hex is not None):
            self.add_crew_color_overall(name, hex)

    def add_crew_color_overall(self, name, hex):
        """
            Adding Crew Color Reference Logic,
            returns crew color id
        """
        new_id = self.func_lib.add_crew_color(name, hex)

        total_ref_list = self.func_lib.get_color_ref_list()
        target_ref = total_ref_list.get(new_id, None)
        if target_ref is not None:
            color_widget = ColorReferenceWidget(target_ref)
            color_widget.double_clicked.connect(self.handle_edit_crew_color)
            self.crew_color_dict[new_id] = color_widget
            color_widget.fillWidget()
            self.ui.CrewColorListScrollContents.layout().addWidget(color_widget)

        return new_id


    def handle_edit_crew_color(self, color_ref):
        """
            DoubleClick Color Reference Widget to Show Crew color Editor \n
            Then Save to DB
        """
        target_name = color_ref.get('name', None)
        sharp_hex = color_ref.get('hex_color', None)
        color_id = color_ref.get('id', -1)
        if (sharp_hex is not None) and (target_name is not None) and (color_id != -1):
            target_hex = sharp_hex.lstrip('#')
            chngd_name, chngd_hex = show_color_picker_dialog(self, target_name, target_hex)

            if (chngd_name is not None) and (chngd_hex is not None):
                self.func_lib.edit_crew_color(color_id, chngd_name, chngd_hex)

                color_ref['name'] = chngd_name
                color_ref['hex_color'] = chngd_hex

                target_widget = self.crew_color_dict.get(color_id)
                if target_widget:
                    target_widget.setWidget(color_ref)

    def on_filter_changed(self):
        """
            Filter Timer will prevent to keep searching\n
            Timer 750ms.
        """
        self.searcher_filter_timer.stop()
        self.searcher_filter_timer.start(750)
        

    def search_filter_changed(self):
        """
            When Filter in Vehicle Search has changed,
            Get All Filter Datas and Update Search Cards
        """
        vehicle_name = self.ui.NameSearcher.displayText()
        selected_class = self.ui.ClassSearcher.currentText()
        selected_manuf = self.ui.ManufacturerSearcher.currentText()
        selected_acq = self.ui.AcquisitionSearcher.currentText()
        input_seat = self.ui.SeatInput.displayText()
        seat_ops = self.ui.SeatSearcher.currentText()
        sort_order = self.ui.SortingOrder.currentIndex() + 1
        reverse_order = not self.ui.ReverseSortCheck.isChecked()

        vname = None if vehicle_name == '' else vehicle_name
        v_class = None if selected_class == '' else selected_class
        mnftrs = None if selected_manuf == '' else selected_manuf
        acq = None if selected_acq == '' else selected_acq
        op_str = None if seat_ops == '' else seat_ops
        basis_seat = None if input_seat == '' else int(input_seat)

        self.update_search_cards_display(sort_order, reverse_order,
                                          vname=vname, vclasses=v_class,
                                          mnftrs=mnftrs, acq=acq,
                                          seat=basis_seat, op_str=op_str)


    def update_search_cards_display(self, sorting_order, is_reversed, **filters):
        """
            First hides all Vehicle Search Cards, \n
            then finds vehicle IDs matching the filter conditions
            and repositions the corresponding cards.
        """
        ### Loading Screen
        if not hasattr(self, 'overlay'):
            self.overlay = LoadingOverlay(self.ui.Search)
        self.overlay.setGeometry(self.ui.Search.rect())
        self.overlay.show()
        self.overlay.raise_()

        ### Get List That already Filtered and sorted
        target_data_list = self.func_lib.get_vehicle_list(sorting_order, is_reversed, **filters)
        
        self.ui.SearchResultScrollGridContainer.setUpdatesEnabled(False)
        
        while self.flow_layout.count():
            item = self.flow_layout.takeAt(0)
            if item.widget():
                item.widget().hide()

        visible_count = 0
        
        ### re-add widgets via Iterating sorted vehicle list
        for vehicle_data in target_data_list:
            card = self.vehicle_card_dict.get(vehicle_data['id'])
            
            if card:
                #row = visible_count // self.vehicle_search_column_count
                #col = visible_count % self.vehicle_search_column_count
                #self.ui.SearchResultScrollGridContainer.layout().addWidget(card, row, col)
                self.flow_layout.addWidget(card)
                card.show()
                visible_count += 1

            ### Optimized by processing in batches of 50
            if visible_count % 50 == 0:
                QCoreApplication.processEvents()

        """
        all_card_ids = set(self.vehicle_card_dict.keys())
        target_ids = set(v['id'] for v in target_data_list)
        hide_ids = all_card_ids - target_ids
        
        for v_id in hide_ids:
            # self.vehicle_card_dict[v_id].hide()
            pass
        """

        self.ui.SearchResultScrollGridContainer.setUpdatesEnabled(True)

        self.overlay.hide()

        self.searcher_image_timer_starts()
        
    def fill_vehicle_viewer(self, vehicle_id):
        """
            Fill Labels in Vehicle Viewer\n
            Add Own Vehicle Cards\n
            Show Acquisition Cards
        """

        ### Measure the height of the Own Card
        self.set_own_card_height()
        self.current_veiwer_veicle_id = vehicle_id
        vsbcb_id = self.ui.VehicleSearchBarComboBox.findData(vehicle_id)
        
        if vsbcb_id != -1:
            self.ui.VehicleSearchBarComboBox.setCurrentIndex(vsbcb_id)
        vehicle_data = self.func_lib.get_clicked_vehicle_data(vehicle_id)

        if vehicle_data is None:
            print(f"vehicle_data is None : on_vehicle_doubleclicked '{vehicle_id}' ")
            return

        ### Fill Labels
        laptime = format_lap_time(vehicle_data['laptime_ms'])
        topspeed = value_to_percentage(vehicle_data['topspeed_10mtph'])

        graph_speed = value_to_percentage(vehicle_data.get('graph_speed', ''))
        graph_acc = value_to_percentage(vehicle_data.get('graph_acc', ''))
        graph_brake = value_to_percentage(vehicle_data.get('graph_brake', ''))
        graph_handle = value_to_percentage(vehicle_data.get('graph_handle', ''))

        sizecm_x = value_to_percentage(vehicle_data.get('sizecm_x', ''))
        sizecm_y = value_to_percentage(vehicle_data.get('sizecm_y', ''))
        sizecm_z = value_to_percentage(vehicle_data.get('sizecm_z', ''))

        self.ui.ManufacturerNameLabel.setText(str(vehicle_data['manufacturer']))
        self.ui.ManuKORnameLabel.setText(str(vehicle_data['manu_translated']))
        self.ui.VehicleNameLabel.setText(str(vehicle_data['name']))
        self.ui.VehicleKORnameLabel.setText(str(vehicle_data['translated_name']))
        self.ui.VehicleTypeLabel.setText(str(vehicle_data['vehicle_class']))
        self.ui.PriceLabel.setText(str(vehicle_data.get('price', 'No Price')))
        self.ui.SeatsLabel.setText(f"{vehicle_data['seats']} seats")
        self.ui.MassLabel.setText(f"{vehicle_data['mass']} kg")
        self.ui.GearLabel.setText(f"{vehicle_data['gears']} gears")
        self.ui.DrivetrainLabel.setText(str(vehicle_data['drivetrain']))
        self.ui.LaptimeLabel.setText(str(laptime))
        self.ui.TopspeedLabel.setText(f"{topspeed} km/h")
        self.ui.SizeLabel.setText(f"{sizecm_x} * {sizecm_y} * {sizecm_z}")
        
        self.ui.SpeedInputLabel.setText(str(graph_speed))
        self.ui.AccInputLabel.setText(str(graph_acc))
        self.ui.BrakeInputLabel.setText(str(graph_brake))
        self.ui.HandleInputLabel.setText(str(graph_handle))

        if isinstance(graph_speed, str):
            graph_speed = 0
        if isinstance(graph_acc, str):
            graph_acc = 0
        if isinstance(graph_brake, str):
            graph_brake = 0
        if isinstance(graph_handle, str):
            graph_handle = 0

        self.ui.SpeedProgressBar.setValue(graph_speed)
        self.ui.ACCProgressBar.setValue(graph_acc)
        self.ui.BrakeProgressBar.setValue(graph_brake)
        self.ui.HandleProgressBar.setValue(graph_handle)


        ### Performs the initial setup required to add an OwnVehicleCard
        own_data = self.func_lib.get_clicked_vehicle_own(vehicle_id)
        self.own_vehicle_dict.clear()
        self.own_inactive_vehicle_dict.clear()
        self.own_index = 0
        while self.ui.OwnedVehicleScrollAreaWidgetContents.layout().count():
            item = self.ui.OwnedVehicleScrollAreaWidgetContents.layout().takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        self.ui.OwnedVehicleScrollAreaWidgetContents.layout().invalidate()
        
        ### Add OwnVehicleCards
        available_garagelist = self.func_lib.get_garages_for_own_vehicle(vehicle_id)
        self.ownv_selectable_garage_dict.clear()
        for slot_data in available_garagelist:
            key = (slot_data['id'], slot_data['slot_type_id'], slot_data['property_type_id'])
            self.ownv_selectable_garage_dict[key] = slot_data

        for owns in own_data:
            self.add_own_vehicle_widget(owns)

        
        ### Hide All ACQ Cards and re-Add ACQ Cards needed
        while self.ui.AcquisitionScrollAreaContents.layout().count():
            item = self.ui.AcquisitionScrollAreaContents.layout().takeAt(0)
            widget = item.widget()
            if widget:
                widget.hide()
            

        acq_data = self.func_lib.get_clicked_vehicle_acq(vehicle_id)

        for acq in acq_data:
            acq_card = self.acq_card_dict[acq]
            acq_card.adjust_content_size(self.acq_card_height)
            self.ui.AcquisitionScrollAreaContents.layout().addWidget(acq_card)
            acq_card.show()

        ### Add Own Vehicle Add Button
        self.add_vehicle_btn = AddButtonCard()
        self.add_vehicle_btn.setFixedSize(int(self.own_card_height*7/3), self.own_card_height)
        self.add_vehicle_btn.clicked.connect(lambda: self.add_new_own_card(vehicle_id))
        if not((self.own_index > 0) and (vehicle_data['is_unique'] == True)):
            self.ui.OwnedVehicleScrollAreaWidgetContents.layout().addWidget(self.add_vehicle_btn)
            self.add_vehicle_btn.show()

            for solds in self.own_inactive_vehicle_dict.values():
                self.ui.OwnedVehicleScrollAreaWidgetContents.layout().removeWidget(solds)
                self.ui.OwnedVehicleScrollAreaWidgetContents.layout().addWidget(solds)

        ### Load Manufacturer and Vehicle Image
        pixmap = ImageManager.get_image("Vehicle", vehicle_data['id'])
        logomap = ImageManager.get_image("Manufacturer", vehicle_data['manufacturer'])
        self.ui.VehicleImageLabel.set_image(pixmap)
        self.ui.ManufacturerImageLabel.set_image(logomap)
    
    def update_vehicle_viewer_image(self):
        """
            Update Vehicle Image in Vehicle Viewer
        """
        pixmap = ImageManager.get_image("Vehicle", self.current_veiwer_veicle_id)
        self.ui.VehicleImageLabel.set_image(pixmap)

    def update_garage_viewer_image(self):
        """
            Update Garage Image in Garage Viewer
        """
        pixmap = ImageManager.get_image("Garage", self.selected_garage_info)
        self.ui.GarageImageLabel.set_image(pixmap)

    def list_own_garage_vehicle(self, garage_info):
        """
            Binds to the Garage Card Model
            and retrieves vehicle information stored in the garage.
        """
        self.selected_garage_info = garage_info

        own_property_id = garage_info[0]
        slot_type_id = garage_info[1]

        garage_memo = self.all_managers.property.get_memo_own_property(own_property_id)
        self.ui.GarageMemoTextLabel.setText(garage_memo)
    
        car_list = self.func_lib.get_own_vehicle_list_in_garage(own_property_id, slot_type_id)
        self.garage_card_model.set_all_cars(car_list)
        self.setup_garage_view(self.garage_card_model)


        """
        구) 카드 ScrollArea 배치 방식

        self.garage_own_card_dict.clear()
        while self.ui.GarageOwnedCarContentWidget.layout().count():
            item = self.ui.GarageOwnedCarContentWidget.layout().takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        vehicle_list = self.func_lib.get_own_vehicle_list_in_garage(own_property_id)
        for slot_type_id, slots in vehicle_list.items():
            print(vehicle_list)
            for slot_index, own_data in slots.items():
                if own_data is None:
                    continue
                vehicle_data = self.func_lib.get_clicked_vehicle_data( own_data.get("vehicle_id", 0) ) 
                
                color_data = self.all_managers.color.paint_presets.get(own_data.get('paint_preset_id'), None)
                color_card = self.make_color_preset_card(color_data, True, False)

                garage_own_card = GarageCarPreviewCard(vehicle_data, own_data, color_card)
                garage_own_card.data_changed.connect(self.handle_own_vehicle_update)
                garage_own_card.adjust_content_size(self.garage_card_width)
                self.garage_own_card_dict[own_data['id']] = garage_own_card
                self.ui.GarageOwnedCarContentWidget.layout().addWidget(garage_own_card)

        self.ui.GarageOwnedCarContentWidget.layout().addStretch(1)
        """


    def setup_garage_view(self, model):
        """
            Garage View Setup by GPT
        """
        self.ui.GarageCardListView.setModel(model)

        # 1. Enable Drag and Drop
        self.ui.GarageCardListView.setDragEnabled(True) # Can start drag from here
        self.ui.GarageCardListView.setAcceptDrops(True) # Can receive drops here
        self.ui.GarageCardListView.setDropIndicatorShown(True) # Show the line where drop will occur ⭐
        self.ui.GarageCardListView.setDefaultDropAction(Qt.DropAction.MoveAction) # Default action is moving
        self.ui.GarageCardListView.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove) # Drag within this view only ⭐
        

        # 2. visual Style
        self.ui.GarageCardListView.setSpacing(10) # Gap between cards ⭐
        self.ui.GarageCardListView.setViewMode(QListView.ListMode) # Items wrap to fit parent width
        self.ui.GarageCardListView.setFlow(QListView.TopToBottom) # Stacks items vertically ⭐
        self.ui.GarageCardListView.setResizeMode(QListView.Adjust) # Re-calculates layout on resize ⭐
        self.ui.GarageCardListView.setMovement(QListView.Snap) # Snaps to grid positions while dragging
        self.ui.GarageCardListView.setWrapping(False)
        self.ui.GarageCardListView.setSpacing(0)
        self.ui.GarageCardListView.setViewportMargins(3,3,3,3)
        self.ui.GarageCardListView.setAutoScroll(True)
        self.ui.GarageCardListView.setAutoScrollMargin(50)
        self.ui.GarageCardListView.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.ui.GarageCardListView.verticalScrollBar().setSingleStep(20)

        self.ui.GarageCardListView.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.ui.GarageCardListView.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # 3. Apply custom Delegate
        self.carCardDelegate = CarCardDelegate(self.all_managers.vehicle.vehicle_map, self.ui.GarageCardListView)
        self.ui.GarageCardListView.setItemDelegate(self.carCardDelegate)

        self.ui.GarageCardListView.setStyleSheet("""
            QListView {
                show-decoration-selected: 1;
            }
            QListView::item:hover {
                background-color: rgba(52, 152, 219, 20);
            }
        """)
        
        # Handle Drag Start Only on the Grab Handle Region ⭐
        # By default, dragging starts on whole item. Override with event filter.
        # self.ui.GarageCardListView.installEventFilter(self.carCardDelegate)
        self.ui.GarageCardListView.viewport().installEventFilter(self.carCardDelegate)

        print("Setup Garage View Complete!")
        return True

    def save_garage_order(self):
        """
            Reflect the order of the Vehicles
            designated by carCardDelegate directly into the Slot Data
        """
        current_cars = self.garage_card_model.cars
        for index, car_data in enumerate(current_cars):
            if car_data.get('slot_index', None) == (index + 1):
                continue
            car_id = car_data.get('id')
            car_data['slot_index'] = index + 1

        if self.selected_garage_info[0] != 0:
            self.func_lib.strg_svc.rebuild_garage_slot_map(self.selected_garage_info[0])
            
    def showEvent(self, event):
        """
            Update card size After App Launched
        """
        print("Making Widgets...")
        self.update_card_sizes()
        super().showEvent(event)

    def resizeEvent(self, event):
        """
            Update card size After Resizing Window
        """
        
        current_size = event.size()

        if current_size == self.last_size:
            return
        
        self.last_size = current_size

        self.resize_timer.stop()
        self.resize_timer.start(100)
        
        
        super().resizeEvent(event)

    def handle_tab_changed(self, index):
        """
            This Event Called After User Changes The Tab
        """
        if index == 0:
            self.update_search_sizes()
        elif index == 1:
            if self.current_veiwer_veicle_id is not None:
                self.fill_vehicle_viewer(self.current_veiwer_veicle_id)
            self.update_paint_subcard_size()
        elif index == 2:
            self.update_garage_card_size()
        elif index == 3:
            #self.fill_vehicle_table()
            pass
        elif index == 4:
            if self.need_refresh_garage:
                self.fill_garage_table()
                self.need_refresh_garage = False
            pass
        elif index == 5:
            self.update_paint_sizes()
        elif index == 6:
            self.update_property_sizes()
        elif index == 7:
            self.init_stat_viewer()

    def update_card_sizes(self):
        """
            Update All Card Sizes
        """
        self.update_search_sizes()
        self.update_property_sizes()
        self.update_paint_sizes()
        self.update_paint_subcard_size()
        self.update_own_vehicle_size()
        # self.update_garage_card_size()

    def update_search_sizes(self):
        """
            Determines the number of cards that can fit per row
            in the Flow Layout while keeping the card size
            between 250 and 400,
            then resizes the cards accordingly.
        """

        total_width = self.ui.SearchResultScrollArea.viewport().width() - 1
        
        ### Determines the number of cards that can fit per row
        spacing = self.flow_layout.spacing()
        margins = self.flow_layout.contentsMargins()
        column_count = max(1, ((total_width - margins.left() - margins.right() + spacing) // (250  + spacing)))

        net_width = total_width - margins.left() - margins.right() - (spacing * (column_count - 1))
        target_card_width = max(250, min(400, net_width // column_count))

        if self.vehicle_card_width != target_card_width:
            self.vehicle_card_width = target_card_width
            
            ### resizes the cards
            for card in self.vehicle_card_dict.values():
                card.adjust_content_size(target_card_width)
                card.setFixedWidth(target_card_width)
                # card.setFixedHeight(target_card_width * 1.2)
            
            ### Layout Updates
            self.flow_layout.invalidate() 

        self.searcher_image_timer_starts()

    def update_property_sizes(self):
        """
            Determines the number of cards that can fit per row
            in the Flow Layout while keeping the card size
            between 200 and 400,
            then resizes the cards accordingly.
        """
        self.ui.PropertiesScrollArea.setWidgetResizable(True)
        total_width = self.ui.PropertiesScrollArea.viewport().width()
        column_count = max(1, ((total_width + 5) // (200  + 5)))
        net_width = total_width - (5 * (column_count - 1))
        target_card_width = max(200, min(400, net_width // column_count))
        self.property_card_width = target_card_width
        """
        for pcard in self.property_card_dict.values():
            pcard.adjust_content_size(target_card_width)
        """
        for category in self.property_category_dict.values():
            category.adjust_content_size(total_width, target_card_width)
        

        self.check_lazy_property_loading()

    def update_paint_sizes(self):
        """
            Determines the number of cards that can fit per row
            in the Flow Layout while keeping the card size
            between 200 and 300,
            then resizes the cards accordingly.
        """

        total_width = self.ui.PaintPresetScrollArea.viewport().width() - 1

        ### Determines the number of cards that can fit per row
        self.flow_layout_paint.setSpacing(1)
        spacing = self.flow_layout_paint.spacing()
        margins = self.flow_layout_paint.contentsMargins()
        column_count = max(1, ((total_width - margins.left() - margins.right() + spacing) // (200  + spacing)))

        net_width = total_width - margins.left() - margins.right() - (spacing * (column_count - 1))
        target_card_width = max(200, min(300, net_width // column_count))
        self.paint_card_width = target_card_width
        self.add_paint_btn.setFixedWidth(target_card_width)
        self.add_paint_btn.setFixedHeight(target_card_width)

        ### resizes the cards
        for card in self.paint_card_dict.values():
            card.adjust_content_size(target_card_width)
            card.setFixedWidth(target_card_width)
            # card.setFixedHeight(target_card_width * 1.2)
        
        ### Layout Updates
        self.flow_layout_paint.invalidate() 

    def update_paint_subcard_size(self):
        """
            Determines the number of cards that can fit per row
            in the Flow Layout while keeping the card size
            between 50 and 100,
            then resizes the cards accordingly.
        """
        total_width = self.ui.CustomPaintScrollArea.viewport().width() - 1
        
        ### Determines the number of cards that can fit per row
        self.flow_vehicle_paint.setSpacing(1)
        spacing = self.flow_vehicle_paint.spacing()
        margins = self.flow_vehicle_paint.contentsMargins()
        column_count = max(1, ((total_width - margins.left() - margins.right() + spacing) // (50  + spacing)))

        net_width = total_width - margins.left() - margins.right() - (spacing * (column_count - 1))
        target_card_width = max(50, min(100, net_width // column_count))
        # print(target_card_width)
        self.paint_subcard_width = target_card_width

        ### resizes the cards
        for card in self.paint_subcard_dict.values():
            card.adjust_content_size(target_card_width)
            card.setFixedWidth(target_card_width)
            # card.setFixedHeight(target_card_width * 1.2)
        
        ### Layout Updates
        self.flow_vehicle_paint.invalidate() 

    def update_own_vehicle_size(self):
        """
            Resizes OwnVehicleCard to match the layout height.
        """
        total_height = self.set_own_card_height()

        self.add_vehicle_btn.setFixedSize(int(total_height*7/3), total_height)

        ### resizes the cards
        for card in self.own_vehicle_dict.values():
            card.adjust_content_size(total_height)
            card.setFixedHeight(total_height)
            # card.setFixedHeight(target_card_width * 1.2)
        
        ### Layout Updates
        self.flow_vehicle_paint.invalidate() 
    
    def set_own_card_height(self):
        """
            It Returns OwnedVehicleScrollArea's Height\n
            It will be used for OwnVehicleCard's Size
        """
        total_height = max(125 ,self.ui.OwnedVehicleScrollArea.viewport().height() - 1)
        self.own_card_height = total_height
        return total_height

    def update_acq_card_size(self):
        """
            ###Not Using####\n
            Resizes AcquisitionCard to match the layout height.
        """
        total_height = self.ui.AcquisitionScrollArea.viewport().height() -1

        self.acq_card_height = total_height

        ### resizes the cards
        for card in self.acq_card_dict.values():
            card.adjust_content_size(total_height)
            card.setFixedHeight(total_height)

        ### Layout Updates
        # self.flow_vehicle_paint.invalidate() 

    def update_garage_card_size(self):
        """
            ###Not Using####\n
            Resizes Card to match the layout width.
        """
        total_width = 320 #self.ui.OwnedCarListScrollArea.viewport().width() - 1

        self.garage_card_width = total_width

        for ovid, card in self.garage_own_card_dict.items():
            card.adjust_content_size(total_width)
            card.setFixedWidth(total_width)

        # GarageOwnedCarContentWidget.layout()

    def handle_image_update(self, category, data_id):
        """
            Replaces the Existing Images
            After successfully Updated Images in the ImageManagerDialog
        """
        ImageManager.update_image(category, data_id)

        if category == 'Vehicle':
            target_vcd = self.vehicle_card_dict.get(data_id, None)
            if target_vcd is not None:
                target_vcd.update_vehicle_image()

            if self.current_veiwer_veicle_id == data_id:
                self.update_vehicle_viewer_image()

            self.ui.GarageCardListView.viewport().update()

        elif category == 'Garage':
            if isinstance(data_id, list):
                data_id = tuple(data_id)

            if self.selected_garage_info == data_id:
                self.update_garage_viewer_image()

        else:
            return

        # Garage : VehicleViewer, GarageViewer

    def init_scroll_design(self, scroll_area):
        """
            Modern Scroll Bar Design By Gemini
        """
        scroll_area.setStyleSheet("""
                            /* 배경색 설정 */
                            QScrollArea {
                                background-color: transparent;
                            }
                                                   
                            QWidget {
                                background-color: transparent;
                            }                       
                                       
                            /* 전체 스크롤바 설정 (가로/세로 공통) */
                            QScrollBar:vertical {
                                border: none;
                                background: transparent;  /* 배경 투명하게 */
                                width: 8px;               /* 얇게 설정 */
                                margin: 0px 0px 0px 0px;
                            }

                            /* 스크롤 핸들 (움직이는 막대기) */
                            QScrollBar::handle:vertical {
                                background: #C0C0C0;      /* 연한 회색 */
                                min-height: 30px;
                                border-radius: 4px;       /* 둥글게 */
                            }

                            /* 마우스 올렸을 때 핸들 색상 변경 */
                            QScrollBar::handle:vertical:hover {
                                background: #A0A0A0;      /* 조금 더 진한 회색 */
                            }

                            /* 화살표 버튼 (보통 숨김 처리) */
                            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                                border: none;
                                background: none;
                                height: 0px;
                            }

                            /* 핸들 위아래의 레일 영역 (배경) */
                            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                                background: none;
                            }
                                  
                            /* 전체 스크롤바 설정 (가로/세로 공통) */
                            QScrollBar:horizontal {
                                border: none;
                                background: transparent;  /* 배경 투명하게 */
                                width: 8px;               /* 얇게 설정 */
                                margin: 0px 0px 0px 0px;
                            }

                            /* 스크롤 핸들 (움직이는 막대기) */
                            QScrollBar::handle:horizontal {
                                background: #C0C0C0;      /* 연한 회색 */
                                min-height: 30px;
                                border-radius: 4px;       /* 둥글게 */
                            }

                            /* 마우스 올렸을 때 핸들 색상 변경 */
                            QScrollBar::handle:horizontal:hover {
                                background: #A0A0A0;      /* 조금 더 진한 회색 */
                            }

                            /* 화살표 버튼 (보통 숨김 처리) */
                            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                                border: none;
                                background: none;
                                height: 0px;
                            }

                            /* 핸들 위아래의 레일 영역 (배경) */
                            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                                background: none;
                            }
                        """)


class AddButtonCard(QWidget):
    """
        You can use it everywhere via clicked Signal
    """
    clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        # UI 파일 로드 또는 직접 구성
        self.ui = Ui_AddButtonCardWidget()
        self.ui.setupUi(self)
        
        # 클릭 이벤트 연결 (카드 본체 클릭 시)
        self.mouseReleaseEvent = lambda e: self.clicked.emit()

    def adjust_content_size(self, new_width, new_height=None):
        """
            resize widget to be fixed (width, height)
        """
        if new_height:
            self.setFixedSize(new_width, new_height)
        else:
            self.setFixedSize(new_width, new_width)


class VehicleSearchCardWidget(QWidget):
    """
        Vehicle Card used for Vehicle Search Tab
    """
    double_clicked = Signal(dict)
    def __init__(self, vehicle_data):
        super().__init__()
        self.ui = Ui_VehicleCardWidget()
        self.ui.setupUi(self)
        self.is_loaded = False

        self.vehicle_data = vehicle_data
        self.ui.VehicleCardStackedWidget.setCurrentIndex(0)

        ### Some seat, pegasus details for Card Underbar
        additioninfo = f"{vehicle_data['seats']} "
        if vehicle_data['seats'] > 1:
            additioninfo = additioninfo + 'seats'
        else:
            additioninfo = additioninfo + 'seat'

        if vehicle_data['is_pegasus']:
            additioninfo = additioninfo + ' · Pegasus Vehicle'

        ### Fill Overlay Labels
        self.ui.AdditionalInfoLabel.setText(additioninfo)
        self.ui.ManufacturerLabel.setText(str(vehicle_data['manufacturer']))
        self.ui.VehicleNameLabel.setText(str(vehicle_data['name']))

        laptime = format_lap_time(vehicle_data['laptime_ms'])
        topspeed = value_to_percentage(vehicle_data['topspeed_10mtph'])

        self.ui.BackPriceLabel.setText(str(vehicle_data['price']))
        self.ui.BackLaptimeLabel.setText(str(laptime))
        self.ui.BackTopspeedLabel.setText(str(topspeed))
        self.ui.BackVehicleClassLabel.setText(str(vehicle_data['vehicle_class']))
        self.ui.BackVehicleNameLabel.setText(str(vehicle_data['name']))

        # self.ui.CardManufacturerLogo
        # self.ui.VehicleImageLabel

    def enterEvent(self, event):
        """
            Card Overlay Starts
        """
        self.ui.VehicleCardStackedWidget.setCurrentIndex(1)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """
            Card Overlay Ends
        """
        self.ui.VehicleCardStackedWidget.setCurrentIndex(0)
        super().leaveEvent(event)

    def adjust_content_size(self, new_width):
        """
            resize widget to be fixed (width, new_width * 0.75)
        """
        target_height = int(new_width * 0.75) 
        self.setFixedSize(new_width, target_height)

        ### Image resizing data
        img_w = new_width - 20 
        img_h = int(img_w * 0.7)

        margin_h = int(new_width * 0.1)
        margin_w = int(new_width * 0.2)

        logo_height = int(new_width * 0.25) 

        ### Resize
        self.ui.VehicleImageLabel.setFixedSize(new_width, target_height)
        self.ui.CardDefault.setFixedSize(new_width, target_height)
        self.ui.CardOverlay.setFixedSize(new_width, target_height)
        self.ui.CardOverlay.layout().setContentsMargins(margin_w, margin_h, margin_w, margin_h)
        self.ui.CardOverlay.layout().setSpacing(int(new_width * 0.015))
        self.ui.CardTextGroupWidget.layout().setContentsMargins(int(new_width * 0.06), int(new_width * 0.025), 0, int(new_width * 0.03))

        self.ui.CardManufacturerLogo.setFixedHeight(logo_height)

        ### Resize Font
        font_size = max(9, new_width // 25) # 너비 250일 때 10pt
        back_name_font_size = max(12, new_width // 20)
        default_font_size = max(8, new_width // 50)
        self.ui.AdditionalInfoLabel.setStyleSheet(f"font-size: {default_font_size}pt; color:rgb(255, 170, 0);")
        self.ui.BackVehicleNameLabel.setStyleSheet(f"font-size: {back_name_font_size}pt; color:white; font-weight: bold;")
        self.ui.BackVehicleClassLabel.setStyleSheet(f"font-size: {default_font_size}pt; color:white;")
        self.ui.BackLaptimeLabel.setStyleSheet(f"font-size: {default_font_size}pt; color:white;")
        self.ui.BackTopspeedLabel.setStyleSheet(f"font-size: {default_font_size}pt; color:white;")
        self.ui.BackPriceLabel.setStyleSheet(f"font-size: {default_font_size}pt; color:white;")
        # self.ui.VehicleNameLabel.setStyleSheet(f"font-size: {font_size}pt; font-weight: bold;")

    def mouseDoubleClickEvent(self, event):
        """
            DoubleClick Event, Check for Mouse Left Doubleclick
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self.double_clicked.emit(self.vehicle_data)
        super().mouseDoubleClickEvent(event)
        
    def update_visibility_logic(self, scroll_area):
        """
            Image Lazy Loading, Renders the image when it is visible in the scroll area
            Otherwise, generates an empty pixmap.
        """
        viewport = scroll_area.viewport()
        widget_pos = self.mapTo(viewport, self.rect().topLeft())
        extended_rect = viewport.rect().adjusted(0, -200, 0, 200)
        is_visible = extended_rect.intersects(self.rect().translated(widget_pos))

        if is_visible:
            if not self.is_loaded:
                # 화면에 들어오면 로드
                pixmap = ImageManager.get_image("Vehicle", self.vehicle_data['id'])
                logomap = ImageManager.get_image("Manufacturer", self.vehicle_data['manufacturer'])
                self.ui.VehicleImageLabel.set_image(pixmap)
                self.ui.CardManufacturerLogo.set_image(logomap)
                self.is_loaded = True
        else:
            if self.is_loaded:
                # 화면 밖으로 나가면 메모리 해제
                self.ui.VehicleImageLabel.set_image(QPixmap())
                self.ui.CardManufacturerLogo.set_image(QPixmap())
                self.is_loaded = False

    def update_vehicle_image(self):
        """
            Just getting Image from ImageManager
        """
        if self.is_loaded:
            pixmap = ImageManager.get_image("Vehicle", self.vehicle_data['id'])
            self.ui.VehicleImageLabel.set_image(pixmap)

class CategoryWidget(QWidget):
    """
        Category Widget for Property and Property Custom
    """
    toggled_category = Signal()
    def __init__(self, type_data, is_final_leaf=False):
        super().__init__()
        self.ui = Ui_CategoryAccordianWidget()
        self.ui.setupUi(self)

        self.current_type_data = type_data
        self.is_final_leaf = is_final_leaf # has only Property, no Child Category
        self.layout_set = False

        """
            When is_final_leaf is enabled, 
            force the use of the Property flow_layout.
            In all other cases, keep it initially expanded.
        """ 
        if self.is_final_leaf:
            self.init_set_frame_to_flow_layout()
        
        ### Widget Size Policy
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

        ### init Category Title set
        self.is_expanded = True
        self.ui.lbl_arrow.setText("▼")
        if type_data.get('key_name', None) is None:
            self.ui.lbl_title.setText(type_data['name'])
        else:
            self.ui.lbl_title.setText(type_data['key_name'])

        ### init Child Set
        self.pcard_dict = dict()
        self.child_dict = dict()
        self.child_count = 0
        
        # Connect HeaderFrame Click Event
        self.ui.HeaderFrame.mousePressEvent = self.toggle_category
        # self.add_cards(objects_list, type_data)

    def init_set_frame_to_flow_layout(self):
        """
            Set Flow layout for [Child Category - Property Cards]
        """
        self.content_layout = FlowLayout(self.ui.ContentFrame)
        self.content_layout.setSpacing(2)
        self.layout_set = True
        self.is_final_leaf = True

    def init_set_frame_to_vbox_layout(self):
        """
            Set Vertical layout for [Parent Category - Child Category]
        """
        self.content_layout = QVBoxLayout(self.ui.ContentFrame)
        self.content_layout.setSpacing(2)
        self.layout_set = True
        self.is_final_leaf = False

    def toggle_category(self, event):
        """
            set Category Expand When Clicked Category Title Event
        """
        if self.is_expanded:
            self.ui.ContentFrame.hide() # 접기
            self.ui.lbl_arrow.setText("▶")
        else:
            self.ui.ContentFrame.show() # 펴기
            self.ui.lbl_arrow.setText("▼")
        
        self.is_expanded = not self.is_expanded

        if self.is_final_leaf:
            for child in self.child_dict.values():
                child.set_category_expanded_call(self.is_expanded)

        ### send Signal To Main Image Manager
        self.toggled_category.emit()

    def adjust_content_size(self, new_width, card_width):
        """
            resize widget to be fixed width, and set card width for Property Cards\n
            Recursively resizes all Child Categories and Properties.
        """

        """
        fl_height = self.content_layout.heightForWidth(new_width)
        tt_height = self.ui.HeaderFrame.height()
        new_height = fl_height + tt_height
        self.setFixedSize(new_width, new_height)
        """
        for child in self.child_dict.values():
            if isinstance(child, CategoryWidget):
                child.adjust_content_size(new_width - 5, card_width)
            elif isinstance(child, PropertyCard):
                child.adjust_content_size(card_width)

        if not self.is_final_leaf:
            self.setFixedWidth(new_width)
        else:
            new_height = self.content_layout.heightForWidth(new_width)
            self.ui.ContentFrame.setFixedSize(new_width, new_height)

        

        """
        for card in self.pcard_dict.values():
            card.adjust_content_size(new_width)
            pass
        """

    def adjust_content_mini(self, new_width):
        """
            resize widget to be fixed width, 3 Property Cards will be placed in a row\n
            It will resize for Only Properties.
        """
        card_width = (new_width - 24) // 3
        for child in self.child_dict.values():
            if isinstance(child, PropertyCard):
                child.adjust_content_mini(card_width)

        if not self.is_final_leaf:
            self.setFixedWidth(new_width)
        else:
            new_height = self.content_layout.heightForWidth(new_width)
            self.ui.ContentFrame.setFixedSize(new_width, new_height)

    def get_child_count(self):
        return self.child_count

    def add_child(self, object):
        """
            If Object wanted to add is Property, Category layout will be flow layout
            Else, Category layout will be vertical layout
        """
        if isinstance(object, PropertyCard) or self.is_final_leaf:
            if (not self.layout_set):
                self.init_set_frame_to_flow_layout()

            self.content_layout.addWidget(object)
            self.child_count += 1
            self.child_dict[self.child_count] = object

        elif isinstance(object, CategoryWidget):
            if (not self.layout_set):
                self.init_set_frame_to_vbox_layout()

            self.content_layout.addWidget(object, alignment=Qt.AlignmentFlag.AlignTop)
            self.child_count += 1
            self.child_dict[self.child_count] = object

    def add_cards(self, objects_list, type_data):
        """
            LEGACY\n
            Use Add_Child Function Instead
        """
        self.button_group = QButtonGroup(self)
        max_owned = type_data.get('max_owned') or 100

        if max_owned > 1:
            self.button_group.setExclusive(False)
        else:
            self.button_group.setExclusive(True)
            self.button_group.buttonClicked.connect(self.check_selection_limit)

        for index, data in enumerate(objects_list):
            card = PropertyCard(data, type_data)
            card.property_changed.connect(self.relay_property_clicked.emit)
            self.pcard_dict[index] = card
            self.flow_layout.addWidget(card)
            self.button_group.addButton(card.selector)
        """
        column_count = 4  # 한 줄에 4개씩 배치
        for index, data in enumerate(objects_list):
            # 1. 카드 객체 생성
            card = PropertyCard(data, type_data)
            
            # 2. 그리드 위치 계산 (행, 열)
            row = index // column_count
            col = index % column_count
            
            # 3. 그리드 레이아웃에 추가
            self.ui.gridLayout.addWidget(card, row, col)
        """

    def check_selection_limit(self, clicked_button):
        """
            LEGACY\n
            Check Category's ButtonGroup.
        """
        max_limit = self.current_type_data['max_owned']
        # 현재 체크된 버튼 리스트 추출
        checked_buttons = [btn for btn in self.button_group.buttons() if btn.isChecked()]
        
        if len(checked_buttons) > max_limit:
            # 한도 초과 시 방금 누른 버튼을 다시 해제
            clicked_button.setChecked(False)
            print(f"최대 {max_limit}개까지만 선택할 수 있습니다.")

class PropertyCard(QWidget):
    """
        PropertyCard used for Select Property and PropertyCustom
    """
    property_changed = Signal(int, bool) # (property_id, is_checked)
    image_clicked = Signal(int) # (property_id)
    def __init__(self, property_data):
        super().__init__()
        self.ui = Ui_PropertyCardWidget()
        self.ui.setupUi(self)
        self.is_loaded = False

        self.property_data = property_data

        self.category_expanded = True
        self.is_unchangeable = False

        self.ui.lbl_image.installEventFilter(self)
        
        ### Property DB has key_name, Property Custom DB has key and name.
        if self.property_data.get('key_name', None) is None:
            self.ui.lbl_name.setText(self.property_data['name'])
            self.ui.lbl_price.setText(f"{self.property_data['price']}")
        else:
            self.ui.lbl_name.setText(self.property_data['key_name'])
            self.ui.lbl_price.setText(f"{self.property_data['price']}")
        
        """
        self.selector.setChecked(self.property_data['is_owned'])
        if self.property_data['is_owned'] and type_data['is_unchangeable']: # 되팔 수 없는 경우
            self.selector.setEnabled(False)
        else:
            self.selector.clicked.connect(self.on_selector_clicked)
            pass
        """

    def init_selector_button(self, is_radio, is_owned, is_unchangeable):
        """
            This must be called before using.\n
            Radio Button will be active when Property Type own limit is Only One
        """
        self.is_unchangeable = is_unchangeable
        if is_radio:
            self.selector = QRadioButton(self.ui.SelectionContainer)
        else:
            self.selector = QCheckBox(self.ui.SelectionContainer)

        self.selector.setFocusPolicy(Qt.NoFocus)

        self.ui.SelectionContainer.layout().addWidget(self.selector, alignment=Qt.AlignmentFlag.AlignCenter)

        self.selector.setChecked(is_owned)
        if is_owned and is_unchangeable: 
            self.lock_selector_button()
        else:
            self.selector.clicked.connect(self.on_selector_clicked)

    def is_ready_to_use(self):
        """
            check function for 'init_selector_button' has Done
        """
        return True if self.selector else False

    def lock_selector_button(self):
        """
            Lock Button When Property is Unchangeable
        """
        if self.selector and self.is_unchangeable:
            self.selector.setEnabled(False)

    def set_category_expanded_call(self, is_expanded):
        """
            Property Image will be unload When Parent Category Collapsed
        """
        self.category_expanded = is_expanded

    def update_visibility_logic(self, scroll_area):
        """
            Image Lazy Loading, Renders the image when it is visible in the scroll area
            Otherwise, generates an empty pixmap.
        """
        viewport = scroll_area.viewport()
        widget_pos = self.mapTo(viewport, self.rect().topLeft())
        extended_rect = viewport.rect().adjusted(0, -200, 0, 200)
        is_visible = extended_rect.intersects(self.rect().translated(widget_pos))

        if is_visible and self.category_expanded:
            if not self.is_loaded:
                # 화면에 들어오면 로드
                pixmap = ImageManager.get_image("Property", f"{self.property_data['id']}")
                self.ui.lbl_image.set_image(pixmap)
                self.is_loaded = True
        else:
            if self.is_loaded:
                # 화면 밖으로 나가면 메모리 해제
                self.ui.lbl_image.set_image(QPixmap()) # 빈 픽스맵 설정
                self.is_loaded = False

    def adjust_content_size(self, new_width):
        """
            resize widget to be fixed (width, width * 4/3)
        """
        self.setFixedSize(new_width, int(new_width*4/3))

    def adjust_content_mini(self, new_width):
        """
            resize widget to be fixed (width, width * 5/6)\n
            This is for Property Customs
        """
        self.setFixedSize(new_width, int(new_width*5/6))

    def disable_checkbox(self):
        """
            Disable Checkbox, Check Button Init
        """
        if self.selector:
            self.selector.setChecked(False)

    def enable_checkbox(self):
        """
            Enable Checkbox, Check Button Init\n
            If Data is Unchangeable, It will be Locked
        """
        if self.selector:
            self.selector.setChecked(True)
        if self.is_unchangeable:
            self.lock_selector_button()

    def on_selector_clicked(self):
        """
            Send 'property_changed' Signal\n
            If Data is Unchangeable, It will be Locked
        """
        self.property_changed.emit(self.property_data['id'], self.selector.isChecked())
        if self.is_unchangeable:
            self.lock_selector_button()

    def eventFilter(self, obj, event):
        """
            Open Custom Dialog Event for Property Image Clicked
        """
        if obj == self.ui.lbl_image and event.type() == QEvent.Type.MouseButtonPress:
            if event.button() == Qt.MouseButton.LeftButton:
                self.image_clicked.emit(self.property_data['id'])
                return True
        return super().eventFilter(obj, event)

class ColorPresetCard(QWidget):
    """
        This is Paint Preset Card\n
        There is some options for Mini, Drag and filter color system\n
        gradient_preview_func is for setting UIs Gradient like 'chrome, prismatic'
    """
    double_clicked = Signal(dict, QWidget) # (PresetData, ColorPresetCard(self))
    right_clicked = Signal(dict) # (PresetData)
    def __init__(self, preset_data, gradient_preview_func, mini_sized=False, drag_available=False, pfilter=None):
        super().__init__()
        self.ui = Ui_ColorPresetPreviewWidget()
        self.ui.setupUi(self)
        self.preset_data = preset_data
        self.drag_available = drag_available
        self.mini_sized = mini_sized
        self.frameborder_width = 5

        ### this is for Vanila Filter
        self.is_modded_preset = False

        self.what_gradient_preview = gradient_preview_func
        # self.ui.PresetNameLabel.setWordWrap(True)

        ### Drag Option
        if self.drag_available:
            self.setAcceptDrops(False) # 자신은 드랍을 안 받지만
            self.setCursor(Qt.CursorShape.OpenHandCursor) # 잡을 수 있다는 표시

        ### hide UIs for Mini Widget
        if self.mini_sized:
            self.ui.PcolorTextLabel.hide()
            self.ui.PColorTagLabel.hide()
            self.ui.ScolorTextLabel.hide()
            self.ui.ScolorTagLabel.hide()
            self.ui.TrimTextLabel.hide()
            self.ui.TrimTagLabel.hide()
            self.ui.WheelTagLabel.hide()
            self.ui.WheelTextLabel.hide()
            self.ui.PearlTagLabel.hide()
            self.ui.PearlTextGroup.hide()
            self.ui.NeonlightTagLabel.hide()
            self.ui.NeonTextLabel.hide()
            self.ui.HeadlightTagLabel.hide()
            self.ui.HeadlightTextLabel.hide()
            self.ui.DialTagLabel.hide()
            self.ui.DialTextLabel.hide()
            self.ui.LiveryTagLabel.hide()
            self.ui.LiveryTextLabel.hide()

        ### Init UI setting
        self.ui.ColorPreviewFrame.show()
        self.ui.ColorDetailOverlayFrame.hide()

        self.preset_filter_status = {
                "CheckVanillaPreset" : False,
                "CheckWheelColor": False,
                "CheckDialColor": False,
                "CheckTrimColor": False,
                "CheckLivery": False,
                "CheckNeonLights": False,
                "CheckHeadlights": False
            }
        if pfilter is not None:
            self.preset_filter_status = copy.deepcopy(pfilter)

        self.fill_frame_colors()

    def edit_preset(self, preset_data):
        """
            Refresh preset Data
        """
        self.preset_data = preset_data
        self.fill_frame_colors()

    def is_modded(self):
        """
            check function for vanila filter
        """
        return self.preset_data['is_modded']
        
    def fill_frame_colors(self):
        """
            Set Stylesheet for the Widget's Label from preset_data\n
            If some data is None or Filtered, It will be not displayed
        """

        self.ui.PresetNameLabel.setText(f"{self.preset_data['name']}")

        self.ui.PcolorTextLabel.setText(f"{self.preset_data['prender']} {self.preset_data['primary']['name']}")
        pis_chrome = self.preset_data['prender'].lower() == 'chrome'
        
        
        if (self.preset_data.get('secondary_color_id', None) is None):
            self.ui.ScolorFrame.hide()
            self.ui.ScolorTextLabel.setText(f"None")
            self.ui.PcolorFrame.setStyleSheet(self.get_custom_stylesheet_text(self.preset_data['primary'], True, False))
        else:
            self.ui.ScolorFrame.show()
            self.ui.ScolorTextLabel.setText(f"{self.preset_data['srender']} {self.preset_data['secondary']['name']}")
            sis_chrome = self.preset_data['srender'].lower() == 'chrome'
            self.ui.ScolorFrame.setStyleSheet(self.get_custom_stylesheet_text(self.preset_data['secondary'], False, True, sis_chrome))
            self.ui.PcolorFrame.setStyleSheet(self.get_custom_stylesheet_text(self.preset_data['primary'], True, True, pis_chrome))

        if (self.preset_data.get('pearl_color_id', None) is None):
            self.ui.PearlFrame.hide()
            self.ui.PearlTextGroup.setText(f"None")
        else:
            self.ui.PearlFrame.show()
            self.ui.PearlTextGroup.setText(f"{self.preset_data['pearl']['name']}")
            self.ui.PearlFrame.setStyleSheet(f"""
                        
                        background-color: qlineargradient(spread:pad, 
                                         x1:0.5, y1:0.443818, 
                                         x2:0.840909, y2:0.869, 
                                         stop:0.301136 rgba(255, 255, 255, 0), 
                                         stop:1 {self.hex_to_rgba(
                                             shade_color(self.preset_data['pearl']['hex_color']), 0.5)});
                    """)

        if (self.preset_filter_status.get("CheckWheelColor", False)) or (self.preset_data.get('wheel_color_id', None) is None):
            self.ui.WheelColorFrame.hide()
            self.ui.WheelTextLabel.setText(f"None")
        else:
            self.ui.WheelColorFrame.show()
            self.ui.WheelTextLabel.setText(f"{self.preset_data['wheel']['name']}")
            self.ui.WheelColorFrame.setStyleSheet(self.get_custom_stylesheet_text(self.preset_data['wheel'], False, False, False))
            
        if (self.preset_filter_status.get("CheckDialColor", False)) or (self.preset_data.get('dial_color_id', None) is None):
            self.ui.DialColorFrame.hide()
            self.ui.DialTextLabel.setText(f"None")
        else:
            self.ui.DialColorFrame.show()
            self.ui.DialTextLabel.setText(f"{self.preset_data['dial']['name']}")
            self.ui.DialColorFrame.setStyleSheet(self.get_custom_stylesheet_text(self.preset_data['dial'], False, False, False))
            
        if (self.preset_filter_status.get("CheckTrimColor", False)) or (self.preset_data.get('trim_color_id', None) is None):
            self.ui.TrimColorFrame.hide()
            self.ui.TrimTextLabel.setText(f"None")
        else:
            self.ui.TrimColorFrame.show()
            self.ui.TrimTextLabel.setText(f"{self.preset_data['trim']['name']}")
            self.ui.TrimColorFrame.setStyleSheet(self.get_custom_stylesheet_text(self.preset_data['trim'], False, False, False))
            
        if (self.preset_filter_status.get("CheckNeonLights", False)) or (self.preset_data.get('neon_color_id', None) is None):
            self.ui.NeonTextLabel.setText(f"None")
            self.ui.NeonlightOutlineFrame.setStyleSheet(f"""
                        color: #00FFFFFF
                    """)
        else:
            self.ui.NeonTextLabel.setText(f"{self.preset_data['neon']['name']}")
            self.ui.NeonlightOutlineFrame.setStyleSheet(f"""
                        color: {self.preset_data['neon']['hex_color']}
                    """)
            
        if (self.preset_filter_status.get("CheckHeadlights", False)) or (self.preset_data.get('headlight_color_id', None) is None):
            self.ui.HeadlightColorFrame.hide()
            self.ui.HeadlightTextLabel.setText(f"None")
        else:
            self.ui.HeadlightColorFrame.show()
            self.ui.HeadlightTextLabel.setText(f"{self.preset_data['headlight']['name']}")
            self.ui.HeadlightColorFrame.setStyleSheet(f"""
                        background-color: {self.preset_data['headlight']['hex_color']};
                    """)
            
        if (self.preset_filter_status.get("CheckLivery", False)) or (self.preset_data.get('livery_type_id', None) is None):
            self.ui.LiveryImageLabel.hide()
            self.ui.LiveryTextLabel.setText(f"None")
        else:
            self.ui.LiveryImageLabel.show()
            self.ui.LiveryTextLabel.setText(f"{self.preset_data['livery_name']}")
            pixmap = ImageManager.get_image('Livery', self.preset_data['livery_name'])
            if pixmap:
                self.ui.LiveryImageLabel.set_image(pixmap)

    def get_custom_stylesheet_text(self, color_ref, is_primary = True, has_secondary = False, is_chrome = False):
        """
            Get Stylesheet for UI Labels\n
            The colorHex will be adjusted here to match GTA's shaders and then output to the Widget.
        """
        
        color_id = color_ref.get('id', None)
        c1 = color_ref.get('hex_color', '#FFFFFF')      # 메인
        c2 = color_ref.get('secondary_hex', '#FFFFFF')  # 보조
        c3 = color_ref.get('tertiary_hex', '#FFFFFF')   # 강조

        result = self.what_gradient_preview(color_id)

        if is_primary and has_secondary:
            x1 = 1 - (22 / 15)
            x2 = 1
            pass
        elif (not is_primary) and has_secondary:
            x1 = 0
            x2 = (22 / 7)
            pass
        else:
            x1 = 0
            x2 = 1
            pass

        c1 = shade_color(c1)
        if c2 is not None:
            c2 = shade_color(c2)
        if c3 is not None:
            c3 = shade_color(c3)
        
        # 기본값
        sheet_string = f"background-color: {c1};"

        if (not is_primary) and (not has_secondary) and (not is_chrome):
            return sheet_string

        # 1. Chrome: 검정(0%) -> 메인(70%) -> 검정(100%)
        if is_chrome or result == "chrome":
            sheet_string = f"background-color: qlineargradient(spread:pad, x1:{x1} , y1:0, x2:{x2}, y2:0, stop:0 {c1}, stop:0.7 #DDDDEE, stop:1 {c1});"

        # 2. Anodized: c3(0%) -> c2(30%) -> c1(70%) -> c2(100%)
        elif result == "Anodized":
            sheet_string = f"background-color: qlineargradient(spread:pad, x1:{x1} , y1:0, x2:{x2}, y2:0, stop:0 {c3}, stop:0.3 {c2}, stop:0.7 {c1}, stop:1 {c2});"

        # 3. Flip: c3(30%) -> c2(50%) -> c1(70%) (양 끝단은 자연스럽게 c3와 c1로 채워짐)
        elif result == "Flip":
            sheet_string = f"background-color: qlineargradient(spread:pad, x1:{x1} , y1:0, x2:{x2}, y2:0, stop:0.3 {c3}, stop:0.5 {c2}, stop:0.7 {c1});"

        # 4. Soft: c1 베이스, 40%~80% 구간에서 c2 -> c3로 부드럽게 전환
        elif result == "Soft":
            c2_soft = blend_colors(c1, c2, 0.5)
            c3_soft = blend_colors(c1, c3, 0.5)
            sheet_string = f"background-color: qlineargradient(spread:pad, x1:{x1} , y1:0, x2:{x2}, y2:0, stop:0 {c1}, stop:0.4 {c1}, stop:0.6 {c3_soft}, stop:0.8 {c2_soft}, stop:1 {c1});"

        # 5. Prismatic: c1 베이스, 40%~80% 구간 무지개 (빨주노초파남보)
        elif result == "Prismatic":
            h3, l3, s3 = hex_to_hsl('#FF3333')
            h2, l2, s2 = hex_to_hsl('#3333FF')
            
            # H값이 자연스럽게 줄어들도록 중간 단계(Color Stops) 계산
            # 40%에서 C2, 80%에서 C3가 되도록 4단계 정도로 나눔
            steps = []
            num_steps = 10
            for i in range(num_steps):
                ratio = i / (num_steps - 1)
                # Hue가 자연스럽게 변하도록 보간 (C2.H -> C3.H)
                current_h = h2 + (h3 - h2) * ratio
                current_l = l2 + (l3 - l2) * ratio
                current_s = s2 + (s3 - s2) * ratio
                
                stop_pos = 0.4 + (0.4 * ratio) # 0.4에서 0.8 사이 배치
                color_str = hsl_to_str(current_h, current_l, current_s)
                steps.append(f"stop:{stop_pos:.2f} {color_str}")

            stops_text = ", ".join(steps)

            sheet_string = f"background-color: qlineargradient(spread:pad, x1:{x1} , y1:0, x2:{x2}, y2:0, stop:0 {c1}, stop:0.35 {c1}, {stops_text}, stop:0.85 {c1});"

        # 6. Holographic: c1 베이스, 20%~95% 구간 넓은 무지개
        elif result == "Holographic":
            c2_soft = blend_colors('#FFFFFF', '#FF3333', 0.9)
            c3_soft = blend_colors('#FFFFFF', '#3333FF', 0.9)

            h3, l3, s3 = hex_to_hsl(c2_soft)
            h2, l2, s2 = hex_to_hsl(c3_soft)
            
            # H값이 자연스럽게 줄어들도록 중간 단계(Color Stops) 계산
            # 40%에서 C2, 80%에서 C3가 되도록 4단계 정도로 나눔
            steps = []
            num_steps = 10
            for i in range(num_steps):
                ratio = i / (num_steps - 1)
                # Hue가 자연스럽게 변하도록 보간 (C2.H -> C3.H)
                current_h = h2 + (h3 - h2) * ratio
                current_l = l2 + (l3 - l2) * ratio
                current_s = s2 + (s3 - s2) * ratio
                
                stop_pos = 0.3 + (0.6 * ratio) # 0.4에서 0.8 사이 배치
                color_str = hsl_to_str(current_h, current_l, current_s)
                steps.append(f"stop:{stop_pos:.2f} {color_str}")

            stops_text = ", ".join(steps)

            sheet_string = f"background-color: qlineargradient(spread:pad, x1:{x1} , y1:0, x2:{x2}, y2:0, stop:0.2 {c1}, {stops_text}, stop:0.9 {c1});"

        # 7. SoftPrismatic: Soft 구조 + 프리즘(30% 투명도 느낌)
        # Qt 스타일시트는 레이어 중첩이 안 되므로, 색상 값을 rgba로 변환하여 '물들인' 느낌을 줍니다.
        elif result == "SoftPrismatic":
            c2_soft = blend_colors(c1, c2, 0.5)
            c3_soft = blend_colors(c1, c3, 0.5)

            h3, l3, s3 = hex_to_hsl(c2_soft)
            h2, l2, s2 = hex_to_hsl(c3_soft)
            
            # H값이 자연스럽게 줄어들도록 중간 단계(Color Stops) 계산
            # 40%에서 C2, 80%에서 C3가 되도록 4단계 정도로 나눔
            steps = []
            num_steps = 10
            for i in range(num_steps):
                ratio = i / (num_steps - 1)
                # Hue가 자연스럽게 변하도록 보간 (C2.H -> C3.H)
                current_h = h2 + (h3 - h2) * ratio
                current_l = l2 + (l3 - l2) * ratio
                current_s = s2 + (s3 - s2) * ratio
                
                stop_pos = 0.4 + (0.4 * ratio) # 0.4에서 0.8 사이 배치
                color_str = hsl_to_str(current_h, current_l, current_s)
                steps.append(f"stop:{stop_pos:.2f} {color_str}")

            stops_text = ", ".join(steps)

            sheet_string = f"background-color: qlineargradient(spread:pad, x1:{x1} , y1:0, x2:{x2}, y2:0, stop:0 {c1}, stop:0.35 {c1}, {stops_text}, stop:0.85 {c1});"

        return sheet_string
          
    def set_hide_parts(self, stvanilla, stwheel, stdial, sttrim, stlivery, stneon, sthead):
        """
            Set Filter to Widget
        """
        self.preset_filter_status = {
            "CheckVanillaPreset" : stvanilla,
            "CheckWheelColor": stwheel,
            "CheckDialColor": stdial,
            "CheckTrimColor": sttrim,
            "CheckLivery": stlivery,
            "CheckNeonLights": stneon,
            "CheckHeadlights": sthead
        }
        self.fill_frame_colors()
        


    def hex_to_rgba(self, hex_str, opacity):
        # #FFFFFF -> (255, 255, 255)
        if hex_str is None:
            return "rgba(255, 255, 255, 0)"
        
        hex_str = hex_str.lstrip('#')
        r, g, b = tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))
        
        # rgba(255, 255, 255, 0.5)
        return f"rgba({r}, {g}, {b}, {opacity})"


    def adjust_content_size(self, new_width):
        """
            resize widget to be fixed (width, width)
        """
        self.frameborder_width = int(new_width * 5 // 300)

        self.setFixedSize(new_width, new_width)
        self.ui.ColorDetailOverlayFrame.setFixedSize(new_width, new_width)
        self.ui.ColorPreviewFrame.setFixedSize(new_width, new_width)

        ### set Color Area sizes
        twicewidth = self.frameborder_width * 2
        margin = self.frameborder_width * 7
        self.ui.NeonlightOutlineFrame.setLineWidth(self.frameborder_width)
        self.ui.LiveryImageLabel.setGeometry(self.frameborder_width, self.frameborder_width, new_width - twicewidth, new_width - twicewidth)
        self.ui.PearlFrame.setGeometry(self.frameborder_width, self.frameborder_width, new_width - twicewidth, new_width - twicewidth)
        self.ui.ColorPaletteFrame.setGeometry(0, self.frameborder_width, new_width - self.frameborder_width, new_width - twicewidth)
        self.ui.ColorDetailOverlayFrame.layout().setContentsMargins(margin, margin, margin, margin)

        ### set Font sizes
        smallest_font = new_width * 3 / 300
        minifontsize = max(smallest_font * 3, 8.5)
        maxfontsize = max(smallest_font * 5, 12)
        self.ui.PresetNameLabel.setMargin(int(new_width * 8 // 300))
        self.ui.PresetNameLabel.setStyleSheet(f"font-size: {maxfontsize}pt; color:white; font-weight: bold;")
        self.ui.PcolorTextLabel.setStyleSheet(f"font-size: {minifontsize}pt; color:white;")
        self.ui.PColorTagLabel.setStyleSheet(f"font-size: {minifontsize}pt; color:white;")
        self.ui.ScolorTextLabel.setStyleSheet(f"font-size: {minifontsize}pt; color:white;")
        self.ui.ScolorTagLabel.setStyleSheet(f"font-size: {minifontsize}pt; color:white;")
        self.ui.TrimTextLabel.setStyleSheet(f"font-size: {minifontsize}pt; color:white;")
        self.ui.TrimTagLabel.setStyleSheet(f"font-size: {minifontsize}pt; color:white;")
        self.ui.WheelTagLabel.setStyleSheet(f"font-size: {minifontsize}pt; color:white;")
        self.ui.WheelTextLabel.setStyleSheet(f"font-size: {minifontsize}pt; color:white;")
        self.ui.PearlTagLabel.setStyleSheet(f"font-size: {minifontsize}pt; color:white;")
        self.ui.PearlTextGroup.setStyleSheet(f"font-size: {minifontsize}pt; color:white;")
        self.ui.NeonlightTagLabel.setStyleSheet(f"font-size: {minifontsize}pt; color:white;")
        self.ui.NeonTextLabel.setStyleSheet(f"font-size: {minifontsize}pt; color:white;")
        self.ui.HeadlightTagLabel.setStyleSheet(f"font-size: {minifontsize}pt; color:white;")
        self.ui.HeadlightTextLabel.setStyleSheet(f"font-size: {minifontsize}pt; color:white;")
        self.ui.DialTagLabel.setStyleSheet(f"font-size: {minifontsize}pt; color:white;")
        self.ui.DialTextLabel.setStyleSheet(f"font-size: {minifontsize}pt; color:white;")
        self.ui.LiveryTagLabel.setStyleSheet(f"font-size: {minifontsize}pt; color:white;")
        self.ui.LiveryTextLabel.setStyleSheet(f"font-size: {minifontsize}pt; color:white;")

    def enterEvent(self, event):
        """
            Card Overlay Starts
        """
        if self.mini_sized is False:
            self.ui.ColorDetailOverlayFrame.show()
        super().enterEvent(event)

    def leaveEvent(self, event):
        """
            Card Overlay Ends
        """
        if self.mini_sized is False:
            self.ui.ColorDetailOverlayFrame.hide()
        super().leaveEvent(event)

    def mouseDoubleClickEvent(self, event):
        """
            DoubleClick Event, Check for Mouse Left Doubleclick
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self.double_clicked.emit(self.preset_data, self)
        super().mouseDoubleClickEvent(event)

    def mousePressEvent(self, event):
        """
            Mouse Right Click to Remove This Widget
        """
        if event.button() == Qt.MouseButton.RightButton:
            self.right_clicked.emit(self.preset_data)
        
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """
            Mouse Drag Event to copy Color Preset Data
        """
        if self.drag_available and event.buttons() == Qt.MouseButton.LeftButton:
            drag = QDrag(self)
            mime_data = QMimeData()
            
            ### Preset Data Converts to Json
            card_recipe = {
                'action': 'copy_color_preset',
                'data': self.preset_data 
            }
            json_data = json.dumps(card_recipe).encode('utf-8')
            mime_data.setData("application/x-color-card", json_data)
            
            drag.setMimeData(mime_data)

            ### Drag Icon
            pixmap = self.grab()
            drag.setPixmap(pixmap)
            # drag.setHotSpot(event.pos())
            
            drag.exec(Qt.DropAction.CopyAction)

class OwnVehicleCard(QWidget):
    """
        Own Vehicle Card for Vehicle Viewer\n
        Needs, Own Vehicla Data, Garage data for Garage Select Combobox,
        ColorPresetCard, Gradient function for Color Card
    """
    data_changed = Signal(int, dict) # (Own_id, Own_data changes)
    sell_restore_vehicle = Signal(int) # (Own_id)
    vehicle_removed = Signal(int) # (Own_id)

    paint_added = Signal(int) # Clicked AddButton In Paint Label (Own_id)

    def __init__(self, own_data, garagedict, color_card, gradient_preview_func):
        super().__init__()
        self.ui = Ui_OwnVehicleInfoCardWidget()
        self.ui.setupUi(self)
        self.own_data = own_data

        self.what_gradient_preview = gradient_preview_func

        self.set_available_garage_dict(garagedict)
        """
        ### LEGACY Setting Garage
        self.garagelist = garagelist
        for gar in self.garagelist:
            info = {
                "own_prop_id": gar['id'],
                "slot_type_id": gar['slot_type_id']
            }
            self.ui.OwnPropertyComboBox.addItem(f"{gar['property_name']} ({gar['slot_type_name']})", info)
        
        """
        target_id = own_data.get('owned_property_id')
        target_slot_type = own_data.get('slot_type_id')

        found_index = -1

        ### Find Saved Location in Garage Select Combo Box
        for i in range(self.ui.OwnPropertyComboBox.count()):
            item_data = self.ui.OwnPropertyComboBox.itemData(i)
            
            ### info['own_prop_id'] == target_id
            if item_data and item_data[0] == target_id:
                if item_data[1] == target_slot_type:
                    found_index = i
                    break

        if found_index != -1:
            self.ui.OwnPropertyComboBox.setCurrentIndex(found_index)
        else:
            self.ui.OwnPropertyComboBox.setCurrentIndex(0)

        ### garage Image Gradient
        self.change_card_garage_image()
        
        ### Set Color Card to Card Area
        self.preset_card = color_card
        self.card_layout = QVBoxLayout(self.ui.CardPaintPresetPreviewWidget)
        self.card_layout.setContentsMargins(0,0,0,0)
        self.card_layout.setSpacing(0)
        self.color_height = self.ui.CardPaintPresetPreviewWidget.height()

        ### If Card is None, Set AddButton
        if self.preset_card is None:
            add_card = AddButtonCard()
            add_card.clicked.connect(self.handle_clicked_add_color)
            self.preset_card = add_card
            self.card_layout.addWidget(self.preset_card)
        else:
            self.card_layout.addWidget(self.preset_card)

        ### change UI If vehicle is sold
        is_sold = self.own_data['is_sold']

        if is_sold:
            self.ui.ButtonStackedWidget.setCurrentIndex(1)
            
            target_index = self.ui.OwnPropertyComboBox.findData(0) 
            if target_index != -1:
                self.ui.OwnPropertyComboBox.setCurrentIndex(target_index)
            
            # Deactive
            self.ui.OwnPropertyComboBox.setEnabled(False)

            self.set_background_color(is_sold)

        else:
            self.ui.ButtonStackedWidget.setCurrentIndex(0)
            self.ui.OwnPropertyComboBox.setEnabled(True)

            self.set_background_color(is_sold)

        ### Set Checkboxes
        self.checkbox_mapping = {
            'limited_mod': self.ui.LimitedModCheckBox,
            'limited_plate': self.ui.LimitedPlateCheckBox,
            'limited_paint': self.ui.LimitedPaintCheckBox,
            'limited_livery': self.ui.LimitedLiveryCheckBox,
            'is_reward': self.ui.RewardCheckBox,
            'mod_custom': self.ui.ModCustomCheckBox,
            'mod_upgrade': self.ui.ModUpgradeCheckBox,
            'mod_imani': self.ui.ModImaniCheckBox,
            'mod_hsw': self.ui.ModHSWCheckBox,
            'mod_drift': self.ui.ModDriftCheckBox
        }

        for field, checkbox in self.checkbox_mapping.items():
            checkbox.setChecked(own_data.get(field, False))
            
            ### connect Signal, It will send for updating DB
            checkbox.clicked.connect(
                lambda checked, f=field, c=checkbox: self.data_changed.emit(self.own_data.get('id'), {f: c.isChecked()})
            )

        def on_combo_changed():
            data = self.ui.OwnPropertyComboBox.currentData()
            if data:
                ### Transfer GarageTuple (id, type) To Dict
                ### Changed Garage Index will be send to DB own Data
                changes = {
                    'owned_property_id': data[0],
                    'slot_type_id': data[1]
                }
                self.data_changed.emit(self.own_data.get('id'), changes)
        self.ui.OwnPropertyComboBox.currentIndexChanged.connect(on_combo_changed)

        ### connect Events
        self.ui.SellButton.clicked.connect(self.handle_sell_restore_button)
        self.ui.RestoreButton.clicked.connect(self.handle_sell_restore_button)
        self.ui.RemoveButton.clicked.connect(
            lambda: self.vehicle_removed.emit(self.own_data.get('id'))
        )

        self.setAcceptDrops(True)

    def change_card_garage_image(self):
        """
            Set or Update Garage Image
        """
        gar_data = self.ui.OwnPropertyComboBox.currentData()
        if gar_data is None:
            return
        garage_tuple = (self.own_data['owned_property_id'], self.own_data['slot_type_id'], gar_data[2])
        pixmap = ImageManager.get_image('Garage', garage_tuple)
        self.ui.GarageImageLabel.set_image(pixmap)

    def set_available_garage_list(self, garagelist):
        """
            LEGACY, Use set_available_garage_dict INSTEAD \n
            Update Garage list in Garage Select ComboBox
        """
        current_ids = set()
        for i in range(self.ui.OwnPropertyComboBox.count()):
            data = self.ui.OwnPropertyComboBox.itemData(i)
            # print(f"Original data: {data}, Type: {type(data)}")

            if data:
                clean_data = tuple(data) if isinstance(data, list) else data
                current_ids.add(clean_data)

        self.garagelist = garagelist


        """
            Changing Items in ComboBox,
            You need to block Signals Because of
            Editing This list sends 'Vehicle Changes' It will make a mess
        """
        self.ui.OwnPropertyComboBox.blockSignals(True)

        for gar in self.garagelist:
            info = (gar['id'], gar['slot_type_id'], gar['property_type_id'])
            if info not in current_ids:
                display_name = f"{gar['property_name']} ({gar['slot_type_name']})"
                self.ui.OwnPropertyComboBox.addItem(display_name, info)

        self.ui.OwnPropertyComboBox.blockSignals(False)

    def set_available_garage_dict(self, garagedict:dict):
        """
            Update Garage list in Garage Select ComboBox\n
            You need to block Signals Because of
            Editing This list sends 'Vehicle Changes' It will make a mess
        """
        self.garagedict = garagedict

        self.ui.OwnPropertyComboBox.blockSignals(True)

        self.ui.OwnPropertyComboBox.clear()

        for info, gar in self.garagedict.items():
            display_name = f"{gar['property_name']} ({gar['slot_type_name']})"
            self.ui.OwnPropertyComboBox.addItem(display_name, info)

            ### Deactive item When Garage slot left 0
            if gar.get('slot_left') < 1:
                idx = self.ui.OwnPropertyComboBox.count() - 1
                self.ui.OwnPropertyComboBox.model().item(idx).setEnabled(False)

        self.ui.OwnPropertyComboBox.blockSignals(False)

    def add_available_garage_dict(self, garage_key, garage_item):
        """
            Add a new Item for Garage Select Combobox\n
            It will be called at Add a Garage(Property) in Main
        """
        self.ui.OwnPropertyComboBox.blockSignals(True)
        
        display_name = f"{garage_item['property_name']} ({garage_item['slot_type_name']})"
        self.ui.OwnPropertyComboBox.addItem(display_name, garage_key)

        ### Deactive item When Garage slot left 0
        if garage_item.get('slot_left') < 1:
            idx = self.ui.OwnPropertyComboBox.count() - 1
            self.ui.OwnPropertyComboBox.model().item(idx).setEnabled(False)
        
        self.ui.OwnPropertyComboBox.blockSignals(False)


    def adjust_content_size(self, new_height):
        """
            resize widget to be fixed (new_height, new_height * 7 / 3)
        """
        new_width = int(new_height * 7 / 3)
        self.setFixedSize(new_width, new_height)
        self.ui.GarageImageLabel.setFixedSize(new_width, new_height)
        self.ui.OwnCardOverlayWidget.setFixedSize(new_width, new_height)
        self.color_height = self.ui.CardPaintPresetPreviewWidget.height()
        self.ui.CardPaintPresetPreviewWidget.setFixedWidth(self.color_height)
        if self.preset_card:
            self.preset_card.adjust_content_size(self.color_height)

    def handle_clicked_add_color(self):
        """
            When OwnCard has no ColorPreset, There will be AddButton\n
            This AddButton sends Paint Added Signal
        """
        self.paint_added.emit(self.own_data.get('id'))

    def handle_sell_restore_button(self):
        """
            Change UI and send 'data_changed{'is_sold': is_sold}' Signal
        """
        is_sold = self.own_data['is_sold']
        is_sold = not is_sold
        self.own_data['is_sold'] = is_sold
        self.data_changed.emit(self.own_data.get('id'), {'is_sold': is_sold})

        if is_sold:
            self.ui.ButtonStackedWidget.setCurrentIndex(1)

            target_index = self.ui.OwnPropertyComboBox.findData(1) 
            if target_index != -1:
                self.ui.OwnPropertyComboBox.setCurrentIndex(target_index)
            
            # 비활성화 (수정 불가)
            self.ui.OwnPropertyComboBox.setEnabled(False)

            self.set_background_color(is_sold)

        else:
            self.ui.ButtonStackedWidget.setCurrentIndex(0)
            self.ui.OwnPropertyComboBox.setEnabled(True)
            self.set_background_color(is_sold)

    def set_background_color(self, sold_flag = False):
        """
            Set Background Gray If Own Vehicle has sold
        """
        if sold_flag:
            self.ui.OwnCardOverlayWidget.setStyleSheet("""
                #OwnCardOverlayWidget{
                background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,
                                                        stop:0.67 rgba(200, 200, 200, 255),
                                                        stop:1 rgba(150, 150, 150, 160))\n}\n
            """)
        else:
            self.ui.OwnCardOverlayWidget.setStyleSheet("""
                #OwnCardOverlayWidget{
                background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,
                                                        stop:0.67 rgba(255, 255, 255, 255),
                                                        stop:1 rgba(255, 255, 255, 160))\n}\n
            """)

    def set_data_refresh(self, own_data, garagedict=None):
        """
            Fully reinitialize data\n
            If Own Vehicle Data is modified
            the Vehicle's Garage ComboBox should also be updated,
            particularly when the assigned Property changes.
        """
        print(f"Refreshing Own Vehicle Card : *[{own_data}]*")
        self.own_data = own_data
        
        ### Refreshes the ComboBox items when garagedict is provided as an argument.
        if garagedict is not None:
            self.set_available_garage_dict(garagedict)

        ### before moving garage, check slot_left Value
        bef_idx = self.ui.OwnPropertyComboBox.currentIndex()
        data = self.ui.OwnPropertyComboBox.currentData()
        bef_garage_tuple = tuple(data) if isinstance(data, list) else data
        bef_garage_data = self.garagedict.get(bef_garage_tuple)

        # print(f"Moving from {bef_garage_tuple} :: {bef_garage_data.get('slot_left')}")
        if bef_garage_data.get('slot_left') < 1:
            self.ui.OwnPropertyComboBox.model().item(bef_idx).setEnabled(False)
        else:
            self.ui.OwnPropertyComboBox.model().item(bef_idx).setEnabled(True)

        ### Find Saved Location in Garage Select Combo Box
        target_index = -1
        for i in range(self.ui.OwnPropertyComboBox.count()):
            item_data = self.ui.OwnPropertyComboBox.itemData(i)
            
            ### info['own_prop_id'] == target_id
            if item_data and item_data[0] == own_data['owned_property_id']:
                if item_data[1] == own_data['slot_type_id']:
                    target_index = i
                    break

        ### Refresh slot_left Value
        if target_index != -1:
            self.ui.OwnPropertyComboBox.setCurrentIndex(target_index)
            data = self.ui.OwnPropertyComboBox.currentData()
            aft_garage_tuple = tuple(data) if isinstance(data, list) else data
            aft_garage_data = self.garagedict.get(aft_garage_tuple)

            if aft_garage_data.get('slot_left') < 1:
                self.ui.OwnPropertyComboBox.model().item(target_index).setEnabled(False)
            else:
                self.ui.OwnPropertyComboBox.model().item(target_index).setEnabled(True)

            self.change_card_garage_image()

        ### Refresh Checkboxes
        for field, checkbox in self.checkbox_mapping.items():
            checkbox.setChecked(own_data.get(field, False))

    def refresh_garage_combobox(self):
        """
            Refreshes the ComboBox items
            because of 'slot_left'
        """
        for i in range(self.ui.OwnPropertyComboBox.count()):
            item_data = self.ui.OwnPropertyComboBox.itemData(i)
            garage_tuple = tuple(item_data) if isinstance(item_data, list) else item_data
            garage_data = self.garagedict.get(garage_tuple)

            if garage_data.get('slot_left') < 1:
                self.ui.OwnPropertyComboBox.model().item(i).setEnabled(False)
            else:
                self.ui.OwnPropertyComboBox.model().item(i).setEnabled(True)

    def dragEnterEvent(self, event):
        """
            Border Outline when ColorPresetCard is Dragged Here
        """
        if event.mimeData().hasFormat("application/x-color-card"):
            self.ui.CardPaintPresetPreviewWidget.setStyleSheet("""
                                                        #CardPaintPresetPreviewWidget {
                                                        border: 4px solid #3498db;
                                                        }
                                                        """) # 파란 테두리 강조
            event.acceptProposedAction()

    def dragLeaveEvent(self, event):
        """
            Remove Style when ColorPresetCard is dragged and leave Here
        """
        self.ui.CardPaintPresetPreviewWidget.setStyleSheet("") 

    def dropEvent(self, event):
        """
            get Paint Data from JSON and make a ColorPresetCard Here
        """
        if event.mimeData().hasFormat("application/x-color-card"):
            # 1. 바이트 데이터 꺼내서 JSON 해독
            raw_data = event.mimeData().data("application/x-color-card").data()
            recipe = json.loads(raw_data.decode('utf-8'))
            
            color_info = recipe['data'] # 복사된 카드 데이터

            # 2. VehicleCard 내부의 특정 레이아웃에 '드래그가 안 되는' 위젯으로 생성
            # 예: self.ui.SelectedColorLayout 같은 곳에 추가
            self.apply_color_to_vehicle(color_info)
            
            self.ui.CardPaintPresetPreviewWidget.setStyleSheet("") 
            event.acceptProposedAction()

    def apply_color_to_vehicle(self, color_info):
        """
            Create ColorPresetCard and add to Layout\n
            Then Send Data changed Signal
        """
        new_small_widget = ColorPresetCard(color_info, self.what_gradient_preview, True, False) # 별도로 만든 심플한 위젯 클래스
        if new_small_widget:
            
            new_small_widget.adjust_content_size(self.color_height)
            self.preset_card = new_small_widget

        item = self.card_layout.takeAt(0)
        itemwidget = item.widget()
        if itemwidget:
            itemwidget.deleteLater()

        self.card_layout.addWidget(self.preset_card)
        
        self.data_changed.emit(self.own_data.get('id'), {'paint_preset_id': color_info['id']})

    def set_paintcard_to_vehicle(self, color_card:ColorPresetCard):
        """
            This is for ColorPresetCard created via AddButton because there is no existing Card
        """
        if color_card:
            color_card.adjust_content_size(self.color_height)
            self.preset_card = color_card

        item = self.card_layout.takeAt(0)
        itemwidget = item.widget()
        if itemwidget:
            itemwidget.deleteLater()

        self.card_layout.addWidget(self.preset_card)
        
        self.data_changed.emit(self.own_data.get('id'), {'paint_preset_id': color_card.preset_data['id']})

    def showEvent(self, event):
        """
            fix Size Error
        """
        super().showEvent(event)
        self.adjust_content_size(self.height())

class AcquisitionCard(QWidget):
    """
        Pre-generated AcquisitionCard cached in memory for later use.
    """
    def __init__(self, acq_name):
        super().__init__()
        self.ui = Ui_ACQWidget()
        self.ui.setupUi(self)

        pixmap = ImageManager.get_image('ACQ', acq_name)
        self.ui.ACQImageLabel.set_image(pixmap)
        self.ui.ACQImageLabel.apply_rounded_corners(10) 
        self.ui.ACQTextLabel.setText(acq_name)
        self.ui.ACQTextLabel.setStyleSheet(
            """
                color: white;
                font-weight: bold;
                font-size: 11pt;
            """
        )

    def adjust_content_size(self, new_height):
        """
            resize widget to be fixed (new_height, new_height * 10)
        """
        new_width = int(new_height * 10)
        self.setFixedSize(new_width, new_height)

class GarageCarPreviewCard(QWidget):
    """
        LEGACY Garage Vehicle Preview Card
        Use Garage Card Delegate Instead
    """
    data_changed = Signal(int, str, object)
    def __init__(self, vehicle_data, own_data, color_card):
        super().__init__()
        self.ui = Ui_GarageVehicleCardWidget()
        self.ui.setupUi(self)

        self.vehicle_data = vehicle_data
        self.own_data = own_data
        self.preset_card = color_card
        self.card_layout = QVBoxLayout(self.ui.CardPaintPresetPreviewWidget)
        self.card_layout.setContentsMargins(0,0,0,0)
        self.card_layout.setSpacing(0)
        self.color_height = self.ui.CardPaintPresetPreviewWidget.height()

        if self.preset_card is not None:
            self.card_layout.addWidget(self.preset_card)
            

        self.ui.ManufacturerLabel.setText( f"{self.vehicle_data.get('manufacturer', 'Unknown')}" )
        self.ui.VehicleNameLabel.setText( f"{self.vehicle_data.get('name', 'Unknown')}" )
        self.ui.ClassLabel.setText( f"{self.vehicle_data.get('vehicle_class', 'Unknown')}" )
        self.ui.PriceLabel.setText( f"{self.vehicle_data.get('price', 'Unknown')}" )

        checkbox_mapping = {
            'limited_mod': self.ui.LimitedModCheckBox,
            'limited_plate': self.ui.LimitedPlateCheckBox,
            'limited_paint': self.ui.LimitedPaintCheckBox,
            'limited_livery': self.ui.LimitedLiveryCheckBox,
            'is_reward': self.ui.RewardCheckBox,
            'mod_custom': self.ui.ModCustomCheckBox,
            'mod_upgrade': self.ui.ModUpgradeCheckBox,
            'mod_imani': self.ui.ModImaniCheckBox,
            'mod_hsw': self.ui.ModHSWCheckBox,
            'mod_drift': self.ui.ModDriftCheckBox
        }

        for field, checkbox in checkbox_mapping.items():
            checkbox.setChecked(own_data.get(field, False))
            
            # 클릭 시 시그널 발송 연결
            # lambda 내부의 f와 c는 루프 시점의 값을 고정하기 위해 사용합니다.
            checkbox.clicked.connect(
                lambda checked, f=field, c=checkbox: self.data_changed.emit(self.own_data.get('id'), f, c.isChecked())
            )

        self.ui.SellButton.clicked.connect(
            lambda: self.data_changed.emit(self.own_data.get('id'), 'is_sold', True)
        )

        self.ui.PageButton.clicked.connect(self.on_page_button_clicked)
        self.ui.PageButton2.clicked.connect(self.on_page_button_clicked)

        pixmap = ImageManager.get_image("Vehicle", f"{self.vehicle_data['id']}")
        self.ui.VehicleImageLabel.set_image(pixmap)

    def on_page_button_clicked(self):
        ### Change page in Stacked Widget
        page = self.ui.GarageVehicleStackedWidget.currentIndex()
        if page == 0:
            self.ui.GarageVehicleStackedWidget.setCurrentIndex(1)
        else:
            self.ui.GarageVehicleStackedWidget.setCurrentIndex(0)

    def adjust_content_size(self, new_width):
        """
            resize widget to be fixed (new_width, new_width * 12 / 32)
        """
        new_height = int(new_width * 12 / 32)
        self.setFixedSize(new_width, new_height)

        print(f"RESIZE Garage Car Card : { new_width }, { new_height }")

        self.color_height = self.ui.CardPaintPresetPreviewWidget.height()
        if self.preset_card:
            print(f"Color Height : {self.color_height}")
            self.preset_card.adjust_content_size(self.color_height)
        pass
    
    def showEvent(self, event):
        """
            fix Size Error
        """
        super().showEvent(event)
        self.adjust_content_size(self.width())

class ColorReferenceWidget(QFrame):
    """
        Widget for Paint tab Sidebar Color Reference
    """
    double_clicked = Signal(dict) # (color ref dict)
    def __init__(self, color_ref):
        super().__init__()
        self.ui = Ui_ColorRefWidget()
        self.ui.setupUi(self)

        self.color_ref = copy.deepcopy(color_ref)
        self.setWidget(color_ref)
        self.ui.ColorTextLabel.setWordWrap(True)

    def fillWidget(self):
        """
            Applies the background color
            and changes the font color
            according to the color's RGB values.
        """
        color_name = self.color_ref.get('name', "Unknown")
        hex_color = self.color_ref.get('hex_color', "#000000")

        self.ui.ColorTextLabel.setText(color_name)
        font_size = 8

        color = QColor(hex_color)
    
        # Calculate background brightness using
        # the W3C weighted formula.
        # Returns a value between 0 and 255.
        brightness = (color.red() * 299 + color.green() * 587 + color.blue() * 114) / 1000
        
        text_color = "white" if brightness < 128 else "black"
        
        self.setStyleSheet(f"""
            #{self.objectName()} {{
                background-color: {hex_color};
                border: none;
                border-radius: 4px;
            }}
            #ColorTextLabel {{
                color: {text_color};
                font-weight: bold;
                font-size: {font_size}pt;
            }}
        """)

    def setWidget(self, color_ref):
        """
            fill color and set Color name
        """
        if (color_ref is None):
            return
        
        #print(f"Color Widget Set : {color_ref}")
        self.color_ref = copy.deepcopy(color_ref)
        self.fillWidget()
        self.setToolTip(f"[{color_ref.get('name', 'Unknown')}] : {color_ref.get('hex_color', "#000000")}")
    
    def mouseDoubleClickEvent(self, event):
        """
            Left DoubleClick Mouse Event to Edit Color Hex
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self.double_clicked.emit(self.color_ref)
        super().mouseDoubleClickEvent(event)
        
"""
def init_data():

    is_new_db = not os.path.exists(DBLoader_GTA.db_file) # 파일 자체가 없는지 확인

    conn = sqlite3.connect(DBLoader_GTA.db_file)
    try:
        seeder_info = {
            'init.sql' : [],
            'vehicle_table.sql' : [
                                    'GTAVOManufacturerDataTable.csv',
                                    'GTAVOVehicleClassTable.csv',
                                    'GTAVOVehicleDrivetrain.csv',
                                    'GTAVOAcquisitionDataTable.csv',
                                    'GTAVOAcquisitionSource.csv',
                                    'GTAVOVehicleDataTable.csv',
                                    'GTAVOVehicleTranslation.csv'
                                ],
            'paintpreset_table.sql' : [
                                        'GTAVORenderMaterial.csv',
                                        'GTAVOColorRefTable.csv',
                                        'GTAVOChameleonType.csv',
                                        'GTAVOLiveryType.csv',
                                        'GTAVODefaultPaintDataTable.csv'
                                    ],
            'property_table.sql' : [
                                    'GTAVOPropertyCustomTable.csv',
                                    'GTAVOPropertyCustomTypeTable.csv',
                                    'GTAVOPropertyDataTable.csv',
                                    'GTAVOPropertyTypeTable.csv'
                                ],
            'storage_table.sql' : [
                                    'GTAVOStorageCompatibilityTable.csv',
                                    'GTAVOStorageDedicatedTable.csv',
                                    'GTAVOStorageLocationTable.csv',
                                    'GTAVOStorageSlotTypeTable.csv'
                                ],
            'buying_table.sql' : [
                                    'GTAVOBonusTargetTable.csv',
                                    'GTAVOBonusDataTable.csv'
                                ]

        }
        seeder = SmartSeeder(conn, seeder_info)
        
        if is_new_db:
            print("🆕 Detected 'Reset argument'. rebuild DB...")
            seeder.run_all(force=True) # seed all
        else:
            seeder.run_all() # seed updated only
            
    finally:
        conn.close()

def init_user():

    is_new_db = not os.path.exists(DBLoader_USER.db_file)
    user_sql = os.path.join(SmartSeeder.SQL_DIR, "player_own_table.sql")
    db_dir = os.path.dirname(DBLoader_USER.db_file)

    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)

    conn = sqlite3.connect(DBLoader_USER.db_file)

    try:
        print("Loading USER DB...")
        if is_new_db:
            print("🆕 Building New USER DB")
            if os.path.exists(user_sql):
                with open(user_sql, 'r', encoding='utf-8') as f:
                    sql_script = f.read()

                conn.cursor().executescript(sql_script)
                conn.commit()
                print(f"📜 SQL Script done: {user_sql}")
            else:
                print(f"⚠️ Cannot Find SQL: {user_sql}")

        else:
            pass

    finally:
        conn.close()
    

if __name__ == "__main__":
    ### 실행 시 'python main.py --reset' 이라고 치면 DB 삭제 후 재생성
    ### Running 'python main.py --reset' deletes and recreates the DB.
    if "--reset" in sys.argv:
        if os.path.exists(DBLoader_GTA.db_file):
            os.remove(DBLoader_GTA.db_file)
            print("🗑️ Removed GTA DB")
        if os.path.exists(DBLoader_USER.db_file):
            os.remove(DBLoader_USER.db_file)
            print("🗑️ Deleted USER DB")
    
    init_data()
    init_user()
    ### Run PySide6 App
    app = QApplication(sys.argv)
    # sys.excepthook = lambda cls, ex, tb: print(f"Fatal Error: {ex}")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
"""
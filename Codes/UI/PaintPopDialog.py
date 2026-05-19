import copy

from PySide6.QtWidgets import QAbstractItemView, QDialog, QLabel, QSizePolicy, QVBoxLayout, QPushButton, QColorDialog, QLineEdit
from PySide6.QtCore import QEvent, Qt, Signal
from PySide6.QtGui import QColor, QPixmap, QStandardItem, QStandardItemModel
from Codes.Library.DataToView import show_color_picker_dialog
from Codes.Service.ImageManager import ImageManager
from Codes.UI.LiveryDialog import LiveryDialog
from Codes.UI.GTAVOVM_PaintingPop import Ui_PaintManager
from Codes.UI.lib.ImageFittingLabel import ImageFittingLabel
from Codes.config import AppConfig

class PaintEditDialog(QDialog):
    """
        Dialog that appears when you click ColorPresetCard or add a paint from OwnVehicleCard
    """
    CHROME_INDEX = 1
    def __init__(self, paint_list, render_map, livery_map, current_data, preset_card, on_crew_add, parent=None):
        super().__init__(parent)
        self.ui = Ui_PaintManager()
        self.ui.setupUi(self)
        self.setModal(True) ### Modal
        
        self.plist = paint_list
        self.render_map = render_map
        self.livery_map = livery_map
        self.data = copy.copy(current_data)
        self.added_ref_dict = dict()
        self.added_index_num = -31
        self.preset_card = preset_card
        self.on_crew_add = on_crew_add ### crew color add function

        print(current_data)

        self.preset_layout = QVBoxLayout(self.ui.ColorPreview) 
        self.preset_layout.setContentsMargins(0,0,0,0)
        self.preset_layout.setSpacing(0)
        self.card_width = self.ui.ColorPreview.width()

        for render_id, render_tag in self.render_map.items():
            if (render_tag == "Custom") or (render_tag == "Index"):
                continue
            self.ui.PrimaryComboBox.addItem(render_tag)
            self.ui.SecondaryComboBox.addItem(render_tag)

        self.ui.PrimaryComboBox.currentIndexChanged.connect(self.on_render_changed)
        self.ui.SecondaryComboBox.currentIndexChanged.connect(self.on_render_changed)

        ### Drag Init
        self.ui.treeView.setDragEnabled(True)  
        self.ui.treeView.setDragDropMode(QAbstractItemView.DragDropMode.DragOnly)      
        self.ui.treeView.doubleClicked.connect(self.on_tree_double_clicked)

        self.current_cursor = None

        ### Maps each color name tag to its corresponding UI frame widget.
        self.color_widget_mapping = {
            'primary': self.ui.PrimaryColorFrame,
            'secondary': self.ui.SecondaryColorFrame,
            'pearl': self.ui.PearlColorFrame,
            'wheel': self.ui.WheelColorFrame,
            'dial': self.ui.DialColorFrame,
            'trim': self.ui.TrimColorFrame,
            'headlight': self.ui.HeadLightColorFrame,
            'neon': self.ui.NeonColorFrame,

        }

        self.ui.ColorPreview.setAcceptDrops(True)
        self.ui.ColorPreview.installEventFilter(self)

        for keys, frames in self.color_widget_mapping.items():
            frames.setAcceptDrops(True)
            frames.installEventFilter(self)

        ### Click LiveryFrame to Open Livery Manager
        self.ui.LiveryColorFrame.installEventFilter(self)
        self.livery_layout = QVBoxLayout(self.ui.LiveryColorFrame)
        self.livery_layout.setContentsMargins(0, 0, 0, 0)
        self.livery_layout.setSpacing(0)
        self.current_livery_label = None

        ### Connect Buttons in Right Bottom Corner
        self.ui.PaintManagerButtonBox.accepted.connect(self.accept) # return 1(Accepted)
        self.ui.PaintManagerButtonBox.rejected.connect(self.reject) # return 0(Rejected)

        ### Connect new Crew Color
        self.ui.PaintPopNewCrewColorButton.clicked.connect(self.add_new_crew_color)

        self.fill_paint_dialog()

    def fill_paint_dialog(self):
        """
            Set Style in Frame, Display ComboBox, and Fill Color Treeview
        """
        if not self.preset_layout.itemAt(0):
            self.preset_card.adjust_content_size(self.card_width)
            self.preset_layout.addWidget(self.preset_card)
        
        self.ui.PresetNameEditor.setText( self.data.get('name', "Unknown") )

        pindex = self.ui.PrimaryComboBox.findText( self.data.get('prender', "Classic") )
        if pindex is not None:
            self.ui.PrimaryComboBox.setCurrentIndex(pindex)

        sindex = self.ui.SecondaryComboBox.findText( self.data.get('srender', "Classic") )
        if sindex is not None:
            self.ui.SecondaryComboBox.setCurrentIndex(sindex)

        for tag, frame in self.color_widget_mapping.items():
            self.set_highlight(frame, False)


        self.update_livery_view()

        self.set_tree_model()

    def clear_layout(self):
        """
            takeAt(0) and deleteLater
        """
        while self.livery_layout.count():
            item = self.livery_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def update_livery_view(self):
        """
            If data has livery_id, set image to my Custom ImageFittingLabel\n
            else, UI Default Image will be set
        """
        livery_id = self.data.get('livery_type_id')
        
        # Clear
        self.clear_layout()

        if livery_id is None:
            # None > UI.PaintNone
            self.current_livery_label = QLabel()
            self.current_livery_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            pixmap = ImageManager.get_image('UI', "PaintNone")
            if pixmap:
                self.current_livery_label.setPixmap(pixmap)

        else:
            # set Image
            self.current_livery_label = ImageFittingLabel()
            lvname = self.livery_map.get(livery_id, {}).get('name', 'Unknown')
            self.data['livery_name'] = lvname
            pixmap = ImageManager.get_image('Livery', lvname)
            self.current_livery_label.set_image(pixmap)

        # Set Style
        self.current_livery_label.setSizePolicy(
            QSizePolicy.Policy.Ignored, 
            QSizePolicy.Policy.Ignored
        )
        self.current_livery_label.setStyleSheet("border: 1px solid #000000; border-radius: 5px;")
        self.livery_layout.addWidget(self.current_livery_label)

    def set_tree_model(self):
        """
            Color List will be set here\n
            There are Categories (Index(Crew) + GTA Default Categories + UserPaintPreset)\n
            Displays child entries with color hex values
            as a tree view within the category
        """
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['Color Name', 'Hex Code'])

        self.crew_parent = QStandardItem("Crew Colors")
        self.crew_parent.setEditable(False)
        self.crew_parent.setDragEnabled(False)
        model.appendRow(self.crew_parent)

        ### Iterating all Paints
        for category, items in self.plist.items():
            ### parent category
            parent_item = QStandardItem(category)
            parent_item.setEditable(False)
            parent_item.setDragEnabled(False)
            model.appendRow(parent_item)

            ### index is simple, just add items
            if category == 'Index':
                for color_id, data in items.items():
                    ### child item
                    name = data.get('name', 'Unknown')
                    hex_code = data.get('hex_color', '#FFFFFF')
                    gta_def = data.get('gta_color_id', None)

                    # 이름 아이템 (여기에 색상 아이콘을 넣을 것)
                    name_item = QStandardItem(name)
                    name_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsDragEnabled) # 드래그 플래그 추가
                    name_item.setData(color_id, Qt.ItemDataRole.UserRole) # ID 값은 숨겨진 데이터로 보관
                    
                    # 🎨 색상 아이콘 만들기
                    pixmap = QPixmap(16, 16)
                    pixmap.fill(QColor(hex_code))
                    name_item.setIcon(pixmap)

                    # HEX코드 아이템
                    code_item = QStandardItem(hex_code)
                    
                    ### If this Index do not have GTA ID, It will be going to Crew Category
                    if gta_def is not None:
                        parent_item.appendRow([name_item, code_item])
                    else:
                        self.crew_parent.appendRow([name_item, code_item])

                """
                    Only the Primary color is shown
                    in the Custom category,
                    but the entire preset will be applied
                    when processing the actual color setup.
                """
            elif category == 'Custom':
                for preset_id, data in items.items():
                    ### child item
                    #print(data)
                    name = data.get('name', 'Unknown')
                    ccid = data.get('primary_color_id', -1)
                    cdata = self.plist.get('Index', {}).get(ccid, None)
                    hex_code = cdata.get('hex_color', '#FFFFFF')

                    # 이름 아이템 (여기에 색상 아이콘을 넣을 것)
                    name_item = QStandardItem(name)
                    name_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsDragEnabled) # 드래그 플래그 추가
                    name_item.setData(preset_id, Qt.ItemDataRole.UserRole) # ID 값은 숨겨진 데이터로 보관
                    
                    # 🎨 색상 아이콘 만들기
                    pixmap = QPixmap(16, 16)
                    pixmap.fill(QColor(hex_code))
                    name_item.setIcon(pixmap)

                    # 코드 아이템
                    code_item = QStandardItem(hex_code)
                    
                    # 부모 아래에 한 줄(Row) 추가
                    parent_item.appendRow([name_item, code_item])

                ### Other GTA Categories like Classic, Metallic...
            else:
                for preset_id, data in items.items():
                    ### child item
                    #print(data)
                    name = data.get('name', 'Unknown')
                    ccid = data.get('primary_color_id', -1)
                    cdata = self.plist.get('Index', {}).get(ccid, None)
                    hex_code = cdata.get('hex_color', '#FFFFFF')

                    # 이름 아이템 (여기에 색상 아이콘을 넣을 것)
                    name_item = QStandardItem(name)
                    name_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsDragEnabled) # 드래그 플래그 추가
                    name_item.setData(preset_id, Qt.ItemDataRole.UserRole) # ID 값은 숨겨진 데이터로 보관
                    
                    # 🎨 색상 아이콘 만들기
                    pixmap = QPixmap(16, 16)
                    pixmap.fill(QColor(hex_code))
                    name_item.setIcon(pixmap)

                    # 코드 아이템
                    code_item = QStandardItem(hex_code)
                    
                    # 부모 아래에 한 줄(Row) 추가
                    parent_item.appendRow([name_item, code_item])

        
        ### set Model View
        self.ui.treeView.setModel(model)
        # self.ui.treeView.expandAll()
        self.ui.treeView.setColumnWidth(0, 300)
        self.ui.treeView.setColumnWidth(1, 30)

    def add_new_crew_color(self):
        """
            Same Function as Main's New Crew Color Function,\n
            And Add Tree item in Crew Category\n
            'on_crew_add' will send Color Data to Main saving DB
        """
        name, hex_code = show_color_picker_dialog(self, "CREW", "000000")

        if name is None or hex_code is None:
            return

        new_crew_id = self.on_crew_add(name, hex_code)

        # model = self.ui.treeView.model()
        # items = model.findItems('Index', Qt.MatchFlag.MatchExactly | Qt.MatchFlag.MatchRecursive)

        #if items:
            # parent_item = items[0]
        name_item = QStandardItem(name)
        name_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsDragEnabled) # 드래그 플래그 추가
        
        new_color_ref = {
            'id' : new_crew_id, #self.added_index_num,
            'name' : name,
            'hex_color' : hex_code
        }
        self.added_ref_dict[new_crew_id] = new_color_ref
        self.plist['Index'][new_crew_id] = new_color_ref
        name_item.setData(new_crew_id, Qt.ItemDataRole.UserRole) 
        # self.added_index_num = self.added_index_num - 1
        
        # 🎨 색상 아이콘 만들기
        pixmap = QPixmap(16, 16)
        pixmap.fill(QColor(hex_code))
        name_item.setIcon(pixmap)

        # 코드 아이템
        code_item = QStandardItem(hex_code)
        
        # 부모 아래에 한 줄(Row) 추가
        # parent_item.appendRow([name_item, code_item])
        self.crew_parent.appendRow([name_item, code_item])
        pass

    def pick_color(self):
        """
            **DEPRECATED**\n
            Old Version Color Picker
        """
        # Qt 기본 색상 선택창 띄우기
        color = QColorDialog.getColor()
        if color.isValid():
            # self.data['color_hex'] = color.name() # #RRGGBB 형태
            # self.color_btn.setStyleSheet(f"background-color: {color.name()};")
            pass

    def get_result(self):
        """
            Returns Edited Paint Data
        """
        self.data['name'] = self.ui.PresetNameEditor.text()
        return self.data
    
    def get_added_crew_color(self):
        """
            **DEPRECATED**\n
            All Crew colors are now sent by 'self.on_crew_add'
        """
        return self.added_ref_dict
    
    def showEvent(self, event):
        """
            Set Dialog size when Opening
        """
        self.adjust_content_size()
        return super().showEvent(event)
    
    def on_tree_double_clicked(self, index):
        """
            Double-clicking a tree item applies its color
            to the currently selected color type
            after a widget or frame has been selected.
        """
        if self.current_cursor is None:
            return
        ### Ignore when User clicked Category
        parent_index = index.parent()
        if not parent_index.isValid():
            return # 카테고리 이름을 더블클릭한 경우 무시

        category = parent_index.data(Qt.ItemDataRole.DisplayRole)
        color_data = index.data(Qt.ItemDataRole.UserRole)

        print(f"Set Color: {category} -> {self.current_cursor}")

        self.apply_dropped_color(self.current_cursor, category, color_data)
        

    def eventFilter(self, watched, event):
        """
            Color Widget, Frame's Click and Drag Events
        """
        is_color_widget = (watched in self.color_widget_mapping.values() or 
                           watched == self.ui.ColorPreview)

        if is_color_widget:
            ### Mouse Left Click
            if event.type() == QEvent.Type.MouseButtonPress:
                if event.button() == Qt.MouseButton.LeftButton:
                    print(f"Clicked: {watched.objectName()}")
                    self.handle_widget_click(watched)
                    return True

            ### Dragging into Widget
            if event.type() == QEvent.Type.DragEnter:
                if event.mimeData().hasFormat("application/x-qabstractitemmodeldatalist"):
                    event.acceptProposedAction()
                    self.refresh_widget_style(self.current_cursor)
                    self.set_highlight(watched, True)
                    return True

            ### Dragging out of Widget
            elif event.type() == QEvent.Type.DragLeave:
                self.refresh_widget_style(watched)
                return True

            ### Drag and Drop
            elif event.type() == QEvent.Type.Drop:
                self.refresh_widget_style(watched)
                
                ### Send Dragged Color id and Category to Widget
                selection = self.ui.treeView.selectedIndexes()
                if selection:
                    child_index = selection[0]
                    parent_index = child_index.parent()

                    category_name = parent_index.data(Qt.ItemDataRole.DisplayRole)
                    color_id = child_index.data(Qt.ItemDataRole.UserRole)
                    self.apply_dropped_color(watched, category_name, color_id)
            
                    event.acceptProposedAction()
                return True
            
        ### Clicked Livery Widget
        elif watched == self.ui.LiveryColorFrame and event.type() == QEvent.Type.MouseButtonPress:
                if event.button() == Qt.MouseButton.LeftButton:
                    self.open_livery_manager()
                    pass

        return super().eventFilter(watched, event)
    
    def open_livery_manager(self):
        """
            Open Livery Dialog When user Clicked Livery Widget
        """
        current_id = self.data['livery_type_id']
        
        dialog = LiveryDialog(self.livery_map, current_id, self)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_livery_id = dialog.get_selected_livery()
            
            if new_livery_id != current_id:
                ### apply Livery id and image to PresetCard and LiveryWidget
                self.data['livery_type_id'] = new_livery_id

                self.update_livery_view()
                print(f"Livery changed to: {new_livery_id}")
                self.preset_card.edit_preset(self.data)
    
    def apply_dropped_color(self, target_widget, category, color_id):
        """
            Set Color to Widget(Preset)
        """
        print(f"Dropped from Category: {category}, Color ID: {color_id}")

        ### Category : Crew colors is same as Index
        if category == "Crew Colors":
            category = "Index"


        """
            Dropping a color onto the Main Preview ColorPreset
            copies the entire preset configuration.

            All colors are copied when the source
            is another user preset.
            In normal cases, only the Primary
            and Pearl colors are mainly transferred.
        """
        if target_widget == self.ui.ColorPreview:
            pdata = self.plist.get(category, {}).get(color_id, None)
            if pdata is None:
                print("selected color results None")
                print("returns")
                return

            if category == "Custom":
                # Custom Preset Logic >> 전부 다 때려박기 하면 됨
                for keys, frames in self.color_widget_mapping.items():
                    cidtag = (f"{keys}_color_id")
                    thisid = pdata.get(cidtag, -1)
                    if (thisid != -1) and (thisid is not None):
                        self.data[cidtag] = thisid
                        self.data[keys] = self.plist.get("Index", {}).get(self.data[cidtag], {"hex_color": "#000000", "name": "Unknown"})
                        self.set_highlight(frames, False)

                prender_id = pdata.get('primary_render_id', -1)
                self.data['primary_render_id'] = prender_id
                self.data['prender'] = self.render_map.get(prender_id, 'Unknown')

                srender_id = pdata.get('secondary_render_id', -1)
                if (srender_id != -1) and (srender_id is not None):
                    self.data['secondary_render_id'] = srender_id
                    self.data['srender'] = self.render_map.get(srender_id, 'Unknown')

            elif (category == "Index") or (category == "Crew Colors"):
                # Ingle Color Ref Index Logic
                self.data['primary_color_id'] = pdata.get('id', -1)
                self.data['primary'] = pdata

                prender_id = pdata.get('default_rendermaterial_id', -1)
                self.data['primary_render_id'] = prender_id
                self.data['prender'] = self.render_map.get(prender_id, 'Unknown')

                pindex = self.ui.PrimaryComboBox.findText( self.data.get('prender', "Unknown") )
                if pindex is not None:
                    self.ui.PrimaryComboBox.setCurrentIndex(pindex)

                self.set_highlight(self.ui.PrimaryColorFrame, False) 

            else:
                # GTA Defaults Logic
                pcid = pdata.get('primary_color_id', -1)
                self.data['primary_color_id'] = pcid
                self.data['primary'] = self.plist.get("Index", {}).get(pcid, {"hex_color": "#000000", "name": "Unknown"})

                prender_id = pdata.get('primary_render_id', -1)
                self.data['primary_render_id'] = prender_id
                prendername = self.render_map.get(prender_id, 'Unknown')
                self.data['prender'] = prendername
                pindex = self.ui.PrimaryComboBox.findText( prendername )
                if pindex is not None:
                    self.ui.PrimaryComboBox.setCurrentIndex(pindex)

                scid = pdata.get('secondary_color_id', -1)
                if (scid != -1) and (scid is not None):
                    self.data['secondary_color_id'] = scid
                    self.data['secondary'] = self.plist.get("Index", {}).get(scid, {"hex_color": "#000000", "name": "Unknown"})

                    srender_id = pdata.get('secondary_render_id', -1)
                    self.data['secondary_render_id'] = srender_id
                    srendername = self.render_map.get(srender_id, 'Unknown')
                    self.data['srender'] = srendername
                    sindex = self.ui.PrimaryComboBox.findText( srendername )
                    if sindex is not None:
                        self.ui.PrimaryComboBox.setCurrentIndex(sindex)

                plid = pdata.get('pearl_color_id', -1)
                if (plid != -1) and (plid is not None):
                    self.data['pearl_color_id'] = plid
                    self.data['pearl'] = self.plist.get("Index", {}).get(plid, {"hex_color": "#000000", "name": "Unknown"})

                self.set_highlight(self.ui.PrimaryColorFrame, False)
                self.set_highlight(self.ui.SecondaryColorFrame, False)
                self.set_highlight(self.ui.PearlColorFrame, False)

        else:
            """
                There are three behaviors when dropping colors onto frames:

                - Custom Category:
                Copies the matching custom color type
                according to the selected frame type.
                Primary and Secondary also copy the render ID.

                - Index Category:
                Applies the color and render ID directly.

                - GTA Categories:
                Applies only the Primary color
                with the render ID.
            """
            if category == "Custom":
                # Custom Preset 로직
                for keys, frames in self.color_widget_mapping.items():
                    if target_widget == frames:
                        pdata = self.plist.get(category, {}).get(color_id, None)
                        cidtag = (f"{keys}_color_id")
                        if pdata is None:
                            print("selected color results None")
                            #"""
                            if keys == 'primary':
                                self.data['prender'] = 'Unknown'
                                self.data['primary_render_id'] = -1
                                self.ui.PrimaryComboBox.setCurrentIndex(-1)
                                
                            elif keys == 'secondary':
                                self.data['srender'] = 'Unknown'
                                self.data['secondary_render_id'] = -1
                                self.ui.SecondaryComboBox.setCurrentIndex(-1)

                            self.data[keys] = {"hex_color": "#000000", "name": "Unknown"}
                            self.data[cidtag] = -1
                            self.set_highlight(target_widget, False)
                            #"""
                            break

                        else:
                            if keys == 'primary':
                                prender_id = pdata.get('primary_render_id', -1)
                                self.data['primary_render_id'] = prender_id
                                self.data['prender'] = self.render_map.get(prender_id, 'Unknown')

                                pindex = self.ui.PrimaryComboBox.findText( self.data.get('prender', "Unknown") )
                                if pindex:
                                    self.ui.PrimaryComboBox.setCurrentIndex(pindex)

                            elif keys == 'secondary':
                                srender_id = pdata.get('secondary_render_id', -1)
                                self.data['secondary_render_id'] = srender_id
                                self.data['srender'] = self.render_map.get(srender_id, 'Unknown')

                                sindex = self.ui.SecondaryComboBox.findText( self.data.get('srender', "Unknown") )
                                if sindex is not None:
                                    self.ui.SecondaryComboBox.setCurrentIndex(pindex)

                            self.data[cidtag] = pdata.get(cidtag, -1)
                            self.data[keys] = self.plist.get("Index", {}).get(self.data[cidtag], {"hex_color": "#000000", "name": "Unknown"})
                            print(f"{cidtag} :\n {self.data[keys]} \n: {self.data[cidtag]}")
                            self.set_highlight(target_widget, False)
                            break
                            
            elif (category == "Index") or (category == "Crew Colors"):
                for keys, frames in self.color_widget_mapping.items():
                    if target_widget == frames:
                        pdata = self.plist.get("Index", {}).get(color_id, None)
                        cidtag = (f"{keys}_color_id")
                        if pdata is None:
                            print("selected color results None")

                            if keys == 'primary':
                                self.data['prender'] = 'Unknown'
                                self.data['primary_render_id'] = -1
                                self.ui.PrimaryComboBox.setCurrentIndex(-1)
                                
                            elif keys == 'secondary':
                                self.data['srender'] = 'Unknown'
                                self.data['secondary_render_id'] = -1
                                self.ui.SecondaryComboBox.setCurrentIndex(-1)

                            self.data[keys] = {"hex_color": "#000000", "name": "Unknown"}
                            self.data[cidtag] = -1
                            self.set_highlight(target_widget, False)
                            break

                        else:
                            if keys == 'primary':
                                prender_id = pdata.get('default_rendermaterial_id', -1)
                                self.data['primary_render_id'] = prender_id
                                self.data['prender'] = self.render_map.get(prender_id, 'Unknown')

                                pindex = self.ui.PrimaryComboBox.findText( self.data.get('prender', "Unknown") )
                                if pindex is not None:
                                    self.ui.PrimaryComboBox.setCurrentIndex(pindex)

                            elif keys == 'secondary':
                                srender_id = pdata.get('default_rendermaterial_id', -1)
                                self.data['secondary_render_id'] = srender_id
                                self.data['srender'] = self.render_map.get(srender_id, 'Unknown')

                                sindex = self.ui.SecondaryComboBox.findText( self.data.get('srender', "Unknown") )
                                if sindex is not None:
                                    self.ui.SecondaryComboBox.setCurrentIndex(sindex)

                            self.data[cidtag] = pdata.get('id', -1)
                            self.data[keys] = pdata
                            print(f"{cidtag} :\n {self.data[keys]} \n: {self.data[cidtag]}")
                            self.set_highlight(target_widget, False)
                            break

            else:
                for keys, frames in self.color_widget_mapping.items():
                    if target_widget == frames:
                        pdata = self.plist.get(category, {}).get(color_id, None)
                        cidtag = (f"{keys}_color_id")
                        if pdata is None:
                            print("selected color results None")
                            #"""
                            if keys == 'primary':
                                self.data['prender'] = 'Unknown'
                                self.data['primary_render_id'] = -1
                                self.ui.PrimaryComboBox.setCurrentIndex(-1)
                                
                            elif keys == 'secondary':
                                self.data['srender'] = 'Unknown'
                                self.data['secondary_render_id'] = -1
                                self.ui.SecondaryComboBox.setCurrentIndex(-1)

                            self.data[keys] = {"hex_color": "#000000", "name": "Unknown"}
                            self.data[cidtag] = -1
                            self.set_highlight(target_widget, False)
                            #"""
                            break
                        else:
                            if keys == 'primary':
                                prender_id = pdata.get('primary_render_id', -1)
                                self.data['primary_render_id'] = prender_id
                                self.data['prender'] = category

                                pindex = self.ui.PrimaryComboBox.findText(category)
                                if pindex is not None:
                                    self.ui.PrimaryComboBox.setCurrentIndex(pindex)

                            elif keys == 'secondary':
                                srender_id = pdata.get('primary_render_id', -1)
                                self.data['secondary_render_id'] = srender_id
                                self.data['srender'] = category

                                sindex = self.ui.SecondaryComboBox.findText(category)
                                if sindex is not None:
                                    self.ui.SecondaryComboBox.setCurrentIndex(sindex)

                            pcid = pdata.get('primary_color_id', -1)
                            self.data[cidtag] = pcid
                            self.data[keys] = self.plist.get("Index", {}).get(pcid, {"hex_color": "#000000", "name": "Unknown"})
                            print(f"{cidtag} :\n {self.data[keys]} \n: {self.data[cidtag]}")
                            self.set_highlight(target_widget, False)
                            break
        
        self.preset_card.edit_preset(self.data)


    def refresh_widget_style(self, widget):
        """
            It will set highlight on widget,
            or unhighlight widget and set self.current_cursor None
        """
        if widget is None:
            return

        self.set_highlight(widget, False)

        if widget == self.current_cursor:
            self.current_cursor = None

    def handle_widget_click(self, clicked_widget):
        """
            Uncheck Currently selected widget
            and If user don't click same widget, Set clicked widget Checked state
        """
        if clicked_widget == self.current_cursor:
            self.refresh_widget_style(clicked_widget)
        else:
            ### Uncheck widget
            self.refresh_widget_style(self.current_cursor)
            ### and set Clicked Widget Checked
            self.current_cursor = clicked_widget
            self.set_highlight(clicked_widget, True)

    def set_highlight(self, widget, is_active=True):
        """
            Highlight the widget outline
            to indicate the currently editable target.
        """
        color_type = next((k for k, v in self.color_widget_mapping.items() if v == widget), None)
        base_color = self.data.get(color_type, {}).get('hex_color', None) if color_type else None

        ### Set Background
        if base_color:
            background_style = f"background-color: {base_color};"
        else:
            # 색상이 없을 경우 표시할 이미지 경로 (예: 투명 배경 아이콘)
            # url() 안에 상대경로나 절대경로를 넣습니다.
            no_color_img = AppConfig.get_main_image('UI', "PaintNone").replace("\\", "/")
            background_style = (
                f"background-image: url({no_color_img}); "
                f"background-position: center; "
                f"background-repeat: no-repeat;"
            )

        ### Border
        obj_name = widget.objectName()
        if is_active:
            border_style = "border: 2px solid #3498db; border-radius: 5px;"
        else:
            border_style = "border: 1px solid #000000; border-radius: 5px;"

        ### Apply Style
        style = f"#{obj_name} {{ {background_style} {border_style} }}"

        widget.setStyleSheet(style)

    def on_render_changed(self, index):
        """
            Apply the render ComboBox value to the PaintData render ID.
        """
        pindex = self.ui.PrimaryComboBox.findText( self.data.get('prender', "Unknown") )
        curpdx = self.ui.PrimaryComboBox.currentIndex()
        if curpdx != pindex:
            self.data['prender'] = self.ui.PrimaryComboBox.currentText()

        sindex = self.ui.SecondaryComboBox.findText( self.data.get('srender', "Unknown") )
        cursdx = self.ui.SecondaryComboBox.currentIndex()
        if cursdx != sindex:
            self.data['srender'] = self.ui.SecondaryComboBox.currentText()

        self.preset_card.edit_preset(self.data)

    def resizeEvent(self, event):
        self.adjust_content_size()
        super().resizeEvent(event)
    
    def adjust_content_size(self):
        """
            resize ColorPresetCard in ColorPreview
        """
        self.card_width = self.ui.ColorPreview.width()
        self.preset_card.adjust_content_size(self.card_width)
        #self.current_livery_label.setFixedSize(self.ui.LiveryColorFrame.size())
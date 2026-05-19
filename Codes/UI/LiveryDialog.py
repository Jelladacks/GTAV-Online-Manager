from PySide6.QtWidgets import QDialog, QVBoxLayout, QListWidget, QListWidgetItem, QDialogButtonBox
from PySide6.QtCore import QTimer, Qt, QSize
from PySide6.QtGui import QIcon, QPixmap
import os

from Codes.Service.ImageManager import ImageManager

class LiveryDialog(QDialog):
    def __init__(self, livery_dict, current_livery_id=None, parent=None):
        super().__init__(parent)
        self.liveries = livery_dict
        self.selected_livery_id = current_livery_id
        self.setWindowTitle("Livery Manager")
        self.setMinimumSize(1050, 800)
        
        self.init_ui()
        self.load_liveries()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # 1. 리스트 위젯 설정 (아이콘 모드)
        self.list_widget = QListWidget()
        self.list_widget.setViewMode(QListWidget.ViewMode.IconMode) # 격자 형태
        self.list_widget.setGridSize(QSize(150, 160))
        self.list_widget.setIconSize(QSize(120, 120))              # 아이콘 크기
        self.list_widget.setSpacing(10)                            # 간격
        self.list_widget.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.list_widget.setMovement(QListWidget.Movement.Static)  # 아이템 고정
        self.list_widget.setWordWrap(True)
        
        layout.addWidget(self.list_widget)

        # 2. 버튼 (확인/취소)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def load_liveries(self):
        """
            Iterating Livery List to fill Items
        """
        self.list_widget.clear()

        self.pending_items = []

        for livery in self.liveries.values():
            # 이미지 경로 (상대경로/절대경로 적절히 조절)
            
            item = QListWidgetItem(livery["name"])

            """
            pixmap = ImageManager.get_image('Livery', livery["name"])
            
            if not pixmap.isNull():
                # 아이콘 크기에 맞춰 부드럽게 스케일링
                icon_pixmap = pixmap.scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio, 
                                          Qt.TransformationMode.SmoothTransformation)
                item.setIcon(QIcon(icon_pixmap))
            """
            
            # 데이터 저장 (ID를 숨겨둠)
            item.setData(Qt.ItemDataRole.UserRole, livery["id"])
            
            self.list_widget.addItem(item)
            self.pending_items.append((item, livery["name"]))
            
            # 현재 설정된 리버리가 있다면 선택 상태로 표시
            if livery["id"] == self.selected_livery_id:
                item.setSelected(True)
        
        ### Prevent slow UI loading
        QTimer.singleShot(100, self.load_images_sequentially)
        
        self.list_widget.sortItems(Qt.SortOrder.AscendingOrder)

        # 1. '도색 없음' (기본) 아이템 추가
        none_item = QListWidgetItem("None")
        
        # ImageManager에서 UI 카테고리의 PaintNone 이미지를 가져옴
        none_pixmap = ImageManager.get_image('UI', "PaintNone")
        
        if none_pixmap and not none_pixmap.isNull():
            # 아이콘 크기에 맞춰 예쁘게 스케일링 (120x120 권장)
            icon_pixmap = none_pixmap.scaled(120, 120, 
                                           Qt.AspectRatioMode.KeepAspectRatio, 
                                           Qt.TransformationMode.SmoothTransformation)
            none_item.setIcon(QIcon(icon_pixmap))
        
        # 데이터 저장 (ID를 None 또는 0으로 설정)
        none_item.setData(Qt.ItemDataRole.UserRole, None) 
        self.list_widget.insertItem(0, none_item)
        

    def load_images_sequentially(self):
        """
            load image slowly so that UI dialog can be open first
        """
        if not self.pending_items:
            self.list_widget.doItemsLayout()
            self.list_widget.updateGeometries()
            self.list_widget.viewport().update()
            return
        
        item, name = self.pending_items.pop(0)

        pixmap = ImageManager.get_image('Livery', name)
        if not pixmap.isNull():
            icon_pixmap = pixmap.scaled(120, 120, 
                                    Qt.AspectRatioMode.KeepAspectRatio, 
                                    Qt.TransformationMode.SmoothTransformation)
            item.setIcon(QIcon(icon_pixmap))

        QTimer.singleShot(5, self.load_images_sequentially)

    def get_selected_livery(self):
        """
            returns Selected livery id
        """
        selected_items = self.list_widget.selectedItems()
        if selected_items:
            return selected_items[0].data(Qt.ItemDataRole.UserRole)
        return self.selected_livery_id
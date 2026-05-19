import os
import shutil
import time
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from Codes.config import AppConfig
from Codes.UI.lib.ImageFittingLabel import ImageFittingLabel

class ImageManagerDialog(QDialog):
    """
        Dialog for Editing Vehicle or Garage Image\n
        You can load path or paste image in this Dialog
    """
    image_updated = Signal(str, object)

    def __init__(self, category, data_key, parent=None):
        super().__init__(parent)
        self.category = category
        self.data_key = data_key
        self.store_key = None
        self.img_dir = AppConfig.CUSTOM_DIR
        self.selected_path = None

        ### Initialize Path
        if category == 'Vehicle':
            self.store_key = f"{int(data_key):04d}"
            self.img_dir = os.path.join(AppConfig.CUSTOM_DIR, "Vehicles")
            self.default_dir = os.path.join(AppConfig.IMAGE_DIR, "Vehicles", f"{self.store_key}.jpg")
        elif category == 'Garage' and isinstance(data_key, tuple):
            self.store_key = f"{data_key[0]}_{data_key[1]}"
            self.img_dir = os.path.join(AppConfig.CUSTOM_DIR, "Garages")
            self.default_dir = os.path.join(AppConfig.IMAGE_DIR, "Garages", f"{data_key[2]}_{data_key[1]}.webp")
        else:
            return
        
        # 폴더가 없으면 생성
        os.makedirs(self.img_dir, exist_ok=True)
        self.init_ui()
        self.load_existing_images()
        print("Dialog Init Complete")

    def init_ui(self):
        self.setWindowTitle(f"Image Manager - {self.category}: {self.store_key}")
        self.setFixedSize(600, 700)
        
        layout = QVBoxLayout(self)

        # 1. 상단: 파일 불러오기 버튼
        btn_layout = QHBoxLayout()
        self.btn_import = QPushButton("Load image file from files")
        self.btn_import.clicked.connect(self.import_from_file)
        btn_layout.addWidget(self.btn_import)
        layout.addLayout(btn_layout)

        # 2. 중앙: 메인 이미지 크게 보기
        self.main_img_label = ImageFittingLabel()
        self.main_img_label.setText("Select a Image or paste it with Ctrl+V")
        self.main_img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_img_label.setFrameShape(QFrame.Shape.Box)
        self.main_img_label.setFixedSize(580, 400)
        self.main_img_label.setScaledContents(True)
        layout.addWidget(self.main_img_label)

        # 3. 하단: 썸네일 리스트 (가로 스크롤)
        self.thumb_list = QListWidget()
        self.thumb_list.setViewMode(QListWidget.ViewMode.IconMode)
        self.thumb_list.setIconSize(QSize(100, 100))
        self.thumb_list.setMovement(QListWidget.Movement.Static)
        self.thumb_list.setFixedHeight(120)
        self.thumb_list.itemClicked.connect(self.on_item_clicked)
        layout.addWidget(self.thumb_list)

        # 4. 최하단: 저장/취소 버튼
        bottom_btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        bottom_btns.accepted.connect(self.save_and_close)
        bottom_btns.rejected.connect(self.reject)
        layout.addWidget(bottom_btns)

    def load_existing_images(self):
        """
            Load all images in the Dir and register them in the widget
        """
        self.thumb_list.clear()
        import glob
        pattern = os.path.join(self.img_dir, f"{self.store_key}_*.jpg")
        files = sorted(glob.glob(pattern))
        
        self.add_thumb_item(self.default_dir)
        for f in files:
            self.add_thumb_item(f)

    def add_thumb_item(self, file_path):
        """
            Add item to List
        """
        item = QListWidgetItem(QIcon(file_path), os.path.basename(file_path))
        item.setData(Qt.ItemDataRole.UserRole, file_path) # 실제 경로 저장
        self.thumb_list.addItem(item)

    def on_item_clicked(self, item):
        path = item.data(Qt.ItemDataRole.UserRole)
        self.selected_path = path
        self.main_img_label.set_image(QPixmap(path))

    ### --- Ctrl + V (Paste Image) ---
    def keyPressEvent(self, event):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_V:
            clipboard = QApplication.clipboard()
            mime_data = clipboard.mimeData()

            if mime_data.hasImage():
                image = clipboard.image()
                # 새 파일명 생성 (ID_타임스탬프.jpg)
                new_filename = f"{self.store_key}_{int(time.time())}.jpg"
                save_path = os.path.join(self.img_dir, new_filename)
                
                if image.save(save_path, "JPG"):
                    self.add_thumb_item(save_path)
                    self.thumb_list.setCurrentRow(self.thumb_list.count() - 1)
                    self.on_item_clicked(self.thumb_list.currentItem())
            return
        super().keyPressEvent(event)

    def import_from_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.xpm *.jpg)")
        if file_path:
            new_filename = f"{self.store_key}_{int(time.time())}.jpg"
            save_path = os.path.join(self.img_dir, new_filename)
            shutil.copy(file_path, save_path)
            self.add_thumb_item(save_path)

    def save_and_close(self):
        if not self.selected_path:
            return

        ### Save imagepath to custom JSON
        AppConfig.set_main_image(self.category ,self.data_key, self.selected_path)
        
        ### Updates all Images that used in Application
        self.image_updated.emit(self.category, self.data_key)
        self.accept()
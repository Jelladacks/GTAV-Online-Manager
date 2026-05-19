from PySide6.QtWidgets import QDialog, QFrame, QGridLayout, QHBoxLayout, QLabel, QScrollArea, QSizePolicy, QSpacerItem, QVBoxLayout, QWidget, QGraphicsDropShadowEffect
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QColor

from Codes.Service.ImageManager import ImageManager
from Codes.UI.lib.ImageFittingLabel import ImageFittingLabel

class PropertyCustomDialog(QDialog):
    """
        A new dialog displaying information about Customs when a PropertyCard is clicked.
        A Category and another PropertyCard(Custom) are going to be placed in the layout.
    """
    def __init__(self, property_data, slot_data, card_dict, parent=None):
        super().__init__(parent)
        self.property_data = property_data
        self.slot_data = slot_data
        self.card_dict = card_dict
        
        ### Created to blend naturally into the Main UI
        ### Frameless, Translucent
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.fixed_width = 100
        ### set Dialog size
        if parent:
            pgeo = parent.geometry()
            self.setGeometry(pgeo)
            self.fixed_width = ( min(pgeo.width(), pgeo.height()) * 9 // 10)

        self.pending_label = []
        
        self.init_ui()

    def init_ui(self):
        """
            Simple White Box in middle with Translucent background
        """
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # 반투명 검정 배경 패널 (Overlay)
        self.overlay_panel = QWidget()
        self.overlay_panel.setObjectName("Overlay")
        self.overlay_panel.setStyleSheet("background-color: rgba(0, 0, 0, 150);") # 투명도 150
        main_layout.addWidget(self.overlay_panel)

        # 중앙 상세 정보창 (Content)
        content_layout = QVBoxLayout(self.overlay_panel)
        
        self.content_widget = QWidget()
        self.content_widget.setFixedSize(self.fixed_width, self.fixed_width) # 상세창 크기 고정
        self.content_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 15px;
            }
        """)
        
        # 그림자 효과 (선택 사항)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(0, 0)
        self.content_widget.setGraphicsEffect(shadow)

        content_layout.addWidget(self.content_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        # 상세 내용 채우기 (이미지, 설명 등)
        self.setup_content_ui()

        ### close Dialog to click background
        self.overlay_panel.mousePressEvent = self.on_overlay_click

    def setup_content_ui(self):
        # 1. 메인 레이아웃 (상세창 전체를 관리)
        content_main_layout = QVBoxLayout(self.content_widget)
        content_main_layout.setContentsMargins(30, 30, 30, 30)
        content_main_layout.setSpacing(20)

        # 2. 상단 섹션 (이미지 + 텍스트 정보)
        top_layout = QHBoxLayout()
        
        # 2-1. 왼쪽 상단: 이미지
        self.detail_image = ImageFittingLabel()
        image_size = self.fixed_width // 3
        self.detail_image.setFixedSize(image_size, image_size)
        self.detail_image.setStyleSheet("background-color: #f0f0f0; border-radius: 10px;")
        self.detail_image.setScaledContents(True)
        self.detail_image.set_image(ImageManager.get_image('Property', self.property_data.get('id')))
        self.detail_image.apply_rounded_corners(10) 
        top_layout.addWidget(self.detail_image)

        # 2-2. 오른쪽 상단: 상세 정보 (Grid 레이아웃으로 정렬)
        info_layout = QGridLayout()
        info_layout.setContentsMargins(10, 0, 0, 0)
        info_layout.setVerticalSpacing(2)

        # 정보 텍스트들
        font_size = self.fixed_width * 4 // 250

        lbl_type = QLabel(f"Type: {self.property_data.get('type_name', 'N/A')}")
        lbl_name = QLabel(self.property_data.get('key_name', 'Property Name'))
        lbl_price = QLabel(f"Price: ${self.property_data.get('price', 0)}")

        lbl_type.setStyleSheet(f"font-size: {font_size}pt;")
        lbl_price.setStyleSheet(f"font-size: {font_size}pt;")
        lbl_price.setContentsMargins(0, 5, 0, 15)
        lbl_name.setStyleSheet(f"font-size: {font_size * 2}pt; font-weight: bold;")
        lbl_name.setWordWrap(True)

        car_slot_widget = self.create_icon_label("CarIcon", f" : {self.slot_data[0]}")
        air_slot_widget = self.create_icon_label("PlaneIcon", f" : {self.slot_data[1]}")
        bike_slot_widget = self.create_icon_label("BikeIcon", f" : {self.slot_data[2]}")
        ect_slot_widget = self.create_icon_label("EtcIcon", f" : {self.slot_data[3]}")

        info_layout.addWidget(lbl_type, 0, 0)
        info_layout.addWidget(lbl_name, 1, 0)
        info_layout.addWidget(lbl_price, 2, 0)

        info_layout.addWidget(car_slot_widget, 4, 0)
        info_layout.addWidget(air_slot_widget, 5, 0)
        info_layout.addWidget(bike_slot_widget, 6, 0)
        info_layout.addWidget(ect_slot_widget, 7, 0)

        # info_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding), 3, 0)

        top_layout.addLayout(info_layout)
        top_layout.setStretch(1, 1) # 정보 영역이 남은 공간을 다 쓰도록 설정
        
        content_main_layout.addLayout(top_layout)

        # 3. 구분선 (Separator)
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #e0e0e0;")
        content_main_layout.addWidget(line)

        # 4. 하단 섹션: Scroll Area (Custom 관련 위젯 배치)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet("""
                            /* 배경색 설정 */
                            QScrollArea {
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
                            
                        """)

        # 스크롤 영역 안에 들어갈 실제 위젯
        self.scroll_content = QWidget()
        self.scroll_content.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.custom_layout = QVBoxLayout(self.scroll_content)
        self.custom_layout.setContentsMargins(0, 0, 0, 0)
        self.custom_layout.setSpacing(5)
        
        # 예시: 여기에 Custom 위젯들을 추가하게 됩니다.
        for ctid, category in self.card_dict.items():
            self.custom_layout.addWidget(category, alignment=Qt.AlignmentFlag.AlignTop)
            
            for child in category.child_dict.values():
                custom_data = (child.property_data['key'], child.ui.lbl_image)
                self.pending_label.append(custom_data)
        
        # 스크롤 하단 빈 공간 채우기
        self.custom_layout.addStretch()

        self.scroll_area.setWidget(self.scroll_content)
        content_main_layout.addWidget(self.scroll_area)

        ### Sequential image loading for optimization
        QTimer.singleShot(100, self.load_images_sequentially)

    def create_icon_label(self, icon_name, text):
        """아이콘과 텍스트가 결합된 위젯 생성"""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8) # 아이콘과 글자 사이 간격

        # 1. 아이콘 레이블
        icon_label = QLabel()
        # ImageManager를 사용하거나 직접 QPixmap 로드
        icon_pixmap = ImageManager.get_image("UI", icon_name) 

        widget_size = self.fixed_width * 4 // 250
        
        if icon_pixmap and not icon_pixmap.isNull():
            # 아이콘 크기 조절 (예: 20x20)
            scaled_icon = icon_pixmap.scaled(widget_size * 2, widget_size * 2, 
                                            Qt.AspectRatioMode.KeepAspectRatio, 
                                            Qt.TransformationMode.SmoothTransformation)
            icon_label.setPixmap(scaled_icon)
        
        # 2. 텍스트 레이블
        text_label = QLabel(text)
        text_label.setStyleSheet(f"font-size: {widget_size}pt;") # 폰트 크기 조절

        layout.addWidget(icon_label)
        layout.addWidget(text_label)
        layout.addStretch() # 오른쪽 빈 공간 채우기

        return container

    def on_overlay_click(self, event):
        # 중앙 흰색 창 밖을 클릭하면 다이얼로그 닫기
        if not self.content_widget.geometry().contains(event.pos()):
            self.accept()

    def load_images_sequentially(self):
        """
            Sequential image loading for optimization
        """
        if not self.pending_label:
            return
        
        name, label = self.pending_label.pop(0)

        pixmap = ImageManager.get_image("PCustom", name)
        label.set_image(pixmap)

        QTimer.singleShot(5, self.load_images_sequentially)

    def showEvent(self, event):
        """
            Adjust size so that 3 PropertyCards fit in one row
        """
        super().showEvent(event)
        actual_width = self.scroll_area.viewport().width()
        for category in self.card_dict.values():
            category.adjust_content_mini(actual_width)
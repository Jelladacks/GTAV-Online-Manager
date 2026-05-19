from PySide6.QtWidgets import QAbstractItemView, QStyledItemDelegate, QStyleOptionViewItem, QStyle
from PySide6.QtGui import QLinearGradient, QPainter, QPainterPath, QPixmap, QIcon, QColor, QBrush, QPen, Qt
from PySide6.QtCore import QEvent, QRect, QSize

from Codes.Service.ImageManager import ImageManager

class CarCardDelegate(QStyledItemDelegate):
    """
        Draw Vehicle Card in Garage Viewer
    """
    def __init__(self, vehicle_map, parent=None):
        super().__init__(parent) # 부모 연결 필수
        self.HANDLE_WIDTH = 40 # Width of the grab handle area
        self.vehicle_map = vehicle_map

    def eventFilter(self, source, event):
        # viewport에서 발생한 이벤트인지 확인
        if event.type() == QEvent.Type.MouseButtonPress:
            # viewport의 부모인 QListView를 가져옴
            list_view = source.parent() 
            if not list_view:
                return super().eventFilter(source, event)

            pos = event.pos()
            index = list_view.indexAt(pos)

            if index.isValid():
                rect = list_view.visualRect(index)
                # 핸들 영역 계산 (왼쪽 40px 정도)
                handle_rect = QRect(rect.left(), rect.top(), self.HANDLE_WIDTH, rect.height())
                
                if handle_rect.contains(pos):
                    list_view.setDragEnabled(True)
                else:
                    list_view.setDragEnabled(False)

        return super().eventFilter(source, event)

    def paint(self, painter, option, index):
        # Base setup
        if not index.isValid():
            return
        
        car_data = index.data(Qt.ItemDataRole.UserRole) # 또는 모델에서 정의한 역할
        if car_data is None:
            return
        
        vehicle_id = car_data.get('vehicle_id', None)
        if vehicle_id is not None:
            vehicle_data = self.vehicle_map.get(vehicle_id, None)
        else:
            vehicle_data = {
                "name" : "Unknown",
                "manufacturer" : "Unknown",
                "class" : "Unknown",
                "price" : 0
            }
        
        is_hovered = option.state & QStyle.StateFlag.State_MouseOver
    
        try:
            """
            painter.save()
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

            rect = option.rect
            
            # Draw background and selection state
            if option.state & QStyle.StateFlag.State_Selected:
                painter.fillRect(rect, option.palette.highlight())
            elif option.state & QStyle.StateFlag.State_MouseOver:
                painter.fillRect(rect, QColor(245, 245, 245)) # Light gray hover
            else:
                painter.fillRect(rect, Qt.GlobalColor.white)
                
            # 드래그 중인 아이템인지 확인하는 가장 정확한 방법 (View의 상태 확인)
            is_dragging = False
            if option.widget:
                is_dragging = (option.state & QStyle.StateFlag.State_Selected) and \
                            (option.widget.state() == QAbstractItemView.State.DraggingState)
            # 1. Draw Grab Handle (the dotted pattern)
            # Check if the drag is currently active on this index
            if is_dragging:
                painter.setOpacity(0.5) # Semitransparent when dragged
            else:
                painter.setOpacity(1.0)
                
            handle_rect = rect.adjusted(0, 0, - (rect.width() - self.HANDLE_WIDTH), 0)
            
            # Use a built-in icon or custom image for handle
            handle_icon = QIcon.fromTheme("format-justify-fill") # or your own ⋮⋮ icon
            handle_pixmap = handle_icon.pixmap(30, 30)
            
            # Center pixmap in handle area
            icon_x = handle_rect.x() + (handle_rect.width() - handle_pixmap.width()) / 2
            icon_y = handle_rect.y() + (handle_rect.height() - handle_pixmap.height()) / 2
            painter.drawPixmap(int(icon_x), int(icon_y), handle_pixmap)

            # 2. Draw Content Area (image, text, color)
            content_rect = rect.adjusted(self.HANDLE_WIDTH, 0, 0, 0)
            # ... Custom painting from previous sessions (image fitting, text, color rectangle) ...
            # (Example) painter.drawText(content_rect, Qt.AlignLeft | Qt.AlignVCenter, index.data())
            
            painter.restore()
            """
            painter.save()
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            rect = option.rect
            
            # 1. 배경 그리기 (둥근 모서리 사각형)
            bg_rect = rect.adjusted(10, 10, -10, -10)
            path = QPainterPath()
            path.addRoundedRect(bg_rect, 10, 10)

            painter.fillPath(path, QColor("#ffffff")) # 기본 배경

            # 2. 테두리 (Shadow 효과 대신 얇은 선)
            painter.setPen(QPen(QColor("#dcdde1"), 1))
            painter.drawPath(path)

            # 3. 핸들 그리기 (왼쪽)
            painter.setPen(QPen(QColor("#a3a6af"), 1))
            handle_icon_rect = QRect(bg_rect.left() + 10, bg_rect.top(), 30, bg_rect.height())
            painter.setOpacity(1.0 if is_hovered else 0.3)
            # 간단한 점 6개(⋮⋮) 그리기
            for i in range(3):
                painter.drawEllipse(handle_icon_rect.center().x() - 3, handle_icon_rect.center().y() - 10 + (i * 8), 3, 3)
                painter.drawEllipse(handle_icon_rect.center().x() + 3, handle_icon_rect.center().y() - 10 + (i * 8), 3, 3)
            painter.setOpacity(1.0)

            # clip path
            handle_rect_full = QRect(bg_rect.left(), bg_rect.top(), self.HANDLE_WIDTH, bg_rect.height())
            
            clip_path = QPainterPath()
            clip_path.addRoundedRect(bg_rect, 10, 10)

            handle_path = QPainterPath()
            handle_path.addRect(handle_rect_full)

            final_clip_path = clip_path.subtracted(handle_path)
            # 4. 차량 이미지 그리기
            pixmap = ImageManager.get_image("Vehicle", f"{vehicle_data['id']}")

            if pixmap:


                pixmap_size = pixmap.size()
                label_size = QRect(
                                bg_rect.left() + self.HANDLE_WIDTH, # x
                                bg_rect.top(),                      # y
                                bg_rect.width() - self.HANDLE_WIDTH,# width (전체 너비에서 핸들 너비를 뺌)
                                bg_rect.height()                    # height (전체 높이 그대로)
                            )

                scale = max(label_size.width() / pixmap_size.width(), 
                            label_size.height() / pixmap_size.height())
                
                new_width = int(pixmap_size.width() * scale)
                new_height = int(pixmap_size.height() * scale)
                
                new_x = - (new_width // 5)
                new_y = (label_size.height() - new_height) // 2

                img_rect = QRect(label_size.left() + new_x, label_size.top() + new_y, new_width, new_height)

                painter.setClipPath(final_clip_path)
                
                # 이미지 그리기
                painter.drawPixmap(img_rect, pixmap.scaled(img_rect.size(), 
                                   Qt.AspectRatioMode.KeepAspectRatioByExpanding, 
                                   Qt.TransformationMode.SmoothTransformation))

                # 4. 그레디언트 (흰색 덮개) 농도 및 지점 조정
                # 이미지가 왼쪽으로 많이 왔으므로, 흰색이 더 빨리 시작되도록(0.3) 설정합니다.
                fade_gradient = QLinearGradient(bg_rect.topLeft(), bg_rect.topRight())
                fade_gradient.setColorAt(0.0, QColor(255, 255, 255, 100))   # 왼쪽 살짝 비침
                fade_gradient.setColorAt(0.3, QColor(255, 255, 255, 150))  # 30% 지점부터 급격히 흰색
                fade_gradient.setColorAt(0.75, QColor(255, 255, 255, 255))  # 60% 지점부턴 완전 흰색 (글자 영역 확보)
                fade_gradient.setColorAt(1.0, QColor(255, 255, 255, 255))
                
                painter.fillRect(bg_rect, fade_gradient) # img_rect 대신 bg_rect 전체를 덮는 게 깔끔합니다.
                painter.setClipping(False)

            title_font = painter.font()
            title_font.setBold(True)
            title_font.setPointSize(14)
            painter.setFont(title_font)
            
            text_rect = bg_rect.adjusted(self.HANDLE_WIDTH + 15, 15, -15, -15)
            painter.setPen(Qt.GlobalColor.black)
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop | Qt.TextFlag.TextWordWrap, vehicle_data.get('name', 'Unknown Car'))

            sub_font = painter.font()
            sub_font.setBold(False)
            sub_font.setPointSize(10)
            painter.setFont(sub_font)
            painter.setPen(Qt.GlobalColor.black)
            text_rect = bg_rect.adjusted(self.HANDLE_WIDTH + 20, 20, -20, -15)

            vprice = vehicle_data.get('price') or 0
            info_text = f"{vehicle_data.get('manufacturer', 'Unknown')}\n{vehicle_data.get('vehicle_class', 'Unknown')}\n${vprice:,}"
            painter.drawText(
                text_rect.adjusted(0, 30, 0, 0), 
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom, 
                info_text
            )

            if is_hovered:
                # 1. 아까 만든 final_clip_path를 그대로 사용하여 테두리 밖으로 안 나가게 설정
                painter.setClipPath(final_clip_path)
                
                # 2. 어두운 오버레이 레이어 (검정색 투명도 20~30%)
                overlay_color = QColor(0, 0, 0, 80) # 0~255 사이에서 투명도 조절
                painter.fillRect(bg_rect, overlay_color)
                
                # 3. 중앙에 "EDIT" 또는 "DRAG TO REORDER" 같은 텍스트나 아이콘 넣기
                # 폰트 설정
                hover_font = painter.font()
                hover_font.setPointSize(9)
                hover_font.setBold(True)
                painter.setFont(hover_font)
                painter.setPen(Qt.GlobalColor.white)
                
                # 텍스트 위치 (이미지 영역 중앙 근처)
                painter.drawText(bg_rect, Qt.AlignmentFlag.AlignCenter, "HOLD HANDLE TO DRAG\nDoubleClick To View")
                
            painter.restore()

        except Exception as e:
            print(f"그리기 에러: {e}")


    def sizeHint(self, option, index):
        # option.widget은 이 델리게이트를 사용하는 QListView입니다.
        if option.widget:
            view = option.widget
            # 1. 뷰포트의 실제 가용 너비를 가져옵니다.
            # contentsMargins를 빼서 실제 아이템이 그려질 영역만 계산합니다.
            margins = view.contentsMargins()
            available_width = view.viewport().width() - margins.left() - margins.right()
            
            # 2. Spacing이 설정되어 있다면 좌우 여백을 위해 2~4px 정도 더 여유를 줍니다.
            # (리스트뷰의 spacing은 아이템 '사이'의 간격이지만, 테두리 여백에도 영향을 줍니다.)
            final_width = available_width - (view.spacing() * 2)
            
            return QSize(final_width, 150)
        
        return QSize(200, 150)
    



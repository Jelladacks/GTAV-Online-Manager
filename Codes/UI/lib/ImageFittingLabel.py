from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPainter, QPainterPath, QPixmap, QRegion
from PySide6.QtCore import Qt

class ImageFittingLabel(QLabel):
    """
        Scale and Fit Image to label
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.original_pixmap = QPixmap()
        self.setScaledContents(False)

    def set_image(self, pixmap):
        """
            Must Use This 'Set_Image' Not 'setImage()'
        """
        if not pixmap or pixmap.isNull():
            self.original_pixmap = QPixmap()
        else:
            self.original_pixmap = pixmap
        self.update()

    def paintEvent(self, event):
        if not self.original_pixmap:
            return super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        pixmap_size = self.original_pixmap.size()
        label_size = self.contentsRect()

        """
            If the image size needs to be increased
            You should choose the one that increases more
            
            and if the image size needs to be decreased,
            You should choose the one that decreases less.
        """
        scale = max(label_size.width() / pixmap_size.width(), 
                    label_size.height() / pixmap_size.height())
        
        ### Scale it
        new_width = int(pixmap_size.width() * scale)
        new_height = int(pixmap_size.height() * scale)
        
        ### Center It
        x = (label_size.width() - new_width) // 2
        y = (label_size.height() - new_height) // 2

        painter.drawPixmap(x, y, new_width, new_height, self.original_pixmap)

    def apply_rounded_corners(self, radius):
        path = QPainterPath()
        path.addRoundedRect(self.rect(), radius, radius)
        self.setMask(QRegion(path.toFillPolygon().toPolygon()))
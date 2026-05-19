from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPainter, QPixmap
from PySide6.QtCore import Qt

class ImageMinLabel(QLabel):
    """
        Scale small into label so that Image looks like mini logo
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
        margin = 5

        """
            If the image size needs to be increased
            You should choose the one that increases less
            
            and if the image size needs to be decreased,
            You should choose the one that decreases more.
        """
        scale = min((label_size.width() - margin) / pixmap_size.width(), 
                    (label_size.height() - margin) / pixmap_size.height())
        
        ### Scale it
        new_width = int(pixmap_size.width() * scale)
        new_height = int(pixmap_size.height() * scale)
        
        ### Center It
        x = (label_size.width() - new_width) // 2
        y = (label_size.height() - new_height) // 2

        painter.drawPixmap(x, y, new_width, new_height, self.original_pixmap)
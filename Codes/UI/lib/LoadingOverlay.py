from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt

class LoadingOverlay(QWidget):
    """
        Notifies the user that it is loading and prevents input during the search.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False) # anti click
        
        ### translucent background settings
        self.setStyleSheet("background-color: rgba(0, 0, 0, 100);")
        
        layout = QVBoxLayout(self)
        self.label = QLabel("Loading...", self)
        self.label.setStyleSheet("color: white; font-weight: bold; font-size: 18px;")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

    def resizeEvent(self, event):
        """
            Adjust to fit parent window size
        """
        self.setFixedSize(self.parent().size())

    def showEvent(self, event):
        """
            Adjust to fit parent window size
        """
        self.setFixedSize(self.parent().size())
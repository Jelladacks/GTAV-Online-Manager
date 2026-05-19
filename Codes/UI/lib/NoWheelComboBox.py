from PySide6.QtWidgets import QComboBox

class NoWheelComboBox(QComboBox):
    """
        ComboBox has no wheel Event
    """
    def __init__(self, parent=None):
        super().__init__(parent)

    def wheelEvent(self, event):
        ### Ignore wheel Event
        event.ignore()
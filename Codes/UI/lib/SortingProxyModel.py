from PySide6.QtCore import Qt, QSortFilterProxyModel

class SortingProxyModel(QSortFilterProxyModel):
    """
        Proxy model for sorting by numeric instead of string
    """
    def __init__(self, parent=None):
        super().__init__(parent)

    def lessThan(self, left_index, right_index):
        ### get data EditRole
        left_data = self.sourceModel().data(left_index, Qt.EditRole)
        right_data = self.sourceModel().data(right_index, Qt.EditRole)

        ### Empty Value (WIP, 0, None) Check
        def is_empty(val):
            if val is None or val == "" or val == "WIP" or val == "None":
                return True
            try:
                return float(val) <= 0
            except (ValueError, TypeError):
                ### String value
                return False

        left_is_empty = is_empty(left_data)
        right_is_empty = is_empty(right_data)

        ### Stop sort if Both sides are empty
        if left_is_empty and right_is_empty:
            return False
        
        ### None object goes Bottom of List
        order = self.sortOrder()
        if left_is_empty:
            return order == Qt.DescendingOrder 
        if right_is_empty:
            return order == Qt.AscendingOrder

        ### Try numeric Sort
        try:
            return float(left_data) < float(right_data)
        except (ValueError, TypeError):
            ### String sort
            l_str = str(self.sourceModel().data(left_index, Qt.DisplayRole)).lower()
            r_str = str(self.sourceModel().data(right_index, Qt.DisplayRole)).lower()
            return l_str < r_str
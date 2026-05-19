from PySide6.QtCore import Qt, QAbstractListModel, QMimeData, QModelIndex, QByteArray, QDataStream, QIODevice, Signal

class GarageCarModel(QAbstractListModel):
    # Custom MIME type for dragged data within the app
    MIME_TYPE = "application/x-car-card-data"
    orderChanged = Signal()

    def __init__(self, cars=None, parent=None):
        super().__init__(parent)
        self.cars = cars or [] # List of car dictionaries/objects
        print("GarageCarModelSuccess")

    def rowCount(self, parent=QModelIndex()):
        return len(self.cars)

    def data(self, index, role):
        if not index.isValid():
            return None
        
        # row 범위 체크 필수
        if index.row() >= len(self.cars):
            return None

        if role == Qt.ItemDataRole.UserRole: # 델리게이트가 쓰는 Role과 일치하는지 확인
            return self.cars[index.row()]
        
        if role == Qt.ItemDataRole.DisplayRole:
            return f"Car {index.row()}"
        
            
        return None
    
    def add_car(self, car_dict):
        # 1. 삽입할 위치 지정 (맨 뒤에 추가할 경우)
        last_row = len(self.cars)
        
        # 2. Qt에게 데이터 삽입을 알림 (시작 위치, 끝 위치)
        self.beginInsertRows(QModelIndex(), last_row, last_row)
        
        # 3. 실제 파이썬 리스트에 데이터 추가
        self.cars.append(car_dict)
        
        # 4. 삽입 종료 알림 -> 이때 ListView가 알아서 새 카드를 그려줍니다.
        self.endInsertRows()

    def remove_car(self, row):
        if 0 <= row < len(self.cars):
            self.beginRemoveRows(QModelIndex(), row, row)
            del self.cars[row]
            self.endRemoveRows()

    def set_all_cars(self, new_car_list):
        # 모델의 데이터 전체가 바뀔 때 사용하는 신호
        self.beginResetModel()
        self.cars = new_car_list
        self.endResetModel()

    # Enable drag support
    def supportedDropActions(self):
        return Qt.DropAction.MoveAction

    def flags(self, index):
        default_flags = super().flags(index)
        if index.isValid():
            # Item is draggable, but can also accept drops
            return default_flags | Qt.ItemFlag.ItemIsDragEnabled | Qt.ItemFlag.ItemIsDropEnabled
        else:
            # View background is drop-enabled for append
            return default_flags | Qt.ItemFlag.ItemIsDropEnabled

    # MIME data handling for dragging
    def mimeTypes(self):
        return [self.MIME_TYPE]

    def mimeData(self, indexes):
        mime_data = QMimeData()
        encoded_data = QByteArray()
        stream = QDataStream(encoded_data, QIODevice.WriteOnly)
        
        for index in indexes:
            if index.isValid():
                # Store the row number being dragged
                stream.writeInt32(index.row())
        
        mime_data.setData(self.MIME_TYPE, encoded_data)
        return mime_data

    # Drop handling for dropping
    def dropMimeData(self, data, action, row, column, parent):
        if action == Qt.DropAction.IgnoreAction:
            return True
        if not data.hasFormat(self.MIME_TYPE) or column > 0:
            return False

        # Get the row numbers being dragged
        encoded_data = data.data(self.MIME_TYPE)
        stream = QDataStream(encoded_data, QIODevice.OpenModeFlag.ReadOnly)
        from_rows = []
        while not stream.atEnd():
            from_rows.append(stream.readInt32())

        # Determine target row
        if row != -1: # Dropped between items
            begin_row = row - 1
        elif parent.isValid(): # Dropped on an item
            begin_row = parent.row()
        else: # Dropped in empty area
            begin_row = self.rowCount()

        # Execute data moves
        for from_row in sorted(from_rows, reverse=True):
            if from_row != begin_row:
                self.moveRow(QModelIndex(), from_row, QModelIndex(), begin_row)
        
        result = super().dropMimeData(data, action, row, column, parent)
        if result:
            self.orderChanged.emit()
        return result

    # Explicit movement logic
    def moveRow(self, sourceParent, sourceRow, destinationParent, destinationChild):
        # Prevent invalid moves
        if sourceRow == destinationChild or sourceRow == destinationChild - 1:
            return False

        self.beginMoveRows(sourceParent, sourceRow, sourceRow, destinationParent, destinationChild)
        car = self.cars.pop(sourceRow)
        self.cars.insert(destinationChild, car)
        self.endMoveRows()
        return True
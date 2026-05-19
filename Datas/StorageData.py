from dataclasses import dataclass

@dataclass
class SlotType:
    id : int
    key_name : str #자전거, 오토바이, 지상이동수단, 공중이동수단, 특정차량한정, 전체범용(페가수스)

@dataclass
class PropertyTypeHasSlot:
    id : int
    propertytype_id : int
    slottype_id : int
    numberofslot : int

@dataclass
class StorageCompatibility:
    vehicle_class_id: int #오토바이는
    slottype_id: int      #바이커에만


@dataclass
class DedicatedStorage:
    id: int
    slottype_id: int          # 테러바이트에
    allowed_vehicle_id: int   # 오프레서2만 들어가는 슬롯 하나 있음
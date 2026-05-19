from dataclasses import dataclass

@dataclass
class VehicleClass:
    id : int
    key_name : str

@dataclass
class Manufacturer:
    id : int
    key_name : str

@dataclass
class Acquisition:
    id : int
    vehicle_id : int
    source_id : int

@dataclass
class AcquisitionSource:
    id : int
    key_name : str
    is_shop : bool

@dataclass
class Drivetrain:
    id : int
    key_name : str
    
@dataclass
class Vehicle:
    id : int
    key_name : str
    manufacturer_id : int
    class_id : int
    price : int
    seats : int
    drivetrain_id : int
    mass : int
    gears : int

    sizecm_x : int
    sizecm_y : int
    sizecm_z : int

    laptime_ms : int
    topspeed_10mtph : int

    graph_speed : int # 0~10000 -> 0.00~100.00
    graph_acc : int
    graph_brake : int
    graph_handle : int

    is_unique : bool #유니크면 알아서 차고 잘 찾아라잇
    is_pegasus : bool

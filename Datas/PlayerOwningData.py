from dataclasses import dataclass

@dataclass
class UserColorRef:
    id : int
    name : str
    gta_color_id : int | None
    default_rendermaterial_id : int 
#RenderMaterial (Classic 타입일 경우에만 Not Modded Pearl, Dial, Trim)
    chameleontype_id : int | None
    hex_color : str
    secondary_hex : str | None #Prism 중심색
    tertiary_hex : str | None #ThreeColor Only
    #이후에 Python에서 로드할 때 Color_ref 다 합칠 것.

@dataclass
class UserPaintPreset:
    id : int
    name : str
    is_hidden : bool
    primary_color_id : int
    primary_render_id : int
    secondary_color_id : int | None
    secondary_render_id : int | None
    pearlescent_id : int | None
    wheel_color_id : int | None
    dial_color_id : int | None
    trim_color_id : int | None
    neon_color_id : int | None
    headlight_color_id : int | None
    livery_color_id : int | None

@dataclass
class OwnedVehicle:
    id : int
    vehicle_id : int
    own_property_id : int
    slot_type_id : int
    slot_index : int
    paint_preset_id : int | None
    is_reward : bool 
    mod_custom : bool
    mod_upgrade : bool
    mod_imani : bool
    mod_hsw : bool
    mod_drift : bool
    limited_mod : bool
    limited_plate : bool
    limited_paint : bool
    limited_livery : bool
    is_sold : bool

@dataclass
class OwnedProperty:
    id : int
    property_id : int
    property_type_id : int
    memo : str | None
    is_active : bool 
    #unchecked 되었으나, 차량이 그곳에 보관되어 있을 경우 처리시 사용
    #이후 부동산 재 구매시 unchecked된거에서 property_id 바꾸면 될 듯


@dataclass
class OwnedPropertyCustom:
    id : int
    own_propery_id : int
    propertycustom_id : int
    propertycustom_type_id : int
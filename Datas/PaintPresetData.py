from dataclasses import dataclass

@dataclass
class GTAPaintPreset:
    id : int
    name : str
    category_render_id : int
    primary_color_id : int
    primary_render_id : int
    secondary_color_id : int | None
    secondary_render_id : int | None
    pearlescent_id : int | None

@dataclass
class RenderMaterial:
    id : int
    name : str #Classic Matte Metallic Metals Chrome Chameleon Worn Util Light

@dataclass
class ChameleonType:
    id : int
    name : str #TwoColor, ThreeColor, SoftPrism, HardPrism

@dataclass
class ColorRef:
    id : int
    name : str
    gta_color_id : int | None
    default_rendermaterial_id : int 
#RenderMaterial (Classic 타입일 경우에만 Not Modded Pearl, Dial, Trim)
    chameleontype_id : int | None
    hex_color : str
    secondary_hex : str | None #Prism 중심색
    tertiary_hex : str | None #ThreeColor Only



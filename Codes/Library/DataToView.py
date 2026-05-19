import numpy as np

from Codes.UI.lib.colorpicker import ColorPicker
from PySide6.QtWidgets import QDialog
import colorsys

def format_lap_time(ms: int) -> str:
    """
        transfer laptime milisecond to MM:SS:mmm string
    """
    if ms is None:
        return 'WIP'
    total_seconds = ms // 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    centiseconds = (ms % 1000) // 10
    return f"{minutes}:{seconds:02}.{centiseconds:02}"

def value_to_percentage(ms):
    """
        input / 100
    """
    if ms is None:
        return 'WIP'
    return ms / 100

def show_color_picker_dialog(parent, name, hex):
    """
        Open Color Picker Dialog, Returns (name, hex)
    """
    picker = ColorPicker(name, hex=hex, parent=parent)
    
    if picker.exec() == QDialog.DialogCode.Accepted:
        return picker.getResult()
    else:
        return None, None

def hex_to_hsl(hex_str):
    """
    Transfer RRGGBB to (H, S, L)   H,S,L(0~1)
    """
    hex_str = hex_str.lstrip('#')
    r, g, b = [int(hex_str[i:i+2], 16) / 255.0 for i in (0, 2, 4)]
    return colorsys.rgb_to_hls(r, g, b) # colorsys는 HLS 순서임

def hsl_to_str(h, l, s, a=1.0):
    """
    H, L, S를 CSS용 hsla 문자열로 변환
    """
    # CSS는 hsl(0~360, 0~100%, 0~100%) 형식을 사용함
    return f"hsla({int(h*360)}, {int(s*100)}%, {int(l*100)}%, {a})"

def blend_colors(hex1, hex2, ratio=0.5):
    """
    hex1 기반에 hex2를 ratio(0~1)만큼 섞음
    ratio 0.7 이면 hex2의 성분이 70%
    """
    hex1 = hex1.lstrip('#')
    hex2 = hex2.lstrip('#')
    
    # 1. 각각 RGB 추출
    r1, g1, b1 = [int(hex1[i:i+2], 16) for i in (0, 2, 4)]
    r2, g2, b2 = [int(hex2[i:i+2], 16) for i in (0, 2, 4)]
    
    # 2. 선형 보간 (Linear Interpolation) 계산
    # 공식: 시작값 + (끝값 - 시작값) * 비율
    r = int(r1 + (r2 - r1) * ratio)
    g = int(g1 + (g2 - g1) * ratio)
    b = int(b1 + (b2 - b1) * ratio)
    
    # 3. 다시 Hex로 변환
    return f"#{r:02x}{g:02x}{b:02x}"

def shade_color(hex):
    """
    hex1 기반에 hex2를 ratio(0~1)만큼 섞음
    ratio 0.7 이면 hex2의 성분이 70%
    """
    L = [0, 0.1,   0.2,   0.3,   0.4,   0.5,   0.6,   0.7,   0.8,   0.9,   1.0]
    V = [0, 0.231, 0.372, 0.580, 0.713, 0.780, 0.820, 0.847, 0.937, 0.945, 1.0]

    def apply_lut(val):
        # 0~255 값을 0~1로 정규화
        norm_val = val / 255.0
        # LUT 데이터를 바탕으로 사이 값을 계산 (보간)
        new_val = np.interp(norm_val, L, V)
        # 다시 0~255로 변환
        return int(round(new_val * 255))
    
    hex = hex.lstrip('#')
    
    r1, g1, b1 = [int(hex[i:i+2], 16) for i in (0, 2, 4)]
    
    r2 = apply_lut(r1) * 231 // 231 # 231 / 240
    g2 = apply_lut(g1) * 227 // 231 # 226 / 240
    b2 = apply_lut(b1) * 211 // 231 # 206 / 240

    r2, g2, b2 = [max(0, min(255, x)) for x in (r2, g2, b2)]

    return f"#{r2:02x}{g2:02x}{b2:02x}"

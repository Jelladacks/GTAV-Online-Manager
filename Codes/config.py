import json
import os
import sys

class AppConfig:
    if getattr(sys, 'frozen', False):
        BASE_DIR = os.path.dirname(sys.executable)
    else:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    IMAGE_DIR = os.path.join(BASE_DIR, "Datas", "images")
    CUSTOM_DIR = os.path.join(BASE_DIR, "Customs", "images")
    DEFAULT_THUMB = os.path.join(IMAGE_DIR, "no_image.png")

    CONFIG_FILE = os.path.join(BASE_DIR, "Customs", "user_config.json") 

    def get_main_image(category, data_key):
        """
            Returns full image Path from Category with Data_key\n
            Load User Custom image path from Custom/user_config.json\n
            ex) ("Vehicle", 0574 : id )\n
            ex) ("Garage", Tuple(3, 2, 3) : (own_property_id, slot_type_id, property_type_id) )\n
            ex) ("Manufacturer", Pegassi : key_name)\n
            ex) ("Property", 13 : id)\n
            ex) ("PCustom", EB_Interiors_Industrial : key)\n
            ex) ("Livery", Princess Robot Bubblegum : name)\n
            ex) ("ACQ", SSASA : key_name)\n
            ex) ("UI", NoImage : string)\n
        """
        section = ""
        search_key = ""
        if category == 'Vehicle':
            search_key = f"{int(data_key):04d}"
            section = "vehicle_main_images"
            CUSTOM_PATH = os.path.join(AppConfig.CUSTOM_DIR, "Vehicles")
            DEFAULT_PATH = os.path.join(AppConfig.IMAGE_DIR, "Vehicles", f"{search_key}.jpg")
            
        elif category == 'Garage' and isinstance(data_key, tuple):
            search_key = f"{data_key[0]}_{data_key[1]}"
            section = "garage_main_images"
            CUSTOM_PATH = os.path.join(AppConfig.CUSTOM_DIR, "Garages")
            DEFAULT_PATH = os.path.join(AppConfig.IMAGE_DIR, "Garages", f"{data_key[2]}_{data_key[1]}.webp")
            
        elif category == 'Manufacturer':
            search_key = f"{data_key}"
            return os.path.join(AppConfig.IMAGE_DIR, "Manufacturers", f"{search_key}.webp")
        elif category == 'Property':
            search_key = f"{data_key}"
            return os.path.join(AppConfig.IMAGE_DIR, "Properties", f"{search_key}.webp")
        elif category == 'PCustom':
            search_key = f"{data_key}"
            return os.path.join(AppConfig.IMAGE_DIR, "PCustoms", f"{search_key}.webp")
        elif category == 'Livery':
            search_key = f"{data_key}"
            return os.path.join(AppConfig.IMAGE_DIR, "Liveries", f"{search_key}.webp")
        elif category == 'ACQ':
            search_key = f"{data_key}"
            return os.path.join(AppConfig.IMAGE_DIR, "ACQs", f"{search_key}.webp")
        elif category == 'UI':
            search_key = f"{data_key}"
            return os.path.join(AppConfig.IMAGE_DIR, "UIs", f"{search_key}.PNG")
        else:
            return AppConfig.DEFAULT_THUMB
        
        if not os.path.exists(AppConfig.CONFIG_FILE):
            os.makedirs(os.path.dirname(AppConfig.CONFIG_FILE), exist_ok=True)
            with open(AppConfig.CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump({}, f, indent=4)
        
        with open(AppConfig.CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)

        file_name = config.get(section, {}).get(str(search_key))

        if file_name:
            full_path = os.path.join(CUSTOM_PATH, file_name)
            if os.path.exists(full_path):
                return os.path.abspath(full_path)
            
        if os.path.exists(DEFAULT_PATH):
            return DEFAULT_PATH
        
        return AppConfig.DEFAULT_THUMB

    def set_main_image(category, data_key, image_path):
        """
            Save User Custom Image Path at Custom/user_config.json\n
            ex) ("Vehicle", 0574 : id )\n
            ex) ("Garage", Tuple(3, 2, 3) : (own_property_id, slot_type_id, property_type_id) )\n
        """
        # 경로에서 파일명만 추출 (예: "C:/.../101_v1.jpg" -> "101_v1.jpg")
        file_name = os.path.basename(image_path)

        if category == 'Vehicle':
            store_key = f"{int(data_key):04d}"
            section = "vehicle_main_images"
        elif category == 'Garage' and isinstance(data_key, tuple):
            store_key = f"{data_key[0]}_{data_key[1]}"
            section = "garage_main_images"

        config = {}
        if os.path.exists(AppConfig.CONFIG_FILE):
            with open(AppConfig.CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
        
        config.setdefault(section, {})[str(store_key)] = file_name
        
        with open(AppConfig.CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
import sqlite3
import os
import sys

class DBLoader_GTA:
    if getattr(sys, 'frozen', False):
        BASE_DIR = os.path.dirname(sys.executable)
    else:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    db_file = os.path.join(BASE_DIR, "Datas", "Database", "db", "gtabase.db")

    ########################
    #
    #       VEHICLE
    #
    ########################
    def load_vehicle():
        # 1. DB 연결
        conn = sqlite3.connect(DBLoader_GTA.db_file)
        conn.row_factory = sqlite3.Row  # 이 설정을 하면 컬럼명으로 데이터 접근이 가능해져요!
        cursor = conn.cursor()

        # 2. 전체 차량 데이터 가져오기
        query = """
        SELECT 
            v.id,
            v.name AS name,
            t.translated_name AS translated_name,
            m.key_name AS manufacturer,
            m.translated_name AS manu_translated,
            vc.key_name AS vehicle_class,
            v.price,
            v.seats,
            d.key_name AS drivetrain,
            v.mass,
            v.gears,
            v.sizecm_x,
            v.sizecm_y,
            v.sizecm_z,
            v.laptime_ms,
            v.topspeed_10mtph,
            v.graph_speed,
            v.graph_acc,
            v.graph_brake,
            v.graph_handle,
            v.is_unique,
            v.is_pegasus
            
        FROM vehicle v
        LEFT JOIN manufacturer m ON v.manufacturer_id = m.id
        LEFT JOIN vehicle_class vc ON v.class_id = vc.id
        LEFT JOIN drivetrain d ON v.drivetrain_id = d.id
        LEFT JOIN vehicle_translated t ON v.id = t.id;
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        # 3. Python 리스트로 변환 (캐싱)
        # dict(row)를 통해 각 행을 딕셔너리 형태로 변환합니다.
        cached_vehicles = [dict(row) for row in rows]

        conn.close()
        return cached_vehicles

    def load_acquisition():
        # 1. DB 연결
        conn = sqlite3.connect(DBLoader_GTA.db_file)
        conn.row_factory = sqlite3.Row  # 이 설정을 하면 컬럼명으로 데이터 접근이 가능해져요!
        cursor = conn.cursor()

        # 2. 전체 데이터 가져오기
        query = """
        SELECT 
            a.id,
            a.vehicle_id,
            s.key_name AS source,
            s.is_shop
            
        FROM acquisition a
        LEFT JOIN acquisition_source s ON a.source_id = s.id;
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        # 3. Python 리스트로 변환 (캐싱)
        # dict(row)를 통해 각 행을 딕셔너리 형태로 변환합니다.
        cached_acquisition = [dict(row) for row in rows]

        conn.close()
        return cached_acquisition

    def load_vehicle_classes():
        # 1. DB 연결
        conn = sqlite3.connect(DBLoader_GTA.db_file)
        conn.row_factory = sqlite3.Row  # 이 설정을 하면 컬럼명으로 데이터 접근이 가능해져요!
        cursor = conn.cursor()

        # 2. 전체 데이터 가져오기
        query = """
        SELECT 
            *
        FROM vehicle_class;
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        # 3. Python 리스트로 변환 (캐싱)
        # dict(row)를 통해 각 행을 딕셔너리 형태로 변환합니다.
        cached_vehicle_class = [dict(row) for row in rows]

        conn.close()
        return cached_vehicle_class

    def load_manufacturer():
        # 1. DB 연결
        conn = sqlite3.connect(DBLoader_GTA.db_file)
        conn.row_factory = sqlite3.Row  # 이 설정을 하면 컬럼명으로 데이터 접근이 가능해져요!
        cursor = conn.cursor()

        # 2. 전체 데이터 가져오기
        query = """
        SELECT 
            *
        FROM manufacturer;
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        # 3. Python 리스트로 변환 (캐싱)
        # dict(row)를 통해 각 행을 딕셔너리 형태로 변환합니다.
        cached_manufacturer = [dict(row) for row in rows]

        conn.close()
        return cached_manufacturer

    def load_drivetrain():
        # 1. DB 연결
        conn = sqlite3.connect(DBLoader_GTA.db_file)
        conn.row_factory = sqlite3.Row  # 이 설정을 하면 컬럼명으로 데이터 접근이 가능해져요!
        cursor = conn.cursor()

        # 2. 전체 데이터 가져오기
        query = """
        SELECT 
            *
        FROM drivetrain;
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        # 3. Python 리스트로 변환 (캐싱)
        # dict(row)를 통해 각 행을 딕셔너리 형태로 변환합니다.
        cached_drivetrain = [dict(row) for row in rows]

        conn.close()
        return cached_drivetrain

    ########################
    #
    #       PROPERTY
    #
    ########################
    def load_property():
        # 1. DB 연결
        conn = sqlite3.connect(DBLoader_GTA.db_file)
        conn.row_factory = sqlite3.Row  # 이 설정을 하면 컬럼명으로 데이터 접근이 가능해져요!
        cursor = conn.cursor()

        # 2. 전체 데이터 가져오기
        query = """
        SELECT 
            *
        FROM property;
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        # 3. Python 리스트로 변환 (캐싱)
        # dict(row)를 통해 각 행을 딕셔너리 형태로 변환합니다.
        cached_property = [dict(row) for row in rows]

        conn.close()
        return cached_property

    def load_property_type():
        # 1. DB 연결
        conn = sqlite3.connect(DBLoader_GTA.db_file)
        conn.row_factory = sqlite3.Row  # 이 설정을 하면 컬럼명으로 데이터 접근이 가능해져요!
        cursor = conn.cursor()

        # 2. 전체 데이터 가져오기
        query = """
        SELECT 
            *
        FROM property_type;
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        # 3. Python 리스트로 변환 (캐싱)
        # dict(row)를 통해 각 행을 딕셔너리 형태로 변환합니다.
        cached_property_type = [dict(row) for row in rows]

        conn.close()
        return cached_property_type

    def load_property_custom_type():
        # 1. DB 연결
        conn = sqlite3.connect(DBLoader_GTA.db_file)
        conn.row_factory = sqlite3.Row  # 이 설정을 하면 컬럼명으로 데이터 접근이 가능해져요!
        cursor = conn.cursor()

        # 2. 전체 데이터 가져오기
        query = """
        SELECT 
            *
        FROM property_custom_type;
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        # 3. Python 리스트로 변환 (캐싱)
        # dict(row)를 통해 각 행을 딕셔너리 형태로 변환합니다.
        cached_property_custom_type = [dict(row) for row in rows]

        conn.close()
        return cached_property_custom_type

    def load_property_custom():
        # 1. DB 연결
        conn = sqlite3.connect(DBLoader_GTA.db_file)
        conn.row_factory = sqlite3.Row  # 이 설정을 하면 컬럼명으로 데이터 접근이 가능해져요!
        cursor = conn.cursor()

        # 2. 전체 데이터 가져오기
        query = """
        SELECT 
            *
        FROM property_custom;
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        # 3. Python 리스트로 변환 (캐싱)
        # dict(row)를 통해 각 행을 딕셔너리 형태로 변환합니다.
        cached_property_custom = [dict(row) for row in rows]

        conn.close()
        return cached_property_custom

    ########################
    #
    #       STORAGE RULE
    #
    ########################
    def load_slot_type():
        # 1. DB 연결
        conn = sqlite3.connect(DBLoader_GTA.db_file)
        conn.row_factory = sqlite3.Row  # 이 설정을 하면 컬럼명으로 데이터 접근이 가능해져요!
        cursor = conn.cursor()

        # 2. 전체 데이터 가져오기
        query = """
        SELECT 
            *
        FROM slot_type;
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        # 3. Python 리스트로 변환 (캐싱)
        # dict(row)를 통해 각 행을 딕셔너리 형태로 변환합니다.
        cached_slot_type = [dict(row) for row in rows]

        conn.close()
        return cached_slot_type

    def load_property_type_has_slot():
        # 1. DB 연결
        conn = sqlite3.connect(DBLoader_GTA.db_file)
        conn.row_factory = sqlite3.Row  # 이 설정을 하면 컬럼명으로 데이터 접근이 가능해져요!
        cursor = conn.cursor()

        # 2. 전체 데이터 가져오기
        query = """
        SELECT 
            *
        FROM property_type_has_slot;
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        # 3. Python 리스트로 변환 (캐싱)
        # dict(row)를 통해 각 행을 딕셔너리 형태로 변환합니다.
        cached_property_type_has_slot = [dict(row) for row in rows]

        conn.close()
        return cached_property_type_has_slot

    def load_storage_compatibility():
        # 1. DB 연결
        conn = sqlite3.connect(DBLoader_GTA.db_file)
        conn.row_factory = sqlite3.Row  # 이 설정을 하면 컬럼명으로 데이터 접근이 가능해져요!
        cursor = conn.cursor()

        # 2. 전체 데이터 가져오기
        query = """
        SELECT 
            sc.id,
            vc.key_name AS vehicle_class,
            sc.slottype_id
        FROM storage_compatibility sc
        LEFT JOIN vehicle_class vc ON sc.vehicle_class_id = vc.id;
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        # 3. Python 리스트로 변환 (캐싱)
        # dict(row)를 통해 각 행을 딕셔너리 형태로 변환합니다.
        cached_storage_compatibility = [dict(row) for row in rows]

        conn.close()
        return cached_storage_compatibility

    def load_dedicated_storage():
        # 1. DB 연결
        conn = sqlite3.connect(DBLoader_GTA.db_file)
        conn.row_factory = sqlite3.Row  # 이 설정을 하면 컬럼명으로 데이터 접근이 가능해져요!
        cursor = conn.cursor()

        # 2. 전체 데이터 가져오기
        query = """
        SELECT 
            *
        FROM dedicated_storage;
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        # 3. Python 리스트로 변환 (캐싱)
        # dict(row)를 통해 각 행을 딕셔너리 형태로 변환합니다.
        cached_dedicated_storage = [dict(row) for row in rows]

        conn.close()
        return cached_dedicated_storage

    ########################
    #
    #       PAINT
    #
    ########################
    def load_gta_paint_preset():
        # 1. DB 연결
        conn = sqlite3.connect(DBLoader_GTA.db_file)
        conn.row_factory = sqlite3.Row  # 이 설정을 하면 컬럼명으로 데이터 접근이 가능해져요!
        cursor = conn.cursor()

        # 2. 전체 데이터 가져오기
        query = """
        SELECT 
            *
        FROM gta_paint_preset;
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        # 3. Python 리스트로 변환 (캐싱)
        # dict(row)를 통해 각 행을 딕셔너리 형태로 변환합니다.
        cached_gta_paint_preset = [dict(row) for row in rows]

        conn.close()
        return cached_gta_paint_preset

    def load_render_material():
        # 1. DB 연결
        conn = sqlite3.connect(DBLoader_GTA.db_file)
        conn.row_factory = sqlite3.Row  # 이 설정을 하면 컬럼명으로 데이터 접근이 가능해져요!
        cursor = conn.cursor()

        # 2. 전체 데이터 가져오기
        query = """
        SELECT 
            *
        FROM render_material;
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        # 3. Python 리스트로 변환 (캐싱)
        # dict(row)를 통해 각 행을 딕셔너리 형태로 변환합니다.
        cached_render_material = [dict(row) for row in rows]

        conn.close()
        return cached_render_material

    def load_chameleon_type():
        # 1. DB 연결
        conn = sqlite3.connect(DBLoader_GTA.db_file)
        conn.row_factory = sqlite3.Row  # 이 설정을 하면 컬럼명으로 데이터 접근이 가능해져요!
        cursor = conn.cursor()

        # 2. 전체 데이터 가져오기
        query = """
        SELECT 
            *
        FROM chameleon_type;
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        # 3. Python 리스트로 변환 (캐싱)
        # dict(row)를 통해 각 행을 딕셔너리 형태로 변환합니다.
        cached_chameleon_type = [dict(row) for row in rows]

        conn.close()
        return cached_chameleon_type

    def load_color_ref():
        # 1. DB 연결
        conn = sqlite3.connect(DBLoader_GTA.db_file)
        conn.row_factory = sqlite3.Row  # 이 설정을 하면 컬럼명으로 데이터 접근이 가능해져요!
        cursor = conn.cursor()

        # 2. 전체 데이터 가져오기
        query = """
        SELECT 
            *
        FROM color_ref;
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        # 3. Python 리스트로 변환 (캐싱)
        # dict(row)를 통해 각 행을 딕셔너리 형태로 변환합니다.
        cached_color_ref = [dict(row) for row in rows]

        conn.close()
        return cached_color_ref

    def load_livery_type():
        # 1. DB 연결
        conn = sqlite3.connect(DBLoader_GTA.db_file)
        conn.row_factory = sqlite3.Row  # 이 설정을 하면 컬럼명으로 데이터 접근이 가능해져요!
        cursor = conn.cursor()

        # 2. 전체 데이터 가져오기
        query = """
        SELECT 
            *
        FROM livery_type;
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        # 3. Python 리스트로 변환 (캐싱)
        # dict(row)를 통해 각 행을 딕셔너리 형태로 변환합니다.
        cached_livery_type = [dict(row) for row in rows]

        conn.close()
        return cached_livery_type

    ########################
    #
    #       BUY RULE
    #
    ########################

    def load_bonus_target_type():
        # 1. DB 연결
        conn = sqlite3.connect(DBLoader_GTA.db_file)
        conn.row_factory = sqlite3.Row  # 이 설정을 하면 컬럼명으로 데이터 접근이 가능해져요!
        cursor = conn.cursor()

        # 2. 전체 데이터 가져오기
        query = """
        SELECT 
            *
        FROM bonus_target_type;
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        # 3. Python 리스트로 변환 (캐싱)
        # dict(row)를 통해 각 행을 딕셔너리 형태로 변환합니다.
        cached_bonus_target_type = [dict(row) for row in rows]

        conn.close()
        return cached_bonus_target_type

    def load_buybonus_rule():
        # 1. DB 연결
        conn = sqlite3.connect(DBLoader_GTA.db_file)
        conn.row_factory = sqlite3.Row  # 이 설정을 하면 컬럼명으로 데이터 접근이 가능해져요!
        cursor = conn.cursor()

        # 2. 전체 데이터 가져오기
        query = """
        SELECT 
            *
        FROM buybonus_rule;
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        # 3. Python 리스트로 변환 (캐싱)
        # dict(row)를 통해 각 행을 딕셔너리 형태로 변환합니다.
        cached_buybonus_rule = [dict(row) for row in rows]

        conn.close()
        return cached_buybonus_rule
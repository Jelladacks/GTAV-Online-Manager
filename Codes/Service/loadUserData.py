import sqlite3
import os
import sys

class DBLoader_USER:
    if getattr(sys, 'frozen', False):
        BASE_DIR = os.path.dirname(sys.executable)
    else:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    db_file = os.path.join(BASE_DIR, "Customs", "userbase.db")

    def load_user_color_ref():
        # 1. DB 연결
        conn = sqlite3.connect(DBLoader_USER.db_file)
        conn.row_factory = sqlite3.Row  # 이 설정을 하면 컬럼명으로 데이터 접근이 가능해져요!
        cursor = conn.cursor()

        # 2. 전체 데이터 가져오기
        query = """
        SELECT 
            *
        FROM user_color_ref;
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        # 3. Python 리스트로 변환 (캐싱)
        # dict(row)를 통해 각 행을 딕셔너리 형태로 변환합니다.
        cached_user_color_ref = [dict(row) for row in rows]

        conn.close()
        return cached_user_color_ref

    def load_user_paint_preset():
        # 1. DB 연결
        conn = sqlite3.connect(DBLoader_USER.db_file)
        conn.row_factory = sqlite3.Row  # 이 설정을 하면 컬럼명으로 데이터 접근이 가능해져요!
        cursor = conn.cursor()

        # 2. 전체 데이터 가져오기
        query = """
        SELECT 
            *
        FROM user_paint_preset;
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        # 3. Python 리스트로 변환 (캐싱)
        # dict(row)를 통해 각 행을 딕셔너리 형태로 변환합니다.
        cached_user_paint_preset = [dict(row) for row in rows]

        conn.close()
        return cached_user_paint_preset

    def load_owned_vehicle():
        # 1. DB 연결
        conn = sqlite3.connect(DBLoader_USER.db_file)
        conn.row_factory = sqlite3.Row  # 이 설정을 하면 컬럼명으로 데이터 접근이 가능해져요!
        cursor = conn.cursor()

        # 2. 전체 데이터 가져오기
        query = """
        SELECT 
            *
        FROM owned_vehicle;
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        # 3. Python 리스트로 변환 (캐싱)
        # dict(row)를 통해 각 행을 딕셔너리 형태로 변환합니다.
        cached_owned_vehicle = [dict(row) for row in rows]

        conn.close()
        return cached_owned_vehicle

    def load_owned_property():
        # 1. DB 연결
        conn = sqlite3.connect(DBLoader_USER.db_file)
        conn.row_factory = sqlite3.Row  # 이 설정을 하면 컬럼명으로 데이터 접근이 가능해져요!
        cursor = conn.cursor()

        # 2. 전체 데이터 가져오기
        query = """
        SELECT 
            *
        FROM owned_property;
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        # 3. Python 리스트로 변환 (캐싱)
        # dict(row)를 통해 각 행을 딕셔너리 형태로 변환합니다.
        cached_owned_property = [dict(row) for row in rows]

        conn.close()
        return cached_owned_property

    def load_owned_property_custom():
        # 1. DB 연결
        conn = sqlite3.connect(DBLoader_USER.db_file)
        conn.row_factory = sqlite3.Row  # 이 설정을 하면 컬럼명으로 데이터 접근이 가능해져요!
        cursor = conn.cursor()

        # 2. 전체 데이터 가져오기
        query = """
        SELECT 
            *
        FROM owned_property_custom;
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        # 3. Python 리스트로 변환 (캐싱)
        # dict(row)를 통해 각 행을 딕셔너리 형태로 변환합니다.
        cached_owned_property_custom = [dict(row) for row in rows]

        conn.close()
        return cached_owned_property_custom

    def insert_user_vehicle(vehicle_id, owned_property_id, slot_type_id, slot_index,
                            paint_preset_id=None, is_reward=False, 
                            mod_custom=False, mod_upgrade=False, 
                            mod_imani=False, mod_hsw=False, mod_drift=False,
                            limited_mod=False, limited_plate=False, 
                            limited_paint=False, limited_livery=False, is_sold=False):
        # 1. DB 연결
        conn = sqlite3.connect(DBLoader_USER.db_file)
        conn.row_factory = sqlite3.Row  # 이 설정을 하면 컬럼명으로 데이터 접근이 가능해져요!
        cursor = conn.cursor()

        # 컬럼 개수만큼 물음표(16개)를 맞춰줘야 합니다.
        placeholders = ", ".join(["?"] * 16)
        sql = f"""
            INSERT INTO owned_vehicle 
            (vehicle_id, owned_property_id, slot_type_id, slot_index, paint_preset_id,
            is_reward, mod_custom, mod_upgrade, mod_imani, mod_hsw, mod_drift,
            limited_mod, limited_plate, limited_paint, limited_livery, is_sold)
            VALUES ({placeholders})
        """

        # 2. 저장
        cursor.execute(sql, (vehicle_id, owned_property_id, slot_type_id, slot_index, paint_preset_id,
                is_reward, mod_custom, mod_upgrade, mod_imani, mod_hsw, mod_drift,
                limited_mod, limited_plate, limited_paint, limited_livery, is_sold))
        
        new_id = cursor.lastrowid

        conn.commit()
        conn.close()

        return new_id

    def update_user_vehicle(own_id, **kwargs):
        """
        vehicle_instance_id: 수정할 레코드의 PK (id)
        **kwargs: 수정하고 싶은 컬럼명과 값을 키워드 인자로 전달
        예: update_user_vehicle(1, is_sold=1, paint_preset_id=5)
        """
        if (kwargs.get('owned_property_id', None) is not None) and (kwargs.get('owned_property_id', None) == 0):
            return
        if (kwargs.get('slot_type_id', None) is not None) and (kwargs.get('slot_type_id', None) == 0):
            return

        conn = sqlite3.connect(DBLoader_USER.db_file)
        cursor = conn.cursor()

        # 입력된 항목들로 SET 절 생성 (예: "is_sold = ?, paint_preset_id = ?")
        columns = ", ".join([f"{key} = ?" for key in kwargs.keys()])
        values = list(kwargs.values())
        values.append(own_id)

        sql = f"UPDATE owned_vehicle SET {columns} WHERE id = ?"

        cursor.execute(sql, values)
        
        conn.commit()
        conn.close()

    def delete_user_vehicle(own_id):
        """
        특정 ID의 차량 데이터를 삭제합니다.
        """
        conn = sqlite3.connect(DBLoader_USER.db_file)
        cursor = conn.cursor()

        # 안전을 위해 WHERE 절 없이 실행되지 않도록 주의하세요!
        cursor.execute("DELETE FROM owned_vehicle WHERE id = ?", (own_id,))

        conn.commit()
        conn.close()
        print(f"ID {own_id} 차량 데이터가 삭제되었습니다.")

    def insert_user_property(property_id, property_type_id, memo, is_active):
        # 1. DB 연결
        conn = sqlite3.connect(DBLoader_USER.db_file)
        conn.row_factory = sqlite3.Row  # 이 설정을 하면 컬럼명으로 데이터 접근이 가능해져요!
        cursor = conn.cursor()

        # 컬럼 개수만큼 물음표(16개)를 맞춰줘야 합니다.
        placeholders = ", ".join(["?"] * 4)
        sql = f"""
            INSERT INTO owned_property 
            (property_id, property_type_id, memo, is_active)
            VALUES ({placeholders})
        """

        # 2. 저장
        cursor.execute(sql, (property_id, property_type_id, memo, is_active))
        
        new_id = cursor.lastrowid

        conn.commit()
        conn.close()

        return new_id

    def update_user_property(own_id, **kwargs):
        conn = sqlite3.connect(DBLoader_USER.db_file)
        cursor = conn.cursor()

        # 입력된 항목들로 SET 절 생성 (예: "is_sold = ?, paint_preset_id = ?")
        columns = ", ".join([f"{key} = ?" for key in kwargs.keys()])
        values = list(kwargs.values())
        values.append(own_id)

        sql = f"UPDATE owned_property SET {columns} WHERE id = ?"

        cursor.execute(sql, values)
        
        conn.commit()
        conn.close()

    def delete_user_property(own_id):
        conn = sqlite3.connect(DBLoader_USER.db_file)
        cursor = conn.cursor()

        # 안전을 위해 WHERE 절 없이 실행되지 않도록 주의하세요!
        cursor.execute("DELETE FROM owned_property WHERE id = ?", (own_id,))

        conn.commit()
        conn.close()
        print(f"ID {own_id} 데이터가 삭제되었습니다.")

    def insert_user_property_custom(owned_property_id, propertycustom_id, propertycustom_type_id):
        # 1. DB 연결
        conn = sqlite3.connect(DBLoader_USER.db_file)
        conn.row_factory = sqlite3.Row  # 이 설정을 하면 컬럼명으로 데이터 접근이 가능해져요!
        cursor = conn.cursor()

        # 컬럼 개수만큼 물음표(16개)를 맞춰줘야 합니다.
        placeholders = ", ".join(["?"] * 3)
        sql = f"""
            INSERT INTO owned_property_custom 
            (owned_property_id, propertycustom_id, propertycustom_type_id)
            VALUES ({placeholders})
        """

        # 2. 저장
        cursor.execute(sql, (owned_property_id, propertycustom_id, propertycustom_type_id))
        
        new_id = cursor.lastrowid

        conn.commit()
        conn.close()

        return new_id

    def update_user_property_custom(own_pcustom_id, **kwargs):
        conn = sqlite3.connect(DBLoader_USER.db_file)
        cursor = conn.cursor()

        # 입력된 항목들로 SET 절 생성 (예: "is_sold = ?, paint_preset_id = ?")
        columns = ", ".join([f"{key} = ?" for key in kwargs.keys()])
        values = list(kwargs.values())
        values.append(own_pcustom_id)

        sql = f"UPDATE owned_property_custom SET {columns} WHERE id = ?"

        cursor.execute(sql, values)
        
        conn.commit()
        conn.close()

    def delete_user_property_custom(own_pcustom_id):
        conn = sqlite3.connect(DBLoader_USER.db_file)
        cursor = conn.cursor()

        # 안전을 위해 WHERE 절 없이 실행되지 않도록 주의하세요!
        cursor.execute("DELETE FROM owned_property_custom WHERE id = ?", (own_pcustom_id,))

        conn.commit()
        conn.close()
        print(f"ID {own_pcustom_id} 데이터가 삭제되었습니다.")

    def insert_user_color_ref(name, default_rendermaterial_id, hex_color):
        # 1. DB 연결
        conn = sqlite3.connect(DBLoader_USER.db_file)
        conn.row_factory = sqlite3.Row  # 이 설정을 하면 컬럼명으로 데이터 접근이 가능해져요!
        cursor = conn.cursor()

        # 컬럼 개수만큼 물음표(16개)를 맞춰줘야 합니다.
        placeholders = ", ".join(["?"] * 3)
        sql = f"""
            INSERT INTO user_color_ref 
            (name, default_rendermaterial_id, hex_color)
            VALUES ({placeholders})
        """

        # 2. 저장
        cursor.execute(sql, (name, default_rendermaterial_id, hex_color))
        
        new_id = cursor.lastrowid

        conn.commit()
        conn.close()

        return new_id

    def update_user_color_ref(color_ref_id, **kwargs):
        conn = sqlite3.connect(DBLoader_USER.db_file)
        cursor = conn.cursor()

        # 입력된 항목들로 SET 절 생성 (예: "is_sold = ?, paint_preset_id = ?")
        columns = ", ".join([f"{key} = ?" for key in kwargs.keys()])
        values = list(kwargs.values())
        values.append(color_ref_id)

        sql = f"UPDATE user_color_ref SET {columns} WHERE id = ?"

        cursor.execute(sql, values)
        
        conn.commit()
        conn.close()

    def delete_user_color_ref(color_ref_id):
        conn = sqlite3.connect(DBLoader_USER.db_file)
        cursor = conn.cursor()

        # 안전을 위해 WHERE 절 없이 실행되지 않도록 주의하세요!
        cursor.execute("DELETE FROM user_color_ref WHERE id = ?", (color_ref_id,))

        conn.commit()
        conn.close()
        print(f"ID {color_ref_id} 데이터가 삭제되었습니다.")

    def insert_user_paint_preset(name, is_hidden, primary_color_id, primary_render_id,
                                secondary_color_id=None, secondary_render_id=None,
                                pearl_color_id=None, wheel_color_id=None,
                                dial_color_id=None, trim_color_id=None,
                                neon_color_id=None, headlight_color_id=None,
                                livery_type_id=None):
        # 1. DB 연결
        conn = sqlite3.connect(DBLoader_USER.db_file)
        conn.row_factory = sqlite3.Row  # 이 설정을 하면 컬럼명으로 데이터 접근이 가능해져요!
        cursor = conn.cursor()

        # 컬럼 개수만큼 물음표(16개)를 맞춰줘야 합니다.
        placeholders = ", ".join(["?"] * 13)
        sql = f"""
            INSERT INTO user_paint_preset 
            (name, is_hidden, primary_color_id, primary_render_id, 
            secondary_color_id, secondary_render_id, pearl_color_id, wheel_color_id, 
            dial_color_id, trim_color_id, neon_color_id, headlight_color_id, livery_type_id)
            VALUES ({placeholders})
        """

        # 2. 저장
        params = (name, is_hidden, primary_color_id, primary_render_id, 
                secondary_color_id, secondary_render_id, pearl_color_id, wheel_color_id, 
                dial_color_id, trim_color_id, neon_color_id, headlight_color_id, livery_type_id)

        cursor.execute(sql, params)
        
        new_id = cursor.lastrowid

        conn.commit()
        conn.close()

        return new_id

    def update_user_paint_preset(preset_id, **kwargs):
        conn = sqlite3.connect(DBLoader_USER.db_file)
        cursor = conn.cursor()

        # 입력된 항목들로 SET 절 생성 (예: "is_sold = ?, paint_preset_id = ?")
        columns = ", ".join([f"{key} = ?" for key in kwargs.keys()])
        values = list(kwargs.values())
        values.append(preset_id)

        sql = f"UPDATE user_paint_preset SET {columns} WHERE id = ?"

        cursor.execute(sql, values)
        
        conn.commit()
        conn.close()

    def delete_user_paint_preset(preset_id):
        conn = sqlite3.connect(DBLoader_USER.db_file)
        cursor = conn.cursor()

        # 안전을 위해 WHERE 절 없이 실행되지 않도록 주의하세요!
        cursor.execute("DELETE FROM user_paint_preset WHERE id = ?", (preset_id,))

        conn.commit()
        conn.close()
        print(f"ID {preset_id} 데이터가 삭제되었습니다.")
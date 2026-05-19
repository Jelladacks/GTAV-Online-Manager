import os
import sqlite3
import sys
import pandas as pd

class SmartSeeder:
    """
        Data/CSV to DB Manager
    """
    if getattr(sys, 'frozen', False):
        BASE_DIR = os.path.dirname(sys.executable)
    else:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    SEED_DIR = os.path.join(BASE_DIR, "Datas", "Database", "seed")
    SQL_DIR = os.path.join(BASE_DIR, "Datas", "Database", "sql")

    def __init__(self, db_conn, seeder_info):
        self.db_conn = db_conn
        self.cursor = self.db_conn.cursor()
        self.seeder_info = seeder_info

    def execute_sql_file(self, sql_file_path):
        """
            Reads an SQL file to create a table
        """
        if os.path.exists(sql_file_path):
            with open(sql_file_path, 'r', encoding='utf-8') as f:
                sql_script = f.read()

            self.cursor.executescript(sql_script)
            self.db_conn.commit()
            print(f"📜 SQL Script done: {sql_file_path}")
        else:
            print(f"⚠️ Cannot Find SQL: {sql_file_path}")

    def check_if_update_needed(self, csv_file):
        """
            Check CSV file with the DB to see if it has been modified
        """
        csv_path = os.path.join(self.SEED_DIR, csv_file)
        if not os.path.exists(csv_path):
            return False
            
        ### file Moditied time
        current_mtime = os.path.getmtime(csv_path)
        
        ### get DB Modified time
        self.cursor.execute("SELECT last_modified FROM _seeding_meta WHERE file_name = ?", (csv_file,))
        result = self.cursor.fetchone()
        
        ### If the file has been modified, return True
        if result is None or current_mtime > result[0]:
            return True
        return False
    
    def get_row_count(self, csv_file):
        """
            get_row_count but Deprecated
        """
        csv_path = os.path.join(self.SEED_DIR, csv_file)
        if not os.path.exists(csv_path):
            return False
        
        self.cursor.execute("SELECT row_count FROM _seeding_meta WHERE file_name = ?", (csv_file,))
        result = self.cursor.fetchone()

        return result


    def update_meta(self, csv_file, row_count):
        """
            Update file information in the DB after seeding is complete
        """
        csv_path = os.path.join(self.SEED_DIR, csv_file)
        current_mtime = os.path.getmtime(csv_path)

        self.cursor.execute("""
            INSERT OR REPLACE INTO _seeding_meta (file_name, last_modified, row_count)
            VALUES (?, ?, ?)
        """, (csv_file, current_mtime, row_count))
        self.db_conn.commit()

    def run_all(self, force=False):
        """
        Receives a dictionary of the form ==
        seeder_info = { 'schema.sql': ['file1.csv', 'file2.csv'] }\n
        and processes it sequentially.
        """
        for sql_file, csv_files in self.seeder_info.items():
            print(f"\n--- 🏗️ Working with schema: {sql_file} ---")
            
            sql_path = os.path.join(self.SQL_DIR, sql_file)
            # 1. 해당 스키마 실행 (테이블 생성 등)
            self.execute_sql_file(sql_path)

            # 2. 연결된 CSV 파일들 처리
            for csv_file in csv_files:
                if force or self.check_if_update_needed(csv_file):
                    print(f"🔄 Seeding: {csv_file}")
                    
                    # CSV 파일마다 데이터 구조가 다를 수 있으므로 
                    # 파일명에 따른 분기 처리가 필요할 수 있습니다.
                    self.insert_by_filename(csv_file) 
                    
                else:
                    print(f"✅ Skipped (Latest): {csv_file}")

    def insert_by_filename(self, csv_file):
        """
            Uses the csv_file name
            to determine the appropriate DB insertion method
        """
        csv_path = os.path.join(self.SEED_DIR, csv_file)
        if not os.path.exists(csv_path):
            return False
        
        success_count = 0
        df = pd.read_csv(csv_path)
        df = df.where(pd.notnull(df), None)

        if csv_file == 'GTAVOColorRefTable.csv':
            self.cursor.execute("DELETE FROM color_ref")
            for _, row in df.iterrows():
                sql = """INSERT INTO color_ref 
                        (id, name, gta_color_id, 
                        default_rendermaterial_id, chameleontype_id, 
                        hex_color, secondary_hex, tertiary_hex) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """
                self.cursor.execute(sql, (row['ID'], row['Name'], row['GTA_Color_ID']
                                          , row['rendermaterial_id'], row['chameleontype_id']
                                          , row['Hex'], row['Hex secondary'], row['Hex tertiary']))
                success_count += 1

        elif csv_file == 'GTAVODefaultPaintDataTable.csv':
            self.cursor.execute("DELETE FROM gta_paint_preset")
            for _, row in df.iterrows():
                sql = """INSERT INTO gta_paint_preset 
                        (id, name, category_render_id, 
                        primary_color_id, primary_render_id, 
                        secondary_color_id, secondary_render_id, pearl_color_id) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """
                self.cursor.execute(sql, (row['ID'], row['Name'], row['Category']
                                          , row['primary_color_id'], row['primary_render_id']
                                          , row['secondary_color_id'], row['secondary_render_id']
                                          , row['pearl_color_id']))
                success_count += 1

        elif csv_file == 'GTAVORenderMaterial.csv':
            self.cursor.execute("DELETE FROM render_material")
            for _, row in df.iterrows():
                sql = "INSERT INTO render_material (id, name) VALUES (?, ?)"
                self.cursor.execute(sql, (row['ID'], row['Name']))
                success_count += 1

        elif csv_file == 'GTAVOChameleonType.csv':
            self.cursor.execute("DELETE FROM chameleon_type")
            for _, row in df.iterrows():
                sql = "INSERT INTO chameleon_type (id, name) VALUES (?, ?)"
                self.cursor.execute(sql, (row['ID'], row['Name']))
                success_count += 1

        elif csv_file == 'GTAVOLiveryType.csv':
            self.cursor.execute("DELETE FROM livery_type")
            for _, row in df.iterrows():
                sql = "INSERT INTO livery_type (id, name) VALUES (?, ?)"
                self.cursor.execute(sql, (row['ID'], row['Name']))
                success_count += 1

        elif csv_file == 'GTAVOManufacturerDataTable.csv':
            self.cursor.execute("DELETE FROM manufacturer")
            for _, row in df.iterrows():
                sql = "INSERT INTO manufacturer (id, key_name, translated_name) VALUES (?, ?, ?)"
                self.cursor.execute(sql, (row['ID'], row['Name'], row['KorName']))
                success_count += 1

        elif csv_file == 'GTAVOVehicleClassTable.csv':
            self.cursor.execute("DELETE FROM vehicle_class")
            for _, row in df.iterrows():
                sql = "INSERT INTO vehicle_class (id, key_name) VALUES (?, ?)"
                self.cursor.execute(sql, (row['ID'], row['Name']))
                success_count += 1

        elif csv_file == 'GTAVOVehicleDrivetrain.csv':
            self.cursor.execute("DELETE FROM drivetrain")
            for _, row in df.iterrows():
                sql = "INSERT INTO drivetrain (id, key_name) VALUES (?, ?)"
                self.cursor.execute(sql, (row['ID'], row['Name']))
                success_count += 1

        elif csv_file == 'GTAVOAcquisitionDataTable.csv':
            self.cursor.execute("DELETE FROM acquisition")
            for _, row in df.iterrows():
                placeholders = ", ".join(["?"] * 3)
                sql = f"""
                    INSERT INTO acquisition 
                    (id, vehicle_id, source_id)
                    VALUES ({placeholders})
                """
                self.cursor.execute(sql, (row['ID'], row['VehicleID'], row['SourceID']))
                success_count += 1

        elif csv_file == 'GTAVOAcquisitionSource.csv':
            self.cursor.execute("DELETE FROM acquisition_source")
            for _, row in df.iterrows():
                placeholders = ", ".join(["?"] * 3)
                sql = f"""
                    INSERT INTO acquisition_source 
                    (id, key_name, is_shop)
                    VALUES ({placeholders})
                """
                self.cursor.execute(sql, (row['ID'], row['Name'], row['is_shop']))
                success_count += 1

        elif csv_file == 'GTAVOVehicleDataTable.csv':
            self.cursor.execute("DELETE FROM vehicle")
            for _, row in df.iterrows():
                placeholders = ", ".join(["?"] * 20)
                sql = f"""
                    INSERT INTO vehicle 
                    (id, name,
                    manufacturer_id, class_id, price,
                    seats, drivetrain_id, mass, gears,
                    sizecm_x, sizecm_y, sizecm_z,
                    laptime_ms, topspeed_10mtph,
                    graph_speed, graph_acc, graph_brake, graph_handle, 
                    is_unique, is_pegasus)
                    VALUES ({placeholders})
                """
                self.cursor.execute(sql, (row['carExIdx'], row['Model'],
                                           row['ManuID'], row['ClassID'], row['Prices']
                                           , row['Seats'], row['DriveID'], row['Weight'], row['Gears']
                                           , row['length'], row['width'], row['height']
                                           , row['LapTime'], row['Top Speed']
                                           , row['Speed'], row['Acceleration'], row['Braking'], row['Handling']
                                           , row['is_unique'], row['is_pegasus']))
                success_count += 1
        
        elif csv_file == 'GTAVOVehicleTranslation.csv':
            self.cursor.execute("DELETE FROM vehicle_translated")
            for _, row in df.iterrows():
                placeholders = ", ".join(["?"] * 3)
                sql = f"""
                    INSERT INTO vehicle_translated 
                    (id, english_name, translated_name)
                    VALUES ({placeholders})
                """
                self.cursor.execute(sql, (row['carExIdx'], row['EngName'], row['KorName']))
                success_count += 1

        elif csv_file == 'GTAVOPropertyCustomTypeTable.csv':
            self.cursor.execute("DELETE FROM property_custom_type")
            for _, row in df.iterrows():
                placeholders = ", ".join(["?"] * 6)
                sql = f"""
                    INSERT INTO property_custom_type 
                    (id, key,
                    name, propertytype_id, is_unchangeable, max_owned)
                    VALUES ({placeholders})
                """
                self.cursor.execute(sql, (row['ID'], row['Key'],
                                           row['Name'], row['Property Type ID'], row['Is Unchangeable'], row['Max Owned']))
                success_count += 1

        elif csv_file == 'GTAVOPropertyTypeTable.csv':
            self.cursor.execute("DELETE FROM property_type")
            for _, row in df.iterrows():
                placeholders = ", ".join(["?"] * 7)
                sql = f"""
                    INSERT INTO property_type 
                    (id, key_name, max_owned,
                    is_abstract, is_hidden, parent_id, is_unchangeable)
                    VALUES ({placeholders})
                """
                self.cursor.execute(sql, (row['ID'], row['Name'], row['MaxOwned'],
                                           row['Abstract'], row['Hidden'], row['Parent_ID'], row['Unchangeable']))
                success_count += 1

        elif csv_file == 'GTAVOPropertyDataTable.csv':
            self.cursor.execute("DELETE FROM property")
            for _, row in df.iterrows():
                placeholders = ", ".join(["?"] * 4)
                sql = f"""
                    INSERT INTO property 
                    (id, key_name,
                    type_id, price)
                    VALUES ({placeholders})
                """
                self.cursor.execute(sql, (row['ID'], row['Name'],
                                           row['Type_ID'], row['Price']))
                success_count += 1

        elif csv_file == 'GTAVOPropertyCustomTable.csv':
            self.cursor.execute("DELETE FROM property_custom")
            for _, row in df.iterrows():
                placeholders = ", ".join(["?"] * 5)
                sql = f"""
                    INSERT INTO property_custom 
                    (id, key, name, 
                    customtype_id, price)
                    VALUES ({placeholders})
                """
                self.cursor.execute(sql, (row['ID'], row['Key'], row['Name'],
                                           row['Custom Type ID'], row['Price']))
                success_count += 1

        elif csv_file == 'GTAVOStorageCompatibilityTable.csv':
            self.cursor.execute("DELETE FROM storage_compatibility")
            for _, row in df.iterrows():
                placeholders = ", ".join(["?"] * 3)
                sql = f"""
                    INSERT INTO storage_compatibility 
                    (id, vehicle_class_id, slottype_id)
                    VALUES ({placeholders})
                """
                self.cursor.execute(sql, (row['ID'], row['Vehicle Class ID'], row['Slot Type ID']))
                success_count += 1

        elif csv_file == 'GTAVOStorageDedicatedTable.csv':
            self.cursor.execute("DELETE FROM dedicated_storage")
            for _, row in df.iterrows():
                placeholders = ", ".join(["?"] * 3)
                sql = f"""
                    INSERT INTO dedicated_storage 
                    (id, slottype_id, allowed_vehicle_id)
                    VALUES ({placeholders})
                """
                self.cursor.execute(sql, (row['ID'], row['Slot Type ID'], row['Allowed Vehicle ID']))
                success_count += 1

        elif csv_file == 'GTAVOStorageLocationTable.csv':
            self.cursor.execute("DELETE FROM property_type_has_slot")
            for _, row in df.iterrows():
                placeholders = ", ".join(["?"] * 5)
                sql = f"""
                    INSERT INTO property_type_has_slot 
                    (id, propertytype_id, slottype_id,
                    numberofslot, is_hidden)
                    VALUES ({placeholders})
                """
                self.cursor.execute(sql, (row['ID'], row['Property Type ID'], row['Slot Type ID'],
                                          row['Number Of Slots'], row['Is_Hidden']))
                success_count += 1

        elif csv_file == 'GTAVOStorageSlotTypeTable.csv':
            self.cursor.execute("DELETE FROM slot_type")
            for _, row in df.iterrows():
                placeholders = ", ".join(["?"] * 2)
                sql = f"""
                    INSERT INTO slot_type 
                    (id, key_name)
                    VALUES ({placeholders})
                """
                self.cursor.execute(sql, (row['ID'], row['Name']))
                success_count += 1

        elif csv_file == 'GTAVOBonusTargetTable.csv':
            self.cursor.execute("DELETE FROM bonus_target_type")
            for _, row in df.iterrows():
                placeholders = ", ".join(["?"] * 2)
                sql = f"""
                    INSERT INTO bonus_target_type 
                    (id, key_name)
                    VALUES ({placeholders})
                """
                self.cursor.execute(sql, (row['ID'], row['Name']))
                success_count += 1

        elif csv_file == 'GTAVOBonusDataTable.csv':
            self.cursor.execute("DELETE FROM buybonus_rule")
            for _, row in df.iterrows():
                placeholders = ", ".join(["?"] * 6)
                sql = f"""
                    INSERT INTO buybonus_rule 
                    (id, triggertype_id, trigger_id,
                    rewardtype_id, reward_id, quantity)
                    VALUES ({placeholders})
                """
                self.cursor.execute(sql, (row['ID'], row['trigger Type ID'], row['trigger Item ID']
                                          , row['Reward Type ID'], row['Reward Item ID'], row['Quantity']))
                success_count += 1

        if success_count > 0:
            self.db_conn.commit()


        self.update_meta(csv_file, len(df))


        print(f"✅ {csv_file} Successfully Done, (Inserted {success_count} rows)")
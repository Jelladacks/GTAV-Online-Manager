

import os
import sqlite3
import sys

from PySide6.QtWidgets import QApplication
from Codes.MainUI import MainWindow
from Datas.Database.init.SmartSeeder import SmartSeeder
from Codes.Service.loadGTAData import DBLoader_GTA
from Codes.Service.loadUserData import DBLoader_USER

def init_data():
    """
        Bundles SQL queries and CSV files by group.
        The Seeder then verifies update information
        for each group and applies DB updates.
    """
    is_new_db = not os.path.exists(DBLoader_GTA.db_file) # 파일 자체가 없는지 확인

    conn = sqlite3.connect(DBLoader_GTA.db_file)
    try:
        seeder_info = {
            'init.sql' : [],
            'vehicle_table.sql' : [
                                    'GTAVOManufacturerDataTable.csv',
                                    'GTAVOVehicleClassTable.csv',
                                    'GTAVOVehicleDrivetrain.csv',
                                    'GTAVOAcquisitionDataTable.csv',
                                    'GTAVOAcquisitionSource.csv',
                                    'GTAVOVehicleDataTable.csv',
                                    'GTAVOVehicleTranslation.csv'
                                ],
            'paintpreset_table.sql' : [
                                        'GTAVORenderMaterial.csv',
                                        'GTAVOColorRefTable.csv',
                                        'GTAVOChameleonType.csv',
                                        'GTAVOLiveryType.csv',
                                        'GTAVODefaultPaintDataTable.csv'
                                    ],
            'property_table.sql' : [
                                    'GTAVOPropertyCustomTable.csv',
                                    'GTAVOPropertyCustomTypeTable.csv',
                                    'GTAVOPropertyDataTable.csv',
                                    'GTAVOPropertyTypeTable.csv'
                                ],
            'storage_table.sql' : [
                                    'GTAVOStorageCompatibilityTable.csv',
                                    'GTAVOStorageDedicatedTable.csv',
                                    'GTAVOStorageLocationTable.csv',
                                    'GTAVOStorageSlotTypeTable.csv'
                                ],
            'buying_table.sql' : [
                                    'GTAVOBonusTargetTable.csv',
                                    'GTAVOBonusDataTable.csv'
                                ]

        }
        seeder = SmartSeeder(conn, seeder_info)
        
        if is_new_db:
            print("🆕 Detected 'Reset argument'. rebuild DB...")
            seeder.run_all(force=True) # seed all
        else:
            seeder.run_all() # seed updated only
            
    finally:
        conn.close()

def init_user():
    """
        Detect UserDB. Create UserDB If UserDB is not detected
    """
    is_new_db = not os.path.exists(DBLoader_USER.db_file)
    user_sql = os.path.join(SmartSeeder.SQL_DIR, "player_own_table.sql")
    db_dir = os.path.dirname(DBLoader_USER.db_file)

    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)

    conn = sqlite3.connect(DBLoader_USER.db_file)

    try:
        print("Loading USER DB...")
        if is_new_db:
            print("🆕 Building New USER DB")
            if os.path.exists(user_sql):
                with open(user_sql, 'r', encoding='utf-8') as f:
                    sql_script = f.read()

                conn.cursor().executescript(sql_script)
                conn.commit()
                print(f"📜 SQL Script done: {user_sql}")
            else:
                print(f"⚠️ Cannot Find SQL: {user_sql}")

        else:
            pass

    finally:
        conn.close()

        
if __name__ == "__main__":
    ### 실행 시 'python main.py --reset' 이라고 치면 DB 삭제 후 재생성
    ### Running 'python main.py --reset' deletes and recreates the DB.
    if "--reset" in sys.argv:
        if os.path.exists(DBLoader_GTA.db_file):
            os.remove(DBLoader_GTA.db_file)
            print("🗑️ Removed GTA DB")
        if os.path.exists(DBLoader_USER.db_file):
            os.remove(DBLoader_USER.db_file)
            print("🗑️ Deleted USER DB")
    
    init_data()
    init_user()
    ### Run PySide6 App
    app = QApplication(sys.argv)
    # sys.excepthook = lambda cls, ex, tb: print(f"Fatal Error: {ex}")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
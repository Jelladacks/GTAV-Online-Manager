def get_vehicle_by_name(conn, vehicle_name: str):
    return None

def find_vehicle_by_name(conn, vehicle_name: str):
    return None

def find_vehicle_class_by_name(conn, class_name: str):
    return None

def find_manufacturer_by_name(conn, manufacturer_name: str):
    return None

def find_acquisition_source_by_name(conn, source_name: str):
    return None

def find_drivetrain_by_name(conn, drivetrain_name: str):
    return None

def find_acquisition_by_vehicle_name(conn, vehicle_name: str):
    return None


### 전체 DB를 그냥 파이썬에 한번 로드시켜서 빠른 필터링 기능으로 하는게 나을 듯.
### 위에 find로 나눠둔거도.. 일단은 두는데 DB 전체 조회해서 파이썬으로 다시 해보자
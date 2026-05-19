import sqlite3

def buying_something(conn, type_name: str, item_id: int):
    """
        Not Using Now
    """
    cur = conn.cursor()

    conn2 = sqlite3.connect("Datas/Database/db/userbase.db")
    cur2 = conn2.cursor()

    #일단 구매처리

    match type_name:
        case 'vehicle':
            cur2.execute("""
                INSERT INTO owned_vehicle 
                        (vehicle_id, owned_property_id,
                        slot_type_id, slot_index)
                VALUES (?, ?, ?, ?)
            """, (item_id, 2, 2, 1))  
        case 'property':
            cur2.execute("""
                INSERT INTO owned_property 
                        (property_id, property_type_id,
                        memo, is_active)
                VALUES (?, ?, ?, ?)
            """, (item_id, 2, 'memeo', 0)) 
        case 'p_custom':
            cur2.execute("""
                INSERT INTO owned_property_custom 
                        (owned_property_id, propertycustom_id,
                         propertycustom_type_id)
                VALUES (?, ?, ?)
            """, (1, item_id, 1)) 

    conn2.commit()

    cur.execute(""" 
        SELECT id
        FROM bonus_target_type
        WHERE key_name = ?
    """, (type_name,))

    ref = cur.fetchone()
    if ref:
        type_id = ref[0]
    else:
        type_id = None

    # 2. 보너스 룰 조회
    cur.execute("""
        SELECT rewardtype_id, reward_id
        FROM buybonus_rule
        WHERE triggertype_id = ?
          AND trigger_id = ?
    """, (type_id, item_id))

    bonuses = cur.fetchall()

    # 3. 보너스 적용
    for bonus in bonuses:
        apply_bonus(conn, bonus)

    conn2.commit()


def apply_bonus(conn, bonus_row):
    """
        Not Using Now
    """
    rewardtype_id = bonus_row["rewardtype_id"]
    reward_id = bonus_row["reward_id"]
    cur = conn.cursor()

    conn2 = sqlite3.connect("Datas/Database/db/userbase.db")
    cur2 = conn2.cursor()

    cur.execute(""" 
        SELECT key_name
        FROM bonus_target_type
        WHERE id = ?
    """, (rewardtype_id, ))

    ref = cur.fetchone()
    if ref:
        rewardtype = ref[0]
    else:
        rewardtype = None

    if rewardtype == "vehicle":
        cur2.execute("""
            INSERT INTO owned_vehicle 
                    (vehicle_id, owned_property_id,
                    slot_type_id, slot_index)
            VALUES (?, ?, ?, ?)
        """, (reward_id, 1, 1, 1)) 

    elif rewardtype == "property":
        cur2.execute("""
            INSERT INTO owned_property 
                    (property_id, property_type_id,
                    memo, is_active)
            VALUES (?, ?, ?, ?)
        """, (reward_id, 1, 'kosatka', 1)) 

    else:
        raise ValueError(f"Unknown bonus type: {rewardtype_id}")
    
    conn2.commit()
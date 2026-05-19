CREATE TABLE IF NOT EXISTS bonus_target_type (
    id INTEGER PRIMARY KEY,
    key_name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS buybonus_rule (
    id INTEGER PRIMARY KEY,
    triggertype_id INTEGER NOT NULL,
    trigger_id INTEGER NOT NULL,
    rewardtype_id INTEGER NOT NULL,
    reward_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,

    FOREIGN KEY (triggertype_id) REFERENCES bonus_target_type(id),
    FOREIGN KEY (rewardtype_id) REFERENCES bonus_target_type(id)
);
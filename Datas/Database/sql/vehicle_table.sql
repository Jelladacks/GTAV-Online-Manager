CREATE TABLE IF NOT EXISTS vehicle_class (
    id INTEGER PRIMARY KEY,
    key_name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS manufacturer (
    id INTEGER PRIMARY KEY,
    key_name TEXT NOT NULL UNIQUE,
    translated_name TEXT
);

CREATE TABLE IF NOT EXISTS acquisition (
    id INTEGER PRIMARY KEY,
    vehicle_id INTEGER NOT NULL,
    source_id INTEGER NOT NULL,

    FOREIGN KEY (vehicle_id) REFERENCES vehicle(id),
    FOREIGN KEY (source_id) REFERENCES acquisition_source(id)
);

CREATE TABLE IF NOT EXISTS acquisition_source (
    id INTEGER PRIMARY KEY,
    key_name TEXT NOT NULL UNIQUE,
    is_shop INTEGER NOT NULL CHECK (is_shop IN (0,1))
);

CREATE TABLE IF NOT EXISTS drivetrain (
    id INTEGER PRIMARY KEY,
    key_name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS vehicle (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    manufacturer_id INTEGER,
    class_id INTEGER NOT NULL,
    price INTEGER,
    seats INTEGER NOT NULL,
    drivetrain_id INTEGER,
    mass INTEGER NOT NULL,
    gears INTEGER,

    sizecm_x INTEGER,
    sizecm_y INTEGER,
    sizecm_z INTEGER,

    laptime_ms INTEGER,
    topspeed_10mtph INTEGER,

    graph_speed INTEGER,
    graph_acc INTEGER,
    graph_brake INTEGER,
    graph_handle INTEGER,

    is_unique INTEGER NOT NULL CHECK (is_unique IN (0,1)),
    is_pegasus INTEGER NOT NULL CHECK (is_pegasus IN (0,1)),

    FOREIGN KEY (manufacturer_id) REFERENCES manufacturer(id),
    FOREIGN KEY (class_id) REFERENCES vehicle_class(id),
    FOREIGN KEY (drivetrain_id) REFERENCES drivetrain(id)
);

CREATE TABLE IF NOT EXISTS vehicle_translated (
    id INTEGER PRIMARY KEY,
    english_name TEXT,
    translated_name TEXT
);
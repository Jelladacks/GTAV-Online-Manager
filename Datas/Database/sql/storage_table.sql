CREATE TABLE IF NOT EXISTS slot_type (
    id INTEGER PRIMARY KEY,
    key_name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS property_type_has_slot (
    id INTEGER PRIMARY KEY,
    propertytype_id INTEGER NOT NULL,
    slottype_id INTEGER NOT NULL,
    numberofslot INTEGER NOT NULL,
    is_hidden NOT NULL CHECK (is_hidden IN (0,1)),

    FOREIGN KEY (propertytype_id) REFERENCES property_type(id),
    FOREIGN KEY (slottype_id) REFERENCES slot_type(id)
);

CREATE TABLE IF NOT EXISTS storage_compatibility (
    id INTEGER PRIMARY KEY,
    vehicle_class_id INTEGER NOT NULL,
    slottype_id INTEGER NOT NULL,

    FOREIGN KEY (vehicle_class_id) REFERENCES vehicle_class(id),
    FOREIGN KEY (slottype_id) REFERENCES slot_type(id)
);

CREATE TABLE IF NOT EXISTS dedicated_storage (
    id INTEGER PRIMARY KEY,
    slottype_id INTEGER NOT NULL,
    allowed_vehicle_id INTEGER NOT NULL,

    FOREIGN KEY (slottype_id) REFERENCES slot_type(id),
    FOREIGN KEY (allowed_vehicle_id) REFERENCES vehicle(id)
);
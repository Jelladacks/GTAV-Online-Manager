CREATE TABLE IF NOT EXISTS property_type (
    id INTEGER PRIMARY KEY,
    key_name TEXT NOT NULL UNIQUE,
    max_owned INTEGER,
    is_abstract INTEGER NOT NULL CHECK (is_abstract IN (0,1)),
    is_hidden INTEGER NOT NULL CHECK (is_hidden IN (0,1)),
    parent_id INTEGER,
    is_unchangeable INTEGER NOT NULL CHECK (is_unchangeable IN (0,1)),

    FOREIGN KEY (parent_id) REFERENCES property_type(id)
);

CREATE TABLE IF NOT EXISTS property (
    id INTEGER PRIMARY KEY,
    key_name TEXT NOT NULL,
    type_id INTEGER NOT NULL,
    price INTEGER,

    FOREIGN KEY (type_id) REFERENCES property_type(id)
);

CREATE TABLE IF NOT EXISTS property_custom_type (
    id INTEGER PRIMARY KEY,
    key TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    propertytype_id INTEGER NOT NULL,
    is_unchangeable INTEGER NOT NULL CHECK (is_unchangeable IN (0,1)),
    max_owned INTEGER,

    FOREIGN KEY (propertytype_id) REFERENCES property_type(id)
);

CREATE TABLE IF NOT EXISTS property_custom (
    id INTEGER PRIMARY KEY,
    key TEXT NOT NULL UNIQUE,
    name TEXT,
    customtype_id INTEGER NOT NULL,
    price INTEGER,

    FOREIGN KEY (customtype_id) REFERENCES property_custom_type(id)
);
CREATE TABLE IF NOT EXISTS user_color_ref (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    gta_color_id INTEGER,
    default_rendermaterial_id INTEGER NOT NULL,
    chameleontype_id INTEGER,
    hex_color TEXT NOT NULL,
    secondary_hex TEXT,
    tertiary_hex TEXT,

    FOREIGN KEY (default_rendermaterial_id) REFERENCES render_material(id),
    FOREIGN KEY (chameleontype_id) REFERENCES chameleon_type(id)
);

CREATE TABLE IF NOT EXISTS user_paint_preset (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    is_hidden INTEGER NOT NULL CHECK (is_hidden IN (0,1)),
    primary_color_id INTEGER NOT NULL,
    primary_render_id INTEGER NOT NULL,
    secondary_color_id INTEGER,
    secondary_render_id INTEGER,
    pearl_color_id INTEGER,
    wheel_color_id INTEGER,
    dial_color_id INTEGER,
    trim_color_id INTEGER,
    neon_color_id INTEGER,
    headlight_color_id INTEGER,
    livery_type_id INTEGER
);

CREATE TABLE IF NOT EXISTS owned_vehicle (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_id INTEGER NOT NULL,
    owned_property_id INTEGER NOT NULL,
    slot_type_id INTEGER NOT NULL,
    slot_index INTEGER NOT NULL,
    paint_preset_id INTEGER,
    is_reward INTEGER NOT NULL CHECK (is_reward IN (0,1)) DEFAULT 0,
    mod_custom INTEGER NOT NULL CHECK (mod_custom IN (0,1)) DEFAULT 0,
    mod_upgrade INTEGER NOT NULL CHECK (mod_upgrade IN (0,1)) DEFAULT 0,
    mod_imani INTEGER NOT NULL CHECK (mod_imani IN (0,1)) DEFAULT 0,
    mod_hsw INTEGER NOT NULL CHECK (mod_hsw IN (0,1)) DEFAULT 0,
    mod_drift INTEGER NOT NULL CHECK (mod_drift IN (0,1)) DEFAULT 0,
    limited_mod INTEGER NOT NULL CHECK (limited_mod IN (0,1)) DEFAULT 0,
    limited_plate INTEGER NOT NULL CHECK (limited_plate IN (0,1)) DEFAULT 0,
    limited_paint INTEGER NOT NULL CHECK (limited_paint IN (0,1)) DEFAULT 0,
    limited_livery INTEGER NOT NULL CHECK (limited_livery IN (0,1)) DEFAULT 0,
    is_sold INTEGER NOT NULL CHECK (is_sold IN (0,1)) DEFAULT 0,

    FOREIGN KEY (vehicle_id) REFERENCES vehicle(id),
    FOREIGN KEY (owned_property_id) REFERENCES owned_property(id),
    FOREIGN KEY (slot_type_id) REFERENCES slot_type(id),
    FOREIGN KEY (paint_preset_id) REFERENCES user_paint_preset(id)
);

CREATE TABLE IF NOT EXISTS owned_property (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id INTEGER NOT NULL,
    property_type_id INTEGER NOT NULL,
    memo TEXT,
    is_active INTEGER NOT NULL CHECK (is_active IN (0,1)),

    FOREIGN KEY (property_id) REFERENCES property(id),
    FOREIGN KEY (property_type_id) REFERENCES property_type(id)
);

CREATE TABLE IF NOT EXISTS owned_property_custom (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owned_property_id INTEGER NOT NULL,
    propertycustom_id INTEGER NOT NULL,
    propertycustom_type_id INTEGER NOT NULL,

    UNIQUE (owned_property_id, propertycustom_id),

    FOREIGN KEY (owned_property_id) REFERENCES owned_property(id),
    FOREIGN KEY (propertycustom_type_id) REFERENCES property_custom_type(id),
    FOREIGN KEY (propertycustom_id) REFERENCES property_custom(id)
);

INSERT INTO owned_property (id, property_id, property_type_id, memo, is_active)
VALUES 
(1, 0, 0, 'TEMPORARY SLOT', 1),
(2, 1, 1, 'Pegasus', 1),
(3, 1000, 100, 'Inventory', 1);

INSERT INTO user_paint_preset (id, name, is_hidden,
            primary_color_id ,primary_render_id, 
            secondary_color_id, secondary_render_id)
VALUES
(1, 'These are', 0, 27, 1, 38, 1),
(2, 'Default Presets', 0, 135, 1, 135, 1),
(3, 'Add Crew Color', 0, 88, 1, 88, 1),
(4, 'DoubleClick To Edit', 0, 38, 1, 0, 1),
(5, 'DoubleClick', 0, 92, 1, 0, 1),
(6, 'To Edit Preset', 0, 64, 1, 68, 1),
(7, 'RightClick', 0, 0, 1, 10, 1),
(8, 'To Remove Preset', 0, 111, 1, 0, 1);
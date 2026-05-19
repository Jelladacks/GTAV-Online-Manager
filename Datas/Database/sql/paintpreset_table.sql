CREATE TABLE IF NOT EXISTS gta_paint_preset (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category_render_id INTEGER NOT NULL,
    primary_color_id INTEGER NOT NULL,
    primary_render_id INTEGER NOT NULL,
    secondary_color_id INTEGER,
    secondary_render_id INTEGER,
    pearl_color_id INTEGER,

    FOREIGN KEY (category_render_id) REFERENCES render_material(id),
    FOREIGN KEY (primary_color_id) REFERENCES color_ref(id),
    FOREIGN KEY (primary_render_id) REFERENCES render_material(id),
    FOREIGN KEY (secondary_color_id) REFERENCES color_ref(id),
    FOREIGN KEY (secondary_render_id) REFERENCES render_material(id),
    FOREIGN KEY (pearl_color_id) REFERENCES color_ref(id)
);

CREATE TABLE IF NOT EXISTS render_material (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS chameleon_type (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS color_ref (
    id INTEGER PRIMARY KEY,
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

CREATE TABLE IF NOT EXISTS livery_type (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);
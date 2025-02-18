CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY UNIQUE,
    username TEXT,
    money INTEGER DEFAULT 5000
);

CREATE TABLE IF NOT EXISTS car_models (
    id SERIAL PRIMARY KEY,
    brand TEXT NOT NULL,
    model TEXT NOT NULL,
    yr INTEGER NOT NULL,
    hp INTEGER NOT NULL,
    nm INTEGER NOT NULL,
    acc FLOAT NOT NULL,
    maxSpeed INTEGER NOT NULL,
    weight INTEGER NOT NULL,
    traction TEXT NOT NULL, 
    price INTEGER NOT NULL,
    UNIQUE (brand, model, yr)
);

CREATE TABLE IF NOT EXISTS cars (
    id SERIAL PRIMARY KEY,
    owner TEXT NOT NULL,
    model_id INTEGER NOT NULL,
    hp_upgrade INTEGER DEFAULT 0,
    nm_upgrade INTEGER DEFAULT 0,
    acc_upgrade FLOAT DEFAULT 0,
    maxSpeed_upgrade INTEGER DEFAULT 0,
    weight_upgrade INTEGER DEFAULT 0,
    traction_upgrade TEXT DEFAULT NULL,
    price_upgrade INTEGER DEFAULT 0,
    FOREIGN KEY (owner) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (model_id) REFERENCES car_models(id) ON DELETE CASCADE
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    full_name TEXT,
    dob TEXT,
    profile_pic TEXT,
    coins INTEGER DEFAULT 0,
    last_checkin TEXT
);

CREATE TABLE progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    subject TEXT,
    percentage REAL,
    FOREIGN KEY(user_id) REFERENCES users(id)
);
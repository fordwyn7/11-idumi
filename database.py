import sqlite3

conn = sqlite3.connect("users_database.db")
cursor = conn.cursor()

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT,
    passport_seria TEXT UNIQUE,
    grade TEXT,
    group_number INTEGER,
    jshshir INTEGER,
    birth_date TEXT,
    private_password TEXT UNIQUE
    )
    """
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS parents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE,
    student_passport_seria TEXT NOT NULL,
    full_name TEXT,
    phone_number TEXT,
    FOREIGN KEY (student_passport_seria) REFERENCES students(passport_seria) ON DELETE CASCADE
    )
    """
)


cursor.execute(
    """
CREATE TABLE IF NOT EXISTS teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE NOT NULL,
    full_name TEXT,
    registration_date TEXT
    )
    """
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS admins (
        user_id INTEGER PRIMARY KEY
    );
"""
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS passwords (
        password_teacher TEXT PRIMARY KEY
    );
    """
)
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS new_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE NOT NULL,
    full_name TEXT,
    registration_date TEXT,
    username TEXT UNIQUE
    """
)
# cursor.execute("DELETE FROM students;")
# cursor.execute("DELETE FROM teachers;")
# cursor.execute("DELETE FROM parents;")
# cursor.execute("DELETE FROM admins;")
MAIN_ADMIN_ID = 6807731973
cursor.execute("INSERT OR IGNORE INTO admins (user_id) VALUES (?)", (MAIN_ADMIN_ID,))

conn.commit()
conn.close()

import sqlite3
import random
import string
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def connect_db():
    return sqlite3.connect("users_database.db")


def is_user_registered(user_id):
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM parents WHERE user_id = ?",
                (user_id,),
            )
            user_1 = cursor.fetchone()
            if user_1:
                return user_1
            cursor.execute(
                "SELECT * FROM teachers WHERE user_id = ?",
                (user_id,),
            )
            user_2 = cursor.fetchone()
            if user_2:
                return user_2
            cursor.execute(
                "SELECT * FROM admins WHERE user_id = ?",
                (user_id,),
            )
            user_3 = cursor.fetchone()
        return user_3
    except sqlite3.Error as e:
        print(f"Error checking if user is registered: {e}")
        return None


def is_user_new(user_id):
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM new_users WHERE user_id = ?",
                (user_id,),
            )
            user = cursor.fetchone()
            if user:
                return False
        return True
    except sqlite3.Error as e:
        print(f"Error checking if user is new: {e}")
        return None


def get_level_user(user_id):
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM admins WHERE user_id = ?",
                (user_id,),
            )
            user_3 = cursor.fetchone()
            if user_3:
                return "admin"
            cursor.execute(
                "SELECT * FROM parents WHERE user_id = ?",
                (user_id,),
            )
            user_1 = cursor.fetchone()
            if user_1:
                return "parent"
            cursor.execute(
                "SELECT * FROM teachers WHERE user_id = ?",
                (user_id,),
            )
            user_2 = cursor.fetchone()
            if user_2:
                return "teacher"

    except:
        return None


def is_password_correct(password):
    if len(password) != 7 or password[:2] != "T_":
        return False
    k = 0
    for i in password[2:]:
        if i.isdigit() or i.isalpha():
            k += 1
    if k == 5:
        return True
    return False


def generate_teacher_password():
    characters = string.ascii_letters + string.digits
    random_part = "".join(random.choices(characters, k=5))
    return f"T_{random_part}"


def count_of_students():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        users = cursor.fetchall()
        if users:
            return len(users)

        return 0


def count_of_parents():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM parents")
        users = cursor.fetchall()
        if users:
            return len(users)
        return 0


def get_admins():
    conn = sqlite3.connect("users_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM admins")
    admins = [row[0] for row in cursor.fetchall()]
    conn.close()
    return admins


def get_seria_by_user_id(user_id):
    conn = sqlite3.connect("users_database.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT student_passport_seria FROM parents WHERE user_id = ?", (user_id,)
    )
    datta = cursor.fetchall()[0]
    conn.close()
    return datta[0]


def get_tachers():
    conn = sqlite3.connect("users_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM teachers")
    teachers = [row[0] for row in cursor.fetchall()]
    conn.close()
    return teachers


def get_parents():
    conn = sqlite3.connect("users_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM parents")
    parents = [row[0] for row in cursor.fetchall()]
    conn.close()
    return parents


def get_student_by_parent_user_id(user_id: int):
    conn = sqlite3.connect("users_database.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT student_passport_seria FROM parents WHERE user_id = ?", (user_id,)
    )
    result = cursor.fetchone()
    if not result:
        conn.close()
        return None
    student_passport_seria = result[0]
    cursor.execute(
        """
        SELECT full_name, passport_seria, grade, group_number
        FROM students
        WHERE passport_seria = ?
    """,
        (student_passport_seria,),
    )
    student = cursor.fetchone()
    conn.close()
    return student


STUDENTS_PER_PAGE = 15


def get_students_by_grade(grade: str, page: int) -> tuple[list, int]:
    offset = page * STUDENTS_PER_PAGE
    conn = sqlite3.connect("users_database.db")
    cursor = conn.cursor()

    try:
        # Get paginated students
        cursor.execute(
            """
            SELECT full_name, passport_seria
            FROM students
            WHERE grade = ?
            ORDER BY full_name COLLATE NOCASE
            LIMIT ? OFFSET ?
        """,
            (grade, STUDENTS_PER_PAGE, offset),
        )
        students = cursor.fetchall()

        # Get total count
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM students
            WHERE grade = ?
        """,
            (grade,),
        )
        total_students = cursor.fetchone()[0]

        total_pages = (total_students + STUDENTS_PER_PAGE - 1) // STUDENTS_PER_PAGE
        return students, total_pages
    finally:
        conn.close()


def count_students_by_grade(grade):
    conn = sqlite3.connect("users_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM students WHERE grade = ?", (grade,))
    count = cursor.fetchone()[0]
    conn.close()
    return count


def get_students_keyboard(
    grade: str, page: int, total_pages: int
) -> InlineKeyboardMarkup:
    inline_keyboard = []

    nav_buttons = []

    if page > 0:
        nav_buttons.append(
            InlineKeyboardButton(
                text="⬅️ Oldingi", callback_data=f"page_{grade}_{page - 1}"
            )
        )

    if page < total_pages - 1:
        nav_buttons.append(
            InlineKeyboardButton(
                text="➡️ Keyingi", callback_data=f"page_{grade}_{page + 1}"
            )
        )

    if nav_buttons:
        inline_keyboard.append(nav_buttons)

    # Back to grades
    inline_keyboard.append(
        [
            InlineKeyboardButton(
                text="🔙 Sinflarga qaytish", callback_data="back_to_grades"
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def count_students_by_grade():
    conn = sqlite3.connect("users_database.db")
    cursor = conn.cursor()
    grades = ["11-A", "11-B", "11-V", "10-A", "10-B", "10-V", "9-A", "8-A", "8-B"]
    result = ["📚 *Sinf kesimida o'quvchilar soni:*"]
    for grade in grades:
        cursor.execute("SELECT COUNT(*) FROM students WHERE grade = ?", (grade,))
        count = cursor.fetchone()[0]
        result.append(f"▫️ *{grade}*: {count}")
    conn.close()
    return "\n".join(result)


def add_user_to_new_users(user_id, full_name, username):
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO new_users (user_id, full_name, registration_date, username) VALUES (?, ?, datetime('now', '+5 hours'), ?)",
                (user_id, full_name, username),
            )
            conn.commit()
    except sqlite3.Error as e:
        print(f"Error adding user to new users: {e}")

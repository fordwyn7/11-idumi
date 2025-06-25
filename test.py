# import pandas as pd
# import sqlite3

# file_path = r"C:\Users\rsfor\Downloads\O'quvchilar ro'yxati.xlsx"

# df = pd.read_excel(file_path, skiprows=0)

# df.columns = df.columns.str.strip()

# print(df.columns.tolist())
# conn = sqlite3.connect("users_database.db")
# cursor = conn.cursor()
# k = 0
# for index, row in df.iterrows():
#     k += 1
#     full_name = row.get("ФИО")
#     seria = str(row.get("Серия")).strip()
#     if k < 282:
#         try:
#             number = int(float(str(row.get("Номер документа"))))
#             passport_seria = seria + str(number)
#             jshshir = int(row.get("ПИНФЛ"))
#             grade = row.get("Класс")
#             birthdate = str(row.get("Дата рождения").date()) if pd.notnull(row.get("Дата рождения")) else None
#             cursor.execute(
#                 """
#             INSERT OR IGNORE INTO students (full_name, passport_seria, grade, jshshir, birth_date)
#             VALUES (?, ?, ?, ?, ?)
#             """,
#                 (full_name, passport_seria, grade, jshshir, birthdate),
#             )
#             conn.commit()
#         except Exception  as e:
#             print(e, k)


# def cyrillic_to_latin(text):
#     mapping = {
#         'А': 'A', 'а': 'a', 'Б': 'B', 'б': 'b', 'В': 'V', 'в': 'v',
#         'Г': 'G', 'г': 'g', 'Д': 'D', 'д': 'd', 'Е': 'E', 'е': 'e',
#         'Ё': 'Yo', 'ё': 'yo', 'Ж': 'J', 'ж': 'j', 'З': 'Z', 'з': 'z',
#         'И': 'I', 'и': 'i', 'Й': 'Y', 'й': 'y', 'К': 'K', 'к': 'k',
#         'Л': 'L', 'л': 'l', 'М': 'M', 'м': 'm', 'Н': 'N', 'н': 'n',
#         'О': 'O', 'о': 'o', 'П': 'P', 'п': 'p', 'Р': 'R', 'р': 'r',
#         'С': 'S', 'с': 's', 'Т': 'T', 'т': 't', 'У': 'U', 'у': 'u',
#         'Ф': 'F', 'ф': 'f', 'Х': 'X', 'х': 'x', 'Ц': 'Ts', 'ц': 'ts',
#         'Ч': 'Ch', 'ч': 'ch', 'Ш': 'Sh', 'ш': 'sh', 'Щ': 'Sh', 'щ': 'sh',
#         'Ъ': '', 'ъ': '', 'Ы': 'I', 'ы': 'i', 'Ь': '', 'ь': '',
#         'Э': 'E', 'э': 'e', 'Ю': 'Yu', 'ю': 'yu', 'Я': 'Ya', 'я': 'ya',
#         'Ў': 'O‘', 'ў': 'o‘', 'Ғ': 'G‘', 'ғ': 'g‘', 'Қ': 'Q', 'қ': 'q',
#         'Ҳ': 'H', 'ҳ': 'h', 'Ь': '', 'ь': '', 'Ъ': '', 'ъ': ''
#     }

#     return ''.join(mapping.get(c, c) for c in text)


# import sqlite3
# from functions import *

# def contains_cyrillic(text):
#     return any('А' <= char <= 'я' or char == 'Ё' or char == 'ё' for char in text)

# def convert_full_names_to_latin():
#     conn = sqlite3.connect("users_database.db")
#     cursor = conn.cursor()

#     cursor.execute("SELECT id, full_name FROM students")
#     students = cursor.fetchall()

#     for student_id, full_name in students:
#         # if contains_cyrillic(full_name):
#             latin_name = full_name.replace("‘", "'")
#             cursor.execute(
#                 "UPDATE students SET full_name = ? WHERE id = ?",
#                 (latin_name, student_id)
#             )
#             print(f"Updated: {full_name} → {latin_name}")

#     conn.commit()
#     conn.close()
#     print("✅ All Cyrillic names converted to Latin.")

# convert_full_names_to_latin()

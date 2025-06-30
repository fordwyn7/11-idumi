from config import *
from states.state import *
from keyboards.keyboard import *
from keyboards.inline import *
import sqlite3
from functions import *


@dp.message(choose_level.password)
async def entering_state(message: types.Message, state: FSMContext):
    msg = message.text
    if msg == "/start":
        await message.answer(
            "Assalomu alaykum 👋\n11 - IDUMIning rasmiy botiga hush kelibsiz 😊\nBotga kim sifatida kirmoqdasiz ? 👇",
            reply_markup=select_level_users,
        )
        await state.clear()
        return
    if msg[:2] == "T_":
        conn = sqlite3.connect("users_database.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM passwords WHERE password_teacher = ?",
            (msg,),
        )
        data = cursor.fetchone()
        if not data:
            await message.answer(
                "Afsuski kiritilgan parol noto'g'ri 😔\nIltimos, qaytadan urinib ko'ring",
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(
                                text="bekor qilish 🚫",
                                callback_data="cancel_the_first_action",
                            )
                        ]
                    ]
                ),
            )
        else:
            await message.answer(
                "Tabriklaymiz parol mos keldi 🎉\nSiz bosh menudsiz 👇",
                reply_markup=main_menu_teacher,
            )
            user_id = message.from_user.id
            fullname = message.from_user.full_name
            cursor.execute(
                """
                INSERT OR IGNORE INTO teachers (user_id, full_name, registration_date)
                VALUES (?, ?, datetime('now',  '+5 hours'))
                """,
                (user_id, fullname),
            )
            conn.commit()
            await state.clear()
    else:
        msg = msg.replace(" ", "")
        conn = sqlite3.connect("users_database.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM students WHERE passport_seria = ?",
            (msg,),
        )
        data = cursor.fetchone()
        if not data:
            await message.answer(
                "Afsuski kiritilgan malumot noto'g'ri 😔\nIltimos, qaytadan urinib ko'ring",
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(
                                text="bekor qilish 🚫",
                                callback_data="cancel_the_first_action",
                            )
                        ]
                    ]
                ),
            )
        else:
            try:
                user_id = message.from_user.id
                full_name = message.from_user.full_name
                phone_number = (
                    message.contact.phone_number if message.contact else "Unknown"
                )
                cursor.execute(
                    "SELECT * FROM parents WHERE student_passport_seria = ?", (msg,)
                )
                old = cursor.fetchone()
                if not old:
                    cursor.execute(
                        """
                        INSERT OR IGNORE INTO parents (user_id, student_passport_seria, full_name, phone_number)
                        VALUES (?, ?, ?, ?)
                        """,
                        (user_id, msg, full_name, phone_number),
                    )
                    conn.commit()
                    await message.answer(
                        "Tabriklaymiz malumot mos keldi 🎉\nEndi siz har kuni farzandingizni maktabga kelgan va ketganligi haqida habarni shu bot orqali olib turasiz",
                        reply_markup=main_menu_parent,
                    )
                    await state.clear()
                else:
                    await message.answer(
                        "Hozirda bu hisobga boshqa telegramdan kirilgan ❗️\nAgar bu siz bo'lmasangiz JSHSHIR orqali shaxsingizni tasdiqlang va hisobha kiring 👇",
                        reply_markup=InlineKeyboardMarkup(
                            inline_keyboard=[
                                [
                                    InlineKeyboardButton(
                                        text="🔖 JSHSHIR orqali tasdiqlash 🔖",
                                        callback_data=f"confirm_with_jshshir_"
                                        + str(msg),
                                    )
                                ],
                                [
                                    InlineKeyboardButton(
                                        text="bekor qilish 🚫",
                                        callback_data="cancel_the_first_action",
                                    )
                                ],
                            ]
                        ),
                    )
                    await state.clear()
            except Exception as e:
                await message.answer(
                    f"Nimadir xato ketdi qaytadan urinib ko'ring ... ",
                    reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=[
                            [
                                InlineKeyboardButton(
                                    text="bekor qilish 🚫",
                                    callback_data="cancel_the_first_action",
                                )
                            ]
                        ]
                    ),
                )


@dp.message(confirm_jshshir.number)
async def confirming_jshsir(message: types.Message, state: FSMContext):
    msg = message.text
    msg = msg.replace(" ", "")
    dt = await state.get_data()
    seria = dt["id_seria"]
    try:
        conn = sqlite3.connect("users_database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE jshshir = ?", (msg,))
        data = cursor.fetchone()
        if data:
            cursor.execute(
                "SELECT user_id FROM parents WHERE student_passport_seria = ?", (seria,)
            )
            userid = cursor.fetchone()[0]
            await bot.send_message(
                chat_id=userid,
                text="Siz hisobdan chiqarib yuborildingiz ❗️\n/start buyrug'ini bosib qaytadan urinib ko'ring. ",
                reply_markup=ReplyKeyboardRemove(),
            )
            cursor.execute(
                "DELETE FROM parents WHERE student_passport_seria = ?", (seria,)
            )
            user_id = message.from_user.id
            fullname = message.from_user.full_name
            cursor.execute(
                """
                        INSERT OR IGNORE INTO parents (user_id, student_passport_seria, full_name)
                        VALUES (?, ?, ?)
                        """,
                (user_id, seria, fullname),
            )
            conn.commit()
            await state.clear()
            await message.answer(
                "Tabriklaymiz malumot mos keldi 🎉\nEndi siz har kuni farzandingizni maktabga kelgan va ketganligi haqida habarni shu bot orqali olib turasiz",
                reply_markup=main_menu_parent,
            )
        else:
            await message.answer(
                "Afsuski kiritilgan malumot noto'g'ri 😔\nIltimos, qaytadan urinib ko'ring",
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(
                                text="bekor qilish 🚫",
                                callback_data="cancel_the_first_action",
                            )
                        ]
                    ]
                ),
            )
    except Exception as e:
        await message.answer(
            "Afsuski kiritilgan malumot noto'g'ri 😔\nIltimos, qaytadan urinib ko'ring",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="bekor qilish 🚫",
                            callback_data="cancel_the_first_action",
                        )
                    ]
                ]
            ),
        )
        print(e)


@dp.message(wait_for_password.password)
async def entering_state(message: types.Message, state: FSMContext):
    msg = message.text
    if is_password_correct(msg):
        conn = sqlite3.connect("users_database.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM passwords;")
        cursor.execute("INSERT INTO passwords (password_teacher) VALUES (?)", (msg,))
        conn.commit()
        await state.clear()
        await message.answer(
            "Parol muvaffaqiyatli o'rnatildi ✅", reply_markup=main_menu_admin
        )
        cursor.execute("SELECT user_id FROM teachers")
        teachers = cursor.fetchall()
        for teacher in teachers:
            user_id = teacher[0]
            try:
                await bot.send_message(
                    chat_id=user_id,
                    text="O'qituvchilar uchun belgilangan parol o'zgartirildi. Admindan yangi parolni olib /start buyrug'i orqali qayta ro'yhatdan o'ting. ♻️",
                    reply_markup=ReplyKeyboardRemove(),
                )
            except Exception as e:
                continue
        cursor.execute("DELETE FROM teachers;")
        conn.commit()
        return
    await message.answer("Iltimos to'g'ri parol kiriting.")


@dp.message(ask_question.question)
async def asking_question_state(message: types.Message, state: FSMContext):
    msg = message.text
    user_id = message.from_user.id
    admins = get_admins()
    for admin in admins:
        try:
            await bot.send_message(
                chat_id=admin,
                text=f"Sizga yangi habar yuborildi 📩\n\nYuboruvchi 🧑‍💻:\n{message.from_user.first_name[:25]}({get_seria_by_user_id(user_id)})\nXabar 👇👇👇:\n{msg}",
            )
        except:
            continue
    await message.answer(
        "Habaringiz muvaffaqiyatli yuborildi ✅", reply_markup=main_menu_parent
    )
    await state.clear()


@dp.message(send_message.seria)
async def get_seria_number(message: types.Message, state: FSMContext):
    text = message.text
    if text == "bekor qilish 🔙":
        await state.clear()
        await message.answer("Siz asosiy menudasiz 👇", reply_markup=main_menu_admin)
        return
    msg = message.text.replace(" ", "")
    conn = sqlite3.connect("users_database.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT user_id FROM parents WHERE user_id = ? OR student_passport_seria = ?",
        (int(msg) if msg.isdigit() else -1, msg),
    )

    data1 = cursor.fetchone()
    if not data1:
        cursor.execute(
            "SELECT user_id FROM teachers WHERE user_id = ?",
            (msg,),
        )
        data2 = cursor.fetchone()
        if not data2:
            cursor.execute(
                "SELECT user_id FROM admins WHERE user_id = ?",
                (msg,),
            )
            data3 = cursor.fetchone()
            if not data3:
                await state.clear()
                await message.answer(
                    "Hozirda bunday foydalanuvchi botda mavjud emas.",
                    reply_markup=main_menu_admin,
                )
                return
    user_id = (data1 or data2 or data3)[0] if (data1 or data2 or data3) else None

    await state.set_data({"id": user_id})
    await message.answer(
        "Endi esa yubormoqchi bo'lgan matningizni yuboring: ",
        reply_markup=cancel_for_admin_panel,
    )
    await state.set_state(send_message.msg)


@dp.message(send_message.msg)
async def sending_message_to_user(message: types.Message, state: FSMContext):
    try:
        text = message.text
        if text == "bekor qilish 🔙":
            await state.clear()
            await message.answer(
                "Siz asosiy menudasiz 👇", reply_markup=main_menu_admin
            )
            return
        data = await state.get_data()
        msg = data["id"]
        await bot.send_message(chat_id=msg, text=text)
        await message.answer(
            "Habaringiz muvaffaqiyatli yuborildi ✅", reply_markup=main_menu_admin
        )
        await state.clear()
    except Exception as e:
        await message.answer(
            f"Xatolik: Siz habar yubormoqchi bo'lgan odam botni bloklagan bo'lishi mumkin !",
            reply_markup=main_menu_admin,
        )
        await state.clear()

@dp.message(add_admin_state.admin_id)
async def add_admin(message: types.Message, state: FSMContext):
    text = message.text
    if text == "bekor qilish 🔙":
        await state.clear()
        await message.answer(
            "Siz asosiy menudasiz 👇", reply_markup=main_menu_admin
        )
        return
    try:
        user_id = int(text)
        conn = sqlite3.connect("users_database.db")
        cursor = conn.cursor()
        # find user_id from new_users table
        cursor.execute(
            "SELECT * FROM new_users WHERE user_id = ?", (user_id,)
        )   
        data = cursor.fetchone()
        if not data:
            await message.answer(
                "Afsuski bunday foydalanuvchi botda mavjud emas ❗️\nSiz asosiy menudasiz 👇",
                reply_markup=main_menu_admin,
            )
            await state.clear()
            return
        cursor.execute(
            "INSERT OR IGNORE INTO admins (user_id) VALUES (?)", (user_id,)
        )
        conn.commit()
        await message.answer(
            "Admin muvaffaqiyatli qo'shildi ✅", reply_markup=main_menu_admin
        )
        await state.clear()
    except Exception as e:
        await message.answer(f"Xatolik yuz berdi: {e}", reply_markup=main_menu_admin)
        await state.clear()
        return
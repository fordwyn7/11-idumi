from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hbold
from config import *
from states.state import *
from middlewares.middleware import *
from keyboards.keyboard import *
from keyboards.inline import *
from functions import *

import sqlite3


@dp.callback_query(lambda c: c.data.startswith("level_"))
async def level_detect(callback: types.CallbackQuery, state: FSMContext):
    level = callback.data.split("level_")[1]
    await callback.message.delete()
    if level == "parent":
        await callback.message.answer(
            "Iltimos, farzandingizni passport seriya va raqamini kiriting: \nNamuna -> AD1234567\nMetrika uchun -> I-AN123456",
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
        await callback.message.answer(
            "Iltimos, o'qituvchilar uchun berilgan parolni kiriting: ",
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
    await state.set_state(choose_level.password)
    await callback.answer()


@dp.callback_query(lambda c: c.data.startswith("changepass_"))
@admin_required()
async def changepasss(callback: types.CallbackQuery, state: FSMContext):
    data = callback.data.split("changepass_")[1]
    if data == "random":
        try:
            await callback.message.delete()
            new_password = generate_teacher_password()
            with connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM passwords;")
                cursor.execute(
                    "INSERT INTO passwords (password_teacher) VALUES (?)",
                    (new_password,),
                )
                conn.commit()
            await callback.message.answer(
                f"Yangi parol muvaffaqiyatli yaratildi ✅\n 👉  `{new_password}`",
                parse_mode="Markdown",
                reply_markup=main_menu_admin,
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
        except sqlite3.Error as e:
            await callback.message.answer(f"❌ Database error: {e}")
    else:
        await callback.message.delete()
        await callback.message.answer(
            "Parol quyidagi shartlarni qanoatlantirishi lozim:\n"
            "— Uzunligi aynan 7 ga teng bo'lishi\n"
            "— Faqat lotin alifbosining katta va kichik harflari yoki raqamlardan tashkil topishi\n"
            "— 'T_' belgisi bilan boshlanishi\n\n"
            "Yangi parolni kiriting:"
        )
        await state.set_state(wait_for_password.password)


@dp.callback_query(F.data.startswith("select_grade:"))
@admin_required()
async def show_students(callback: types.CallbackQuery):
    grade = callback.data.split(":")[1]
    page = 0
    students, total_pages = get_students_by_grade(grade, page)

    if not students:
        await callback.answer("Bu sinfda hech qanday o'quvchi yo'q.", show_alert=True)
        return
    start_number = page * STUDENTS_PER_PAGE + 1
    bot_username = "IDUMI_11_bot"
    text = "\n".join(
        [
            f"{start_number + i}. [{ ' '.join(s[0].split()[:-2]) }](https://t.me/{bot_username}?start=info_{s[1]})"
            for i, s in enumerate(students)
        ]
    )

    await callback.message.edit_text(
        f"*{grade} sinfidagi o'quvchilar (page {page+1}/{total_pages}):*\n\n{text}",
        parse_mode="Markdown",
        reply_markup=get_students_keyboard(grade, page, total_pages),
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("page_"))
@admin_required()
async def paginate_students_by_grade(callback: CallbackQuery):
    data_parts = callback.data.split("_")
    if len(data_parts) != 3:
        await callback.answer("Invalid callback data", show_alert=True)
        return

    grade = data_parts[1]
    try:
        page = int(data_parts[2])
    except ValueError:
        await callback.answer("Invalid page number", show_alert=True)
        return

    students, total_pages = get_students_by_grade(grade, page)

    start_number = page * STUDENTS_PER_PAGE + 1
    bot_username = "IDUMI_11_bot"

    text = "\n".join(
        [
            f"{start_number + i}. [{ ' '.join(s[0].split()[:-2]) }](https://t.me/{bot_username}?start=info_{s[1]})"
            for i, s in enumerate(students)
        ]
    )

    await callback.message.edit_text(
        f"*{grade} sinfidagi o'quvchilar (page {page+1}/{total_pages}):*\n\n{text}",
        parse_mode="Markdown",
        reply_markup=get_students_keyboard(grade, page, total_pages),
    )
    await callback.answer()


grades = ["11-A", "11-B", "11-V", "10-A", "10-B", "10-V", "9-A", "8-A", "8-B"]


@dp.callback_query(lambda c: c.data == "back_to_grades")
@admin_required()
async def back_to_grades(callback: CallbackQuery):
    builder = InlineKeyboardBuilder()
    for grade in grades:
        builder.button(text=grade, callback_data=f"select_grade:{grade}")
    builder.adjust(3)
    await callback.message.edit_text(
        "📚 Qaysi sinfni ko'rmoqchisiz?", reply_markup=builder.as_markup()
    )


@dp.callback_query(lambda c: c.data == "confirm_log_out_parent")
@parent_required()
async def confirm_log_out_parents(callback: CallbackQuery):
    try:
        conn = sqlite3.connect("users_database.db")
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM parents WHERE user_id = ?", (callback.from_user.id,)
        )
        conn.commit()
        conn.close()
        await callback.message.delete()
        await callback.message.answer(
            "Siz hisobdan muvaffaqiyatli chiqdingiz ✅",
            reply_markup=ReplyKeyboardRemove(),
        )
        await callback.message.answer(
            "Botga kim sifatida kirmoqdasiz ? 👇", reply_markup=select_level_users
        )
    except:
        await callback.message.delete()
        await callback.message.answer(
            "Xatolik yuz berdi 😕. Birozdan so'ng qayta urinib ko'ring",
            reply_markup=main_menu_parent,
        )


@dp.callback_query(lambda c: c.data == "cancel_log_out_parent")
@parent_required()
async def cancel_log_out_parents(callback: CallbackQuery):
    await callback.answer("Muvaffaqiyatli bekor qilindi ✔️", show_alert=True)
    await callback.message.delete()
    await callback.message.answer(
        "Siz asosiy menudasiz 👇",
        reply_markup=main_menu_parent,
    )


@dp.message(CommandStart(deep_link=True))
@admin_required()
async def handle_deep_link(message: types.Message, command: CommandObject):
    if command.args and command.args.startswith("info_"):
        secret = command.args[5:]
        conn = sqlite3.connect("users_database.db")
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT full_name, passport_seria, grade, group_number, jshshir, birth_date, private_password
            FROM students
            WHERE passport_seria = ? OR id = ?
        """,
            (secret, secret),
        )

        student = cursor.fetchone()
        conn.close()

        if student:
            (
                full_name,
                passport_seria,
                grade,
                group_number,
                jshshir,
                birth_date,
                private_password,
            ) = student
            student_info = (
                f"👤 *To'liq ismi:* {full_name}\n"
                f"📜 *Passport Seria:* {passport_seria}\n"
                f"🏫 *Sinf:* {grade}\n"
                f"🆔 *JSHSHIR:* {jshshir}\n"
                f"📅 *Tug'ilgan sana:* {birth_date}\n"
            )
            await message.answer(
                student_info,
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(
                                text="🔙 Sinflarga qaytish",
                                callback_data="back_to_grades",
                            )
                        ]
                    ]
                ),
            )
        else:
            await message.answer(
                "📚 *O'quvchilar topilmadi!*",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(
                                text="🔙 Sinflarga qaytish",
                                callback_data="back_to_grades",
                            )
                        ]
                    ]
                ),
            )


@dp.callback_query(lambda c: c.data == "confirm_log_out_teacher")
@teacher_required()
async def confirm_log_out_teachers(callback: CallbackQuery):
    try:
        conn = sqlite3.connect("users_database.db")
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM teachers WHERE user_id = ?", (callback.from_user.id,)
        )
        conn.commit()
        conn.close()
        await callback.message.delete()
        await callback.message.answer(
            "Siz hisobdan muvaffaqiyatli chiqdingiz ✅",
            reply_markup=ReplyKeyboardRemove(),
        )
        await callback.message.answer(
            "Botga kim sifatida kirmoqdasiz ? 👇", reply_markup=select_level_users
        )
    except:
        await callback.message.delete()
        await callback.message.answer(
            "Xatolik yuz berdi 😕. Birozdan so'ng qayta urinib ko'ring",
            reply_markup=main_menu_teacher,
        )


@dp.callback_query(lambda c: c.data == "cancel_log_out_teacher")
@teacher_required()
async def cancel_log_out_teachers(callback: CallbackQuery):
    await callback.answer("Muvaffaqiyatli bekor qilindi ✔️", show_alert=True)
    await callback.message.delete()
    await callback.message.answer(
        "Siz asosiy menudasiz 👇",
        reply_markup=main_menu_teacher,
    )


@dp.callback_query(F.data.startswith("confirm_with_jshshir_"))
async def confirm_with_jshshir_query(callback: CallbackQuery, state: FSMContext):
    seria = callback.data.split("_with_jshshir_")[1]
    await callback.message.delete()
    await callback.message.answer(
        "Iltimos, 14 xonadan iborat JSHSHIR raqamingizni kiriting ✏️",
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
    await state.set_data({"id_seria": seria})
    await state.set_state(confirm_jshshir.number)


@dp.callback_query(lambda c: c.data == "cancel_the_first_action")
async def cancel_confirming_with_jshshir_query(
    callback: CallbackQuery, state: FSMContext
):
    await callback.answer("Muvaffaqiyatli bekor qilindi ✔️", show_alert=True)
    await callback.message.edit_text(
        "Assalomu alaykum 👋\n11 - IDUMIning rasmiy botiga hush kelibsiz 😊\nBotga kim sifatida kirmoqdasiz ? 👇",
        reply_markup=select_level_users,
    )
    await state.clear()


@dp.callback_query(lambda c: c.data == "cancel_andtomain")
async def cancel_and_to_main_menu(
    callback: CallbackQuery, state: FSMContext
):
    await callback.answer("Muvaffaqiyatli bekor qilindi ✔️", show_alert=True)
    await callback.message.delete()
    await callback.message.answer(
        "Siz asosiy menudasiz 👇", reply_markup=main_menu_parent
    )
    await state.clear()




@dp.callback_query(F.data.startswith("delete_admin"))
async def delete_admin_callback(query: types.CallbackQuery):
    callback_data = query.data.split(":")
    action = callback_data[0]
    admin_id = int(callback_data[1])
    if int(admin_id) in [6807731973, 1155076760]:
        await query.answer("Bu botning asosiy admini. Siz uni o'chira olmaysiz❗️")
    else:
        if action == "delete_admin":
            conn = sqlite3.connect("users_database.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM admins WHERE user_id = ?", (admin_id,))
            conn.commit()
            conn.close()
            await query.answer("Admin muvaffaqiyatli o'chirildi.")

            conn = sqlite3.connect("users_database.db")
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM admins")
            remaining_admins = [row[0] for row in cursor.fetchall()]
            conn.close()
            keyboard_builder = InlineKeyboardBuilder()
            for admin in remaining_admins:
                keyboard_builder.button(
                    text=f"❌ Admin {admin}", callback_data=f"delete_admin:{admin}"
                )
            keyboard = keyboard_builder.adjust(1).as_markup()
            await query.message.edit_reply_markup(reply_markup=keyboard)

from config import *
from states.state import *
from keyboards.keyboard import *
from keyboards.inline import *
from functions import *
from middlewares.middleware import *
import sqlite3


@dp.message(F.text == "Statistika ⭐️")
@admin_required()
async def statistics(message: types.Message, state: FSMContext):
    await message.answer(
        f"📊 *Bot statistikasi:*\n\n"
        f"👤 *Jami o'quvchilar soni:* {count_of_students()}\n"
        f"👨‍👩‍👧‍👦 *Botdagi ota-onalar:* {count_of_parents()}\n\n"
        f"{count_students_by_grade()}",
        parse_mode="Markdown",
    )


grades = ["11-A", "11-B", "11-V", "10-A", "10-B", "10-V", "9-A", "8-A", "8-B"]


@dp.message(F.text == "O'quvchilar baza 📫")
@admin_required()
async def data_of_students(message: types.Message, state: FSMContext):
    builder = InlineKeyboardBuilder()
    for grade in grades:
        builder.button(text=grade, callback_data=f"select_grade:{grade}")
    builder.adjust(3)
    await message.answer(
        "📚 Qaysi sinfni ko'rmoqchisiz?", reply_markup=builder.as_markup()
    )


@dp.message(F.text == "Habar yuborish 📤")
@admin_required()
async def send_message_to_users(message: types.Message, state: FSMContext):
    await message.answer(
        "Habar yubormoqchi bo'lgan odamingizni telegram ID si yoki pasport seria va raqamini kiriting ✏️:",
        reply_markup=cancel_for_admin_panel,
    )
    await state.set_state(send_message.seria)


@dp.message(F.text == "Admin qoshish ➕")
@admin_required()
async def add_admin(message: types.Message, state: FSMContext):
    await message.answer(
        "Yangi admin qo'shish uchun uning telegram ID sini kiriting: ✏️",
        reply_markup=cancel_for_admin_panel,
    )
    await state.set_state(add_admin_state.admin_id)


@dp.message(F.text == "Adminlar paneli 📋")
@admin_required()
async def admin_paneli(message: types.Message, state: FSMContext):
    await message.answer(
        "Quyidagi amallardan birini tanlang 👇",
        reply_markup=adminlar_paneli,
    )
    await state.clear()


@dp.message(F.text == "admin panelga qaytish 🔙")
@admin_required()
async def back_to_admin_panel(message: types.Message, state: FSMContext):
    await message.answer("Siz admin paneldasiz 👇", reply_markup=main_menu_admin)
    await state.clear()


@dp.message(F.text == "Adminlarni ko'rish 📋")
@admin_required()
async def show_admins(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if not user_id in [1155076760, 6807731973]:
        await message.answer(
            "Sizda bu amalni bajarish huquqi yo'q.", reply_markup=adminlar_paneli
        )
        return
    admins = get_admins2()
    if not admins:
        await message.answer("Hozircha adminlar ro'yxati bo'sh.")
        return
    keyboard = InlineKeyboardBuilder()
    for admin in admins:
        callback_data = generate_callback("delete_admin", admin["id"])
        keyboard.row(
            InlineKeyboardButton(
                text=f"❌ {admin['name'] or admin['id']}",
                callback_data=callback_data,
            )
        )

    await message.answer("Adminlar ro'yxati:", reply_markup=keyboard.as_markup())


@dp.message(F.text == "bekor qilish 🔙")
@admin_required()
async def back_to_admin_panel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Siz asosiy menudasiz 👇", reply_markup=main_menu_admin)


@dp.message(F.text == "Savol so'rash ❓")
async def asking_question(message: types.Message, state: FSMContext):
    await message.answer(
        "So'ramoqchi bo'lgan savolingizni yozib qoldiring 📝: \nE'tibor bering ❗️ Savolingiz maktab ma'muriyatiga yuboriladi, shuning uchun avval o'zingizni tanishtirishni va aniq savol yozishni unutmang.",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Bekor qilish 🚫", callback_data="cancel_andtomain"
                    )
                ]
            ]
        ),
    )
    await state.set_state(ask_question.question)


@dp.message(F.text == "Aloqa 📞")
async def contact_informations(message: types.Message, state: FSMContext):
    await message.answer(
        f"Maktab ma'muriyatidagilar 👇\n\n"
        f"👉 Direktor: +998-99-996-51-10\n"
        f"👉 O'TIBDO': +998-88-124-57-96\n"
        f"👉 Orinbosar: +998-90-544-70-03\n"
    )


@dp.message(F.text == "Qabul 📩")
async def admission(message: types.Message, state: FSMContext):
    await message.answer(
        f"Hozirda qabul jarayoni yopiq ❗️\nQabul ochilganda bizning rasmiy kanalimizda habar beriladi.",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Rasmiy kanalimiz 🌐", url="https://t.me/asaka11idumi"
                    )
                ]
            ]
        ),
    )


@dp.message(F.text == "Biz haqimizda 💠")
async def teachers_section(message: types.Message, state: FSMContext):
    await message.answer(f"11 - IDUMI haqida ma'lumotlar: \n\n"
                         f"👉 Tashkil etilgan yil: 1995 yil\n"
                         f"Hozirda faoliyat ko'rsatayotgan o'qituvchilar: 28 ta"
                         f"O'quvchilar soni: 280(2024-2025 o'quv yili)\n\n"
                         f"Bitiruvchilar soni: 87 ta\n"
                         f"Ulardan o'qishga kirganlar soni: N ta\n")


# @dp.message(F.text == "O'qituvchilar uchun parol ✍️")
# @admin_required()
# async def password_change_section(message: types.Message, state: FSMContext):
#     conn = sqlite3.connect("users_database.db")
#     cursor = conn.cursor()
#     cursor.execute(
#         "SELECT * FROM passwords",
#     )
#     data = cursor.fetchone()
#     if not data:
#         await message.answer("Hozirda qarol o'rnatilmagan, iltimos uni kiriting.")
#         await state.set_state(wait_for_password.password)
#     else:
#         await message.answer(
#             f"Hozirgi parol: `{data[0]}`\nAgar uni o'zgartirishni hohlasangiz quidagilardan birini tanlang 👇",
#             reply_markup=change_password_inline,
#             parse_mode="Markdown",
#         )


# @dp.message(F.text == "profil 👤")
# @parent_required()
# async def student_profile_show(message: types.Message, state: FSMContext):
#     user_id = message.from_user.id
#     student = get_student_by_parent_user_id(user_id)
#     if student:
#         full_name, passport_seria, grade, group_number = student
#         full_name = full_name.split()
#         if len(full_name) == 4:
#             name = full_name[1]
#         else:
#             name = full_name[1] + " " + full_name[2]
#         surname = full_name[0]

#         text = (
#             f"*👤 Profil:*\n"
#             f"*🎫 Ism:* {name}\n"
#             f"*ℹ️ Familiya:* {surname}\n"
#             f"*📄 Passport:* `{passport_seria}`\n"
#             f"*🎓 Sinf:* {grade}\n"
#         )
#     else:
#         text = "Sizning profilingiz topilmadi. Iltimos, avval ro'yxatdan o'ting."

#     await message.answer(text, parse_mode="Markdown")


# @dp.message(F.text == "bot haqida 💠")
# @parent_required()
# async def about_bot(message: types.Message, state: FSMContext):
#     await message.answer(
#         f"Bu bot orqali quidagilarni amalga oshira olashingiz mumkin 👇\n\n 🔸 Farzandlarni kunlik kelib ketishlarini nazorat qilish\n\n 🔹 Maktabdan javob so'rash \n\n 🔺 Ma'muriyat bilan oson aloqaga chiqish"
#     )


# @dp.message(F.text == "Hisobdan chiqish 🔚")
# @parent_required()
# async def log_out_account(message: types.Message, state: FSMContext):
#     await message.answer(
#         "Rostan ham hisobdan chiqishni hohlaysizmi ❓\n",
#         reply_markup=InlineKeyboardMarkup(
#             inline_keyboard=[
#                 [
#                     InlineKeyboardButton(
#                         text="Ha ✅", callback_data="confirm_log_out_parent"
#                     ),
#                     InlineKeyboardButton(
#                         text="Yo'q ❌", callback_data="cancel_log_out_parent"
#                     ),
#                 ],
#             ]
#         ),
#     )


# @dp.message(F.text == "davomat hisoboti 📊")
# @parent_required()
# async def davomat_hisoboti(message: types.Message, state: FSMContext):
#     await message.answer(f"Turniket ishga tushishi kutilmoqda ...🛠")


# @dp.message(F.text == "javob so'rash 🙋‍♂️")
# @parent_required()
# async def asking_to_stay_home(message: types.Message, state: FSMContext):
#     await message.answer(f"Turniket ishga tushishi kutilmoqda ...🛠")


# @dp.message(F.text == "statistika 📊")
# @teacher_required()
# async def statistics_teacher(message: types.Message, state: FSMContext):
#     await message.answer(
#         f"📊 *Bot statistikasi:*\n\n"
#         f"👤 *Jami o'quvchilar soni:* {count_of_students()}\n"
#         f"👨‍👩‍👧‍👦 *Botdagi ota-onalar:* {count_of_parents()}\n\n"
#         f"{count_students_by_grade()}",
#         parse_mode="Markdown",
#     )


# @dp.message(F.text == "Profildan chiqish 🔙")
# @teacher_required()
# async def log_out_account_teacher(message: types.Message, state: FSMContext):
#     await message.answer(
#         "Rostan ham hisobdan chiqishni hohlaysizmi ❓\n",
#         reply_markup=InlineKeyboardMarkup(
#             inline_keyboard=[
#                 [
#                     InlineKeyboardButton(
#                         text="Ha ✅", callback_data="confirm_log_out_teacher"
#                     ),
#                     InlineKeyboardButton(
#                         text="Yo'q ❌", callback_data="cancel_log_out_teacher"
#                     ),
#                 ],
#             ]
#         ),
#     )

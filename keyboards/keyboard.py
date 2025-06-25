from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_menu_parent = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="davomat hisoboti 📊"),
        ],
        [
            KeyboardButton(text="javob so'rash 🙋‍♂️"),
            KeyboardButton(text="profil 👤"),
        ],
        [
            KeyboardButton(text="bot haqida 💠"),
            KeyboardButton(text="aloqaga chiqish 📞"),
        ],
        [
            KeyboardButton(text="Savol so'rash ❓"),
            KeyboardButton(text="Hisobdan chiqish 🔚"),
        ],
    ],
    resize_keyboard=True,
)

main_menu_teacher = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="davomat 📝"),
            KeyboardButton(text="sinflar 🧑‍🎓"),
        ],
        [
            KeyboardButton(text="statistika 📊"),
        ],
        [
            KeyboardButton(text="Profildan chiqish 🔙"),
        ],
    ],
    resize_keyboard=True,
)

main_menu_admin = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Hisobot 🗒"),
            KeyboardButton(text="statistika ⭐️"),
        ],
        [
            KeyboardButton(text="o'quvchilar ID kartalari 💳"),
            KeyboardButton(text="o'qituvchilar uchun parol ✍️"),
        ],
        [
            KeyboardButton(text="o'quvchilar baza 📫"),
            KeyboardButton(text="Habar yuborish 📤"),
        ],
    ],
    resize_keyboard=True,
)

cancel_for_admin_panel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="bekor qilish 🔙"),
        ]
    ],
    resize_keyboard=True,
)

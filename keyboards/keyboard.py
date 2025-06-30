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
            KeyboardButton(text="Statistika ⭐️"),
            KeyboardButton(text="O'qituvchilar uchun parol ✍️"),
        ],
        [
            KeyboardButton(text="O'quvchilar baza 📫"),
            KeyboardButton(text="Habar yuborish 📤"),
        ],
        [
            KeyboardButton(text="Adminlikdan chiqish 🔙"),
            KeyboardButton(text="Adminlar paneli 📋"),
        ],
    ],
    resize_keyboard=True,
)

adminlar_paneli = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Admin qoshish ➕"),
            KeyboardButton(text="Adminlarni ko'rish 📋"),
            KeyboardButton(text="Asosiy menuga qaytish 🔙"),
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

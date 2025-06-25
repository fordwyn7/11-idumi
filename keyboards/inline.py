import sqlite3
import asyncio
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

select_level_users = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Ota - Ona 👥", callback_data="level_parent"),
        ],
        [
            InlineKeyboardButton(text="O'qituvchi 👨‍🏫", callback_data="level_teacher"),
        ],
    ]
)

change_password_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text = "random 🎲", callback_data="changepass_random"),
        ], 
        [
            InlineKeyboardButton(text = "qolda kiritish ✍️", callback_data="changepass_mannual"),
        ]
    ]
)

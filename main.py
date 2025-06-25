from keyboards.keyboard import *
from keyboards.inline import *
from config import *
from states.state import *
from functions import *

import sqlite3
import logging
import database
import handlers
import asyncio
import keyboards.queries
import states.state_handler
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id 
    if is_user_registered(user_id):
        level = get_level_user(user_id)
        if level == "parent":
            await message.answer("Siz bosh menudasiz 👇", reply_markup=main_menu_parent)
        elif level == "teacher":
            await message.answer("Siz bosh menudasiz 👇", reply_markup=main_menu_teacher)
        else:
            await message.answer("Siz bosh menudasiz 👇", reply_markup=main_menu_admin)
    else:
        await message.answer("Assalomu alaykum 👋\n11 - IDUMIning rasmiy botiga hush kelibsiz 😊\nBotga kim sifatida kirmoqdasiz ? 👇", reply_markup=select_level_users)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandStart, CommandObject
from datetime import datetime, timedelta
from aiogram import types
from aiogram.types import ReplyKeyboardRemove



bot = Bot(token="7501290180:AAGat34VYCh2d3F1NuXe0IJqCh1IGdm2wYo")
dp = Dispatcher(storage=MemoryStorage())
# dp.include_router(dp)
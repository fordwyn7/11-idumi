import sqlite3
from functions import *
from functools import wraps
from config import *

def admin_required():
    def decorator(handler):
        @wraps(handler)
        async def wrapper(message: types.Message, *args, **kwargs):
            admin_list = list(get_admins())
            user_id = message.from_user.id
            if not user_id in admin_list:
                return
            return await handler(message, *args, **kwargs)
        return wrapper
    return decorator

def teacher_required():
    def decorator(handler):
        @wraps(handler)
        async def wrapper(message: types.Message, *args, **kwargs):
            teacher_list = list(get_tachers())
            user_id = message.from_user.id
            if not user_id in teacher_list:
                return
            return await handler(message, *args, **kwargs)
        return wrapper
    return decorator

def parent_required():
    def decorator(handler):
        @wraps(handler)
        async def wrapper(message: types.Message, *args, **kwargs):
            parents_list = list(get_parents())
            user_id = message.from_user.id
            if not user_id in parents_list:
                return
            return await handler(message, *args, **kwargs)
        return wrapper
    return decorator
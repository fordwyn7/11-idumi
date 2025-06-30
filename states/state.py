from aiogram.fsm.state import State, StatesGroup

class choose_level(StatesGroup):
    password = State()
    
class wait_for_password(StatesGroup):
    password = State()
    
class confirm_jshshir(StatesGroup):
    number = State()
    
class ask_question(StatesGroup):
    question = State()
    
class send_message(StatesGroup):
    msg = State()
    seria = State()
    
class add_admin_state(StatesGroup):
    admin_id = State()
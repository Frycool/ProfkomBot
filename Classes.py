from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup

class IsAdmin(BaseFilter):
    def __init__(self, admin_ids: list[int]) -> None:
        # В качестве параметра фильтр принимает список с целыми числами
        self.admin_ids = admin_ids

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_ids

class FSMFillForm(StatesGroup):

    FIO = State()        # ФИО
    study_form = State()         # Форма обучения
    que = State()        # Собственно вопрос


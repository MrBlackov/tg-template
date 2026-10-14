from aiogram.types import CopyTextButton, InlineKeyboardButton, InlineKeyboardMarkup

from app.tg.callback.main import MyStateCall, BackCall
from app.tg.buttons.base import BotIKB, MenuCall

class MainIKB(BotIKB):    
    def back(self, where: str):
        return self.builder.button(text='↩️ Назад', callback_data=BackCall(where=where, tg_id=self.tg_id)).as_markup()

    def my_state(self):
        return self.builder.button(text='🔄️ Обновить', callback_data=MyStateCall(tg_id=self.tg_id)).as_markup()
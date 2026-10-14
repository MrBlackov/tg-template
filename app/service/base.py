import asyncio, functools
from typing import TypeVar
from datetime import datetime
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InputRichMessage
from aiogram.filters import CommandStart, Command, CommandObject

from config import settings, bot
from app.logging.base import botlog
from app.tg.buttons.base import BotIKB
from app.tg.fsm.utils import FSMUtils
from app.validate.tg import Answer, AnswerBody

NOT_NEW_STATE = object()
DATA_PAGE = TypeVar('DATA_PAGE')

class BaseService:
    asyncio = asyncio
    datetime = datetime
    botlog = botlog

    def __init__(self, 
                 message: Message, 
                 state: FSMContext | None = None, 
                 callback: CallbackQuery | None = None, 
                 command: CommandObject | None = None, 
                 **kwargs):
        self.settings = settings
        self.bot = bot
        self.message = message
        self.callback = callback
        self.command = command
        self.kwargs = kwargs

        self.user = self.callback.from_user if self.callback else self.message.from_user
        self.chat = self.callback.message.chat if self.callback else self.message.chat
        self.tg_id = self.user.id

        self.is_bot_message = bool(self.callback)
        self.enter_args: bool = self.command.args != None if command else False
        self.to_edit_message: bool = self.kwargs.get('to_edit_message', bool(self.callback))

        self.fsm: FSMUtils = FSMUtils(state)
        self.IKB = BotIKB(self.tg_id)
        self.text = None
        self.logic = None

    @property
    def purpose(self):
        if self.message.reply_to_message and self.message.is_topic_message and self.kwargs.get('is_reply'):
            return self.message.reply_to_message.from_user
        elif self.message.reply_to_message and not self.message.is_topic_message:
            return self.message.reply_to_message.from_user
        else:
            return self.user

    @property
    def is_admin(self):
        return self.tg_id in self.settings.admins

    async def text_boardcast(self, answer_body_list: list[Answer], delay: int = 20):
        k = 0
        results: list[Message] = []
        for body in answer_body_list:
            k += 1
            if body.is_reply_answer:
                msg = await self.bot.send_message(text=body.text, reply_markup=body.reply_markup, reply_to_message_id=body.message_id, chat_id=body.chat_tg_id)
            elif body.is_rich_text and body.edit_message:
                msg = await self.bot.edit_message_text(rich_message=InputRichMessage(html=body.text), reply_markup=body.reply_markup, chat_id=body.chat_tg_id, message_id=body.message_id)
            elif body.is_rich_text:
                msg = await self.bot.send_rich_message(rich_message=InputRichMessage(html=body.text), reply_markup=body.reply_markup, chat_id=body.chat_tg_id)
            elif body.edit_message:
                msg = await self.bot.edit_message_text(text=body.text, reply_markup=body.reply_markup, chat_id=body.chat_tg_id, message_id=body.message_id)
            else:
                msg = await self.bot.send_message(text=body.text, reply_markup=body.reply_markup, chat_id=body.chat_tg_id)
            results.append(msg)
            if k%delay == 0:
                await asyncio.sleep(2)
        return results

    def to_pages(self, datas: list[DATA_PAGE], value_in_page: int = 5) -> list[tuple[DATA_PAGE, ...]]:
        return [tuple(datas[i:i+value_in_page]) for i in range(0, len(datas), value_in_page)] if datas else []

    async def answer(self, answer_body_list: list[AnswerBody]):
        return await self.text_boardcast([
            Answer(
                chat_tg_id=self.chat.id, 
                _user_tg_id=self.tg_id, 
                message_id=self.message.message_id, 
                edit_message=self.to_edit_message,

                text=body.text, 
                reply_markup=body.reply_markup,
                is_rich_text=body.is_rich_text, 
                is_reply_answer=body.is_reply_answer, 
                ) for body in answer_body_list
                ])

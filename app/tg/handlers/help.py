from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from telegram_click_aio.decorator import command

from app.service.help import HelpService
from app.tg.middlewares import ServiceMiddleware
from app.tg.args import base_args, Optionals, Requireds

help_router = Router()

help_router.message.middleware(ServiceMiddleware(HelpService))
help_router.callback_query.middleware(ServiceMiddleware(HelpService))

@help_router.message(Command('help'))
@command(name='help', arguments=base_args, description='')
async def cmd(message: Message, service: HelpService, **kwargs):
    await service.main()

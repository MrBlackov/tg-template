from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.service.help import HelpService

help_router = Router()

@help_router.message(Command('help'))
async def cmd(message: Message, state: FSMContext):
    await HelpService(message, state).main()

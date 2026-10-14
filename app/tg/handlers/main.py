from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.service.main import MainService
from app.tg.callback.main import MyStateCall

main_router = Router()

@main_router.message(Command('mystate'))
async def cmd(message: Message, state: FSMContext, **kwargs):
    await MainService(message, state, **kwargs).my_state()
    
@main_router.callback_query(MyStateCall.filter())     
async def call(callback: CallbackQuery, callback_data: MyStateCall, state: FSMContext, **kwargs):
    await MainService(callback.message, state, callback, **kwargs).my_state()

@main_router.message(Command('mystateclear'))
async def cmd(message: Message, state: FSMContext, **kwargs):
    await MainService(message, state, **kwargs).my_state_clear()


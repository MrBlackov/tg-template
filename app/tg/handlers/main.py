from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from telegram_click_aio.decorator import command

from app.service.main import MainService
from app.tg.callback.main import MyStateCall
from app.tg.middlewares import ServiceMiddleware
from app.tg.args import base_args, Optionals, Requireds
 
main_router = Router()

main_router.message.middleware(ServiceMiddleware(MainService))
main_router.callback_query.middleware(ServiceMiddleware(MainService))

@main_router.message(CommandStart(deep_link=False))
@command(name='start', description='')
async def cmd(message: Message, service: MainService, **kwargs):
    await service.start()

@main_router.message(Command('redactstate'))
@command(name='redactstate', arguments=[Requireds.key, Requireds.value], description='')
async def cmd(message: Message, service: MainService, key: str, value: str, **kwargs):
    await service.add_state(key, value)

@main_router.message(Command('mystate'))
@command(name='mystate', arguments=base_args, description='')
async def cmd(message: Message, service: MainService, **kwargs):
    await service.my_state()
    
@main_router.callback_query(MyStateCall.filter())  
async def call(callback: CallbackQuery, callback_data: MyStateCall, service: MainService, **kwargs):
    await service.my_state()

@main_router.message(Command('mystateclear'))
@command(name='mystateclear', arguments=base_args, description='')
async def cmd(message: Message, service: MainService, **kwargs):
    await service.my_state_clear()


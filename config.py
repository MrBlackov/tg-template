import os, redis.asyncio as redis, asyncio
from dotenv import load_dotenv
from pathlib import Path
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (BotCommand, 
                           BotCommandScopeChat, 
                           BotCommandScopeAllPrivateChats, 
                           BotCommandScopeAllGroupChats, 
                           BotCommandScopeAllChatAdministrators,
                           User)
from aiogram.exceptions import TelegramBadRequest
from aiogram.client.session.aiohttp import AiohttpSession
from app.logging.base import botlog

load_dotenv(Path(__file__).parent / '.env')

class Settings:
    bot_token = os.getenv('bot_token')
    dev_bot_token = os.getenv('dev_bot_token', bot_token)
    _is_dev = os.getenv('is_dev', 'f')

    admins = [int(x) for x in os.getenv('admins').split(',')]
    owner = int(os.getenv('owner'))

    _use_proxy = os.getenv('use_proxy', 'f')
    proxy_url = os.getenv('proxy_url')

    _use_redis = os.getenv('use_redis', 'f')
    redis_url = os.getenv('redis_url')
    state_ttl = os.getenv('state_ttl', 60*60*24)
    data_ttl = os.getenv('data_ttl', 60*60*24)

    docs_url = os.getenv('docs_url')

    db_user = os.getenv('db_user')
    db_password = os.getenv('db_password')
    db_host = os.getenv('db_host')
    db_port = os.getenv('db_port')
    db_name = os.getenv('db_name')  
    database_url = os.getenv('database_url')  
    db_drivers = os.getenv('db_drivers', 'postgresql+asyncpg://')  

    info: dict = {}

    @property
    def is_dev(self):
        return True if self._is_dev in ['t', 'true', '1'] else False

    @property
    def token(self):
        return self.dev_bot_token if self.is_dev else self.bot_token

    @property
    def use_redis(self):
        return True if self._use_redis in ['t', 'true', '1'] else False
    
    @property
    def use_proxy(self):
        return True if self._use_proxy in ['t', 'true', '1'] else False

    @property
    def db_url(self):
        return f"{self.db_drivers}{self.database_url}" or f"{self.db_drivers}{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    @property
    def bot(self) -> User:
        return self.info.get('main')
    
settings = Settings()

if settings.use_proxy:
    bot_session = AiohttpSession(proxy=settings.proxy_url)
else:
    bot_session = AiohttpSession()

if settings.use_redis:
    storage = RedisStorage(
        redis=redis.from_url(settings.redis_url),
        state_ttl=settings.state_ttl,
        data_ttl=settings.data_ttl
    )
else:
    storage = MemoryStorage()

bot = Bot(token=settings.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML, link_preview_is_disabled=True), session=bot_session)
dp = Dispatcher(storage=storage)

cmds = {
    'help':'📚 Получить справку',
}

admin_cmds = cmds | {
    'mystate':'🗂️ Ваши куки',
    'mystateclear':'🗑️ Очистить куки',
}

async def to_menu_cmds():
    admin_menu = [BotCommand(command=cmd, description=desc) for cmd, desc in admin_cmds.items()]
    user_menu = [BotCommand(command=cmd, description=desc) for cmd, desc in cmds.items()]
    [await bot.set_my_commands(admin_menu, scope=BotCommandScopeChat(chat_id=admin)) for admin in settings.admins]
    await bot.set_my_commands(user_menu, scope=BotCommandScopeAllGroupChats())
    await bot.set_my_commands(user_menu, scope=BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(user_menu, scope=BotCommandScopeAllChatAdministrators())

async def update_bot_info():
    try:
        bot_info = await bot.get_me()
        settings.info['main'] = bot_info
        return bot_info
    except TelegramBadRequest: 
        botlog.logger.critical('Телеграм недоступен')
        await bot.session.close()        
        asyncio.get_running_loop().stop()

import asyncio

from config import dp, bot, to_menu_cmds
from app.tg.handlers.base import base_router
from app.tg.middlewares import (BotLogMessageMiddleware, 
                                BotLogCallbackQueryMiddleware, 
                                ExceptionMessageMiddleware, 
                                ExceptionCallbackQueryMiddleware,
                                UserMiddleware)
from app.logging.base import botlog

@botlog.logger.catch(reraise=True)
async def main():
    dp.message.middleware(BotLogMessageMiddleware())
    dp.callback_query.middleware(BotLogCallbackQueryMiddleware())
    dp.message.middleware(ExceptionMessageMiddleware())
    dp.callback_query.middleware(ExceptionCallbackQueryMiddleware())
    dp.update.middleware(UserMiddleware())
    dp.include_router(base_router) 
    botlog.start()
    await bot.delete_webhook(drop_pending_updates=True)
    await to_menu_cmds()
    await dp.start_polling(bot)

@dp.shutdown()
async def stop(bot):
    await dp.storage.close()
    botlog.stop()

if __name__ == "__main__": 
    try:
        asyncio.run(main())
    except RuntimeError as e:
        botlog.stop()
    



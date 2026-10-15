import asyncio

from config import dp, bot, to_menu_cmds, settings, botlog, update_bot_info
from app.tg.handlers.base import base_router
from app.tg.middlewares import (BotLogMessageMiddleware, 
                                BotLogCallbackQueryMiddleware, 
                                ExceptionMessageMiddleware, 
                                ExceptionCallbackQueryMiddleware,
                                UserMiddleware)
from app.db.base import engine

@botlog.logger.catch(reraise=True)
async def main():
    botlog.logger.info('Бот запускается')
    bot_info = await update_bot_info()
    if bot_info:
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
    await engine.dispose()

if __name__ == "__main__": 
    asyncio.run(main())

    



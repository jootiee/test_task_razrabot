import asyncio
import logging
from bot import bot, dp, setup_routers

logging.basicConfig(level=logging.INFO)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    setup_routers()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
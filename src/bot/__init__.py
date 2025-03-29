from aiogram import Bot, Dispatcher, Router
from config import BOT_TOKEN
from wb import WBApi
from utils import Analyzer, Formatter

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

router = Router()

analyzer = Analyzer()
formatter = Formatter(analyzer)
wb_api = WBApi(analyzer=analyzer)

def setup_routers():
    from bot.handlers import router as handlers_router
    dp.include_router(handlers_router)

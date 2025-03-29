import logging
import asyncio
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command  # Import Command filter
from wb import WBApi
from utils import Analyzer, Formatter
from config import BOT_TOKEN

# Initialize logging
logging.basicConfig(level=logging.INFO)


# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
router = Router()

# Initialize API components
analyzer = Analyzer()
formatter = Formatter(analyzer)
wb_api = WBApi(analyzer=analyzer)

@router.message(Command(commands=["help"]))
async def help(message: types.Message):
    """
    Handle /help command.
    """
    await message.answer(
        "You can use the following commands:\n"
        "/search <query> - Search for products by query\n"
        "/get_ids <query> - Get product IDs for a query"
    )

@router.message()
async def search_products(message: types.Message):
    """
    Handle /search command to search for products.
    """
    if not formatter.is_valid_url(message.text): 
        await message.answer("Please provide a valid url.\nExample: https://www.wildberries.ru/catalog/221713845/detail.aspx")
        return
    
    nmId = formatter.extract_nmid_from_url(message.text)
    card = wb_api.get_card(nmId)
    if card is None:
        await message.answer("Product not found.")
        return

    tags = formatter.extract_tags_from_card(card)
    tags_frequencies = analyzer.get_frequencies(tags)

    response = f"Tags of {nmId}:\n"
    for tag, frequency in sorted(tags_frequencies.items(), key=lambda x: x[1], reverse=True)[:5]:
        response += f"- {tag}: {frequency}\n"
    await message.answer(response)

@router.message(Command(commands=["get_ids"]))
async def get_product_ids(message: types.Message):
    """
    Handle /get_ids command to extract product IDs.
    """
    query = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None
    if not query:
        await message.answer("Please provide a search query. Example: /get_ids iphone 12")
        return

    await message.answer(f"Fetching product IDs for '{query}'...")
    products = wb_api.get_products_by_query(query)
    if not products:
        await message.answer("No products found for your query.")
        return

    ids = formatter.extract_ids_from_products(products)
    response = "Product IDs:\n" + "\n".join(ids)
    await message.answer(response)

async def main():
    # Start the bot
    await bot.delete_webhook(drop_pending_updates=True)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

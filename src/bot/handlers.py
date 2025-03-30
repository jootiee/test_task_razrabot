from aiogram import types
from aiogram.filters import Command
from aiogram.types import CallbackQuery

from bot import router, wb_api, formatter, analyzer
from bot.keyboards import get_positions_keyboard
from constants import (
    HELP_MESSAGE, 
    INVALID_URL_MESSAGE, 
    PRODUCT_NOT_FOUND_MESSAGE,
    MAX_TAGS
)

@router.message(Command(commands=["start", "help"]))
async def help_handler(message: types.Message):
    """
    Handle the /start and /help commands.
    
    Sends the help message to the user explaining what the bot does
    and how to use it.
    
    Args:
        message (types.Message): The incoming message object.
    """
    await message.answer(HELP_MESSAGE)

@router.message()
async def search_products(message: types.Message):
    """
    Process messages sent by users and expects URL.
    
    This handler:
    1. Validates the URL format
    2. Extracts product ID from the URL
    3. Fetches product data from API
    4. Extracts and analyzes meaningful tags
    5. Responds with the top tags and their frequencies
    
    Args:
        message (types.Message): The incoming message object.
    """
    if not formatter.is_valid_url(message.text): 
        await message.answer(INVALID_URL_MESSAGE)
        return
    
    nm_id = formatter.extract_nm_id_from_url(message.text)
    card = wb_api.get_card(nm_id)
    if card is None:
        await message.answer(PRODUCT_NOT_FOUND_MESSAGE)
        return

    tags = formatter.extract_tags_from_card(card)
    tags_frequencies = sorted(analyzer.get_frequencies(tags).items(), key=lambda x: x[1], reverse=True)[:MAX_TAGS]

    response = f"Tags of {nm_id}:\n"
    for tag, frequency in tags_frequencies:
        response += f"- {tag}: {frequency}\n"

    keyboard = get_positions_keyboard(nm_id)
    await message.answer(response, reply_markup=keyboard)

@router.callback_query(lambda c: c.data.startswith("positions-"))
async def get_positions(callback_query: CallbackQuery):
    """
    Handle "Get Positions" button clicks and show product positions in search results.
    
    This callback:
    1. Extracts the product ID from the callback data
    2. Re-fetches the product data from API
    3. Finds product position in search results for each tag
    4. Updates the message with position information progressively
    
    Args:
        callback_query (CallbackQuery): The callback query from the button press.
    """
    nm_id = int(callback_query.data.split("-")[1])
    card = wb_api.get_card(nm_id)
    if card is None:
        await callback_query.message.answer(PRODUCT_NOT_FOUND_MESSAGE)
        return

    tags = formatter.extract_tags_from_card(card)
    tags_frequencies = sorted(analyzer.get_frequencies(tags).items(), key=lambda x: x[1], reverse=True)[:MAX_TAGS]

    text = f"Positions in search for {nm_id}:\n"
    msg = await callback_query.message.answer(text)
    for tag, _ in tags_frequencies:
        page, pos = wb_api.get_position_in_search(nm_id, tag)
        if page == -1 and pos == -1:
            text += f"- {tag}: Not found\n"
        else:
            text += f"- {tag}: Page {page}, #{pos}\n"
        await msg.edit_text(text)
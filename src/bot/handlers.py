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
    await message.answer(HELP_MESSAGE)

@router.message()
async def search_products(message: types.Message):
    if not formatter.is_valid_url(message.text): 
        await message.answer(INVALID_URL_MESSAGE)
        return
    
    nmId = formatter.extract_nmid_from_url(message.text)
    card = wb_api.get_card(nmId)
    if card is None:
        await message.answer(PRODUCT_NOT_FOUND_MESSAGE)
        return

    tags = formatter.extract_tags_from_card(card)
    tags_frequencies = sorted(analyzer.get_frequencies(tags).items(), key=lambda x: x[1], reverse=True)[:MAX_TAGS]

    response = f"Tags of {nmId}:\n"
    for tag, frequency in tags_frequencies:
        response += f"- {tag}: {frequency}\n"

    keyboard = get_positions_keyboard(nmId)
    await message.answer(response, reply_markup=keyboard)

@router.callback_query(lambda c: c.data.startswith("positions-"))
async def get_positions(callback_query: CallbackQuery):
    nmId = int(callback_query.data.split("-")[1])
    card = wb_api.get_card(nmId)
    if card is None:
        await callback_query.message.answer(PRODUCT_NOT_FOUND_MESSAGE)
        return

    tags = formatter.extract_tags_from_card(card)
    tags_frequencies = sorted(analyzer.get_frequencies(tags).items(), key=lambda x: x[1], reverse=True)[:MAX_TAGS]

    text = f"Positions in search for {nmId}:\n"
    msg = await callback_query.message.answer(text)
    for tag, _ in tags_frequencies:
        page, pos = wb_api.get_position_in_search(nmId, tag)
        if page == -1 and pos == -1:
            text += f"- {tag}: Not found\n"
        else:
            text += f"- {tag}: Page {page}, #{pos}\n"
        await msg.edit_text(text)
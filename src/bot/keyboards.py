from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_positions_keyboard(nm_id):
    """Create keyboard with 'Get Positions' button"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Get Positions", callback_data=f"positions-{nm_id}")]
    ])

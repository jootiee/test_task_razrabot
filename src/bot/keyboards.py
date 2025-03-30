from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_positions_keyboard(nm_id):
    """
    Create an inline keyboard with 'Get Positions' button for a specific product.
    
    Args:
        nm_id: The product ID to associate with the callback data.
        
    Returns:
        InlineKeyboardMarkup: A keyboard with a single button to get positions.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Get Positions", callback_data=f"positions-{nm_id}")]
    ])

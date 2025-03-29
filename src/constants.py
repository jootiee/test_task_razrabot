# URLs
CATALOG_URL_PATTERN = r"https://www\.wildberries\.ru/catalog/(\d+)/detail\.aspx(?:\?[^/]*)?$"
SEARCH_URL_TEMPLATE = "https://search.wb.ru/exactmatch/ru/common/v9/search?ab_testing=false&appType=1&curr=rub&dest=-1257786&hide_dtype=13&lang=ru&page={}&query={}&resultset=catalog&sort=popular&spp=30&suppressSpellcheck=false"
CARD_URL_TEMPLATE = "https://basket-{}.wbbasket.ru/vol{}/part{}/{}/info/ru/card.json"

NM_ID_RANGES = [
    (0, 14399999),
    (14400000, 28799999),
    (28800000, 43199999),
    (43200000, 71999999),
    (72000000, 100799999),
    (100800000, 106199999),
    (106200000, 111599999),
    (111600000, 116999999),
    (117000000, 131399999),
    (131400000, 160199999),
    (160200000, 165599999),
    (165600000, 191999999),
    (192000000, 204599999),
    (204600000, 218999999),
    (219000000, 240599999),
    (240600000, 262199999),
    (262200000, 283799999),
    (283800000, 305399999),
    (305400000, 326999999),
    (327000000, 348599999),
    (348600000, 370199999),
    (370200000, 391799999),
    (391800000, 413399999),
    (413400000, 434999999),
    (435000000, 456599999)
]

# Product data fields
PRODUCT_FIELDS = ["imt_name", "subj_name", "description", "subj_root_name", "contents"]

# Valid parts of speech for tags
VALID_PARTS_OF_SPEECH = {"NOUN", "ADJF", "ADJS", "NUMR", "VERB", "INFN", "PRTF", "PRTS", "GRND", "ADVB"}

# Message templates
HELP_MESSAGE = """
This bot provides tags of Wildberries item and its position in search by retrieved keywords.
Send item link to proceed.
Example: https://www.wildberries.ru/catalog/12345/detail.aspx
"""

INVALID_URL_MESSAGE = "Please provide a valid url.\nExample: https://www.wildberries.ru/catalog/12345/detail.aspx"
PRODUCT_NOT_FOUND_MESSAGE = "Product not found."

# Default values and limits
MAX_TAGS = 5

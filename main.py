import requests
import re
import pymorphy2
from math import log10
from time import sleep
from random import randint

morph = pymorphy2.MorphAnalyzer()

def get_api_endpoint(nmId: int) -> str:
    """
    Generate the API endpoint URL for a given nmId.

    The generated URL follows the format:
    "https://basket-{}.wbbasket.ru/vol{}/part{}/{}/info/ru/card.json".

    - `{}` (basket number): Determined by the index of the range in which `nmId` falls.
    - `{}` (vol): Calculated based on the first `slice_range` digits of `nmId`.
    - `{}` (part): Calculated based on the first `slice_range + 2` digits of `nmId`.
    - `{}` (full nmId): The full `nmId` value.

    Args:
        nmId (int): The unique identifier of the item.

    Returns:
        str: The API endpoint URL for the item, or None if `nmId` does not fall within any range.
    """
    ranges = [
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

    url = "https://basket-{}.wbbasket.ru/vol{}/part{}/{}/info/ru/card.json"
    slice_range = int(log10(nmId)) - 4
    for idx, (a, b) in enumerate(ranges):
        if a <= nmId <= b:
            return url.format(str(idx + 1).zfill(2),
                              str(nmId)[:slice_range],
                              str(nmId)[:2 + slice_range],
                              nmId)
    return None


def format_string(string: str) -> str:
    """
    Format a string by removing non-alphabetic characters and converting to lowercase.

    Args:
        string (str): The input string to format.

    Returns:
        str: The formatted string.
    """
    return re.sub(r"[^a-zA-Zа-яА-Я]", " ", string).lower()


def extract_lines_from_dict(data: dict) -> list:
    """
    Extract relevant text fields from a dictionary and split them into words.

    Args:
        data (dict): The dictionary containing item data.

    Returns:
        list: A list of words extracted from the specified fields.
    """
    fields = ["imt_name", "subj_name", "description", "subj_root_name", "contents"]
    words = []
    for field in fields:
        words.extend(data.get(field, "").split())
    return words

def get_card(nmId: int) -> dict:
    """
    Fetch the item data from the API using the nmId.

    Args:
        nmId (int): The unique identifier of the item.

    Returns:
        dict: The JSON response containing item data.
    """
    url = get_api_endpoint(nmId)
    if url is None:
        return None
    req = requests.get(url)
    if req.status_code // 200 == 1:
        return req.json()
    return None

def get_tags(card: dict) -> list:
    """
    Extract tags from the item card.

    Args:
        card (dict): The dictionary containing item data.

    Returns:
        list: A list of meaningful words extracted from the item data.
    """
    words = extract_lines_from_dict(card)
    formatted_words = list()
    for word in words:
        if not word.isalpha():
            continue
        formatted_word = format_string(word)
        meaningful = is_meaningful_word(formatted_word)
        if len(formatted_word) and meaningful:
            formatted_words.append(formatted_word)
    return formatted_words


def get_frequencies(tags: list) -> dict:
    """
    Calculate the frequency of lemmatized words in a given list.

    Args:
        words (list): A list of words (strings) to process.

    Returns:
        dict: A dictionary containing lemmatized words as keys and their frequencies as values.
    """
    frequencies = dict()
    for tag in tags:
        lemma = morph.parse(tag)[0].normal_form
        frequencies[lemma] = frequencies.get(lemma, 0) + 1
    return frequencies

def is_meaningful_word(word: str) -> bool:
    """
    Check if a word is meaningful based on its part of speech.

    Args:
        word (str): The word to check.

    Returns:
        bool: True if the word is meaningful, False otherwise.
    """
    parsed = morph.parse(word)
    valid_pos = {"NOUN", "ADJF", "ADJS", "NUMR", "VERB", "INFN", "PRTF", "PRTS", "GRND", "ADVB"}
    return all(p.tag.POS in valid_pos for p in parsed if p.tag.POS is not None)
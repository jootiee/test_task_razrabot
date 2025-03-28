import requests

def get_api_endpoint(nmId: int) -> str:
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

    for idx, (a, b) in enumerate(ranges):
        if a <= nmId <= b:
            return url.format(str(idx + 1).zfill(2), str(nmId)[:2], str(nmId)[:4], nmId)
    return None

def format_string(string: str) -> str:
    return string.replace("\n", " ").replace("\r", " ").replace("\t", " ").lower()

def extract_words_from_json(data) -> list:
    words = []
    if isinstance(data, dict):
        for value in data.values():
            words.extend(extract_words_from_json(value))
    elif isinstance(data, list):
        for item in data:
            words.extend(extract_words_from_json(item))
    elif isinstance(data, str):
        words.extend(data.split())
    return words

def get_words(nmId: int) -> dict:
    url = get_api_endpoint(nmId)
    print(url)
    if url is None:
        return None
    response = requests.get(url).json()
    words = extract_words_from_json(response)
    formatted_words = [format_string(word) for word in words]
    return formatted_words

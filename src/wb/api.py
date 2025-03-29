import requests
from math import log10

from utils import Analyzer, Formatter 
from utils.config import proxies

class WBApi:
    def __init__(self, analyzer: Analyzer, proxies=None):
        """
        Initialize the WBApi class with optional proxy support.

        Args:
            proxies (dict, optional): A dictionary of proxies to use for requests.
        """
        self.proxies = proxies
        self.analyzer = Analyzer()

    def get_api_endpoint(self, nmId: int) -> str:
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


    def get_card(self, nmId: int) -> dict:
        """
        Fetch the item data from the API using the nmId.

        Args:
            nmId (int): The unique identifier of the item.

        Returns:
            dict: The JSON response containing item data.
        """
        url = WBApi.get_api_endpoint(nmId)
        if url is None:
            return None
        req = requests.get(url, proxies=self.proxies)
        if req.status_code // 200 == 1:
            return req.json()
        return None

    
    def get_products_by_query(self, query: str) -> list[dict]:
        url = "https://search.wb.ru/exactmatch/ru/common/v9/search?ab_testing=false&appType=1&curr=rub&dest=-1257786&hide_dtype=13&lang=ru&page=1&query={}&resultset=catalog&sort=popular&spp=30&suppressSpellcheck=false".format(query)
        req = requests.get(url, proxies=self.proxies)
        if req.status_code // 200 == 1:
            return req.json()["data"]["products"]
        return None

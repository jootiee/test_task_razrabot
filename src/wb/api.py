import requests
from math import log10

from utils import Analyzer
from config import proxies
from constants import NM_ID_RANGES, CARD_URL_TEMPLATE, SEARCH_URL_TEMPLATE 

class WBApi:
    def __init__(self, analyzer: Analyzer):
        """
        Initialize the WBApi class with optional proxy support.

        Args:
            proxies (dict, optional): A dictionary of proxies to use for requests.
        """
        self.proxies = proxies
        self.analyzer = Analyzer()

    def get_api_endpoint(self, nm_id: int) -> str:
        """
        Generate the API endpoint URL for a given nm_id.

        The generated URL follows the format:
        "https://basket-{}.wbbasket.ru/vol{}/part{}/{}/info/ru/card.json".

        - `{}` (basket number): Determined by the index of the range in which `nm_id` falls.
        - `{}` (vol): Calculated based on the first `slice_range` digits of `nm_id`.
        - `{}` (part): Calculated based on the first `slice_range + 2` digits of `nm_id`.
        - `{}` (full nm_id): The full `nm_id` value.

        Args:
            nm_id (int): The unique identifier of the item.

        Returns:
            str: The API endpoint URL for the item, or None if `nm_id` does not fall within any range.
        """
        slice_range = int(log10(nm_id)) - 4
        for idx, (a, b) in enumerate(NM_ID_RANGES):
            if a <= nm_id <= b:
                return CARD_URL_TEMPLATE.format(str(idx + 1).zfill(2),
                                            str(nm_id)[:slice_range],
                                            str(nm_id)[:2 + slice_range],
                                            nm_id)
        return None


    def get_card(self, nm_id: int) -> dict:
        """
        Fetch the item data from the API using the nm_id.

        Args:
            nm_id (int): The unique identifier of the item.

        Returns:
            dict: The JSON response containing item data.
        """
        url = self.get_api_endpoint(nm_id)
        if url is None:
            return None
        req = requests.get(url, proxies=self.proxies)
        if req.status_code // 200 == 1:
            return req.json()
        return None

    
    def get_products_by_query(self, query: str, page=1) -> list[dict]:
        """
        Fetch products from Wildberries search API based on a search query.
        
        Args:
            query (str): The search term to query for products.
            page (int, optional): Page number of the search results. Defaults to 1.
            
        Returns:
            list[dict]: A list of product dictionaries, or None if the request fails.
        """
        url = SEARCH_URL_TEMPLATE.format(page, query)
        req = requests.get(url, proxies=self.proxies)
        if req.status_code // 200 == 1:
            return req.json()["data"]["products"]
        return None

    def get_position_in_search(self, nm_id: int, tag: str) -> tuple[int, int]:
        """
        Find the position of a product in search results at pages 1-60 (61st is not available).
        
        Args:
            nm_id (int): The product ID to search for.
            tag (str): The search term to use.
            
        Returns:
            tuple[int, int]: A tuple of (page number, position on page),
                             or (-1, -1) if the product is not found.
        """
        for page in range(1, 61):
            products = self.get_products_by_query(tag, page=page)
            for position, product in enumerate(products):
                if product['id'] == nm_id:
                    return (page, position + 1)
        return (-1, -1)

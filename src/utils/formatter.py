import re
from utils import Analyzer
from constants import PRODUCT_FIELDS, CATALOG_URL_PATTERN

class Formatter:
    def __init__(self, analyzer: Analyzer):
        self.analyzer = analyzer

    def format_string(self, string: str) -> str:
        """
        Format a string by removing non-alphabetic characters and converting to lowercase.

        Args:
            string (str): The input string to format.

        Returns:
            str: The formatted string.
        """
        return re.sub(r"[^a-zA-Zа-яА-Я]", " ", string).lower()

    def extract_lines_from_dict(self, data: dict) -> list:
        """
        Extract relevant text fields from a dictionary and split them into words.

        Args:
            data (dict): The dictionary containing item data.

        Returns:
            list: A list of words extracted from the specified fields.
        """
        words = []
        for field in PRODUCT_FIELDS:
            words.extend(data.get(field, "").split())
        return words

    def extract_tags_from_card(self, card: dict) -> list:
        """
        Extract tags from the item card.

        Args:
            card (dict): The dictionary containing item data.

        Returns:
            list: A list of meaningful words extracted from the item data.
        """
        words = self.extract_lines_from_dict(card)
        formatted_words = list()
        for word in words:
            if not word.isalpha():
                continue
            formatted_word = self.format_string(word)
            meaningful = self.analyzer.is_meaningful_word(formatted_word)
            if len(formatted_word) and meaningful:
                formatted_words.append(formatted_word)
        return formatted_words

    def extract_ids_from_products(self, products: dict) -> list[str]:
        """
        Extract nm_ids from the products dictionary.

        Args:
            products (dict): The dictionary containing product data.

        Returns:
            list[str]: A list of nm_ids extracted from the products dictionary.
        """
        return [product["id"] for product in products]

    def is_valid_url(self, url: str) -> bool:
        """
        Validate if the given URL matches the Wildberries product URL pattern.

        Args:
            url (str): The URL to validate.

        Returns:
            bool: True if the URL matches the pattern, False otherwise.
        """
        return bool(re.match(CATALOG_URL_PATTERN, url))

    def extract_nm_id_from_url(self, url: str) -> int:
        """
        Extract the numeric product ID (nm_id) from a Wildberries product URL.
        
        Args:
            url (str): The Wildberries product URL.
            
        Returns:
            int: The extracted product ID as an integer.
        """
        return int(url.split("/")[-2])
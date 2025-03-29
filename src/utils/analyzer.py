import pymorphy2
from constants import VALID_PARTS_OF_SPEECH


class Analyzer:
    """
    A utility class for text analysis, including lemmatization and filtering meaningful words.

    This class uses the `pymorphy2` library to process Russian text. It provides methods to:
    - Calculate the frequency of lemmatized words in a list.
    - Determine if a word is meaningful based on its part of speech.

    Attributes:
        morph (pymorphy2.MorphAnalyzer): An instance of the pymorphy2 morphological analyzer.
    """
    def __init__(self):
        self.morph = pymorphy2.MorphAnalyzer()

    def get_frequencies(self, tags: list) -> dict:
        """
        Calculate the frequency of lemmatized words in a given list.

        Args:
            tags (list): A list of words (strings) to process.

        Returns:
            dict: A dictionary containing lemmatized words as keys and their frequencies as values.
        """
        frequencies = dict()
        for tag in tags:
            lemma = self.morph.parse(tag)[0].normal_form
            frequencies[lemma] = frequencies.get(lemma, 0) + 1
        return frequencies

    def is_meaningful_word(self, word: str) -> bool:
        """
        Check if a word is meaningful based on its part of speech.

        Args:
            word (str): The word to check.

        Returns:
            bool: True if the word is meaningful, False otherwise.
        """
        parsed = self.morph.parse(word)
        return all(p.tag.POS in VALID_PARTS_OF_SPEECH for p in parsed if p.tag.POS is not None)
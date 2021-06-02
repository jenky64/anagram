#!/usr/bin/python3

from pprint import pprint
from itertools import combinations
from anagram.model import database, Words
from peewee import *


class Generator:
    """
    A simple anagram generator.

    The generator works by sorting the characters in
    alphabetical order and then finding all words
    in a datastore that have the same sort sequence.

    Example:
    To get all the 4 letter anagrams of the word
    'stop', we do the following:
    1) alphabetically sort the word -> 'opst'
    2) search the datastore for all the words
       that have the same sorted value
    3) select * from words where anagram = 'opst';
       103163|opts|4|opst
       116133|post|4|opst
       116563|pots|4|opst
       144805|spot|4|opst
       146935|stop|4|opst
       156928|tops|4|opst

    So, opts, post, pots, spot, and tops
    are all anagrams of 'stop'

    The generator allows for subsets of the word.
    For example, three letter anagrams of the word
    'stop' would search for words with the following
    alphabetical sorts
    ops -> ops, sop, pos
    opt -> opt, pot, top
    ost -> sot
    pst -> pst
    """
    def __init__(self,
                 word: str = None,
                 min_size: int = 2,
                 max_size: int = None,
                 size: int = None,
                 dbname: str= None) -> None:
        """
        initialize the generator

        :param word: str: word to anagram
        :param min_size: int: minimum anagram size
        :param max_size: int: maximum anagram size
        :param size: int: absolute anagram size
        :param dbname: str: database to use
        """
        self.database = database
        self.words = Words

        self.word = word
        self.min_size = min_size
        self.max_size = max_size
        self.size = size
        self.db_name = dbname
        self.word_count = 0
        self.max_word_length = 0
        self.anagrams: dict = dict()

        self.initialize_db(self.db_name)

        # set word and sizing if values provided
        if word is not None:
            self.set_word(word, min_size, max_size, size)
        else:
            self.word = None

    @property
    def word(self):
        return self._word

    @word.setter
    def word(self, val):
        self._word = val

    @property
    def min_size(self):
        return self._min_size

    @min_size.setter
    def min_size(self, val):
        self._min_size = val

    @property
    def max_size(self):
        return self._max_size

    @max_size.setter
    def max_size(self, val):
        self._max_size = val

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, val):
        self._size = val

    @property
    def word_count(self):
        return self._word_count

    @word_count.setter
    def word_count(self, val):
        self._word_count = val

    @property
    def db_name(self):
        return self._db_name

    @db_name.setter
    def db_name(self, val):
        self._db_name = val

    def initialize_db(self, db_name: str = None) -> None:
        """
        initialize the database. the enables swapping
        out databases at runtime
        :param db_name: str: database name
        :return:
        """
        if db_name:
            self.database.init(db_name)
            self.get_stats()
        elif self.db_name:
            self.database.init(self.db_name)
            self.get_stats()

    def get_stats(self) -> None:
        """
        set two values:
        get the length of longest word in dictionary
        get the number of words in the dictionary
        :return:
        """
        self.max_word_length = self.words.select(fn.MAX(self.words.size)).scalar()
        self.word_count = self.words.select().count()

    def set_word(self,
                 word: str,
                 min_size: int = 2,
                 max_size: int = None,
                 size: int = None) -> None:
        """
        set the word and size parameters for next generation of anagrams
        :param word: str: word to anagram
        :param min_size: int: minimum anagram size
        :param max_size: int: maximum anagram size
        :param size: int: absolute anagram size
        :return: None
        """
        self.word = sorted(word)
        self.set_sizes(min_size=min_size, max_size=max_size, size=size)

    def set_sizes(self,
                  min_size: int = 2,
                  max_size: int = None,
                  size: int = None):
        """
        set anagram size values
        :param min_size: int: minimum anagram size
        :param max_size: int: maximum anagram size
        :param size: int: absolute anagram size
        :return: None
        """
        # all fetches are calculated from min_size and max_size,
        # so if size is absolute, set min_size and max_size accordingly
        if size:
            self.min_size = size
            self.max_size = size + 1
            return

        self.min_size = min_size

        # if max_size is not set, we assume anagrams of all sizes.
        # so, set the max_size to the length of the word
        if max_size:
            self.max_size = max_size + 1
        else:
            self.max_size = len(self.word) + 1

    def generate_anagrams(self, size: int = None) -> None:
        """
        retrieve matching words from the database.
        Algorithm:
        1) generate all letter combinations of word to anagram
           limiting the size of the combinations by the size restrictions
        2) iterating over the list:
           a. sort the letters alphabetically
           b. create the query string
           c. retrieve matching records from the database
           d. append to running anagrams list

        :param size: int: word size. This is needed if no
                          word is provided. in that case,
                          all words of size are retrieved
        :return: None
        """
        self.anagrams: dict = dict()
        lists: list = list()
        if self.word is None:
            self.generate_all(size)
        else:
            # generate all combinations for the word
            for num in range(self.min_size, self.max_size):
                anagrams = []
                for item in combinations(self.word, num):
                    anagrams.append(''.join(sorted(item)))
                lists.append(sorted(list(set(anagrams))))

        # iterate over the lists and get matching words
        for item in lists:
            word_size = len(item[0])
            results = self.words.select(self.words.word).where(self.words.anagram << item)
            if results.exists():
                anagrams = []
                for word in results:
                    anagrams.append(word.word)
                self.anagrams[word_size] = sorted(anagrams[:])

    def generate_all(self, size: int = None) -> None:
        """
        retrieve all words from the database.
        The wisdom of doing this is dependent
        upon the size of the wordlist

        restrict the words by size if provided
        :param size: int: size of word
        :return: None
        """
        self.anagrams: dict = dict()
        for num in range(2, self.max_word_length + 1):
            self.anagrams[num] = []

        if size:
            results = self.words.select(self.words.word, self.words.size).where(self.words.size == size)
        else:
            results = self.words.select(self.words.word, self.words.size)

        for word in results:
            self.anagrams[word.size].append(word.word)

    def get_anagrams(self) -> dict:
        """
        return the anagrams as a dict of lists, keyed by word size.
        Each list is sorted alphabetically.

        :return: dict of words, keyed by size
        """
        return self.anagrams

    def print_anagrams(self) -> None:
        """
        print the generated anagrams
        :return: None
        """
        pprint(self.anagrams)


if __name__ == '__main__':
    am = Generator()
    am.db_name = 'collins.db'
    am.initialize_db()
    am.set_word('stop')
    am.generate_anagrams()
    am.print_anagrams()
    am.set_word(word='development', size=7)
    am.generate_anagrams()
    am.print_anagrams()
    am.set_word(word='python', min_size=3, max_size=7)
    am.generate_anagrams()
    am.print_anagrams()

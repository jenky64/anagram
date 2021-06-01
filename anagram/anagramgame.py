#!/usr/bin/python3

import argparse
import re
import sys

from anagram.generator import Generator

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--database', help='database to use')
args = parser.parse_args()

# set database to None of provided database name
# option exists so that the database does not have to be
# set on object creation
if args.database:
    database_name = args.database
else:
    database_name = None


class AnagramGame:
    """
    A simple game wrapper for the Generator object
    """

    def __init__(self, db_name: str = database_name) -> None:
        """
        create game object
        :param db_name: database name
        """
        self.word: str = ''
        self.size_str: str = ''
        self.min_size: int = 0
        self.max_size: int = 0
        self.size: int = 0
        self.inc: list = list()
        self.inc_type: str = ''
        self.exc: list = list()
        self.exc_type: str = ''
        self.pattern: str = ''
        self.anagrams: dict = dict()
        self.lists: list = list()
        self.by_size_list = ('2', '4', '6')
        self.commands = {'1': self.opt_anagram, '2': self.opt_anagram, '3': self.opt_inc_ex,
                         '4': self.opt_inc_ex, '5': self.opt_pattern, '6': self.opt_pattern,
                         '7': self.opt_file, '8': self.opt_set_database, '9': self.opt_quit}

        self.generator = AnagramGenerator()

        if db_name:
            self.opt_set_database(db_name=db_name)

    @property
    def word(self):
        return self._word

    @word.setter
    def word(self, val):
        self._word = val

    @property
    def str_size(self):
        return self._str_size

    @str_size.setter
    def str_size(self, val):
        self._str_size = val

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
    def inc(self):
        return self._inc

    @inc.setter
    def inc(self, val):
        self._inc = val

    @property
    def inc_type(self):
        return self._inc_type

    @inc_type.setter
    def inc_type(self, val):
        self._inc_type = val

    @property
    def exc(self):
        return self._exc

    @exc.setter
    def exc(self, val):
        self._exc = val

    @property
    def ext_type(self):
        return self._ext_type

    @ext_type.setter
    def ext_type(self, val):
        self._ext_type = val

    @property
    def pattern(self):
        return self._pattern

    @pattern.setter
    def pattern(self, val):
        self._pattern = val

    def get_option(self) -> str:
        """
        display menu and get menu option
        :return: str: menu option
        """
        self.print_menu()
        return input('select option: ')

    def print_menu(self) -> None:
        """
        display menu
        :return: None
        """
        print() 
        print(f'-----------------------------------------')
        print(f'  1) anagrams - all')
        print(f'  2) anagrams - by size')
        print(f'  3) include/exclude letters (expensive)')
        print(f'  4) include/exclude letters - by size')
        print(f'  5) include pattern (expensive)')
        print(f'  6) include pattern - by size')
        print(f'  7) save to file')
        print(f'  8) set database')
        print(f'  9) quit')
        print(f'-----------------------------------------')
        print() 

    def select_option(self) -> None:
        """
        continually show menu and prompt for option
        set flags and parameters according to option chosen
        :return: None
        """
        cont = ''
        while cont != '10':
            self.word = None
            self.size_str = ''
            size_flag = False
            cont = self.get_option()
            if cont in self.commands.keys():
                if cont == '9':
                    self.opt_quit()
                if cont in self.by_size_list:
                    size_flag = True
                # if option is not quit, write to file, or swap database
                # get the required word and size parameters
                if cont not in ['7', '8']:
                    self.word, self.min_size, self.max_size, self.size, self.size_str = self.get_anagram_parameters(cont, size_flag)
                    self.get_anagrams(self.word, self.min_size, self.max_size, self.size, self.size_str)
                self.commands[cont]()
            else:
                print(f'invalid command: {cont}')
          
    def get_anagram_parameters(self, opt: str, flag: bool):
        """

        :param opt: str: option chosen
        :param flag: bool: option has size restriction
        :return:
        """
        size_str = None
        no_word = False

        # get parameters for desired option
        if opt in ['1', '2']:
            word = input('characters to anagram: ')
            if len(word) == 0:
                no_word = True
                word = 'placeholder'
        else:
            no_word = True
            word = 'placeholder'

        if flag is True:
            min_size, max_size, size, size_str = self.get_sizes(word)
        else:
            min_size, max_size, size = 2, len(word), None

        if no_word is True:
            word = None
        return word, min_size, max_size, size, size_str

    def get_anagrams(self, word: str, min_size: int, max_size: int, size: int, size_str: int) -> None:
        """
        generate the anagrams
        :param word: str: word to anagram
        :param min_size: int: minimum anagram size
        :param max_size: int: maximum anagram size
        :param size: int: absolute anagram size
        :param size_str:
        :return:
        """
        self.generator.set_word(word, min_size, max_size, size)
        self.generator.generate_anagrams(size_str)
        self.anagrams = self.generator.get_anagrams()
 
    def opt_anagram(self):
        self.print_words(self.min_size, self.max_size+1)

    def opt_inc_ex(self):
        il = input('letters to include: ')
        # default to boolean or for excluded letters
        if len(il) > 0:
            self.inc = sorted(il.split(' '))
            self.inc_type = input('all included letters must exist in word to include? [y/n] ')
            if self.inc_type != 'y':
                self.inc_type = 'n'
        else:
            self.inc_type = 'n'

        el = input('letters to exclude: ')
        # default to boolean or for excluded letters
        if len(el) > 0:
            self.exc = sorted(el.split(' '))
            self.exc_type = input('all excluded letters must exist in word to exclude? [y/n] ')
            if self.exc_type != 'y':
                self.exc_type = 'n'
        else:
            self.exc_type = 'n'

        for num in range(self.min_size, self.max_size+1):
            if num in self.anagrams.keys() and len(self.anagrams[num]) > 0:
                if len(il) > 0:
                    self.anagrams[num] = [word for word in self.anagrams[num] if self.inc_filter(word)]
                if len(el) > 0:
                    self.anagrams[num] = [word for word in self.anagrams[num] if self.exc_filter(word)]

        self.print_words(self.min_size, self.max_size)

    def opt_pattern(self):
        self.pattern = input('pattern: ')
        for num in range(self.min_size, self.max_size+1):
            if num in self.anagrams.keys() and len(self.anagrams[num]) > 0:
                self.anagrams[num] = [word for word in self.anagrams[num] if self.pat_match(word)]

        self.print_words(self.min_size, self.max_size)

    def opt_file(self):
        fname = input('enter filename: ')
        self.print_file(self.min_size, self.max_size, fname)
        print(f"words printed to file: {fname}")

    def opt_set_database(self, db_name: str = None):
        if not db_name:
            db_name = input('enter database: ')
        self.generator.initialize_db(db_name=db_name)

    def opt_quit(self):
        print('\n')
        print(f'thank you for playing')
        print('\n')
        sys.exit()

    def get_sizes(self, word):
        size_str = input('size restrictions: ( <num, <=num, =num, >num, >=num, num-num) ')
        
        if size_str.find('-') > 0:
            size_st = ''
            minsize, maxsize = size_str.split('-')
            for i in range(int(minsize), int(maxsize)+1):
                size_st += str(i) + ','
            size_st = ' in (' + size_st[:-1] + ')'
            return int(minsize), int(maxsize), None, size_st
        elif size_str.find('<=') == 0:
            minsize, maxsize = size_str.split('<=')
            return 2, int(maxsize), None, size_str
        elif size_str.find('>=') == 0:
            trash, minsize = size_str.split('>=')
            return int(minsize), len(word), None, size_str
        elif size_str.find('=') == 0:
            trash, size = size_str.split('=')
            return int(size), int(size), None, size_str
        elif size_str.find('<') == 0:
            trash, maxsize = size_str.split('<')
            return 2, int(maxsize) - 1, None, size_str
        elif size_str.find('>') == 0:
            print(f"found > sign")
            trash, minsize = size_str.split('>')
            return int(minsize) + 1, len(word), None, size_str

    def pat_match(self, word):
        if re.match(self.pattern, word):
            return 1
        else:
            return 0
        
    def inc_filter(self, word):
        # 1 of the letters must exist in word
        if self.inc_type == 'n':
            for letter in self.inc:
                if letter in word:
                    return 1
            return 0
        # all letters must exist in word
        else:
            p = True
            for letter in self.inc:
                if letter not in word:
                    p = False
                    break
            return p       

    def exc_filter(self, word):
        # just one of the excluded letters must exist in word
        if self.exc_type == 'n':
            for letter in self.exc:
                if letter in word:
                    return 0
            return 1
        # all excluded letters must exist in word to exclude it
        else:
            p = False
            for letter in self.exc:
                if letter not in word:
                    p = True
                    break
            return p
        
    def print_file(self, min_size, max_size, fname):
        total = 0
        with open(fname, 'w') as f:
            for num in range(min_size, max_size+1):
                if num in self.anagrams.keys() and len(self.anagrams[num]) > 0:
                    num_words = len(self.anagrams[num])
                    total += num_words
                    f.write(f'size: {str(num)}, number of words: {str(num_words)}')
                    f.write('')
                    for word in self.anagrams[num]:
                        f.write(f'{word}')
                        f.write(f'')
                    f.write('\n\n')
            f.write('total words: ' + str(total) + '\n')

    def print_words(self, min_size, max_size):
        total = 0

        # need to reset max if word is none
        max_size = self.generator.max_word_length

        print(f'')
        for num in range(min_size, max_size+1):
            if num in self.anagrams.keys() and len(self.anagrams[num]) > 0:
                num_words = len(self.anagrams[num])
                total += num_words
                print(f'size: {num}, number of words: {num_words}')
                for word in self.anagrams[num]:
                    print(f'{word} ', end='')
                print(f'')
                print(f'')
        print(f'')
        print(f"total words: {total}")


if __name__ == '__main__':
    a = AnagramGame()
    a.select_option()

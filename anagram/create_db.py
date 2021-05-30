#!/bin/env python
import argparse
import json
import sys
from peewee import *

# ###### peewee stuff goes here ########words: dict = dict()
database = SqliteDatabase(None)

class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class Words(BaseModel):
    word = TextField(unique=True)
    size = IntegerField()
    anagram = TextField(index=True)

    class Meta:
        table_name = 'words'

# ###### peewee stuff ends here ########

def set_names(fname: str) -> tuple:
    """
    create database name and outfile name from input filename
    :param fname: input file name
    :return: tuple: database name, output filename
    """
    db_name: str = '.'.join((fname.split('.')[0], 'db'))
    outfile: str = '.'.join((fname.split('.')[0], 'json'))

    return db_name, outfile


def process_word(word: str) -> tuple:
    """
    get size, anagram, and dict/list entries for word
    :param word: word to be processed
    :return: tuple: size, anagram, dict entry, list entry
    """
    size = str(len(word))
    anagram = ''.join(sorted(word))

    return size, anagram, {'size': int(size), 'anagram': anagram}, {'word': word, 'size': size, 'anagram': anagram}


def load_database(database, words: list) -> None:
    """
    load data into database
    :param database: database name
    :param words: list: list of processed words
    :return:
    """
    with database.atomic():
        for idx in range(0, len(words), 1000):
            Words.insert_many(wordlist[idx:idx+1000]).execute()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help = "file to format")
    args = parser.parse_args()

    if args.file:
        db_name, outfile = set_names(fname=args.file)
    else:
        print(f'no file provided')
        sys.exit()

    words: dict = dict()
    wordlist: list = list()

    database.init(db_name)
    database.connect()
    database.create_tables([Words])

    # iterate file and process each word
    # get size and alphabetical sort of the word
    # format data for database entry and json
    #with open(args.file, 'rb') as f:
    with open(args.file, 'r') as f:
        for line in f:
            #word = line[:-1].decode("utf8", "ignore")
            word = line[:-1]
            if word.isalpha():
                size = str(len(word))
                anagram = ''.join(sorted(word))
                words[word] = {'size': int(size), 'anagram': anagram}
                wordlist.append({'word': word, 'size': size, 'anagram': anagram})

    with open(outfile, 'w') as f:
        json.dump(words, f)

    load_database(database=database, words=wordlist)

#!/usr/bin/python

from sqlalchemy import Table, create_engine 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///twl06.db')
Session = sessionmaker(bind=engine)
Base = declarative_base(engine=engine)
class Words(Base):
    __table__ = Table('words', Base.metadata, autoload=True)

    def __init__(self, word = None, size = None, anagram = None):
        self.word = word
        self.size = size
        self.anagram = anagram

    def __repr__(self):
        return "<Word('%s','%d','%s')>" % (self.word,self.size,self.anagram)

if __name__ == '__main__':
   session = Session()
   rows = session.query(Words).filter_by(anagram='opst').all()
   print(f'number of words = {len(rows)}')
   print(f"words are:")
   for item in rows:
       print('  {item.word}')
   engine1 = create_engine('sqlite:///enable2k.db')
   Session.configure(bind=engine1)
   Base.metadata.bind = engine1
   session = Session()
   rows = session.query(Words).filter_by(anagram='opst').all()
   print(f"number of words = {len(rows)}")
   print(f"words are:")
   for item in rows:
       print('  {item.word}')

from peewee import *

database = SqliteDatabase(None)


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class Words(BaseModel):
    anagram = TextField(index=True)
    size = IntegerField()
    word = TextField(unique=True)

    class Meta:
        table_name = 'words'


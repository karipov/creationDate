from pathlib import Path
from peewee import Model, SqliteDatabase
from peewee import CharField, IntegerField, BooleanField


class User(Model):
    user_id = IntegerField()
    language = CharField()
    requests = IntegerField()
    is_ban = BooleanField()

    class Meta:
        database = SqliteDatabase(Path.cwd().joinpath('src/data/users.db'))

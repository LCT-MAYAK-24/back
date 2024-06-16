from users.models import User, Place
from peewee import *
from gigachat.models import db


class Favorite(Model):
    user = ForeignKeyField(User)
    place = ForeignKeyField(Place)

    class Meta:
        database = db

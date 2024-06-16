from gigachat.models import db
from peewee import *
from users.models import User, Place


class Feedback(Model):
    reason = CharField(max_length=500)
    lat = FloatField(null=True)
    lon = FloatField(null=True)
    place = ForeignKeyField(Place, null=True)
    user = ForeignKeyField(User)

    class Meta:
        database = db

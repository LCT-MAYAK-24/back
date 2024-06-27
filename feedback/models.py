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
    
    def to_json(self):
        lat, lon = self.lat, self.lon
        if lat is None:
            lat = self.place.lat
        if lon is None:
            lon = self.place.lon
        return {
            'lat': lat,
            'lon': lon,
            'reason': self.reason
        }
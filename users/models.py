from gigachat.models import db
from peewee import *
from users.consts import *
from geopy import distance


class User(Model):
    phone = CharField(max_length=20)

    class Meta:
        database = db
    
    def get_prompt(self):
        settings: Settings = self.settings[0]
        return f'''Пользователь имеет следующие отклонения:
Проблемы с глазами: {eye_problem_decoding[settings.eye_level]}
Проблемы со слухом: {ear_problem_decoding[settings.ear_level]}
Проблемы с передвижением: {move_problem_decoding[settings.ear_level]}
'''


class Settings(Model):
    eye_level = IntegerField()
    text_size = IntegerField()
    theme = IntegerField()
    ear_level = IntegerField()
    move_level = IntegerField()
    user = ForeignKeyField(User, backref='settings')

    class Meta:
        database = db
    
    def to_dict(self):
        return {
            'eye_level': self.eye_level,
            'text_size': self.text_size,
            'theme': self.theme,
            'ear_level': self.ear_level,
            'move_level': self.move_level,
            'user': self.user.id
        }


class Place(Model):
    name = TextField()
    place_type = CharField(max_length=100)
    address = CharField(max_length=500)
    accesible_category = CharField(max_length=100)
    wheelchair_accesibility_level = IntegerField()
    movement_accesibility_level = IntegerField()
    eye_accesibility_level = IntegerField()
    ear_accesibility_level = IntegerField()
    mental_accesibility_level = IntegerField()
    lat = FloatField()
    lon = FloatField()
    link = TextField()

    class Meta:
        database = db
    

    def to_map(self):
        return {
            'lat': self.lat,
            'lon': self.lon,
            'id': self.id
        }
    

    def to_json(self, user):
        from places.models import Favorite
        try:
            Favorite.get(user=user, place=self)
            favorite = True
        except Exception as e:
            favorite = False
        return {
            'name': self.name,
            'type': self.place_type,
            'category': self.accesible_category,
            'wheelchair_accessibility_level': self.wheelchair_accesibility_level,
            'movement_accesibility_level': self.movement_accesibility_level,
            'eye_accesibility_level': self.eye_accesibility_level,
            'ear_accesibility_level': self.ear_accesibility_level,
            'mental_accesibility_level': self.mental_accesibility_level,
            'link': self.link,
            'favorite': favorite,
            'id': self.id,
            'lat': self.lat,
            'lon': self.lon,
            'place_type': self.place_type
        }
    
    def get_prompt(self, user_lat, user_lon):
        p1 = (user_lat, user_lon)
        p2 = (self.lat, self.lon)
        dist = distance.geodesic(p1, p2).km
        dist_prompt = ''
        if dist < 100:
            dist_prompt = f'Расстояние места до данного пользователя: {dist:.2f} километров'
        return f'''Место: {self.name}
Доступность для инвалидной коляски: {accesibility_decoding[self.wheelchair_accesibility_level]}
Доступность в передвижении: {accesibility_decoding[self.movement_accesibility_level]}
Доступность для слабослышащих: {accesibility_decoding[self.movement_accesibility_level]}
{dist_prompt}\n\n
''', dist
from users.models import User, Place, Settings
from places.consts import filter_types, filter_categories as type_filter_categories
from geopy import distance

def filter_recommendations(user: User, page: int, eye_level: int=None, ear_level: int=None, move_level: int=None):
    print(user, user.id, user.settings.count())
    settings: Settings = user.settings[0]
    if eye_level is None:
        eye_level = settings.eye_level
    if move_level is None:
        move_level = settings.move_level
    if ear_level is None:
        ear_level = settings.ear_level

    q = Place.select().where(
        Place.eye_accesibility_level >= eye_level &
        Place.movement_accesibility_level >= move_level &
        Place.ear_accesibility_level >= ear_level
    ).paginate(page, 30)
    if not q.count():
        q = Place.select().where(
            Place.movement_accesibility_level >= move_level &
            Place.ear_accesibility_level >= ear_level
        ).paginate(page, 30)
    if not q.count():
        q = Place.select().where(
            Place.ear_accesibility_level >= ear_level
        ).paginate(page, 30)
    if not q.count():
        q = Place.select().where().paginate(page, 30)
    return q


def filter_categories(places, categories):
    eye_level = 3
    move_level = 3
    ear_level = 3
    wheelchair_level = 3
    if 'Для людей с проблемами слуха' in categories:
        ear_level = 1
    if 'Для людей с нарушениями опорно-двигательного аппарата' in categories:
        move_level = 1
    if 'Для людей, передвигающихся на инвалидных колясках' in categories:
        wheelchair_level = 1
    if 'Неадаптированные места' in categories:
        eye_level = 3
        move_level = 3
        ear_level = 3
        wheelchair_level = 3
    filtered = []
    for place in places:
        if place['wheelchair_accessibility_level'] <= wheelchair_level and \
           place['eye_accesibility_level'] <= eye_level and \
           place['ear_accesibility_level'] <= ear_level and \
           place['movement_accesibility_level'] <= move_level:
            filtered.append(place)
    return filtered



def filter_places(places, types, categories, max_distance, user_lat, user_lon):
    if not isinstance(types, list):
        types = filter_types
    if not isinstance(categories, list):
        categories = type_filter_categories
    if not isinstance(max_distance, int):
        max_distance = 10_000
    filtered = []
    
    for place in places:
        if place['place_type'] in categories:
            p1 = (user_lat, user_lon)
            p2 = (place['lat'], place['lon'])
            if distance.geodesic(p1, p2).km <= max_distance:
                filtered.append(place)
    return filter_categories(filtered, types)
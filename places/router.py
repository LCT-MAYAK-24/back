from fastapi import APIRouter, Header, Query
from typing import Annotated, List
from users.models import User, Place
from places.models import Favorite
from places.utils import filter_recommendations, filter_places
from places.consts import filter_categories, filter_types

router = APIRouter()


@router.post('/favorite/{place_id}', tags=['favorite'])
def add_to_favorite(place_id: str, user_id: Annotated[str, Header()]):
    user = User.get(id=user_id)
    place = Place.get(id=place_id)
    favorite, created = Favorite.get_or_create(place=place, user=user)
    return {'created': created}


@router.delete('/favorite/{place_id}', tags=['favorite'])
def delete_favorite(place_id: str, user_id: Annotated[str, Header()]):
    user = User.get(id=user_id)
    place = Place.get(id=place_id)
    favorite, created = Favorite.get_or_create(place=place, user=user)
    favorite.delete_instance()
    return {'deleted': True}


@router.get('/favorite', tags=['favorite', 'filter_route'])
def get_favorite(
    user_id: Annotated[str, Header()],
    categories: List[str] = Query(None),
    types: List[str] = Query(None),
    distance: int = Query(None),
    user_lat: float = Query(),
    user_lon: float = Query()
):
    user = User.get(id=user_id)
    places = []
    for favorite in Favorite.filter(user=user):
        places.append(favorite.place.to_json(user))
    return filter_places(places, types, categories, distance, user_lat, user_lon)

@router.get('/places', tags=['places', 'filter_route'])
def get_places(
    user_id: Annotated[str, Header()], 
    page_number: str,
    categories: List[str] = Query(None),
    types: List[str] = Query(None),
    distance: int = Query(None),
    user_lat: float = Query(),
    user_lon: float = Query()
):
    user = User.get(id=user_id)
    places = []
    for place in Place.select().paginate(int(page_number), 700):
        places.append(place.to_json(user))
    return filter_places(places, types, categories, distance, user_lat, user_lon)

@router.get('/places/{place_id}', tags=['places'])
def get_place(
    user_id: Annotated[str, Header()], 
    place_id: str
):
    user = User.get(id=user_id)
    place = Place.get(id=place_id)
    return place.to_json(user)


@router.get('/recommendations', tags=['recommendations', 'filter_route'])
def get_recommendations(
    user_id: Annotated[str, Header()], 
    page: str,
    categories: List[str] = Query(None),
    types: List[str] = Query(None),
    distance: int = Query(None),
    user_lat: float = Query(),
    user_lon: float = Query()
):
    user = User.get(id=user_id)
    items: List[Place] = filter_recommendations(user, int(page))
    res = []
    for item in items:
        res.append(item.to_json(user))
    return filter_places(res, types, categories, distance, user_lat, user_lon)

@router.get('/map/places', tags=['map'])
def get_map_places():
    return list(
        map(
            lambda x: x.to_map(),
            Place.select()
        )
    )

@router.get('/filter/categories', tags=['filter'])
def get_categories_filter():
    return filter_categories

@router.get('/filter/types', tags=['filter'])
def get_types_filter():
    return filter_types
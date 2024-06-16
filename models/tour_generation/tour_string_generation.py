from .filter_places import filter_places
import pickle
from random import shuffle, randint

city_data = None
with open('./models/tour_generation/city-data.pickle', 'rb') as file:
    city_data = pickle.load(file)


def tour_string_generation(city: str, how_long: int, chat_id: str, generation_type: str,  pref_cat=[]):
    data = []
    if generation_type == 'tour':
        string = '<p><h4>Вот ваш маршрут</h4><br/>'
        for day in range(max(1, how_long)):
            places = filter_places(city, pref_cat)
            data.append({"day": day+1, "places": places})
            local_string = f'<strong>День {day+1}</strong><br/>'
            current_timing = 10
            for place in places:
                local_string += f'<strong>{current_timing}:00 - {current_timing+2}:00</strong> <a href="/#/chat/{chat_id}/{place["header"]}">{place["header"]}</a> <br/>'
                current_timing += 2
            local_string += '<br/><br/>'
            string += local_string
    elif generation_type == 'list':
        string = '<p><h4>Вот список мест</h4><br/>'
        places = filter_places(city, pref_cat)
        data = [{'day': -1, 'places': places}]
        for place in places:
            string += f'<a href="/#/chat/{chat_id}/{place["header"]}">{place["header"]}</a><br/>'
    elif generation_type == 'regions':
        string = '<p><h4>Вот популярные направления которые можно посетить</h4><br/>'
        shuffle(city_data)
        moscow = {'name': 'Москва', 'lat': '56,326797', 'lon': '44,006516'}
        data = []
        for i, city in enumerate([moscow] + city_data[0:randint(2, 5)]):
            string += f'{i+1}. <a href="/#/chat/{chat_id}/{city["name"]}">{city["name"]}</a><br/>'
            data.append({
                'header': city['name'],
                'lat': float(city['lat'].replace(',', '.')),
                'long': float(city['lon'].replace(',', '.'))
            })
        data = [{'day': -2, 'places': data}]
    return string, data

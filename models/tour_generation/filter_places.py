import pickle
from typing import List
import geopy.distance
from python_tsp.exact import solve_tsp_dynamic_programming
import numpy as np


data = None

def load_data():
    global data
    with open('./models/tour_generation/data.pickle', 'rb') as file:
        data = pickle.load(file).dropna()

load_data()

def data_loaded(func):
    def wrapper(*args, **kwargs):
        global data
        if data is None:
            load_data()
        return func(*args, **kwargs)
    return wrapper

@data_loaded
def filter_places(city: str, preference_categories: List[str]=[]):
    global data
    local_filter_data = data[data.city == city]

    if len(preference_categories):
        cat_filters = set()
        if isinstance(preference_categories, str):
            preference_categories = ['музей']
        for cat in preference_categories:
            cat_filters = cat_filters | set(local_filter_data[local_filter_data['Тип'].str.lower().str.contains(cat.lower())]['Id активности'].tolist())
        local_filter_data_ = local_filter_data[local_filter_data['Id активности'].isin(cat_filters)]
        if len(local_filter_data_):
            local_filter_data = local_filter_data_
    samples = local_filter_data[local_filter_data.city == city].sample(5)[['header', 'long', 'lat']].to_dict(orient='records')
    d_matrix = []
    for element in samples:
        distances = []
        for element1 in samples:
            distances.append(geopy.distance.geodesic((element['lat'], element['long']), (element1['lat'], element1['long'])).km)
        d_matrix.append(distances)
    perm = solve_tsp_dynamic_programming(np.array(d_matrix))
    sorted_samples = [samples[i] for i in perm[0]]
    return sorted_samples

import pandas as pd
from users.models import Place

df = pd.read_csv('places/data.csv')
data = df.to_dict(orient='records')

for item in data:
    item.pop('id', None)
    Place.create(
        **item
    )
import streamlit as st
from feedback.models import Feedback
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt


st.title('Дашборд ошибок')

feedbacks = list(map(lambda x: x.to_json(), Feedback.select()))


reasons = list(map(lambda x: x['reason'], feedbacks))

chart_data = list(
    map(
        lambda x: {
            'y': x[1],
            'x': x[0]
        },
        Counter(reasons).most_common(len(set(reasons)))
    )
)

fig1, ax1 = plt.subplots()
cnt = Counter(reasons).most_common(len(set(reasons)))
print(list(map(lambda x: x['x'], chart_data)))
print(list(map(lambda x: x['y'], chart_data)))

ax1.pie(
    list(map(lambda x: x['y'], chart_data)), 
    labels=list(map(lambda x: x['x'], chart_data)), 
    autopct='%1.1f%%'
)
ax1.axis('equal')
st.pyplot(fig1)

print(feedbacks)

st.map(feedbacks)

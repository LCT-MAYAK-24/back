import requests as r
import json
from gigachat.requests.get_jwt import get_jwt
from random import shuffle


mock_messages = [
        {
            'role': 'user',
            'content': 'Скажи привет'
        }
    ]


def chat_completion(messages):
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    payload = json.dumps({
        "model": "GigaChat",
        "messages": messages,
        "temperature": 1,
        "top_p": 0.1,
        "n": 1,
        "stream": False,
        "max_tokens": 512,
        "repetition_penalty": 1,
        "update_interval": 0
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + get_jwt()['access_token']
    }

    response = r.request("POST", url, headers=headers, data=payload, verify=False)

    return response.json()


def build_start_message(user_lat, user_lon, user_id, first_question):
    from users.models import User, Place
    user: User = User.get(id=user_id)
    user_prompt = user.get_prompt()
    place_prompts = []
    for place in Place.select():
        place_prompts.append(place.get_prompt(user_lat, user_lon))
    place_prompts.sort(key=lambda x: x[1])
    prompt = f'''Ты маяк - ассистент для людей с дополнительными потребностями в вопросе выбора мест в Волгоградской области и самом волгограде
Ты помогаешь людям подбирать им места из базы данных либо составить для них маршрут.
Тебе дана информация про пользователя:
{user_prompt}

А вот база данных объектов, которые надо рекомендовать или составлять из них туры:
{"".join([place[0] for place in place_prompts[0:100]])}
Важно: В своем ответе в точности указывай названия мест которых рекомендуешь и ничего не меняй в них
Используй только данные тебе объекты, ничего не придумывай
Первый вопрос от этого пользователя: {first_question}
Отвечай кратко, не более 100 слов.
Do not use Markdown.
Не используй маркдаун.
Не пиши в ответе никакие английские буквы
'''
    answer = call(prompt, [])
    if user_lat == 0 and user_lon == 0:
        answer = answer.replace('\\', '').replace('n', '').replace('*', '')
    return answer, prompt


def call(prompt, history):
    url = "http://127.0.0.1:5000/history"
    payload = json.dumps({
        "data": prompt,
        "history": history
    })
    headers = {
        'Authorization': 'Token 4dae2ea3dd371277afdf2bbc06c507ffaf4cabdf',
        'Content-Type': 'application/json'
    }
    response = r.request("POST", url, headers=headers, data=payload)
    return response.text
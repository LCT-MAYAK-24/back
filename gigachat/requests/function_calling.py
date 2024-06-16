import requests
import json
from .get_jwt import get_jwt_pro

url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

mock_messages = [
        {
            "role": "user",
            "content": "Сгенерируй мне тур в Санкт-Петербург на неделю"
        }
    ]

tour_generate_function = {
    "name": "tour_generate",
    "description": "Генерирует туристический тур в город на конкретный день",
    "parameters": {
        "type": "object",
        "properties": {
        "location": {
            "type": "string",
            "description": "Название города"
        },
        "num_days": {
            "type": "integer",
            "description": "Количество дней, на которые надо сгенерировать тур"
        },
        "prefered_category": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "description": "Предпочтительные категории для мест в туре"
        },
        "generation_type": {
            "type": "string",
            "enum": ["tour", "list", 'regions'],
            "description": "аргумент, показывающий надо генерировать полноценный тур (tour), просто список мест (list), или направления для путешествий (regions)"
        }
        },
        "required": [
            "location",
            "generation_type"
        ],
        "few_shot_examples": [
            {
                'request': 'Сделай мне тур в Москву на 2 дня',
                'params': {
                    'generation_type': 'tour',
                    'num_days': 2,
                    'location': 'Москва'
                }
            },
            {
                'request': 'Покажи мне места которые есть в Казани',
                'params': {
                    'generation_type': 'list',
                    'location': 'Казань'
                }
            },
            {
                'request': 'Какие есть популярные направления',
                'params': {
                    'generation_type': 'regions',
                    'location': ''
                }
            },
        ]
    }
}

def tour_generate_calling(messages):
    global tour_generate_function

    payload = json.dumps({
        "model": "GigaChat-Pro-preview",
        "messages": messages,
        "function_call": "auto",
        "functions": [
            tour_generate_function
        ],
        "temperature": 1,
        "top_p": 0.1,
        "n": 1,
        "stream": False,
        "max_tokens": 4096,
        "repetition_penalty": 1,
        "update_interval": 0
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + get_jwt_pro()['access_token']
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)

    return response.json()

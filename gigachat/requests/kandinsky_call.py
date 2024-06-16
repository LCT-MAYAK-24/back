import json
import time

import requests

import base64
from PIL import Image
from io import BytesIO
from ..models import Conversation
from .chat_completion import chat_completion

api_key = 'B53199BA272784C82A9799BFE5C73082'
secret = '38C03BC4A0F27A3693EFE4584CF7C568'

def base64_to_image(base64_string, output_file):
    """
    Convert a base64 encoded image string to a .jpg file.
    
    Parameters:
        base64_string (str): The base64 encoded image string.
        output_file (str): The path to save the output .jpg file.
        
    Returns:
        None
    """
    try:
        # Decode the base64 string into bytes
        image_data = base64.b64decode(base64_string)
        
        # Open the image using PIL
        image = Image.open(BytesIO(image_data))
        
        # Save the image to the specified file
        image.save(output_file, 'JPEG')
        print("Image saved successfully as", output_file)
    except Exception as e:
        print("Error:", e)

# Example base64 encoded image string
base64_string = "YOUR_BASE64_ENCODED_STRING_HERE"

# Specify the output file path
output_file = "output_image.jpg"

# Convert base64 image to .jpg file
base64_to_image(base64_string, output_file)



class Text2ImageAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"beautiful view city photorealistic style place {prompt}"
            },
            "style": "UHD",
            "negativePromptUnclip": "people люди лица faces"
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)



def generate_image(prompt: str):
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', api_key, secret)
    model_id = api.get_model()
    uuid = api.generate(prompt, model_id)
    images = api.check_generation(uuid, delay=3)
    return images


def add_image_to_conversation(conversation_id: str):
    conversation: Conversation = Conversation.get(id=conversation_id)

    name = chat_completion([
        {
            'role': 'assistant',
            'content': conversation.get_tour_message()
        },
        {
            'role': 'user',
            'content': 'Назови этот туристический тур. Не возвращай ничего кроме названия'
        }
    ])['choices'][0]['message']['content']

    base = generate_image('Туристический тур ' + name)[0]
    file = f'/static/{conversation_id}.jpg'
    base64_to_image(base, f'.{file}')
    conversation.name = name
    conversation.image = file
    conversation.save()
    return {
        'name': name,
        'image': file
    }

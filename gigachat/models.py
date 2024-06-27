from peewee import *
from .requests.chat_completion import call, build_start_message
from .requests.function_calling import tour_generate_calling
from models.tour_generation.tour_string_generation import tour_string_generation
import datetime
import json
from fastapi import BackgroundTasks
import re

db = SqliteDatabase('./conversations.db')


def transform_to_cyrillic(input_string):
    # Define a regular expression pattern to match all Cyrillic characters
    cyrillic_pattern = re.compile(r'[А-яЁё0-9]+')
    
    # Find all substrings that match the pattern
    matches = cyrillic_pattern.findall(input_string)
    
    # Join all the matched substrings into a single string
    result = ''.join(matches)
    
    return result.lower()


class GigachatModel(Model):
    class Meta:
        database = db



class Conversation(GigachatModel):
    name = CharField(max_length=200, default='Переписка')
    is_generating = BooleanField(default=True)
    date_created = DateTimeField(default=datetime.datetime.now)
    places_info = TextField(default='[]')
    image = CharField(default='/')

    def get_messages(self):
        return [message.to_json() for message in self.messages]
    
    def get_prompt_messages(self):
        return [message.to_json() for message in self.messages if message.role != 'function']
    
    def get_tour_message(self):
        return list(
            filter(
                lambda x: x.role == 'tour_generated',
                self.messages
            )
        )[-1].text
    
    def get_places_info(self):
        return json.loads(self.places_info)
    
    def to_json(self):
        return {
            'name': self.name,
            'created': self.date_created,
            'messages': self.get_messages(),
            'id': self.id,
            'places_info': self.get_places_info(),
            'image': self.image
        }
    
    def get_salut_message(self):
        prompt = 'Вот места которые можно посетить: ' + ',\n'.join([place['header'] for place in json.loads(self.places_info)[0]['places']])
        return prompt
    
    def to_model(self):
        return [
            m.to_prompt() for m in self.messages
        ]
    
    def get_last_message_text(self):
        return self.get_messages()[-1]['content']


def from_string_to_places(string, user_id):
    from users.models import Place, User
    user = User.get(id=user_id)
    string = transform_to_cyrillic(string)
    selected = []
    for place in Place.select():
        if not len(transform_to_cyrillic(place.name)):
            continue
        if transform_to_cyrillic(place.name) in string:
            selected.append(place.to_json(user))
    return selected


class Message(GigachatModel):
    text = TextField()
    conversation = ForeignKeyField(Conversation, backref='messages')
    role = CharField(max_length=100)
    date_created = DateTimeField(default=datetime.datetime.now)
    

    def to_prompt(self):
        return {
            'role': 'user' if self.role == 'user' else 'model',
            'text': self.text
        }


    def to_json(self):
        content = self.text
        role = self.role
        if self.role == 'function':
            content = json.loads(self.text)
        if self.text.startswith('Ты маяк'):
            content = self.text.split('Первый вопрос от этого пользователя: ')[-1]
        # else:
        #     content = ' '.join(re.findall(r'[А-яЁё]+', content))
        if self.role == 'tour_generated':
            role = 'assistant'
        return {'content': content, 'role': role, 'date_created': str(self.date_created)}
    
    @classmethod
    def create_user_message(
        cls, 
        content, 
        conversation: Conversation, 
        user_lat, 
        user_lon, 
        user_id
    ):
        conversation.is_generating = True
        conversation.save()
        messages = conversation.to_model()
        if len(messages) > 10:
            messages = [messages[0]] + messages[-10:]
        print(len(messages))
        if len(messages) == 0:
            answer, content = build_start_message(
                user_lat,
                user_lon,
                user_id,
                content
            )
            msg_type = 'system'
        else:
            answer = call(content, messages)
            msg_type = 'model'
        print('fuck')
        
        Message.create(text=content, conversation=conversation, role='user')

        Message.create(text=answer, conversation=conversation, role='model')
        
        current_places = conversation.get_places_info()
        candidates_places = from_string_to_places(answer, user_id)
        current_places_ids = set([place['name'] for place in current_places])
        candidate_places_ids = set([place['name'] for place in candidates_places])
        
        if len(candidates_places):
            conversation.places_info = json.dumps(candidates_places)
        conversation.save()

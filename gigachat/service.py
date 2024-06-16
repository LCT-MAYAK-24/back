from fastapi import APIRouter, BackgroundTasks
from .models import Conversation, Message


router = APIRouter()


def create_conversation(name: str='Переписка'):
    conversation: Conversation = Conversation.create(name=name)
    return conversation.to_json()

def create_message(
        content: str, 
        conversation_id: str, 
        background: BackgroundTasks,
        user_id,
        user_lat,
        user_lon
    ):
    Message.create_user_message(
        content, 
        Conversation.get(id=conversation_id), 
        user_lat,
        user_lon,
        user_id,
    )
    return Conversation.get(id=conversation_id).to_json()

def get_conversation(conv_id: str):
    return Conversation.get(id=conv_id).to_json()

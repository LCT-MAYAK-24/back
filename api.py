from fastapi import FastAPI, APIRouter, BackgroundTasks, Header, Query
from gigachat.service import get_conversation, create_conversation, create_message
# from models.tour_generation.search import search
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from gigachat.models import Conversation, Message
from users.router import router as user_router
from places.router import router as places_router
from feedback.router import router as feedback_router
from typing import Annotated
from users.models import User

class CreateConversationModel(BaseModel):
    name: Optional[str]

class CreateMessage(BaseModel):
    content: str
    conversation_id: str


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()

app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(user_router)
app.include_router(places_router)
app.include_router(feedback_router)


@app.get('/api/conversation/{id}/', tags=['Conversation'])
def get_conversation_route(id: str):
    return get_conversation(id)

@app.post('/api/conversation/', tags=['Conversation'])
def create_conversation_route(data: CreateConversationModel):
    return create_conversation(name=data.name)

@app.post('/api/conversation/create_message', tags=['Conversation'])
def create_message_route(
    data: CreateMessage, 
    background: BackgroundTasks,
    user_id: Annotated[int, Header()],
    user_lat: float = Query(),
    user_lon: float = Query(),
    ):
    return create_message(
        data.content, 
        data.conversation_id, 
        background,
        user_id,
        user_lat,
        user_lon
    )

@app.get('/api/conversation/hints', tags=['Conversation'])
def get_hints_route():
    return [
        "Сделай мне маршрут по Москве на 3 дня",
        "Маршрут по музеям Санкт-Петербурга",
        "Туристический маршрут в Казань"
    ]

# @app.post('/api/search', tags=['Search'])
# def seearh_route(data: str):
#     return search(data)

class SalutModel(BaseModel):
    text: str

@app.get('/api/salut', tags=['salut'])
def salut_route(
    data: str, 
    background: BackgroundTasks,
):
    print('start', data)
    conversation: Conversation = Conversation.create(name='переписка')
    Message.create_user_message(data, conversation, 0, 0, 1)
    path_generated = True
    try:
        tour_msg = conversation.get_last_message_text()
    except Exception as e:
        conversation.get_messages()[-1]
        tour_msg = conversation.get_messages()[-1]['content']
        path_generated = False
    return {'answer': tour_msg, 'path_generated': path_generated}
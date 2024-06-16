from fastapi import APIRouter, Header
from users.schema import *
from users.models import User, Settings
from typing import Annotated

router = APIRouter()


@router.post('/sign-up', tags=['onboarding'])
def sign_up(data: SignUpInput):
    user = User.create(phone=data.phone)
    return {'id': user.id}

@router.post('/form-fill', tags=['onboarding'])
def form_fill(data: FormFillInput, user_id: Annotated[str, Header()]):
    user = User.get(id=user_id)
    try:
        settings = Settings.get(user=user)
        for key, value in data.dict():
            setattr(settings, key, value)
        settings.save()
    except:
        settings: Settings = Settings.create(
            **data.dict(),
            user=user
        )
    return settings.to_dict()

@router.get('/sign-in')
def sign_in(phone: str):
    user = User.get(phone=phone)
    return user.id


@router.get('/settings')
def get_settings(user_id: Annotated[str, Header()]):
    user = User.get(id=user_id)
    return user.settings[0].to_dict()
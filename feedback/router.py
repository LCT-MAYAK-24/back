from fastapi import APIRouter, Header
from typing import Annotated
from users.models import User, Place
from feedback.schema import FeedbackCreate
from feedback.models import Feedback

router = APIRouter()


@router.post('/feedback', tags=['feedback'])
def create_feedback(data: FeedbackCreate, user_id: Annotated[str, Header()]):
    user = User.get(id=user_id)
    try:
        place = Place.get(id=data.place_id)
    except:
        place = None
    Feedback.create(
        reason=data.reason,
        lat=data.lat,
        lon=data.lon,
        place=place,
        user=user
    )
    return {}
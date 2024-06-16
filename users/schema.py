from pydantic import BaseModel

class SignUpInput(BaseModel):
    phone: str


class FormFillInput(BaseModel):
    eye_level: int
    text_size: int
    theme: int
    ear_level: int
    move_level: int
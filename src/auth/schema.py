from pydantic import BaseModel, Field
import uuid
from datetime import datetime


class UserCreateModel(BaseModel):
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=25)
    username: str = Field(max_length=8)
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)

    model_config = {
        "json_schema_extra": {
            "example": {
                "first_name": "hans",
                "last_name": "Anselme",
                "username": "hansou",
                "email": "hansanselme@gmail.com",
                "password": "testpass123",
            }
        }
    }


class UserReadModel(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    password_hash: str = Field(exclude=True)
    created_at: datetime
    update_at: datetime

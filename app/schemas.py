
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class ContactCreate(BaseModel):
    name: str
    email: EmailStr


class ContactResponse(ContactCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ReminderCreate(BaseModel):
    contact_id: int
    event: str
    due_at: datetime


class ReminderResponse(ReminderCreate):
    id: int
    status: str

    model_config = ConfigDict(from_attributes=True)

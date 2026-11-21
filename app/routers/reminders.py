
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Contact, Reminder
from app.schemas import ReminderCreate, ReminderResponse

router = APIRouter(prefix="/reminders", tags=["Reminders"])


@router.post("/", response_model=ReminderResponse, status_code=201)
def create_reminder(
    reminder: ReminderCreate,
    db: Session = Depends(get_db)
):
    contact = db.get(Contact, reminder.contact_id)

    if contact is None:
        raise HTTPException(
            status_code=404,
            detail="Contact not found"
        )

    new_reminder = Reminder(
        contact_id=reminder.contact_id,
        event=reminder.event,
        due_at=reminder.due_at,
        status="PENDING"
    )

    db.add(new_reminder)
    db.commit()
    db.refresh(new_reminder)

    return new_reminder


@router.get("/", response_model=list[ReminderResponse])
def list_reminders(db: Session = Depends(get_db)):
    return db.query(Reminder).all()

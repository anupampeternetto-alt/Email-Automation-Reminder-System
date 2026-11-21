
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)

    reminders = relationship("Reminder", back_populates="contact")


class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=False)
    event = Column(String(255), nullable=False)
    due_at = Column(DateTime, nullable=False)
    status = Column(String(30), default="PENDING", nullable=False)

    contact = relationship("Contact", back_populates="reminders")

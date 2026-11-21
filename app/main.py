
from fastapi import FastAPI

from app.routers import contacts, reminders

app = FastAPI(
    title="Email Automation & Reminder System",
    description="Python-based email automation and reminder management API",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "project": "Email Automation & Reminder System",
        "status": "running",
        "message": "Welcome to the Email Automation API"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


app.include_router(contacts.router)
app.include_router(reminders.router)

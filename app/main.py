
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import contacts, reminders, automation, tracking


# Create FastAPI application
app = FastAPI(
    title="Email Automation & Reminder System",
    description="Python-based email automation and reminder management API",
    version="1.0.0",
)


# Enable communication with Next.js dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Home endpoint
@app.get("/")
def home():
    return {
        "project": "Email Automation & Reminder System",
        "status": "running",
        "message": "Welcome to the Email Automation API",
    }


# Health-check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }


# Register API routers
app.include_router(contacts.router)
app.include_router(reminders.router)
app.include_router(automation.router)
app.include_router(tracking.router)

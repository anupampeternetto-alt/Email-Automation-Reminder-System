
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import text
from app.database import engine
from datetime import datetime, timezone
import uuid

router = APIRouter(tags=["Automation"])

class TemplateIn(BaseModel):
    name: str
    subject: str
    body_md: str

class CampaignIn(BaseModel):
    name: str
    template_id: str
    sender_name: str
    sender_email: EmailStr

def fetch_all(query):
    with engine.connect() as db:
        return [dict(row) for row in db.execute(text(query)).mappings()]

@router.get("/templates")
def list_templates():
    return fetch_all("SELECT * FROM templates")

@router.post("/templates", status_code=201)
def create_template(item: TemplateIn):
    new_id = str(uuid.uuid4())
    try:
        with engine.begin() as db:
            db.execute(text("""
                INSERT INTO templates
                (id, name, subject, body_md, created_at)
                VALUES (:id, :name, :subject, :body, :created)
            """), {
                "id": new_id,
                "name": item.name,
                "subject": item.subject,
                "body": item.body_md,
                "created": datetime.now(timezone.utc).isoformat()
            })
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return {"id": new_id}

@router.get("/campaigns")
def list_campaigns():
    return fetch_all("SELECT * FROM campaigns")

@router.post("/campaigns", status_code=201)
def create_campaign(item: CampaignIn):
    new_id = str(uuid.uuid4())
    with engine.begin() as db:
        template = db.execute(
            text("SELECT id FROM templates WHERE id=:id"),
            {"id": item.template_id}
        ).first()
        if not template:
            raise HTTPException(404, "Template not found")

        db.execute(text("""
            INSERT INTO campaigns
            (id, name, template_id, sender_name, sender_email, created_at)
            VALUES (:id, :name, :tid, :sender, :email, :created)
        """), {
            "id": new_id,
            "name": item.name,
            "tid": item.template_id,
            "sender": item.sender_name,
            "email": item.sender_email,
            "created": datetime.now(timezone.utc).isoformat()
        })
    return {"id": new_id}

@router.get("/messages")
def list_messages():
    return fetch_all("SELECT * FROM messages")

import asyncio
from src.renderer import render_email
from src.mailer import Mailer

class SendTestIn(BaseModel):
    template_id: str
    recipient_email: EmailStr
    recipient_name: str

@router.post("/send-test")
async def send_test(item: SendTestIn):
    with engine.connect() as db:
        template = db.execute(
            text("SELECT subject, body_md FROM templates WHERE id=:id"),
            {"id": item.template_id}
        ).mappings().first()

    if not template:
        raise HTTPException(404, "Template not found")

    try:
        subject, html = render_email(
            template["subject"],
            template["body_md"],
            {"name": item.recipient_name}
        )
    except Exception as exc:
        raise HTTPException(400, f"Template error: {exc}")

    result = await Mailer(dry_run=True).send_html(
        "Demo Team",
        "demo@example.com",
        item.recipient_email,
        subject,
        html
    )

    return {
        "subject": subject,
        "recipient": item.recipient_email,
        "result": result
    }

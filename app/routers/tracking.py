
import base64
from urllib.parse import urlparse

from fastapi import APIRouter, HTTPException, Response
from sqlalchemy import text
from app.database import engine

router = APIRouter(tags=["Tracking"])

PIXEL = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGP4BwQACfsD/UE8oRUAAAAASUVORK5CYII="
)

@router.get("/t/o/{message_id}.png")
def track_open(message_id: str):
    with engine.begin() as db:
        result = db.execute(
            text("""
                UPDATE messages
                SET status='opened'
                WHERE id=:id AND status='sent'
            """),
            {"id": message_id}
        )

    if result.rowcount == 0:
        raise HTTPException(404, "Sent message not found")

    return Response(content=PIXEL, media_type="image/png")


@router.get("/t/c/{message_id}")
def track_click(message_id: str, url: str):
    parsed = urlparse(url)

    if parsed.scheme != "https" or parsed.hostname != "example.com":
        raise HTTPException(400, "Redirect destination not allowed")

    with engine.begin() as db:
        result = db.execute(
            text("""
                UPDATE messages
                SET status='clicked'
                WHERE id=:id AND status IN ('sent', 'opened')
            """),
            {"id": message_id}
        )

    if result.rowcount == 0:
        raise HTTPException(404, "Sent message not found")

    return Response(
        status_code=302,
        headers={"Location": url}
    )


import sqlite3
import uuid
import httpx

db = sqlite3.connect("email_automation.db")
message_id = str(uuid.uuid4())

db.execute("""
    INSERT INTO messages (id, status)
    VALUES (?, 'sent')
""", (message_id,))
db.commit()

base = "http://127.0.0.1:8002"

opened = httpx.get(
    f"{base}/t/o/{message_id}.png",
    timeout=10
)

status_after_open = db.execute(
    "SELECT status FROM messages WHERE id=?",
    (message_id,)
).fetchone()[0]

clicked = httpx.get(
    f"{base}/t/c/{message_id}",
    params={"url": "https://example.com"},
    follow_redirects=False,
    timeout=10
)

status_after_click = db.execute(
    "SELECT status FROM messages WHERE id=?",
    (message_id,)
).fetchone()[0]

print("OPEN HTTP:", opened.status_code)
print("STATUS AFTER OPEN:", status_after_open)
print("CLICK HTTP:", clicked.status_code)
print("STATUS AFTER CLICK:", status_after_click)

assert opened.status_code == 200
assert status_after_open == "opened"
assert clicked.status_code == 302
assert status_after_click == "clicked"

print("MILESTONE 7 TRACKING TEST PASSED")

db.execute("DELETE FROM messages WHERE id=?", (message_id,))
db.commit()
db.close()

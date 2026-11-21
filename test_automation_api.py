
import httpx
import uuid

base = "http://127.0.0.1:8001"
unique = uuid.uuid4().hex[:8]

template = httpx.post(
    base + "/templates",
    json={
        "name": "Class Reminder " + unique,
        "subject": "Hello {{name}}",
        "body_md": "Hi **{{name}}**, your class starts soon."
    }
)

print("TEMPLATE:", template.status_code, template.json())

if template.status_code == 201:
    campaign = httpx.post(
        base + "/campaigns",
        json={
            "name": "Python Class " + unique,
            "template_id": template.json()["id"],
            "sender_name": "Demo Team",
            "sender_email": "demo@example.com"
        }
    )
    print("CAMPAIGN:", campaign.status_code, campaign.json())

for path in ["/templates", "/campaigns", "/messages"]:
    response = httpx.get(base + path)
    print(path, "STATUS:", response.status_code,
          "RECORDS:", len(response.json()))

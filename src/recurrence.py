
from datetime import datetime, timezone
from dateutil.rrule import rrulestr
from apscheduler.schedulers.background import BackgroundScheduler

UTC = timezone.utc

def next_occurrences(start_at_utc, rule, count=5):
    start = datetime.fromisoformat(
        start_at_utc.replace("Z", "+00:00")
    )
    if start.tzinfo is None:
        start = start.replace(tzinfo=UTC)

    recurrence = rrulestr(rule, dtstart=start)
    return [
        occurrence.isoformat()
        for occurrence in list(recurrence[:count])
    ]

def create_scheduler():
    scheduler = BackgroundScheduler(timezone="UTC")
    return scheduler

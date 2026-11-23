from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

SHANGHAI = ZoneInfo("Asia/Shanghai")

def get_next_reset_time(now: datetime) -> datetime:
    return (now.astimezone(SHANGHAI) + timedelta(days=1)).replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    ).astimezone(timezone.utc)


from datetime import datetime
from datetime import timezone


def datetime_utc()->datetime :
    return datetime.now(timezone.utc)

from pytz import timezone
from datetime import datetime, timedelta


def get_seoul_time():
    seoul_tz = timezone("Asia/Seoul")
    return datetime.now(seoul_tz)

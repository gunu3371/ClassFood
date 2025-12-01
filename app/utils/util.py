from pytz import timezone
from datetime import datetime, timedelta

def get_weekdays(day = -1):
    seoul_time = datetime.now(timezone("Asia/Seoul"))
    today = seoul_time.date()
    
    
    if day is -1:
        return today
    
    target_weekday = day
    current_weekday = today.weekday()
    
    days_diff = target_weekday - current_weekday
    target_date = today + timedelta(days=days_diff)
    
    return target_date

if __name__ == "__main__":
    print(get_weekdays())
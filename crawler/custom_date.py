import time
from datetime import date, timedelta


def get_custom_date(direction="before", days=2):
    if direction == "before":
        custom_date = date.today() - timedelta(days=days)
    elif direction == "after":
        custom_date = date.today() + timedelta(days=days)
    else:
        print("get_custom_date Error")
        return None
    return custom_date
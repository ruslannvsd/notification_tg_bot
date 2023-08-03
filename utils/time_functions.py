from datetime import datetime, timedelta

TG_TIME = "%Y-%m-%dT%H:%M:%S%z"
ART_TIME = "%I.%M%p %d/%m/%y"


def convert_to_millis(datetime_str):
    datetime_obj = datetime.strptime(datetime_str, TG_TIME)
    return datetime_obj.timestamp() * 1000


def convert_to_readable_time(millis):
    datetime_obj = datetime.fromtimestamp(millis / 1000.0)
    formatted_datetime = datetime_obj.strftime(ART_TIME)
    return formatted_datetime


def within_one_day(millis):
    now = datetime.now()
    one_day = now - timedelta(hours=2)
    milli_time = datetime.fromtimestamp(millis / 1000)
    if one_day <= milli_time <= now:
        return True
    else:
        return False

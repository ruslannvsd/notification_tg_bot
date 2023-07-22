from datetime import datetime


def convert_to_millis(datetime_str):
    datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S%z")
    return datetime_obj.timestamp() * 1000


def convert_to_readable_time(millis):
    datetime_obj = datetime.fromtimestamp(millis / 1000.0)
    formatted_datetime = datetime_obj.strftime("%I.%M%p %d/%m/%y")
    return formatted_datetime

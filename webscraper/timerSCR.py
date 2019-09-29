from datetime import datetime
from django.utils import timezone
import pytz
import sys

if __name__ == "__main__":
    print("'timerSCR.py' should not be use as external file. To use it run 'setup.py'.")
    # sys.exit()


def get_current_datetime():
    response = datetime.now()  # .strftime('%Y-%m-%d %H:%M:%S:%f')
    return response


def get_current_date():
    response = datetime.now().date().strftime('%Y-%m-%d')
    return response


def get_current_time():
    response = datetime.now().time().strftime('%H:%M:%S:%f')
    return response


def get_current_hour():
    response = datetime.now().hour
    return response


def get_current_minute():
    response = datetime.now().minute
    return response


"""
    FOR TEST PURPOSE ONLY
"""
# x = get_current_time()
# print(x)

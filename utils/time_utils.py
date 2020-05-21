import datetime


def now_str():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d-%H-%M-%S")

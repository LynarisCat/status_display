import datetime
import calendar
from typing import Dict


def getLastMonths() -> Dict[str, int]:

    today = datetime.date.today().replace(day=1)
    ret = {}

    for i in range(3):
        last_day_of_prev = today - datetime.timedelta(days=1)

        name = last_day_of_prev.strftime("%B")
        days = calendar.monthrange(last_day_of_prev.year, last_day_of_prev.month)[1]

        ret[name] = days

        today = last_day_of_prev.replace(day=1)

    return ret





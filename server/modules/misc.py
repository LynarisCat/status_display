import datetime
import calendar
from typing import List


def getLastMonths() -> List[(str, int)]:

    today = datetime.date.today().replace(day=1)
    ret = []

    for i in range(3):

        name = today.strftime("%B")
        days = calendar.monthrange(today.year, today.month)[1]

        ret.append((name, days))

        today = today - datetime.timedelta(days=1)
        today = today.replace(day=1)

    return ret





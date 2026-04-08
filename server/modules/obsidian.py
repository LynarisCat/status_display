from .misc import getLastMonths
from typing import List
import datetime
import configparser


config = configparser.ConfigParser()
config.read("config.ini")

obsidianPath = config["obsidian"]["pathToDayData"]


def countTags(file: str) -> int:

    try:
        with open(file, "r") as f:
            text = f.read()

            c = text.count("#Task")

    except FileNotFoundError:
        c = 0

    return c


# go through all relevant date files and collect the number of tags for each day
def getMonthData() -> List[List[int]]:
    
    months = getLastMonths()
    today = datetime.date.today()

    num_of_days = sum(months[i][1] for i in range(3))
    num_of_days_no_data = months[0][1] - today.day

    day_data = [[], [], []]

    year = today.year
    month = today.month
    day = today.day

    # fill future days with 0
    for i in range(num_of_days_no_data):
        day_data[0].append(0)


    for m in range(3):

        for d in range(day):
            file = obsidianPath+"/"+str(year)+str(month).zfill(2)+str(day-d).zfill(2)+".md"
            day_data[m].append( countTags(file) )

        # finished after running for all months
        if m >= 2:
            break

        day = months[m+1][1]
        month -= 1

        # if range crosses year
        if month <= 0:
            month = 12
            year -= 1

    # dates are reversed: current month -> older month; future date -> older date
    return day_data 

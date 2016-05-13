import time
from colors import bcolors

SC_TIME_FORMAT = "%Y/%m/%d %H:%M:%S +0000"


class Event:
    logged = False

    def __init__(self, date, content):
        self.date = date
        self.content = content
        self.epoch = self.calculate_epoch()

    def __hash__(self):
        return hash((self.date, self.content))

    def calculate_epoch(self):
        return int(time.mktime(time.strptime(self.date, SC_TIME_FORMAT)))

    def pretty_timestamp(self):
        return bcolors.FAIL + self.date.split(" +0000")[0]

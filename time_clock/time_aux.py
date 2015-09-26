from datetime import date
from datetime import datetime


class TimeAux:
    def __init__(self):
        self.now = datetime.now()

    def current_date(self):
        return self.now.strftime("%A %d. %B %Y")

    def time_stamp(self):
        return self.now

    def update(self):
        self.now = datetime.now()

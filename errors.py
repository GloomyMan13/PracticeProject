class StartDateAttributeError(Exception):
    def __init__(self, date):
        self.date = date

    def __str__(self):
        return f"Wrong date: {self.date}," \
               f"start_date must be not later, than today"


class DateDifferError(Exception):
    def __str__(self):
        return "Date start can't be bigger, than date end"


class TakeAndSkipDifferError(Exception):
    def __init__(self, take, skip):
        self.take = take
        self.skip = skip

    def __str__(self):
        return f"Differ between take ({self.take} and skip" \
               f"({self.skip} must be between 1000 and 0)"

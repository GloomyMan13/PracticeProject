class StartDateAttributeError(Exception):
    """
    Own Exception. Used in gui, raises if date_start later than today
    """
    def __init__(self, date):
        self.date = date

    def __str__(self):
        return f"Wrong date: {self.date}," \
               f"start_date must be not later, than today"


class DateDifferError(Exception):
    """
    Own Exception. Used in gui, raises if date_start bigger than date_end
    """
    def __str__(self):
        return "Date start can't be bigger, than date end"


class TakeAndSkipDifferError(Exception):
    """
    Own Exception. Used in gui, raises if (take-skip) > 1000 or < 1
    """
    def __init__(self, take, skip):
        self.take = take
        self.skip = skip

    def __str__(self):
        return f"Differ between take ({self.take} and skip" \
               f"({self.skip} must be between 1000 and 0)"

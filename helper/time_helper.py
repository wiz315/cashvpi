from datetime import datetime, timedelta
import pytz

class Timez():
    def time_now():
        dt = pytz.utc.localize(datetime.now())
        ist_dt = dt.astimezone(pytz.timezone('Asia/Damascus'))
        return ist_dt
    def next_order_time(days):
        day = Timez.time_now() + timedelta(days)
        return day

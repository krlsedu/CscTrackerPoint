import os
from datetime import datetime

import pytz

from service.Interceptor import Interceptor


class Utils(Interceptor):
    def __init__(self):
        super().__init__()

    @staticmethod
    def work_time():
        n = datetime.now()
        t = n.timetuple()
        y, m, d, h, min, sec, wd, yd, i = t
        h = h - 3
        return 8 <= h <= 19

    @staticmethod
    def work_day():
        n = datetime.now()
        t = n.timetuple()
        y, m, d, h, min, sec, wd, yd, i = t
        return wd < 5

    @staticmethod
    def read_file(file_name):
        file_dir = os.path.dirname(os.path.realpath('__file__'))
        file_name = os.path.join(file_dir, file_name)
        file_handle = open(file_name)
        content = file_handle.read()
        file_handle.close()
        return content

    @staticmethod
    def get_diff_time(time_a, time_b):
        try:
            time_a = datetime.strptime(time_a, "%Y-%m-%d %H:%M:%S")
        except:
            time_a = datetime.strptime(time_a, "%Y-%m-%d %H:%M:%S.%f")

        try:
            time_b = datetime.strptime(time_b, "%Y-%m-%d %H:%M:%S")
        except:
            time_b = datetime.strptime(time_b, "%Y-%m-%d %H:%M:%S.%f")
        diff = time_b - time_a
        return diff.seconds

    @staticmethod
    def get_format_date_time(dt_string, format):
        try:
            dt_string = datetime.strptime(dt_string, "%Y-%m-%d %H:%M:%S")
        except:
            dt_string = datetime.strptime(dt_string, "%Y-%m-%d %H:%M:%S.%f")
        return dt_string.strftime(format)

    @staticmethod
    def get_format_date_time_in_tz(dt_string, format, original_tz='America/Sao_Paulo', new_tz='UTC'):
        dt_obj = datetime.strptime(dt_string, format)

        original_tz_ = pytz.timezone(original_tz)
        dt_obj = original_tz_.localize(dt_obj)

        new_tz_ = pytz.timezone(new_tz)
        new_dt_obj = dt_obj.astimezone(new_tz_)

        return new_dt_obj.strftime(format)



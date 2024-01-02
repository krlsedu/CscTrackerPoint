from datetime import datetime, timezone

import pandas as pd

from repository.HttpRepository import HttpRepository
from service.Interceptor import Interceptor
from service.Utils import Utils

http_repository = HttpRepository()


class PointService(Interceptor):
    def __init__(self):
        super().__init__()

    def save(self, data, headers=None, args=None):
        if 'delete' in data:
            date_time_ = None
            if 'date_time' in data:
                date_time_ = data['date_time']
                del data['date_time']

            if data['delete']:
                del data['delete']
                http_repository.delete('user_points', data, headers)
                if date_time_ is not None:
                    data['date_time'] = date_time_
            else:
                return

        configs = http_repository.get_object('configs', {}, headers)

        if 'date_time' not in data:
            data['date_time'] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        else:
            time_ = Utils.get_format_date_time(data['date_time'], "%Y-%m-%d %H:%M:%S")
            data['date_time'] = Utils.get_format_date_time_in_tz(time_, "%Y-%m-%d %H:%M:%S",
                                                                 configs['time_zone'], 'UTC')

        date_time = Utils.get_format_date_time_in_tz(data['date_time'], "%Y-%m-%d %H:%M:%S",
                                                     'UTC', configs['time_zone'])

        date = date_time.split(' ')[0]
        data['date'] = date
        points = http_repository.get_objects('user_points', {'date': date}, headers)
        points = sorted(points, key=lambda d: d['date_time'], reverse=True)
        for point in points:
            if 'id' in data and data['id'] == point['id']:
                point['edited'] = True
                for key in point.keys():
                    if key in data:
                        point[key] = data[key]
            else:
                point['edited'] = False

        if 'id' not in data:
            data['edited'] = True
            points.append(data)

        points = sorted(points, key=lambda d: d['date_time'])
        count = 1
        data_list = []
        for point in points:
            if point['edited'] or point['seq_mark'] != count:
                point['seq_mark'] = count
                point['type'] = "S" if point['seq_mark'] % 2 == 0 else "E"
                data_list.append(point)

            if 'edited' in point:
                del point['edited']

            count += 1

        http_repository.save('user_points', data_list, headers)

        worked_time = 0
        time_ant = None
        for point in points:
            if point['type'] == "E":
                time_ant = point['date_time']
            elif point['type'] == "S":
                worked_time += Utils.get_diff_time(time_ant, point['date_time'])

        worked_time_ = http_repository.get_object('user_worked_time', {'date': date}, headers)

        if worked_time_ is not None and worked_time_['id'] is not None:
            worked_time_['worked_time'] = worked_time
        else:
            worked_time_ = {
                'worked_time': worked_time,
                'date': date
            }

        http_repository.save('user_worked_time', worked_time_, headers)

    def get_agrupped_points(self, headers=None, args=None):
        configs = http_repository.get_object('configs', {}, headers)
        if 'mesAno' not in args:
            args['mesAno'] = datetime.now(timezone.utc).strftime("%Y-%m")

        ano_ = args['mesAno'].split('-')[0]
        mes_ = args['mesAno'].split('-')[1]
        period_ = f"date >= {args['mesAno']}-01 and date <= {args['mesAno']}-{Utils.last_month_day(mes_, ano_)}"
        filter_ = {
            'period': period_
        }
        points = http_repository.get_objects('user_points', filter_, headers)
        points = sorted(points, key=lambda d: d['date_time'])
        points_list = []
        date = None
        point_ = {}
        dates_ = []
        for point in points:
            date_ = Utils.get_format_date_time(point['date'], "%Y-%m-%d")
            if date is None or date != date_:
                date = date_
                worked_time_ = http_repository.get_object('user_worked_time', {'date': date}, headers)
                if worked_time_ is None:
                    worked_time_ = 0
                else:
                    worked_time_ = worked_time_['worked_time']
                point_ = {
                    'date': date_,
                    'worked_time': worked_time_,
                    'points': []
                }
                points_list.append(point_)
                dates_.append(date_)
            del point['date']
            del point['last_update']
            del point['create_date']
            del point['user_id']
            point['date_time'] = Utils.get_format_date_time_in_tz(point['date_time'], "%Y-%m-%d %H:%M:%S.%f",
                                                                  'UTC', configs['time_zone'])
            point_['points'].append(point)
        for day in Utils.all_days(mes_, ano_):
            day_ = args['mesAno'] + "-" + Utils.fill_left(str(day), 2)
            if day_ not in dates_:
                point_ = {
                    'date': day_,
                    'worked_time': 0,
                    'points': []
                }
                points_list.append(point_)
        points_list = sorted(points_list, key=lambda d: d['date'])
        return points_list

    def get_worked_time(self, headers=None):
        data = http_repository.get_all_objects('user_worked_time', headers)
        holidays = http_repository.get_all_objects('user_holidays', headers)
        df = pd.DataFrame(data)
        df_holidays = pd.DataFrame(holidays)

        df['date'] = pd.to_datetime(df['date'], utc=True)
        df_holidays['date'] = pd.to_datetime(df_holidays['date'], utc=True)

        df = df[df['date'] != pd.to_datetime('today').strftime('%Y-%m-%d')]
        df_holidays = df_holidays[df_holidays['date'] != pd.to_datetime('today').strftime('%Y-%m-%d')]

        df_holidays['holiday_time'] = df_holidays.apply(
            lambda row: 0 if row['date'].weekday() in [5, 6] else 8 * 3600 + 48 * 60, axis=1)

        df['expected_time'] = df.apply(lambda row: 0 if row['date'].weekday() in [5, 6] else 8 * 3600 + 48 * 60, axis=1)

        df_agg = df.groupby(['user_id']).agg({'worked_time': 'sum',
                                              'expected_time': 'sum',
                                              'date': ['min', 'max']})

        df_agg.columns = ['_'.join(col) for col in df_agg.columns.values]
        df_agg.reset_index(inplace=True)

        df_agg['working_days'] = df_agg.apply(self.calculate_working_days, axis=1)

        df_agg['expected_time_sum'] = df_agg['working_days'] * (8 * 3600 + 48 * 60)

        df_agg['expected_time_sum'] = df_agg['expected_time_sum'] - df_holidays['holiday_time'].sum()

        df_agg['extra_time'] = df_agg['worked_time_sum'] - df_agg['expected_time_sum']

        df_agg['worked_time_sum'] = df_agg['worked_time_sum'].apply(
            lambda x: f'{x // 3600}h {(x // 60) % 60:02d}m {x % 60:02d}s')
        df_agg['expected_time_sum'] = df_agg['expected_time_sum'].apply(
            lambda x: f'{x // 3600}h {(x // 60) % 60:02d}m {x % 60:02d}s')
        df_agg['extra_time'] = df_agg['extra_time'].apply(lambda x: f'{x // 3600}h {(x // 60) % 60:02d}m {x % 60:02d}s')

        df_agg['date_min'] = df_agg['date_min'].dt.strftime('%Y-%m-%d')
        df_agg['date_max'] = df_agg['date_max'].dt.strftime('%Y-%m-%d')
        # df_agg['worked_time_sum'] = df_agg['worked_time_sum'].apply(str)
        # df_agg['expected_time_sum'] = df_agg['expected_time_sum'].apply(str)
        # df_agg['extra_time'] = df_agg['extra_time'].apply(str)

        df_agg = df_agg.rename(columns={'worked_time_sum': 'worked_time',
                                        'expected_time_sum': 'expected_time'})
        df_agg = df_agg.rename(columns={'date_min': 'first_day',
                                        'date_max': 'last_day'})

        return df_agg.to_json(orient='records')

    def calculate_working_days(self, row):
        today = pd.Timestamp.now(tz=row['date_min'].tzinfo)
        yesterday = today - pd.DateOffset(days=1)
        return len(pd.bdate_range(row['date_min'], yesterday))

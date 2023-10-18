from datetime import datetime, timezone

from repository.HttpRepository import HttpRepository
from service.Interceptor import Interceptor
from service.Utils import Utils

http_repository = HttpRepository()


class PointService(Interceptor):
    def __init__(self):
        super().__init__()

    def save(self, data, headers=None, args=None):
        if 'delete' in data:
            if data['delete']:
                del data['delete']
                http_repository.delete('user_points', data, headers)
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

        points = http_repository.get_objects('user_points', args, headers)
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
        points_list = sorted(points_list, key=lambda d: d['date'])
        return points_list

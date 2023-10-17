from datetime import datetime

from repository.HttpRepository import HttpRepository
from service.Interceptor import Interceptor

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
        if 'date_time' not in data:
            data['date_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        date_time = data['date_time']
        date = date_time.split(' ')[0]
        data['date'] = date
        points = http_repository.get_objects('user_points', {'date': date}, headers)
        points = sorted(points, key=lambda d: d['date_time'], reverse=True)
        for point in points:
            if 'id' in data and data['id'] == point['id']:
                for key in point.keys():
                    if key in data:
                        point[key] = data[key]

        if 'id' not in data:
            data['seq_mark'] = 0
            points.append(data)

        points = sorted(points, key=lambda d: d['date_time'])
        count = 1
        data_list = []
        for point in points:
            if point['seq_mark'] != count:
                point['seq_mark'] = count
                point['type'] = "S" if point['seq_mark'] % 2 == 0 else "E"
                data_list.append(point)
            count += 1

        http_repository.save('user_points', data_list, headers)

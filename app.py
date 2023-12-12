from flask import Flask, request
from flask_cors import CORS
from prometheus_flask_exporter import PrometheusMetrics

from service.PointService import PointService
from service.Utils import Utils

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

metrics = PrometheusMetrics(app, group_by='endpoint', default_labels={'application': 'CscTrackerPoint'})

point_service = PointService()


@app.route('/register', methods=['POST'])
def register_post():  # put application's code here
    headers = request.headers
    args = request.args
    data = request.get_json()
    try:
        point_service.save(data, headers, args)
        added_ = {"status": "success", "message": "register added"}
        if 'id' not in data:
            msg_ = "Marcação adicionada com sucesso: " + str(data)
        else:
            msg_ = "Marcação atualizada com sucesso: " + str(data)
        Utils.inform_to_client(added_, "Marcação", headers, msg_)
        return added_, 201, {'Content-Type': 'application/json'}
    except Exception as e:
        print(e)

        not_added_ = {"status": "error", "message": "register not added"}

        if 'id' not in data:
            msg_ = "Erro ao adicionar marcação: " + str(data)
        else:
            msg_ = "Erro ao atualizar marcação: " + str(data)

        Utils.inform_to_client(not_added_, "Marcação", headers, msg_)
        return not_added_, 500, {'Content-Type': 'application/json'}


@app.route('/register', methods=['GET'])
def register_get():  # put application's code here
    headers = request.headers
    args = request.args
    try:
        points = point_service.get_agrupped_points(headers, args)
        return points, 200, {'Content-Type': 'application/json'}
    except Exception as e:
        print(e)
        return {"status": "error", "message": "register getted"}, 500, {'Content-Type': 'application/json'}


@app.route('/worked-time', methods=['GET'])
def worked_time():  # put application's code here
    headers = request.headers
    args = request.args
    try:
        points = point_service.get_worked_time(headers)
        return points, 200, {'Content-Type': 'application/json'}
    except Exception as e:
        print(e)
        return {"status": "error", "message": "register getted"}, 500, {'Content-Type': 'application/json'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

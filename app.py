from flask import Flask, request

from flask_cors import CORS
from prometheus_flask_exporter import PrometheusMetrics

from service.PointService import PointService

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
        return {"status": "success", "message": "register added"}, 201, {'Content-Type': 'application/json'}
    except Exception as e:
        print(e)
        return {"status": "error", "message": "register not added"}, 500, {'Content-Type': 'application/json'}


@app.route('/register', methods=['GET'])
def register_get():  # put application's code here
    headers = request.headers
    args = request.args
    try:
        points = point_service.get_agrupped_points( headers, args)
        return points, 200, {'Content-Type': 'application/json'}
    except Exception as e:
        print(e)
        return {"status": "error", "message": "register getted"}, 500, {'Content-Type': 'application/json'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

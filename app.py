from csctracker_py_core.starter import Starter
from csctracker_py_core.utils.utils import Utils

from service.PointService import PointService

starter = Starter()
app = starter.get_app()
http_repository = starter.get_http_repository()

point_service = PointService(starter.get_remote_repository())


@app.route('/register', methods=['POST'])
def register_post():  # put application's code here
    headers = http_repository.get_headers()
    args = http_repository.get_args()
    data = http_repository.get_json_body()
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
    headers = http_repository.get_headers()
    args = http_repository.get_args()
    try:
        points = point_service.get_agrupped_points(headers, args)
        return points, 200, {'Content-Type': 'application/json'}
    except Exception as e:
        print(e)
        return {"status": "error", "message": "register getted"}, 500, {'Content-Type': 'application/json'}


@app.route('/worked-time', methods=['GET'])
def worked_time():  # put application's code here
    headers = http_repository.get_headers()
    try:
        points = point_service.get_worked_time(headers)
        return points, 200, {'Content-Type': 'application/json'}
    except Exception as e:
        print(e)
        return {"status": "error", "message": "register getted"}, 500, {'Content-Type': 'application/json'}


starter.start()

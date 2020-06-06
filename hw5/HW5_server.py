from flask import Flask, jsonify, request
from multiprocessing import Process
from HW5_backend import train_script
from HW5_backend import data_checker
from HW5_backend import get_free_id
from HW5_backend import Datasets
from HW5_backend import Models
from HW5_backend import get_session
from HW5_backend import predict_from_model
from logging.config import dictConfig
import logging
import sys


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://sys.stdout',
        'formatter': 'default'
    }},
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi']
    }
})


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.debug("test")
app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
session = get_session()


@app.route('/model/<id>', methods=['GET'])
def model_info(id=None):
    logging.debug("'GET' branch in model/<id>")
    model_db = session.query(Models).get(id)
    if model_db is not None:
        return jsonify(response={"status": model_db.status,
                                 "model": model_db.model,
                                 "cv_results": model_db.cv_results})
    return jsonify(response={"error": "Not valid model_id"}), 400


@app.route('/model/<id>/predict', methods=['POST'])
def model(id=None):
    if request.method == 'POST':
        logging.debug("'POST' branch in /model/<id>/predict")
        model_db = session.query(Models).get(id)
        if model_db is not None:
            m_str = "model with id : {} in DB".format(model_db.id)
            logging.debug(m_str)
            res = {"error": "unknown error"}
            if model_db.status == "train":
                m_dict = {"error":
                          "model already in training stage"}
                return jsonify(response=m_dict), 400
            elif model_db.status == "new":
                m_dict = {"error":
                          "model in line for training"}
                return jsonify(response=m_dict), 400
            elif model_db.status == "ready":
                pred = []
                try:
                    pred = predict_from_model(
                        request.get_json()["data"],
                        model_db
                    )
                except Exception as e:
                    return jsonify(response={"error": str(e)}), 400
                return jsonify(response=pred)
            elif model_db.status == "error":
                m_dict = {"error":
                          "can't train model"}
                return jsonify(response=m_dict), 400
            return jsonify(response=res)
        else:
            m_dict = {"error": "Model not exist: " + str(id)}
            return jsonify(response=m_dict), 400
    return jsonify(response={"error": "Not valid model_id"}), 400


@app.route('/hello', methods=['GET'])
def hello_world():
    arr = dict()
    arr["blah"] = []
    arr["blah"].append("stuff")
    return jsonify(response=arr)


@app.route('/train', methods=['GET', 'POST'])
def train():
    if request.method == 'GET':
        logging.debug("'GET' branch in app/train")
        return jsonify(response={"status": "work"})
    elif request.method == 'POST':
        logging.debug("'POST' branch in app/train")
        if type(request.get_json()["data"]) != str\
                or type(request.get_json()["target"]) != str\
                or type(request.get_json()["n_folds"]) != int\
                or type(request.get_json()["fit_intercept"]) != bool\
                or type(request.get_json()["l2_coef"]) != list:
            return jsonify(response={"error": "not valid request"}), 400
        error = data_checker(
            request.get_json()["data"],
            request.get_json()["target"]
        )
        if error is not None:
            logging.error("'data_checker' end with error")
            return jsonify(response={'error': error}), 400
        model_id = get_free_id()
        d_obj = Datasets(id=model_id,
                         data=request.get_json()["data"],
                         target=request.get_json()["target"],
                         n_folds=request.get_json()["n_folds"],
                         fit_intercept=request.get_json()["fit_intercept"],
                         l2_coef=request.get_json()["l2_coef"])
        new_model = Models(id=model_id,
                           model={},
                           cv_results={},
                           status="new",
                           datasets_id=model_id,
                           datasets=d_obj)
        session.add(new_model)
        session.commit()
        logging.debug("'POST' commit after checker")
        return jsonify(response={"model_id": model_id})
    return jsonify(response={"error": "not valid request"}), 400


if __name__ == '__main__':
    p = Process(target=train_script)
    p.start()
    app.run()

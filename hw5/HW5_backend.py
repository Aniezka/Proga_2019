from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, ForeignKey, Text
from sqlalchemy import create_engine, Column, Integer, MetaData, Float, Boolean
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import relationship, backref, sessionmaker
from time import sleep
from io import StringIO
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, make_scorer
import pandas as pd
import numpy as np
import logging


with open("config.json", "r") as f:
    DATABASE = eval(f.read())
engine = create_engine(URL(**DATABASE))
Base = declarative_base()


class Models(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    model = Column(JSONB)
    cv_results = Column(JSONB)
    status = Column(Text)
    datasets_id = Column(
        Integer,
        ForeignKey('datasets.id'), unique=True
    )
    datasets = relationship('Datasets',
                            backref=backref('models', uselist=False))


class Datasets(Base):
    __tablename__ = 'datasets'
    id = Column(Integer, primary_key=True)
    data = Column(Text)
    target = Column(Text)
    n_folds = Column(Integer)
    fit_intercept = Column(Boolean, unique=False, default=True)
    l2_coef = Column(ARRAY(Float))


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def get_session():
    return session


def check_models_db():
    for model in session.query(Models):
        if model.status == "new":
            m_str = "'check_model_db' find new model with id: "
            logging.debug(m_str + str(model.id))
            session.query(Models)\
                .filter_by(id=model.id)\
                .update({"status": "train"})
            session.commit()
            m_str = "script set 'train' status for model with id: "
            logging.debug(m_str + str(model.id))
            fit_inter = model.datasets.fit_intercept
            n_folds = model.datasets.n_folds
            alpha_arr = model.datasets.l2_coef
            status_tr = "ready"
            res = {}
            try:
                X_train, Y_train = get_train_data(model.datasets.data,
                                                  model.datasets.target)
                res = train_kfold(
                    X_train,
                    Y_train,
                    k_folds=n_folds,
                    fit_intercept=fit_inter,
                    alpha_arr=alpha_arr
                )
            except Exception as e:
                status_tr = "error"
                m_str = "Error in 'train' model: "
                logging.debug(m_str + str(model.id))
                logging.debug("Exception: " + str(e))
                res["model"] = {}
                res["cv_results"] = {}
            session.query(Models)\
                .filter_by(id=model.id)\
                .update({"model": res["model"],
                         "cv_results": res["cv_results"],
                         "status": status_tr})
            m_str = "script set " + status_tr\
                    + " status for model with id: "
            logging.debug(m_str + str(model.id))
            session.commit()


def train_script():
    while True:
        sleep(10)
        check_models_db()
        m_str = "'train_script' check new models once in 10 sec."
        logging.debug(m_str)


def data_checker(data, target):
    data = StringIO(data)
    logging.debug("'data_cheker' working\n")
    try:
        df = pd.read_csv(data, sep=",")
    except Exception:
        return "'read_csv' end with error"
    if target not in df.columns:
        return "'target' column noi in data"
    if df.isnull().values.any():
        return "'data' contain NaN"
    return None


def get_free_id():
    count = 1
    idx_arr = [i[0] for i in session.query(Models.id).all()]
    while count in idx_arr:
        count += 1
    return count


def get_train_data(data, target):
    data = StringIO(data)
    df = pd.read_csv(data, sep=",")
    df = df.reindex(sorted(df.columns), axis=1)
    y_train = df[target].to_frame()
    X_train = df.drop(target, axis=1)
    return X_train, y_train


def predict_from_model(data, model_db):
    m_str = "'predict_from_model' with id: "
    logging.debug(m_str + str(model_db.id))
    data = StringIO(data)
    df = pd.read_csv(data, sep=",")
    X_predict = df.reindex(sorted(df.columns), axis=1)
    fit_inter = model_db.datasets.fit_intercept
    mdl = Ridge()
    if fit_inter:
        mdl.intercept_ = model_db.model["intercept"]
    coef_arr = []
    m_str = "'predict_from_model' with id: "
    logging.debug(m_str + str(model_db.model))
    for feature in X_predict.columns:
        for name_coef, val in model_db.model["coef"].items():
            if feature == name_coef:
                coef_arr.append(val)
    if len(model_db.model["coef"].keys()) != len(X_predict.columns):
        m_str = "data for prediction is not valid for this model"
        return {"error": m_str}
    if df.isnull().values.any():
        return {"error": "'data' contain NaN"}
    mdl.coef_ = np.array(coef_arr)
    res = mdl.predict(X_predict)
    m_str = "end 'predict_from_model': "
    logging.debug(m_str + str(res))
    return {"result": res.tolist()}


def train_kfold(X_train_df,
                y_train_df,
                k_folds=2,
                fit_intercept=True,
                alpha_arr=[1, 0.1, 0.01, 0.001]):
    logging.debug("'train_kfold' function is progress...")
    X_train, y_train = np.array(X_train_df), np.array(y_train_df)
    logging.debug(X_train)
    parameters = [{'fit_intercept': [fit_intercept],
                   'alpha': alpha_arr}]
    clf = GridSearchCV(Ridge(),
                       parameters,
                       cv=k_folds,
                       scoring=make_scorer(
                           mean_squared_error,
                           greater_is_better=False))
    clf.fit(X_train, y_train)
    best_model = clf.best_estimator_
#    logging.debug(best_model.intercept_)
#    logging.debug(best_model.coef_)
    result_json = dict()
    result_json["model"] = {}
    if fit_intercept:
        result_json["model"]["intercept"] = best_model.intercept_[0]
    result_json["model"]["coef"] = {}
    for ind, coef in enumerate(best_model.coef_[0]):
        ind_buf = X_train_df.columns[ind]
        result_json["model"]["coef"][ind_buf] = coef
    result_json["cv_results"] = {}
    for ind, alp in enumerate(alpha_arr):
        m_dict = {
            "mean_mse": -clf.cv_results_['mean_test_score'][ind]
        }
        result_json["cv_results"][alp] = m_dict
    logging.debug("'train_kfold' function end")
#    logging.debug(result_json)
    return result_json

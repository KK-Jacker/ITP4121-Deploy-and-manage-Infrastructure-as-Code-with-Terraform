import flask
from flask_login import current_user


def query_application_by_id(application_model, application_id):
    if current_user.user_type == "student":
        return flask.g.session.query(application_model).filter_by(
            id=application_id).filter_by(student=current_user).first()

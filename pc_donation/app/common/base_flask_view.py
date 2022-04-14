from flask_classful import FlaskView


class BaseFlaskView(FlaskView):
    method_dashified = True

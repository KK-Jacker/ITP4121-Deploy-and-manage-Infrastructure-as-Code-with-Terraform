import flask
from flask import render_template

from app import TemplateConstants
from app.errors import bp


@bp.errorhandler(404)
def not_found_error(error):
    app.logger.error(error)
    return render_template(TemplateConstants.Errors.STATUS_404), 404


@bp.errorhandler(500)
def internal_error(error):
    flask.g.session.rollback()
    app.logger.error(error)
    return render_template(TemplateConstants.Errors.STATUS_500), 500

import logging
import os
from logging.handlers import SMTPHandler, RotatingFileHandler

import flask
import login as login
from flask import Flask, request, current_app, session, render_template, redirect, url_for
from flask_babel import Babel
from flask_babel import lazy_gettext as _l
from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from jaraco.docker import is_docker
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.ext.flask.flask_middleware import FlaskMiddleware
from opencensus.trace.samplers import AlwaysOnSampler
from sqlalchemy.orm import sessionmaker, with_polymorphic
from werkzeug.middleware.proxy_fix import ProxyFix

# from app import User
from app.common.azure_blob import get_img_url_with_blob_sas_token
from app.common.base_flask_view import BaseFlaskView
from app.loader import get_views
from app.model.models import User
from app.route_constants import RouteConstants
from app.template_constants import TemplateConstants
from config import Config, GoogleMapConfig

login.login_view = RouteConstants.NoAuthView.LOGIN
login.login_message = _l("Please log in to access this page.")
db = SQLAlchemy(use_native_unicode='utf8')

migrate = Migrate()
login = LoginManager()
mail = Mail()
bootstrap = Bootstrap()
dp = datepicker()
moment = Moment()
babel = Babel()
csrf = CSRFProtect()


def create_app(config_class=Config):
    app = Flask(__name__)
    # logger = logging.getLogger(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    dp.init_app(app)
    moment.init_app(app)
    babel.init_app(app)
    csrf.init_app(app)
    # FlaskMiddleware(app, exporter=AzureExporter(
    #     connection_string="InstrumentationKey={}".format(app.config["APPINSIGHTS_INSTRUMENTATIONKEY"])),
    #                 sampler=ProbabilitySampler(rate=1.0))
    FlaskMiddleware(app,
                    exporter=AzureExporter(
                        connection_string="InstrumentationKey={}".format(
                            app.config["APPINSIGHTS_INSTRUMENTATIONKEY"])),
                    sampler=AlwaysOnSampler())

    # let the template able to call custom function
    app.jinja_env.globals.update(RouteConstants=RouteConstants)
    app.jinja_env.globals.update(get_locale=get_locale)
    app.jinja_env.globals.update(google_map_key=GoogleMapConfig.KEY)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    for view in get_views():
        view.register(app)

    if app.config["MAIL_SERVER"]:
        auth = None
        if app.config["MAIL_USERNAME"] or app.config["MAIL_PASSWORD"]:
            auth = (app.config["MAIL_USERNAME"],
                    app.config["MAIL_PASSWORD"])
        secure = None
        if app.config["MAIL_USE_TLS"]:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config["MAIL_SERVER"], app.config["MAIL_PORT"]),
            fromaddr="no-reply@" + app.config["MAIL_SERVER"],
            toaddrs=app.config["ADMINS"],
            subject="Pc_donation Failure",
            credentials=auth,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    if not os.path.exists("logs"):
        os.mkdir("logs")
    file_handler = RotatingFileHandler(
        "logs/{}_pc_donation.log".format("docker" if is_docker() else "host"),
        maxBytes=10240,
        backupCount=10)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s: %(message)s "
                          "[in %(pathname)s:%(lineno)d]"))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    # logger = logging.getLogger(__name__)
    # handler = AzureEventHandler(
    #     connection_string="InstrumentationKey={}".format(app.config["APPINSIGHTS_INSTRUMENTATIONKEY"]))
    handler = AzureLogHandler(
        connection_string="InstrumentationKey={}".format(
            app.config["APPINSIGHTS_INSTRUMENTATIONKEY"]))
    handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s: %(message)s "
                          "[in %(pathname)s:%(lineno)d]"))
    handler.setLevel(logging.ERROR)
    app.logger.addHandler(handler)
    app.register_error_handler(404, page_not_found)

    # for logHandler in app.logger.handlers:
    #     logHandler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s "
    #                                               "[in %(pathname)s:%(lineno)d]"))
    # logger.addHandler(
    #     AzureLogHandler(
    #         connection_string="InstrumentationKey={}".format(app.config["APPINSIGHTS_INSTRUMENTATIONKEY"])
    #     )
    # )

    app.logger.setLevel(logging.INFO)
    app.logger.info("pc_donate startup")

    @app.before_request
    def before_request():
        flask.g.locale = "zh_TW" if str(get_locale()).startswith("zh") else str(get_locale())
        session = sessionmaker()
        session.configure(bind=db.engine)
        flask.g.session = session()


    @app.after_request
    def after_request(response):
        flask.g.session.close()
        return response

    return app

@babel.localeselector
def get_locale():
    # return request.accept_languages.best_match(current_app.config["LANGUAGES"])
    # return "zh"

    language = request.accept_languages.best_match(
        current_app.config["LANGUAGES"])

    if language == "zh":
        language = "zh_Hant"
    if session.get("language") is not None:
        language = session["language"]

    return language


def page_not_found(e):
    return render_template(TemplateConstants.Errors.STATUS_404), 404


@login.unauthorized_handler
def unauthorized():
    # do stuff
    return redirect(url_for(RouteConstants.NoAuthView.LOGIN))


@login.user_loader
def load_user(current_user_id):
    all_user_type = with_polymorphic(User, "*")
    current_user = flask.g.session.query(all_user_type).filter(
        User.id == current_user_id).first()
    return current_user




import json
import os
from functools import cache

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

basedir = os.path.abspath(os.path.dirname(__file__))


@cache
def get_secret(name):
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=os.environ.get('VAULT_URL'), credential=credential)
    retrieved_secret = client.get_secret(name)
    return retrieved_secret.value


class DatabaseConfig(object):
    # db_user = 'test@project-share-test'
    # db_pass = 'Fyp12345'
    # db_host = 'project-share-test.mysql.database.azure.com'
    # db_port = '3306'
    # db_name = 'pc_donation'
    # web_port = 80
    db_user = os.environ["DB_USER"]
    db_pass = os.environ["DB_PASS"]
    db_host = os.environ["DB_HOST"]
    db_port = 3306
    db_name = os.environ["DB_NAME"]
    web_port = 80


class SmtpConfig(object):
    # server = "smtp.sendgrid.net"
    # port = 587
    # TLS = True
    # user = "apikey"
    # key = "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"
    # sender = "no-reply@em7761.ishare.support"
    sender = "no-reply@em7761.ishare.support"
    server = "0.0.0.0"
    port = 25
    TLS = False
    user = ""
    key = ""


class ApplicationInsightConfig(object):
    KEY = get_secret("ApplicationInsightsKey")


class GoogleMapConfig(object):
    KEY = get_secret("GoogleMapKey")


class RecaptchaConfig(object):
    SECRET_KEY = get_secret("RecaptchaSecretKey")
    RECAPTCHA_SITE_KEY = get_secret("RecaptchaSiteKey")
    ENABLE = False


class AiAnalyzeConfig(object):
    KEY = get_secret("CognitiveAccountComputerVisionKey")
    ENDPOINT = get_secret("CognitiveAccountComputerVisionEndpoint")


class AiChatbotConfig(object):
    webChatBotSecret = json.loads(get_secret("WebChatBotSecret"))
    donor_chatbot_key = webChatBotSecret["donor"]
    student_chatbot_key = webChatBotSecret["student"]
    teacher_chatbot_key = webChatBotSecret["teacher"]
    volunteer_chatbot_key = webChatBotSecret["volunteer"]
    anonymous_chatbot_key = webChatBotSecret["anonymous"]


class AiTranslateConfig(object):
    KEY = get_secret("CognitiveAccountTextTranslationKey")
    ENDPOINT = get_secret("CognitiveAccountTextTranslationEndpoint")
    LOCATION = "eastasia"
    PATH = "/translate"
    CONSTRUCTED_URL = ENDPOINT + PATH


class AiTextAnalyticsConfig(object):
    KEY = get_secret("CognitiveAccountTextAnalyticsKey")
    ENDPOINT = get_secret("CognitiveAccountTextAnalyticsEndpoint")


class ContentModeratorConfig(object):
    KEY = get_secret("CognitiveAccountContentModeratorKey")
    ENDPOINT = get_secret("CognitiveAccountContentModeratorEndpoint")


class AiFaceConfig(object):
    KEY = get_secret("CognitiveAccountFaceKey")
    ENDPOINT = get_secret("CognitiveAccountFaceEndpoint")


class FormRecognizeConfig(object):
    KEY = get_secret("RecaptchaSecretKey")
    ENDPOINT = get_secret("CognitiveAccountFormRecognizerEndpoint")


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SECURITY_PASSWORD_SALT = os.environ.get(
        'SECURITY_PASSWORD_SALT') or 'you-will-never-guess'
    RECAPTCHA_PUBLIC_KEY = os.environ.get(
        'RECAPTCHA_PUBLIC_KEY') or RecaptchaConfig.RECAPTCHA_SITE_KEY
    RECAPTCHA_PRIVATE_KEY = os.environ.get(
        'RECAPTCHA_PRIVATE_KEY') or RecaptchaConfig.SECRET_KEY
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DatabaseConfig.db_user}:{DatabaseConfig.db_pass}@{DatabaseConfig.db_host}:{DatabaseConfig.db_port}/{DatabaseConfig.db_name}?charset=utf8"

    # for local
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db') + "?charset=utf8mb4"

    # SQLALCHEMY_ENGINE_OPTIONS = {"max_overflow": 20, "pool_size": 30}

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or SmtpConfig.server
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or SmtpConfig.port)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or SmtpConfig.user
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or SmtpConfig.key
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or SmtpConfig.sender
    NGINX_PORT = os.environ.get('NGINX_PORT') or DatabaseConfig.web_port
    # TODO: put all RELATED Azure config back to form or model not controller (need debug)
    AZURE_STORAGE_ACCOUNT_NAME = os.environ.get(
        'AZURE_STORAGE_ACCOUNT_NAME') or get_secret("StorageAccountName")
    AZURE_STORAGE_ACCOUNT_KEY = os.environ.get('AZURE_STORAGE_ACCOUNT_KEY') or get_secret("StorageAccountKey")
    AZURE_STORAGE_CONNECTION_STRING = os.environ.get('AZURE_STORAGE_CONNECTION_STRING') or get_secret(
        "StorageConnectionString")
    AZURE_STORAGE_TEMP_CONTAINER_NAME = os.environ.get(
        'AZURE_STORAGE_TEMP_CONTAINER_NAME') or "temp"
    AZURE_STORAGE_CONTAINER_NAME = os.environ.get(
        'AZURE_STORAGE_CONTAINER_NAME') or "picture"
    APPINSIGHTS_INSTRUMENTATIONKEY = os.environ.get(
        'APPINSIGHTS_INSTRUMENTATIONKEY') or ApplicationInsightConfig.KEY
    ADMINS = ['your-email@example.com']
    LANGUAGES = ['zh', 'en']
    GOOGLEMAPS_KEY = os.environ.get('GOOGLEMAPS_KEY') or GoogleMapConfig.KEY
    POSTS_PER_PAGE = 25
    PAGING_PER_PAGE = 10

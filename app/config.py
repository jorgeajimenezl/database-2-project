from datetime import timedelta
from secrets import token_hex
import os


class Environments(object):
    PRODUCTION = "production"
    DEVELOPMENT = "development"


def _read_file(path):
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        return f.read()


# Core
SERVER_NAME = os.environ.get("SERVER_NAME", "127.0.0.1:5000")
SECRET_KEY = os.environ.get("SECRET_KEY", token_hex(30))
ENV = os.environ.get("FLASK_ENV", Environments.PRODUCTION)
DEBUG = ENV == "development"

# Database
SQLALCHEMY_DATABASE_URI = os.environ.get(
    "SQLALCHEMY_DATABASE_URI", "mysql+pymysql://root:m@127.0.0.1:3306/Trucks?charset=utf8mb4"
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Authentication
JWT_PRIVATE_KEY = _read_file(os.environ.get("JWT_PRIVATE_KEY", ".keys/jwtRS256.key"))
JWT_PUBLIC_KEY = _read_file(os.environ.get("JWT_PUBLIC_KEY", ".keys/jwtRS256.key.pub"))
PWD_RESET_EXP = timedelta(seconds=os.environ.get("PWD_RESET_EXP", 3_600))
ACCOUNT_VERIFICATION = (
    JWT_PRIVATE_KEY and JWT_PUBLIC_KEY and os.environ.get("ACCOUNT_VERIFICATION", False)
)
REMEMBER_COOKIE_DURATION = timedelta(
    seconds=os.environ.get("REMEMBER_COOKIE_DURATION", 3_600 * 24 * 7)
)
LOGIN_MAX_RETIRES = os.environ.get("LOGIN_MAX_RETIRES", 4)

# Email
MAIL_SERVER = os.environ.get("MAIL_SERVER", "localhost")
MAIL_PORT = os.environ.get("PORT", 465)
MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", False)
MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL", False)
MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "console")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "example")
MAIL_DEFAULT_SENDER = os.environ.get(
    "MAIL_DEFAULT_SENDER", f"{MAIL_USERNAME}@{MAIL_SERVER}"
)
MAIL_DEBUG = ENV == Environments.DEVELOPMENT

# Debug
DEBUG_TB_ENABLED = DEBUG
DEBUG_TB_INTERCEPT_REDIRECTS = False

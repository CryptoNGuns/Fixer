from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import RotatingFileHandler
from elasticsearch import Elasticsearch
import os
from flask import request
from flask_babel import Babel

app = Flask(__name__)
app.config.from_object(Config)

babel = Babel(app)
def get_locale():
    #return request.accept_languages.best_match(app.config['LANGUAGES'])
    return 'pl'
babel.init_app(app, locale_selector=get_locale)

app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']],ca_certs="./security/elastic_http_ca.crt",basic_auth=("elastic", app.config['ELASTIC_PASSWORD'])) \
    if app.config['ELASTICSEARCH_URL'] else None

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'


if not app.debug:
    # ... I will not use crash email notifications at now

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/fixer.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Fixer startup')

	
from app import routes, models, errors
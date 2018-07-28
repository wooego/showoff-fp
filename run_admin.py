#!/usr/bin/env python
#coding:utf-8
from flask import Flask
from showoff.admin.controllers import admin
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config.from_envvar('SHOWOFF_ADMIN_CONFIG', silent=True)

handler = RotatingFileHandler(app.config['ADMIN_LOGFILE'],encoding='UTF-8')
handler.setLevel(logging.DEBUG)
logging_format = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
handler.setFormatter(logging_format)
app.logger.addHandler(handler)

app.register_blueprint(admin, url_prefix=app.config['ADMIN_PREFIX'])

if __name__ == '__main__':
    app.run(host=app.config['ADMIN_HOST'], port=app.config['ADMIN_PORT'])


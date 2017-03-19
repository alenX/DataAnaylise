# -*- coding: utf-8 -*-
from flask import Flask
app = Flask(__name__)
# DEBUG = True
# SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:1128@localhost:3306/douban?charset=utf8'
SQLALCHEMY_DATABASE_URI = 'sqlite:////douban.db'
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
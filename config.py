# -*- coding: utf-8 -*-
from flask import Flask
import os
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# DEBUG = True
# SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:1128@localhost:3306/douban?charset=utf8'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'douban.sqlite')
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
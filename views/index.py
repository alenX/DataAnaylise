# -*- coding: utf-8 -*-
from flask import Flask, Blueprint, render_template

app = Flask(__name__)
vw_index = Blueprint('index', __name__, template_folder='templates')
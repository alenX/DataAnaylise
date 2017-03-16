# -*- coding: utf-8 -*-
from flask import Flask
from views.index import vw_index
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.register_blueprint(vw_index)
    app.run(debug=True)

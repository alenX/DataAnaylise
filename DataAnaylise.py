# -*- coding: utf-8 -*-
from flask import Flask
from views.index import vw_index
from views.book_view import vw_book
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.register_blueprint(vw_index)
    app.register_blueprint(vw_book)
    app.run(debug=True)

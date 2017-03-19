# -*- coding: utf-8 -*-
from flask import Flask
from views.index import vw_index
from views.book_view import vw_book
from ext import db as mysql_db

app = Flask(__name__)
app.config.from_object('config')
mysql_db.init_app(app)
with app.app_context():
    mysql_db.create_all()


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.register_blueprint(vw_index)
    app.register_blueprint(vw_book)
    app.run(debug=True)

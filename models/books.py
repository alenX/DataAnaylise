# -*- coding: utf-8 -*-
from ext import db as mysql_db


class douban_new_books(mysql_db.Model):
    __tablename__ = 'dt_douban_new_books'
    id = mysql_db.Column(mysql_db.Integer, primary_key=True)
    title = mysql_db.Column(mysql_db.String(256))
    author = mysql_db.Column(mysql_db.String(256))
    desc = mysql_db.Column(mysql_db.String(256))
    href = mysql_db.Column(mysql_db.String(256))
    src = mysql_db.Column(mysql_db.String(256))
    comment = mysql_db.Column(mysql_db.String(512))
    score = mysql_db.Column(mysql_db.Float)
    batchdate = mysql_db.Column(mysql_db.String(32))

    def seris(self):
        return {'id': self.id, 'title': self.title, 'author': self.author,
                'desc': self.desc, 'comment': self.comment, 'score': self.score,
                'batchdate': self.batchdate}

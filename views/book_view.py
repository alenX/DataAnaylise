# -*- coding: utf-8 -*-

# 图书趋势分析
from flask import Flask, app

app = Flask(__name__)

douban_url = 'https://book.douban.com/latest?icn=index-latestbook-all'  # 新书速递


@app.route('/collect_douban_book')
def collect_douban_book():
    pass

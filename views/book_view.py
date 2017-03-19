# -*- coding: utf-8 -*-

# 图书趋势分析
from flask import Flask, Blueprint, jsonify
import requests
from bs4 import BeautifulSoup
import datetime, re
from models.books import douban_new_books
from ext import db  as mysql_db

vw_book = Blueprint('book', __name__, template_folder='templates')

# app = Flask(__name__)

douban_url = 'https://book.douban.com/latest?icn=index-latestbook-all'  # 新书速递


@vw_book.route('/collect_douban_book', methods=['POST'])
def collect_douban_book():
    bs = BeautifulSoup(requests.get(douban_url).content, 'lxml')
    for u in bs.select('#content > div > div.article > ul > li'):
        href = str(u.select_one('a')['href']).strip()
        title = str(u.select_one('div > h2 > a').text).strip()
        src = str(u.select_one('a > img')['src']).strip()
        score = str(u.select_one('div > p.rating > span.font-small.color-lightgray').text).strip()
        desc = str(u.select_one('div > p.color-gray').text).strip()
        comment = str(u.select_one('div > p.detail').text).strip()
        if not re.findall(r'\d+', score):
            score = 0
        dnb = douban_new_books()
        dnb.href = href
        dnb.author = (desc.split('/')[0]).strip().encode('utf-8')
        dnb.title = title.encode('utf-8')
        dnb.src = src.encode('utf-8')
        dnb.score = score
        dnb.comment = comment.encode('utf-8')
        dnb.desc = desc.encode('utf-8')
        dnb.batchdate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        mysql_db.session.add(dnb)
    mysql_db.session.commit()
    return jsonify({'code': 1})

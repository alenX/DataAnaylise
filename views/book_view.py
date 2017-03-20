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
    type = ['.article', '.aside']
    for tt in type:
        for u in bs.select('#content > div > div' + tt + ' > ul > li'):
            href = str(u.select_one('a')['href']).strip()
            title = str(u.select_one('div > h2 > a').text).strip()
            src = str(u.select_one('a > img')['src']).strip()
            score = str(u.select_one('div > p.rating > span.font-small.color-lightgray').text).strip()
            desc = str(u.select_one(
                'div > p.color-gray').text).strip()
            if tt == '.article':
                comment = str(u.select_one(
                    'div > p.detail').text).strip()
            elif tt == '.aside':
                i = 0
                comment = ''
                for divp in u.select('div > p'):
                    i += 1
                    if i == 3:
                        comment = divp.text.strip()
            else:
                comment = ''
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


@vw_book.route('/query_books')
def query_books_score():
    first_book = douban_new_books.query.filter_by(score=0).all()
    second_book = douban_new_books.query.filter(douban_new_books.score>0,douban_new_books.score <=4).all()
    third_book = douban_new_books.query.filter(douban_new_books.score > 4 , douban_new_books.score <= 7).all()
    fourth_book = douban_new_books.query.filter(douban_new_books.score > 7).all()
    return jsonify({'data': [len(first_book), len(second_book), len(third_book), len(fourth_book)], 'categories': ['0', '1-4', '5-7', '8-10']})

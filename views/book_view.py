# -*- coding: utf-8 -*-

# 图书趋势分析
from flask import Flask, Blueprint, render_template
import requests
from bs4 import BeautifulSoup
import MySQLdb
import time, re

vw_book = Blueprint('book', __name__, template_folder='templates')
conn = MySQLdb.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='1128',
    db='douban',
)
cur = conn.cursor()

conn.set_character_set('utf8')
cur.execute('SET NAMES utf8;')
cur.execute('SET CHARACTER SET utf8;')
cur.execute('SET character_set_connection=utf8;')
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
        content = str(u.select_one('div > p.detail').text).strip()
        print('------')
        sql = "insert into dt_douban_new_books values(1,%s,%s,%s,%s,%s,%s,%s,%s)"
        if not re.findall(r'\d+', score):
            score = 0
        cur.execute(sql,
                    (title, '', desc, href, src, content, float(score),
                     ''
                     ))
        conn.commit()
    cur.close()
    conn.commit()
    conn.close()
    return render_template('index.html')

# -*- coding: utf-8 -*-
# 采集诗词工具类

from ext import db as mysql_db

from bs4 import BeautifulSoup
import requests
import re


class Ci(mysql_db.Model):  # 古诗词
    __tablename__ = 'dt_boot_ci'
    id = mysql_db.Column(mysql_db.Integer, primary_key=True)
    title = mysql_db.Column(mysql_db.String(256))
    author = mysql_db.Column(mysql_db.String(256))
    dynasty = mysql_db.Column(mysql_db.String(256))
    content = mysql_db.Column(mysql_db.BLOB)
    media = mysql_db.Column(mysql_db.String(256))


def SpliderDetail(detail_url):
    if detail_url is None:
        return
    bs_detail = BeautifulSoup(requests.get(detail_url).content, 'lxml')
    title = str(bs_detail.select_one(
        'body > div.main3 > div.shileft > div.son1 > h1'))  # body > div.main3 > div.shileft > div.son1 > h1
    dynasty = str(bs_detail.select_one(
        'body > div.main3 > div.shileft > div.son2 > p '))  # body > div.main3 > div.shileft > div.son2 > p:nth-child(2)
    author = str(bs_detail.select_one('body > div.main3 > div.shileft > div.son2 > p + p  > a'))
    content = str(bs_detail.select_one('body > div.main3 > div.shileft > div.son2 > div.cont'))[29:-6]
    print(content)
    if author == 'None':
        author = str(bs_detail.select_one(
            'body > div.main3 > div.shileft > div.son2 > p + p  '))  # body > div.main3 > div.shileft > div.son2 > p:nth-child(2)
    # re_ti = re.search(r'<h1>[\u4E00-\u9FFF]+·?[\u4E00-\u9FFF]+</h1>', title)
    re_dy = re.search(r'</span>[\u4E00-\u9FFF]+</p>', dynasty)
    re_au = re.search(r'>[\u4E00-\u9FFF]+<', author)

    title_rs = '未知'
    author_rs = '未名'
    dynasty_rs = '未知'
    title_rs = title[4:-5]

    if re_dy:
        dynasty_rs = re_dy.group(0)[7:-4]

    if re_au:
        author_rs = re_au.group(0)[1:-1]

    ci = Ci()
    ci.title = title_rs.encode('utf-8')
    ci.author = author_rs.encode('utf-8')
    ci.dynasty = dynasty_rs.encode('utf-8')
    ci.content = content.encode('utf-8')
    ci.media=''
    mysql_db.session.add(ci)
    mysql_db.session.commit()
    print(title_rs + '--' + dynasty_rs.replace("\n", "") + '--' + author_rs.replace("\n", ""))


def CiSplider(ci_url='http://so.gushiwen.org/type.aspx?p=1'):
    bs = BeautifulSoup(requests.get(ci_url).content, 'lxml')
    for item in bs.find_all(attrs={"class": "sons"}):
        m = re.search(r'<p><a href="/\w+.aspx', str(item))
        if m:
            SpliderDetail('http://so.gushiwen.org/' + m.group(0).split('/')[1])

# if __name__ == '__main__':
#     CiSplider()
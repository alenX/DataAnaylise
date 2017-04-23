# -*- coding: utf-8 -*-
from ext import db as mysql_db

class Ci(mysql_db.Model):
    __tablename__='boot_ci'

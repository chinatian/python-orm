#!/usr/bin/env python
#-*- coding: utf8 -*-

import random
import settings
import models
from db.connection import Connection
from datetime import datetime

class User(models.Model):
    __tablename__ = "user"
    __pk__ = "id"
    __insert_counter__ = random.randint(0, settings.DB_TABLES_LEN-1)

class UserDetail(models.Model):
    __tablename__ = "user_detail"
    __pk__ = "id"
    __shard_field__ = "user_id"

class UserIndex(models.Model):
    __tablename__ = "user_index"
    __pk__ = "id"
    __shard_field__ = "field_value"
    
    @classmethod
    def get_user_id(cls, field_name, field_value):
        db_conf, tb_shard = models.get_db_table(field_value)
        cnn = Connection(*db_conf)
        try:
            tb_name = '%s_%d' % (cls.__tablename__, tb_shard,)
            sql = 'SELECT `user_id` FROM `%s` WHERE `field_name`=%%s AND `field_value`=%%s' % (tb_name,)
            row = cnn.get(sql, field_name, field_value)
            return row.user_id
        finally:
            cnn.close()

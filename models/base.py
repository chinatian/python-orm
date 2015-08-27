#!/usr/bin/env python
#-*- coding: utf8 -*-

"""A lightweight sharding orm framework."""

import random
import settings
from db.connection import Connection

class Model(object):
    """模型基类"""
    __tablename__ = None
    __pk__ = "id"
    __shard_field__ = None
    __insert_counter__ = random.randint(0, settings.DB_TABLES_LEN-1)
    
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    
    def insert(self):
        """插入当前对象"""
        cls = self.__class__
        if cls.__shard_field__:
            db_conf, tb_shard = get_db_table(getattr(self, cls.__shard_field__))
        else:
            print cls.__insert_counter__
            db_conf, tb_shard = get_db_table(cls.__insert_counter__)
            cls.__insert_counter__ = cls.__insert_counter__ + 1
            if cls.__insert_counter__ >= settings.DB_TABLES_LEN:
                cls.__insert_counter__ = 0
        cnn = Connection(*db_conf)
        print 'db = %s ' % db_conf[1]
        try:
            tb_name = '%s_%d' % (cls.__tablename__, tb_shard,)

            sql = "UPDATE `seq` SET `id`=LAST_INSERT_ID(`id`+%d) WHERE `tb`=%%s" % settings.DB_TABLES_LEN
            print sql % tb_name 
            id = cnn.execute(sql, tb_name)
            print 'lastid %d' % id
            setattr(self, cls.__pk__, id)
            attrs = self.__dict__
           
            sql = "INSERT INTO `%s` (%s) VALUES (%s)" % (
                    tb_name,
                    ', '.join(map(lambda x: '`%s`' % x, attrs)),
                    ', '.join(['%s' for _ in attrs]),
                )
            print sql
            parameters = [attrs[x] for x in attrs]
            cnn.execute(sql, *parameters)
			
            return getattr(self, cls.__pk__)
        finally:
            cnn.close()
    
    @classmethod
    def get(cls, id):
        db_conf, tb_shard = get_db_table(id)
        cnn = Connection(*db_conf)
        try:
            tb_name = '%s_%d' % (cls.__tablename__, tb_shard,)
            sql = 'SELECT * FROM `%s` WHERE `%s`=%%s' % (tb_name, cls.__pk__,)
            row = cnn.get(sql, id)
            return cls(**row)
        finally:
            cnn.close()
    
    def update(self):
        """修改当前对象"""
        cls = self.__class__
        id = getattr(self, cls.__pk__)
        db_conf, tb_shard = get_db_table(id)
        cnn = Connection(*db_conf)
        try:
            tb_name = '%s_%d' % (cls.__tablename__, tb_shard,)
            attrs = self.__dict__
            sql = 'UPDATE `%s` SET %s WHERE `%s`=%%s' % (
                    tb_name,
                    ', '.join(['%s=%%s' % x for x in attrs if x != cls.__pk__]),
                    cls.__pk__,
                )
            parameters = [attrs[x] for x in attrs if x != cls.__pk__]
            parameters.append(getattr(self, cls.__pk__))
            return cnn.execute(sql, *parameters)
        finally:
            cnn.close()
    
    def delete(self):
        """删除当前对象"""
        cls = self.__class__
        id = getattr(self, cls.__pk__)
        db_conf, tb_shard = get_db_table(id)
        cnn = Connection(*db_conf)
        try:
            tb_name = '%s_%d' % (cls.__tablename__, tb_shard,)
            sql = 'DELETE FROM `%s` WHERE `%s`=%%s' % (tb_name, cls.__pk__,)
            return cnn.execute(sql, id)
        finally:
            cnn.close()

def get_db_table(val):
    if type(val) not in (long, int,):
        val = hash(val)
    if val < 0:
        val = abs(val)
    if val >= settings.DB_TABLES_LEN:
        val = val % settings.DB_TABLES_LEN
	print val
    return settings.DB_TABLES[val]

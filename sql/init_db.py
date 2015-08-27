#-*- coding: utf-8 -*-

import MySQLdb

for d in range(16):
    conn=MySQLdb.Connect(host='localhost',user='root',passwd='sa')
    curs=conn.cursor()
    curs.execute('drop database platform_test_%d' % d)
    curs.execute('create database platform_test_%d' % d)
    curs.close()
    conn.commit()
    conn.close()

print 'create table for seq...'
import seq
print 'seq over'
print 'ceate table for user...'
import user
print 'user over'

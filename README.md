# 使用python千行代码搞定数据库分布分表
## 要解决的问题
- 应用程序随着业务量增加主要的性能瓶颈在数据库存取上
- 大多数数据库没有完善的分库分表的机制，单表超过1000万速度会明显下降
- 本文章是通过python语言实现一个可在生产环境下使用的一套分库分表系统
## 技术储备
- 要求python2.6+，但不是3
- 安装mysql数据库
- 在win下或者linux下下载各种资源包使python能够连接mysql
- 能够使用python独立完成程序的编写

## 代码编写
### 基本原理说明
如何解决怎么分配主键id的问题，其实这个问题有两个一是主键如何分配，二是主键id如何不重复
在每个数据内放置一个单独记录该数据中有哪些表并且每个表当前最大id是多少。
该表数据结构如下
<pre><code>
CREATE TABLE `seq` (
  `id` bigint(20) NOT NULL,
  `tb` varchar(32) NOT NULL,
  UNIQUE KEY `tb_UNIQUE` (`tb`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='生成id序列号';
</code></pre>
- seq存放数据如下：
<pre><code>
id  tb
1	user_0
17	user_1
417	user_10
177	user_11
193	user_12
209	user_13
225	user_14
241	user_15
289	user_2
49	user_3
65	user_4
337	user_5
97	user_6
113	user_7
129	user_8
145	user_9
1	user_index_0
17	user_index_1
161	user_index_10
177	user_index_11
193	user_index_12
209	user_index_13
225	user_index_14
241	user_index_15
33	user_index_2
49	user_index_3
65	user_index_4
337	user_index_5
97	user_index_6
113	user_index_7
129	user_index_8
145	user_index_9
</code></pre>


 
每个数据库中都会存在这样一个表，主键的id分配由各自的数据库负责，减少由中心服务器分配带来的压力单点的问题。
 
### 分库分表的规模设定
设定分为16个数据库，每个表在每个数据库中有16个分表。
比如user表：
<pre><code>
CREATE TABLE `user_0` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(200) DEFAULT NULL,
  `create_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=36583 DEFAULT CHARSET=utf8;
</code></pre>

建立16个数据库，每个数据库中user表的数量为16个，这样user表会有16×16个分表
数据库如下：
<pre><code>
CREATE DATABASE `platform_test_0`;

CREATE DATABASE `platform_test_1`;

CREATE DATABASE `platform_test_2`;

CREATE DATABASE `platform_test_3`;

CREATE DATABASE `platform_test_4`;

CREATE DATABASE `platform_test_5`;

CREATE DATABASE `platform_test_6`;

CREATE DATABASE `platform_test_7`;

CREATE DATABASE `platform_test_8`;

CREATE DATABASE `platform_test_9`;

CREATE DATABASE `platform_test_10`;

CREATE DATABASE `platform_test_11`;

CREATE DATABASE `platform_test_12`;

CREATE DATABASE `platform_test_13`;

CREATE DATABASE `platform_test_14`;

CREATE DATABASE `platform_test_15`;
</code></pre>
 
每个数据库中user表的如下：
<pre><code>
seq
user_0
user_1
user_10
user_11
user_12
user_13
user_14
user_15
user_2
user_3
user_4
user_5
user_6
user_7
user_8
user_9
user_index_0
user_index_1
user_index_10
user_index_11
user_index_12
user_index_13
user_index_14
user_index_15
user_index_2
user_index_3
user_index_4
user_index_5
user_index_6
user_index_7
user_index_8
user_index_9
</code></pre>

 
## 代码编写
### 目录结构
- db - 数据库访问工具类
- moddels - 数据模型
- sql - 数据库创建及数据表创建
### 数据库访问工具类
直接使用Facebook的开源代码，如下：

<pre><code>
"""A lightweight wrapper around MySQLdb."""

import copy
import MySQLdb.constants
import MySQLdb.converters
import MySQLdb.cursors
import itertools
import logging
import time

class Connection(object):
    """A lightweight wrapper around MySQLdb DB-API connections.

    The main value we provide is wrapping rows in a dict/object so that
    columns can be accessed by name. Typical usage:

        db = database.Connection("localhost", "mydatabase")
        for article in db.query("SELECT * FROM articles"):
            print article.title

    Cursors are hidden by the implementation, but other than that, the methods
    are very similar to the DB-API.

    We explicitly set the timezone to UTC and the character encoding to
    UTF-8 on all connections to avoid time zone and encoding errors.
    """
    def __init__(self, host, database, user=None, password=None,
                 max_idle_time=7*3600):
        self.host = host
        self.database = database
 
 </code></pre>
### 数据库创建及数据表创建

数据库以及表的创建需要编写程序实现，主要代码存在sql中
  
1. init_db.py 负责创建16个数据库：
 
2. seq.py在每个表中创建seq表
 
3. 创建具体数据表
 
### 核心models层说明
 

base.py 作为全部models的基类，其他类需继承 代码如下：
 
 <pre><code>

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
  </code></pre>

## 代码使用
插入：
 <pre><code>
from models.user import User
from datetime import datetime
for n in range(1000):
	name = 'chinatian_%d' % n
	phone = '1234432343'
	pw = '123456'
	pw_md5 = '343243243'
	u = User(name=name,
			password='dsfdsfdsfds', 
			last_login_time=datetime.now())
	u.insert()
	
</code></pre>
 
查询：
  <pre><code>
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

</code></pre>

## 其他第三方数据库分库方案
- [mycat] http://mycat.io/ 脱胎于淘宝
- [Oceanus] https://github.com/58code/Oceanus 58同城数据库中间件
- [本项目托管地址] https://github.com/chinatian/python-orm

作者：田强
10年互联网研发，就职大唐电信新华瑞德，qq:27998561 
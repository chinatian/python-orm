#-*- coding: utf-8 -*-

import MySQLdb

for d in range(16):
    db=MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="sa",
        db="platform_test_%d" % d,
        use_unicode=True,
        charset="utf8")
    for t in range(16):
        c = db.cursor()
        c.execute("""
            CREATE  TABLE `user_index_%d` (
              `id` BIGINT NOT NULL,
              `field_name` VARCHAR(32) NOT NULL ,
              `field_value` VARCHAR(127) NOT NULL ,
              `user_id` BIGINT NOT NULL ,
              PRIMARY KEY (`id`) ,
              INDEX `index_field_value` (`field_value` ASC) )
            COMMENT = '用户索引表，按照field_value分片，映射到user_id'
            """ % t)
        c.execute("INSERT INTO seq (id, tb) VALUES (%s, %s)", (16*t+d, 'user_index_%d' % t))
        c.close()
    db.commit()
    db.close()

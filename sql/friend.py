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
            CREATE  TABLE `friend_%d` (
              `id` BIGINT NOT NULL,
              `user_id` BIGINT NOT NULL,
              `friend_id` BIGINT NOT NULL,
              `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
              PRIMARY KEY (`id`),
              INDEX `index_user_id` (`user_id` ASC) )
            COMMENT = '好友关系'
            """ % t)
        c.execute("INSERT INTO seq (id, tb) VALUES (%s, %s)", (16*t+d, 'friend_%d' % t))
        c.close()
    db.commit()
    db.close()

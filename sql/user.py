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
            CREATE  TABLE `user_%d` (
                `id` BIGINT NOT NULL,
                `name` VARCHAR(32) NULL,
                `password` VARCHAR(64) NULL,
                `gender` VARCHAR(2) NULL,
                `head_img_url` VARCHAR(255) NULL,
                `status` INT NULL,
                `last_login_time` DATETIME NOT NULL,
                `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`) );
            """ % t)
        c.execute("INSERT INTO seq (id, tb) VALUES (%s, %s)", (16*t+d, 'user_%d' % t))
        c.close()
    db.commit()
    db.close()

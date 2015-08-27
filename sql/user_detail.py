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
            CREATE  TABLE `user_detail_%d` (
                `id` BIGINT NOT NULL,
                `user_id` BIGINT NOT NULL,
                `field_name` VARCHAR(32) NOT NULL,
                `field_value` VARCHAR(127) NULL,
                `updated_at` DATETIME NOT NULL,
                `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`),
                INDEX `user_id_index` (`user_id` ASC) )
            """ % t)
        c.execute("INSERT INTO seq (id, tb) VALUES (%s, %s)", (16*t+d, 'user_detail_%d' % t))
        c.close()
    db.commit()
    db.close()

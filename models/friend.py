#!/usr/bin/env python
#-*- coding: utf8 -*-

from db.connection import Connection
import models
from models.user import User

class Friend(models.Model):
    __tablename__ = "friend"
    __pk__ = "id"
    __shard_field__ = "user_id"
    
    @classmethod
    def get_friends(cls, user_id):
        """返回好友列表"""
        db_conf, tb_shard = models.get_db_table(user_id)
        cnn = Connection(*db_conf)
        try:
            tb_name = '%s_%d' % (cls.__tablename__, tb_shard,)
            sql = 'SELECT `id`, `user_id`, `friend_id`, `created_at` FROM `%s` WHERE `user_id`=%%s' % (tb_name,)
            iter = cnn.iter(sql, user_id)
            return [cls(**row) for row in iter]
        finally:
            cnn.close()
    
    @classmethod
    def get_friend_users(cls, user_id):
        """返回好友用户信息列表"""
        return [User.get(friend.friend_id) for friend in cls.get_friends(user_id)]
#coding: utf-8

import os.path

DEBUG = True

DATABASES_LEN = 16
TABLES_LEN = 16
DB_TABLES_LEN = DATABASES_LEN * TABLES_LEN

# [(db_host, db_name, db_user, db_password), ...]
DATABASES = [('localhost', 'platform_test_%d' % x, 'root', 'sa') for x in range(DATABASES_LEN)]

DB_TABLES = [None for x in range(DB_TABLES_LEN)]
for t in range(TABLES_LEN):
    for d in range(DATABASES_LEN):
        DB_TABLES[t * DATABASES_LEN + d] = (DATABASES[d], t,)

OPTIONS = dict(
    platform_title=u"Rekoo Social Game Platform",
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    #ui_modules={"Entry": EntryModule},
    xsrf_cookies=False,
    cookie_secret="TWqWFYJERdS9JZxonBt8hxLCtYeaD0N8skhbbhTU8MY=",
    login_url="/auth/login",
)


import logging
           
logger = logging.getLogger()
hdlr = logging.FileHandler('log.txt')
formatter = logging.Formatter('%(message)s')
hdlr.setFormatter(formatter)           
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)
          
  

for t in range(256):
    print '%d = %s' % (t, DB_TABLES[t])
    logger.info('%d = %s' % (t, DB_TABLES[t]))
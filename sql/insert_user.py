
from models.user import User

for n in range(2000):
	name = 'chinatian_%d' % n
        phone = '12344%d' % n
        pw = '123456'
        pw_md5 = '123455'
        pw_md5.update(pw)
        u = User(name=name, password=pw_md5.hexdigest(), last_login_time=datetime.now())
        u.insert()
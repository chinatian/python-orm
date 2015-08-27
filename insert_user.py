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
	
		
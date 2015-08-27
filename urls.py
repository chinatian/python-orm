#-*- coding: utf8 -*-

import controllers
from controllers import user, auth, friend

handlers = [
    (r"/", controllers.HomeHandler),
    (r"/auth/login", auth.LoginHandler),
    (r"/auth/logout", auth.LogoutHandler),
    (r"/user/signup", user.SignUpHandler),
    (r"/user/signup/phone", user.SignUpPhoneHandler),
    (r"/user/signup/password", user.SignUpPasswordHandler),
    (r"/me/friends", friend.MyFriendsHandler),
]

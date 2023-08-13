# -*- encoding: utf-8 -*-
import unittest

from app import db, app
from app.utils.saltypassword import *
from app.models import *


class UserModelTest(unittest.TestCase):
    def setUp(self) -> None:
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_info(self):
        pwd = SaltyPassword.saltify('123456')
        user = BlogUser(username='user', email='useremail@example.com', password=pwd)
        user.set_avatar(size=100, default='https://blog.miguelgrinberg.com/static/miguel.jpg')

        self.assertTrue(user.password.is_('123456'))

    def test_db_actions(self):
        admin1 = BlogUser(username='admin1', email='admin1@example.com')
        admin2 = BlogUser(username='admin2', email='shguoju2008@example.com')

        BlogUser(False).add(admin1).add(admin2).commit()

        self.assertEqual(BlogUser.get_uuser(username='admin1'), admin1)
        self.assertNotEqual(BlogUser.get_uuser(email='admin@example.com'), admin2)

    def test_user_subscription(self):
        user1 = BlogUser(username='user1', email='user1@example.com')
        user2 = BlogUser(username='user2', email='user2@example.com')
        user3 = BlogUser(username='user3', email='user3@example.com')
        BlogUser(False).add_all([user1, user2, user3]).commit()

        user1.follows(user3).follows(user2)
        user2.follows(user1)
        user3.follows(user2)

        BlogUser(False).commit()

        self.assertTrue(user3 in user1.following and user2 in user1.following)
        self.assertTrue(user1 in user2.following)
        self.assertTrue(user2 in user3.following)


if __name__ == '__main__':
    unittest.main()

# -*- encoding: utf-8 -*-
import unittest

from app import db, app
from app.security.saltypassword import *
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
        user = BlogUser(username='user', email='admin@example.com', password=pwd)
        user.set_avatar(size=100, default='https://blog.miguelgrinberg.com/static/miguel.jpg')

        avatar_url_expect = ('https://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61/?s=100&d=https%3A%2F'
                             '%2Fblog.miguelgrinberg.com%2Fstatic%2Fmiguel.jpg')
        self.assertTrue(user.password.is_('123456'))
        self.assertEqual(user.avatar, avatar_url_expect)

    def test_user_posts(self):
        """
        TODO test cases completion + db stuff add
        :return:
        """
        ...

    def test_user_subscription(self):
        ...

    def test_user_unsubscription(self):
        ...

    def test_fetch_subscribed_posts(self):
        ...


if __name__ == '__main__':
    unittest.main()

# -*- encoding: utf-8 -*-
import random

from context import *
from app.models import *
from app.utils.saltypassword import *


chr_type = [
        lambda: chr(random.randint(97, 122)),
        lambda: chr(random.randint(48, 57))
    ]


@app_context
class BuildUser:
    @staticmethod
    def random_email() -> str:
        return ''.join([random.choice(chr_type)() for _ in range(20)])+'@testuser.com'

    @staticmethod
    def random_password() -> str:
        return ''.join([chr(random.randint(48, 122)) for _ in range(random.randint(20, 36))])

    def build_user(self) -> Self:
        # creating adminds
        pwd = SaltyPassword.saltify('china666')
        admin1 = BlogUser(username='admin', email='shanebilibili@outlook.com', password=pwd)
        admin2 = BlogUser(username='shane_admin', email='bwxiang23@uwcchina.org', password=pwd)
        BlogUser(False).add(admin1).add(admin2)

        # creating random test-users
        BlogUser(False).add_all([BlogUser(
            email=(email := self.random_email()),
            username=email,
            password=SaltyPassword.saltify(self.random_password())
        ) for _ in range(4)]).commit()

        return self

    def build_posts(self) -> Self:
        users = BlogUser(False).all()
        for _ in range(10):
            user = random.choice(users)
            post = Posts()
            post.poster = user
            post.content = f'I say {_}'
            Posts().add(post)
        Posts().commit()
        return self

    def build_user_relation(self) -> Self:
        users = BlogUser(False).all()
        for _ in range(12):
            user1: BlogUser = random.choice(users)
            user2: BlogUser = random.choice(users)
            if user1 == user2:
                continue
            user1.follow(user2, autocommit=False)
            user2.follow(user1, autocommit=False)
        BlogUser(False).commit()
        return self

    def build(self) -> None:
        (self.build_user()
         .build_posts()
         .build_user_relation())


if __name__ == '__main__':
    BuildUser().build()

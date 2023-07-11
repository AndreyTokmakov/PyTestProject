from typing import List

import pytest
from faker import Faker

from Training.day_two.Fakes.UserDetails import User

from Jobs import JobProvider


class Test_User(object):

    @pytest.fixture()
    def fake_user(self):
        fake = Faker()
        fake.add_provider(JobProvider)

        self.user = User(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            # job=fake.job(),
            job=fake.random_job_title(),
            address=fake.address(),
        )

    def test_fake_user_type(self, fake_user):
        assert User is type(self.user)

    def test_user_name(self, fake_user):
        assert f'{self.user.first_name} {self.user.last_name}' == self.user.name
        print('\n', self.user)

    def test_job_title(self, fake_user):
        titles_expected: List[str] = ['Software Engineer', 'Database admin']
        assert any(self.user.job == title for title in titles_expected)


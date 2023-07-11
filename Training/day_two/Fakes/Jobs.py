import random
from typing import List

from faker import Faker
from faker.providers import BaseProvider


class JobProvider(BaseProvider):

    def random_job_title(self):
        titles: List[str] = ['Software Engineer', 'Database admin']
        return random.choice(titles)

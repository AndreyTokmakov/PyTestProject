import pytest
from ThePerson import Person


@pytest.fixture
def list_of_persons():
    return [
        Person('Jonh', 'McClane', 'Police Officer'),
        Person('Sara', 'Jala', 'IT Manager'),
    ]
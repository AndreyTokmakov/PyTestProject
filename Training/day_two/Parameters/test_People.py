from ThePerson import Person
from People import printListOfPeople, printListOfPeopleOld


def test_printListOfPeopleOld(list_of_persons):
    assert printListOfPeopleOld(list_of_persons) == [
        'Jonh: Police Officer',
        'Sara: IT Manager',
    ]


def test_printListOfPeople(list_of_persons):
    assert printListOfPeople(list_of_persons) == [
        'Jonh: Police Officer',
        'Sara: IT Manager',
    ]

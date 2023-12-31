from ThePerson import Person


def test_person_repr(list_of_persons):
    p1: Person = list_of_persons[0]
    assert 'Person(Jonh McClane, Job: Police Officer)' == str(p1)


def test_person_format(list_of_persons):
    p1: Person = list_of_persons[0]
    assert 'Jonh McClane, Police Officer' == p1.format()


def test_person_csv_format(list_of_persons):
    p1: Person = list_of_persons[0]
    assert 'Jonh,McClane,Police Officer' == p1.to_cv_format()

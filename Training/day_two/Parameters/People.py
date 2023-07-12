from typing import List


theList: List[str] = []


def printListOfPeopleOld(people_list) -> List[str]:
    for person in people_list:
        var = f'{person.person_name}: {person.job_title}'
        theList.append(var)
    return theList


def printListOfPeople(people_list) -> List[str]:
    return [f'{p.person_name}: {p.job_title}' for p in people_list]

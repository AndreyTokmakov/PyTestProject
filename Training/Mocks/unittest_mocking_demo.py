from http import HTTPStatus
from typing import Dict
import requests


def get_joke(timeout: int = 20):
    url: str = 'http://api.icndb.com/jokes/random'
    # url: str = 'https://api.jokes.one'

    try:
        response = requests.get(url, timeout=timeout)
    except requests.exceptions.ConnectionError as exc:
        return 'ConnectionError'
    except requests.exceptions.Timeout as exc:
        return 'Timeout'
    else:
        if HTTPStatus.OK == response.status_code:
            content: Dict = response.json()
            return content.get('value').get('joke')
        else:
            return 'No Jokes'


def joke_length() -> int:
    joke = get_joke()
    return len(joke)


if __name__ == '__main__':
    print(get_joke())

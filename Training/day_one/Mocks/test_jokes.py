import pytest
from unittest.mock import patch, MagicMock

import requests

from unittest_mocking_demo import joke_length, get_joke
from requests.exceptions import Timeout


class TestJokes(object):

    @pytest.mark.parametrize("joke, length", [
        ('Some funny joke', 15),
        ('Joke', 4),
        ('', 0),
        ('      ', 6)
    ])
    @patch('unittest_mocking_demo.get_joke')
    def test_the_joke_length(self, get_joke_mock, joke, length):
        get_joke_mock.return_value = joke
        assert length == joke_length()

    @pytest.mark.parametrize("code, joke, joke_expected", [
        (200, 'Nice joke', 'Nice joke'),
        (500, '', 'No Jokes'),
    ])
    @patch('unittest_mocking_demo.requests')
    def test_get_joke(self, requests_mock, code, joke, joke_expected):
        mocked_response = MagicMock(status_code=code)
        mocked_response.json.return_value = {'value': {'joke': joke}}
        requests_mock.get.return_value = mocked_response

        assert get_joke() == joke_expected

    @pytest.mark.parametrize("exception_type, joke, description", [
        (requests.exceptions.Timeout, 'Timeout', 'Server is down'),
        (requests.exceptions.ConnectionError, 'ConnectionError', 'Server is down'),
    ])
    @patch('unittest_mocking_demo.requests')
    def test_get_joke_exception_handling(self, requests_mock, exception_type, joke, description):
        requests_mock.exceptions = requests.exceptions
        requests_mock.get.side_effect = exception_type(description)

        assert get_joke() == joke

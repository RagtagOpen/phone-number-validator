import json
import pytest
from urllib.parse import urlencode

from phonescrubber import create_app


@pytest.fixture
def client():
    app = create_app('testing')
    client = app.test_client()

    yield client


def assert_phone_response(client, number, expected_response):
    """Runs a single test through phone_scrubber endpoint.

    Asserts that the formatting response for {number} is equal to
    {expected_response}.

    Args:
        client: a Flask client object, constructed in the fixture above and
            supplied as first parameter to each test in this file.
        number: a string of the number parameter to be supplied as the
            parameter to /v1/number/{number}.
        expected_response: a dictionary object representing expected JSON
            response.
    """
    query_string = urlencode({'number': number})
    rv = client.get(f'/v1/number/validate?{query_string}')
    json_loaded = json.loads(rv.data)

    assert (len(json_loaded['results']) == 1)
    assert (json_loaded['results'][0] == expected_response)


def test_valid_number(client):
    assert_phone_response(
        client,
        '5088435861',
        {
            "formatted": {
                "e164": "+15088435861",
                "national": "(508) 843-5861"
            },
            "location": {
                "description": "Massachusetts",
                "tz": ["America/New_York"]
            },
            "input": "5088435861",
            "reason": "possible",
            "type": "fixed_or_mobile",
            "valid": True
        }
    )


def test_valid_number_plus_and_parens(client):
    assert_phone_response(
        client,
        '+1(808)555-1212',
        {
            "formatted": {
                "e164": "+18085551212",
                "national": "(808) 555-1212"
            },
            "location": {
                "description": "Hawaii",
                "tz": ["Pacific/Honolulu"]
            },
            "input": "+1(808)555-1212",
            "reason": "possible",
            "type": "fixed_or_mobile",
            "valid": True
        }
    )


def test_valid_number_spaces(client):
    assert_phone_response(
        client,
        '603 555 1234',
        {
            "formatted": {
                "e164": "+16035551234",
                "national": "(603) 555-1234"
            },
            "location": {
                "description": "New Hampshire",
                "tz": ["America/New_York"]
            },
            "input": "603 555 1234",
            "reason": "possible",
            "type": "fixed_or_mobile",
            "valid": True
        }
    )


def test_valid_number_dots(client):
    assert_phone_response(
        client,
        '+1 781.555.1212',
        {
            "formatted": {
                "e164": "+17815551212",
                "national": "(781) 555-1212"
            },
            "location": {
                "description": "Massachusetts",
                "tz": ["America/New_York"]
            },
            "input": "+1 781.555.1212",
            "reason": "possible",
            "type": "fixed_or_mobile",
            "valid": True
        }
    )


def test_number_too_short(client):
    assert_phone_response(
        client,
        '508843',
        {
            "input": "508843",
            "reason": "too_short",
            "valid": False
        }
    )


def test_number_too_long(client):
    assert_phone_response(
        client,
        '+150884358688',
        {
            "input": "+150884358688",
            "reason": "too_long",
            "valid": False
        }
    )


def test_number_too_long_parens(client):
    assert_phone_response(
        client,
        '+1 (508) 843-58688',
        {
            "input": "+1 (508) 843-58688",
            "reason": "too_long",
            "valid": False
        }
    )

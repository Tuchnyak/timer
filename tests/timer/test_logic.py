import pytest
from timer.logic import format_time

def test_format_time_under_a_minute():
    assert format_time(5) == "00:05"


def test_format_time_with_minutes():
    assert format_time(125) == "02:05"


@pytest.mark.parametrize("seconds, expected", [
    (0, "00:00"),
    (5, "00:05"),
    (125, "02:05"),
    (3600, "60:00"),
])
def test_format_time(seconds, expected):
    assert format_time(seconds) == expected


def test_format_time_minus_one():
    assert format_time(-1) == "00:00"



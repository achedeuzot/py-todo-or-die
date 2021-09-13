import datetime
from unittest.mock import patch

import pytest

from todo_or_die.exceptions import OverdueException
from todo_or_die.main import todo_or_die


def test_base_usage_works():
    todo_or_die("This is a message", when=False)
    with pytest.raises(OverdueException):
        todo_or_die("This is a message", when=True)

def test_usage_with_value_works():
    result = todo_or_die(42, "some todo message", when=False)
    assert result == 42
    with pytest.raises(OverdueException):
        todo_or_die(42, "some todo message", when=True)

def test_usage_with_callable_works():
    result = todo_or_die(lambda: 42, "some todo message", when=False)
    assert result == 42
    with pytest.raises(OverdueException):
        todo_or_die(lambda: 42, "some todo message", when=True)

def test_raises_if_wrong_args():
    # No args
    with pytest.raises(ValueError):
        todo_or_die()
    # Missing message
    with pytest.raises(ValueError):
        todo_or_die(when=False)
    with pytest.raises(ValueError):
        todo_or_die(when=True)
    # Second arg is not a string
    with pytest.raises(ValueError):
        todo_or_die(42, 17, when=True)
    # First arg is not a string
    with pytest.raises(ValueError):
        todo_or_die(42, when=True)


def test_raises_if_wrong_kwargs():
    with pytest.raises(ValueError):
        todo_or_die("This should be done for next week")


def test_raises_if_unknown_kwargs():
    with pytest.raises(ValueError):
        todo_or_die("This should be done for next week", unknown=True)


@patch('todo._utcnow')
def test_does_nothing_if_datetime_is_still_in_the_future(mocked_utcnow):
    mocked_utcnow.return_value = datetime.datetime(2021, 1, 1, 1, 1, 1)
    result = todo_or_die(42, "This need to be fixed later", by=datetime.datetime(2021, 12, 31, 1, 1, 1))
    assert result == 42

@patch('todo._utcnow')
def test_raises_if_datetime_is_past_due(mocked_utcnow):
    mocked_utcnow.return_value = datetime.datetime(2022, 1, 1, 1, 1, 1)
    with pytest.raises(OverdueException):
        todo_or_die(42, "This need to be fixed later", by=datetime.datetime(2021, 12, 31, 1, 1, 1))

# Works with date and datetime
@patch('todo._utcnow')
def test_raises_if_date_is_past_due(mocked_utcnow):
    mocked_utcnow.return_value = datetime.datetime(2022, 1, 1, 1, 1, 1)
    with pytest.raises(OverdueException):
        todo_or_die(42, "This need to be fixed later", by=datetime.date(2021, 12, 31))


def test_does_nothing_if_condition_is_boolean_false():
    result = todo_or_die(42, "This needs to be fixed later", when= 1 == 0)
    assert result == 42

def test_raises_when_condition_is_boolean_true():
    with pytest.raises(OverdueException):
        todo_or_die(42, "This needs to be fixed later", when= 1 == 1)

def test_does_nothing_if_condition_is_callable_that_returns_false():
    result = todo_or_die(42, "This needs to be fixed later", when= lambda: 1 == 0)
    assert result == 42

def test_raises_when_condition_is_callable_that_returns_true():
    with pytest.raises(OverdueException):
        todo_or_die(42, "This needs to be fixed later", when= lambda: 1 == 1)

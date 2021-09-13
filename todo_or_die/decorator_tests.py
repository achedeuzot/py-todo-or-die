import datetime
from unittest.mock import patch

import pytest

from todo_or_die.exceptions import OverdueException
from todo_or_die.decorator import TodoOrDie


def test_decorator_base_usage_works():
    @TodoOrDie("This need to be fixed later", when=False)
    def some_function(arg):
        return arg

    assert callable(some_function)
    assert some_function(True) == True

    with pytest.raises(OverdueException):
        @TodoOrDie("This need to be fixed later", when=True)
        def some_function(arg):
            return arg

def test_decorator_raises_if_wrong_arg():
    # Message is not a string
    with pytest.raises(ValueError):
        @TodoOrDie(42, when=False)
        def some_function(arg):
            return arg

def test_decorator_raises_if_no_kwargs():
    with pytest.raises(ValueError):
        @TodoOrDie("This needs to be fixed later")
        def some_function(arg):
            return arg

def test_decorator_raises_if_unknown_kwargs():
    with pytest.raises(ValueError):
        @TodoOrDie("This needs to be fixed later", unknown=True)
        def some_function(arg):
            return arg

@patch('todo._utcnow')
def test_decorator_does_nothing_if_datetime_is_still_in_the_future(mocked_utcnow):
    mocked_utcnow.return_value = datetime.datetime(2021, 1, 1, 1, 1, 1)
    @TodoOrDie("This need to be fixed later", by=datetime.datetime(2021, 12, 31, 1, 1, 1))
    def some_function(arg):
        return arg

    assert some_function(True) == True

@patch('todo._utcnow')
def test_decorator_raises_if_datetime_is_past_due(mocked_utcnow):
    mocked_utcnow.return_value = datetime.datetime(2022, 1, 1, 1, 1, 1)
    with pytest.raises(OverdueException):
        @TodoOrDie("This need to be fixed later", by=datetime.datetime(2021, 12, 31, 1, 1, 1))
        def some_function(arg):
            return arg

# Works with date and datetime
@patch('todo._utcnow')
def test_decorator_raises_if_date_is_past_due(mocked_utcnow):
    mocked_utcnow.return_value = datetime.datetime(2022, 1, 1, 1, 1, 1)
    with pytest.raises(OverdueException):
        @TodoOrDie("This need to be fixed later", by=datetime.date(2021, 12, 31))
        def some_function(arg):
            return arg

def test_decorator_does_nothing_if_condition_is_boolean_false():
    @TodoOrDie("This needs to be fixed later", when= 1 == 0)
    def some_function(arg):
        return arg
    assert some_function(True) == True

def test_decorator_raises_if_condition_is_boolean_true():
    with pytest.raises(OverdueException):
        @TodoOrDie("This needs to be fixed later", when= 1 == 1)
        def some_function(arg):
            return arg

def test_decorator_does_nothing_if_condition_is_callable_that_returns_false():
    @TodoOrDie("This needs to be fixed later", when= lambda: 1 == 0)
    def some_function(arg):
        return arg
    assert some_function(True) == True

def test_decorator_raises_if_condition_is_callable_that_returns_true():
    with pytest.raises(OverdueException):
        @TodoOrDie("This needs to be fixed later", when= lambda: 1 == 1)
        def some_function(arg):
            return arg

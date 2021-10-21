import datetime

from todo_or_die.exceptions import OverdueException

_ACCEPTED_KWARGS = ["by", "when"]


def todo_or_die(*args, **kwargs: dict):
    result = None
    if len(args) == 2 and isinstance(args[1], str):
        result = args[0]
        message = args[1]
    elif len(args) == 1 and isinstance(args[0], str):
        message = args[0]
    else:
        raise ValueError("todo_or_die accepts the following args: [value or callable, todo message, **kwargs] OR [todo message, **kwargs]")

    if len(kwargs) == 0:
        raise ValueError("todo_or_die needs at least one error criteria (see README).")
    for key in kwargs.keys():
        if key not in _ACCEPTED_KWARGS:
            raise ValueError(f"todo_or_die received unknown keyword: {key}")

    expires = kwargs.get("by", None)
    _raise_if_datetime_overdue(expires, message)

    cond = kwargs.get("when", None)
    _raise_if_condition_true(cond, message)

    if callable(result):
        return result()
    return result


def _raise_if_datetime_overdue(expires, message):
    if expires is None:
        return None
    if isinstance(expires, datetime.date):
        expires = datetime.datetime.combine(expires, datetime.datetime.min.time())
    if expires and _utcnow() > expires:
        raise OverdueException(f'TODO: "{message}" came due on {_utcnow()}. Do it!')


def _raise_if_condition_true(cond, message):
    if cond is None:
        return None
    if callable(cond) and cond():
        raise OverdueException(f'TODO: "{message}" came due now. Do it!')
    if isinstance(cond, bool) and cond:
        raise OverdueException(f'TODO: "{message}" came due now. Do it!')


def _utcnow():
    """
    Used for monkey-patching during tests to manipulate time with more ease.
    :return: datetime now in UTC timezone
    """
    return datetime.datetime.utcnow()

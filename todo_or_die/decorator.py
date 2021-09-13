import functools
from todo_or_die.main import todo_or_die

def TodoOrDie(message: str, **kwargs: dict):
    todo_or_die(message, **kwargs)

    def decorator_todo_or_die(func):
        @functools.wraps(func)
        def wrapper_todo_or_die(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper_todo_or_die

    return decorator_todo_or_die

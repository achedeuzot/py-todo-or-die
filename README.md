# todo-or-die [Python edition]
Don't let your TODOs rot in your python projects anymore !

Inspired by :
- https://github.com/davidpdrsn/todo-or-die (Rust)
- https://github.com/searls/todo_or_die (Ruby)

## Examples
Once installed in your project, you can use it in any part of your code:

```python
from todo_or_die import todo_or_die, TodoOrDie

# raise an OverdueException when we're after a certain date or datetime
todo_or_die("This should be fixed by now.", by = datetime.datetime(2021, 6, 25, 15, 34, 55))

# raise an OverdueException when a given condition is true
todo_or_die("This should fail when we reach 1000 users", when = DB.users.count() > 1000)

# it also accepts a callable as a first argument
def myfunc():
    return 42

result = todo_or_die(myfunc, "Fix this in 6 months", by=datetime.date(2021, 6, 31))
result == 42 # True

# or simply any value will be passed back
result = todo_or_die(42, "Fix this in 6 months", by=datetime.date(2021, 6, 31))
result == 42 # True

from myapp import __version__

# Finally, you can use it as a function decorator
@TodoOrDie("This function should be removed in the next version", when=__version__ > 2000)
def myfunc(some = "arg"):
    pass

```

## Keep your projects clean
To understand why you would ever call a function to write a comment, read on.

If you have some code you know you'll need to change later, don't just leave a
comment for later that you'll never read, ever again.

For all the following cases, forgetting a TODO is NOT GOOD:
- remove some code when the dependency support expires, 
- remove a feature flag, 
- update some code related to another project,
- update a dependency when another refactoring is done,
- ...

This can lead to nasty issues so make your TODOs speak up when they need to 
with this module ;)

You can now replace your simple comment with this function that will raise
and error when the time or the condition are met and remind you to do something
about it.

## Caution
This can cause some production apps to break ! This code is named `todo_or_die`,
not `todo_and_kittens` so be careful.

Pull-Requests are welcome to make this more production-ready !

Note this module has no warranty, see the LICENSE !

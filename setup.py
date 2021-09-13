import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="todo-or-die",
    version="0.1.0",
    description="Never let your TODOs rot in your python code ever again",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/achedeuzot/py-todo-or-die",
    author="Klemen Sever",
    author_email="klemen@achedeuzot.me",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    packages=["todo_or_die"],
    include_package_data=True,
    install_requires=[],
    entry_points={},
)
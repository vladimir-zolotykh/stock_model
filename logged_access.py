#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import logging
from unittest.mock import patch


logging.basicConfig(level=logging.INFO)


def fake_info(fmt, *args):
    print(fmt % args)


class LoggedAccess:
    def __set_name__(self, owner, name):
        self.pub_name = name
        self.priv_name = "_" + name

    def __get__(self, instance, owner=None):
        val = getattr(instance, self.priv_name)
        with patch.object(logging, "info", side_effect=fake_info):
            logging.info("Accessing %r gives %r", self.pub_name, val)
        return val

    def __set__(self, instance, value):
        with patch.object(logging, "info", side_effect=fake_info):
            logging.info("Updating %r to %r", self.pub_name, value)
        setattr(instance, self.priv_name, value)


class Person:
    """
    >>> vars(vars(Person)["name"])
    {'pub_name': 'name', 'priv_name': '_name'}
    >>> vars(vars(Person)['age'])
    {'pub_name': 'age', 'priv_name': '_age'}
    >>> pete = Person("Peter P", 10)
    Updating 'name' to 'Peter P'
    Updating 'age' to 10
    >>> kate = Person("Catherine K", 20)
    Updating 'name' to 'Catherine K'
    Updating 'age' to 20
    >>> pete.age
    Accessing 'age' gives 10
    10
    >>> pete.birthday()
    Accessing 'age' gives 10
    Updating 'age' to 11
    >>> kate.name
    Accessing 'name' gives 'Catherine K'
    'Catherine K'
    """

    name = LoggedAccess()
    age = LoggedAccess()

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def birthday(self):
        self.age += 1


if __name__ == "__main__":
    import doctest

    doctest.testmod()

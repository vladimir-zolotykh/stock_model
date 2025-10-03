#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import os
import logging
from unittest.mock import patch


# Directorysize
class DirectorySize:
    def __get__(self, instance, owner=None):
        return len(os.listdir(instance._dirname))


class Directory:
    """
    >>> d1 = Directory("/etc/")
    >>> d1.size
    222
    >>> d2 = Directory(os.path.expanduser("~/Documents/projects/python/"))
    >>> d2.size
    27
    """

    size = DirectorySize()

    def __init__(self, dirname):
        self._dirname = dirname

    @property
    def dirname(self):
        return self._dirname


logging.basicConfig(level=logging.INFO)


def fake_info(fmt, *args, **kwargs):
    print(fmt % args)


class LoggedAgeAccess:
    def __get__(self, instance, owner=None):
        value = instance._age
        with patch.object(logging, "info", side_effect=fake_info):
            logging.info("Accessing %r gives %r", "age", value)
        return value

    def __set__(self, instance, value):
        with patch.object(logging, "info", side_effect=fake_info):
            logging.info("Updating %r to %r", "age", value)
        instance._age = value


class Person:
    """
    >>> mary = Person("Mary M", 30)
    Updating 'age' to 30
    >>> dave = Person("David D", 40)
    Updating 'age' to 40
    >>> vars(mary)
    {'name': 'Mary M', '_age': 30}
    >>> vars(dave)
    {'name': 'David D', '_age': 40}
    >>> mary.age
    Accessing 'age' gives 30
    30
    >>> mary.birthday()
    Accessing 'age' gives 30
    Updating 'age' to 31
    >>> dave.name
    David D
    >>> dave.age
    Accessing 'age' gives 40
    40
    """

    age = LoggedAgeAccess()

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def birthday(self):
        self.age += 1


if __name__ == "__main__":
    import doctest

    doctest.testmod()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import os
import logging


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


class LoggedAgeAccess:
    def __get__(self, instance, owner=None):
        value = instance._age
        logging.info("Accessing %r gives %r", "age", value)
        return value

    def __set__(self, instance, value):
        logging.info("Updating %r to %r", "age", value)
        instance._age = value


class Person:
    age = LoggedAgeAccess()

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def birthday(self):
        self.age += 1


if __name__ == "__main__":
    import doctest

    doctest.testmod()

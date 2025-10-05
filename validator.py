#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Never
from abc import ABC, abstractmethod
import unittest


class Validator(ABC):
    def __set_name__(self, owner, name):
        self.priv_name = "_" + name

    def __get__(self, instance, owner=None):
        return getattr(instance, self.priv_name)

    def __set__(self, instance, value):
        self.validate(value)
        setattr(instance, self.priv_name, value)

    @abstractmethod
    def validate(self, value) -> Never:
        pass


class OnOfError(ValueError):
    pass


class OneOf(Validator):
    def __init__(self, options):
        self.options = options

    def validate(self, value):
        if value not in self.options:
            raise OnOfError(f"{value!r} must be one of {self.options!r}")


class NumberError(ValueError):
    pass


class Number(Validator):
    def __init__(self, minval=0, maxval=None):
        self.minval = minval
        self.maxval = maxval

    def validate(self, value):
        if not isinstance(value, (int, float)):
            raise NumberError(f"{value!r} must be int or float")
        if isinstance(self.minval, (int, float)) and value < self.minval:
            raise NumberError(f"{value!r} must not be less that {self.minval!r}")
        if isinstance(self.maxval, (int, float)) and value > self.maxval:
            raise NumberError(f"{value!r} must not exceed {self.maxval!r}")


class StringError(ValueError):
    pass


class String(Validator):
    def __init__(self, minsize, maxsize, predicate):
        self.minsize = minsize
        self.maxsize = maxsize
        self.predicate = predicate

    def validate(self, value):
        if isinstance(self.minsize, int) and len(value) < self.minsize:
            raise StringError(f"{value!r} must not be shorter that {self.minsize!r}")
        if isinstance(self.maxsize, int) and len(value) > self.maxsize:
            raise StringError(f"{value!r} must not be longer than {self.maxsize!r}")
        if callable(self.predicate) and not self.predicate(value):
            raise StringError(f"{self.predicate!r} must return True for {value!r}")


class Component:
    """
    >>> c = Component("WIDGET", "metal", 12)
    >>> c.name, c.kind, c.quantity
    ('WIDGET', 'metal', 12)
    """

    name = String(2, 8, str.isupper)
    kind = OneOf(["metal", "wood", "plastic"])
    quantity = Number(0, 100)

    def __init__(self, name, kind, quantity):
        self.name = name
        self.kind = kind
        self.quantity = quantity

    def as_tuple(self) -> tuple[str, str, str]:
        return tuple((self.name, self.kind, self.quantity))


class TestValidator(unittest.TestCase):

    def test_component(self):
        self.assertEqual(
            Component("WIDGET", "metal", 12).as_tuple(), ("WIDGET", "metal", 12)
        )

    def test_string(self):
        with self.assertRaises(StringError):
            # ValueError: <method 'isupper' of 'str' objects> must return True for 'Widget'
            Component("Widget", "metal", 12)

    def test_one_of(self):
        with self.assertRaises(OnOfError):
            # ValueError: 'metle' must be one of ['metal', 'wood', 'plastic']
            Component("WIDGET", "metle", 5)

    def test_number1(self):
        # ValueError: -5 must not be less that 0
        with self.assertRaises(NumberError):
            Component("WIDGET", "metal", -5)

    def test_number2(self):
        # TypeError: 'V' must be int or float
        with self.assertRaises(NumberError):
            Component("WIDGET", "metal", "V")


if __name__ == "__main__":
    unittest.main()

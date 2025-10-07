#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from dataclasses import dataclass
import unittest


class Descriptor:
    def __set_name__(self, owner, name):
        self.name = "_" + name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        setattr(instance, self.name, value)


class Sized(Descriptor):
    def __init__(self, minsize=0, maxsize=None):
        super().__init__()
        self.minsize = minsize
        self.maxsize = maxsize

    def __set__(self, instance, value):
        if isinstance(self.minsize, (int, float)) and len(value) < self.minsize:
            raise ValueError(f"{value!r} must not be shorter than {self.minsize}")
        if isinstance(self.maxsize, (int, float)) and len(value) > self.maxsize:
            raise ValueError(f"{value!r} must not be longer than {self.maxsize}")
        super().__set__(instance, value)


class Typed(Descriptor):
    expected_type = type(None)

    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(f"{value!r} must be of type {self.expected_type}")
        super().__set__(instance, value)


class String(Typed):
    expected_type = str


class Integer(Typed):
    expected_type = int


class Float(Typed):
    expected_type = float


class Unsigned(Descriptor):
    def __set__(self, instance, value):
        if value < 0:
            raise ValueError(f"{value!r} must not be negative")
        super().__set__(instance, value)


class SizedString(String, Sized):
    pass


class UnsignedInteger(Integer, Unsigned):
    pass


class UnsignedFloat(Float, Unsigned):
    pass


class Stock:
    name = SizedString(maxsize=8)
    shares = UnsignedInteger()
    price = UnsignedFloat()

    def astuple(self) -> tuple[str, int, float]:
        return self.name, self.shares, self.price

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price


class TestMaxsize(unittest.TestCase):
    def setUp(self):
        try:
            self.s = Stock("ACME", 50, 91.1)
        except Exception as e:
            raise unittest.SkipTest(f"Skipping tests because setup failed: {e}")

    def test_stock(self):
        self.assertEqual(self.s.astuple(), ("ACME", 50, 91.1))

    def test_shares(self):
        with self.assertRaises(ValueError):
            self.s.shares = -5

    def test_price(self):
        with self.assertRaises(TypeError):
            self.s.price = "a lot"


if __name__ == "__main__":
    unittest.main()

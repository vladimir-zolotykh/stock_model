#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import os


class DirectorySize:
    def __get__(self, instance, owner=None):
        return len(os.listdir(instance._dirname))


class Directory:
    size = DirectorySize()

    def __init__(self, dirname):
        self._dirname = dirname

    @property
    def dirname(self):
        return self._dirname


if __name__ == "__main__":
    d1 = Directory("/etc/")
    d2 = Directory(os.path.expanduser("~/Documents/projects/python/"))
    print(d1.dirname, d1.size)
    print(d2.dirname, d2.size)

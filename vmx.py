#!/usr/bin/env python3
# coding=utf-8

# SPDX-FileCopyrightText: © 2014-2022 David Parsons
# SPDX-License-Identifier: MIT

from configobj import ConfigObj

# Redefine the MISSING default from ConfigObj
MISSING = ConfigObj


# TODO: Error and exception handling
class VMX(ConfigObj):
    # This is a simplistic case-insensitive version of ConfigObj
    # Override basic methods that require a key
    def __init__(self, infile=None):
        self._keys = dict()
        super().__init__(infile)
        for key in super().keys():
            self._setkey(key)
        return

    def _delkey(self, key):
        return self._keys.pop(self._getkey(key), None)

    def _getkey(self, key):
        return self._keys.get(key.lower(), None)

    def _renamekey(self, oldkey, newkey):
        self._delkey(oldkey)
        self._setkey(newkey)
        return

    def _setkey(self, key):
        self._keys[key.lower()] = key
        return

    def __getitem__(self, item):
        real_key = self._getkey(item)
        return super().__getitem__(real_key)

    def __setitem__(self, key, value, unrepr=False):
        if key not in self._keys:
            self._setkey(key)
        real_key = self._getkey(key)
        super().__setitem__(real_key, value, unrepr)
        return

    def __delitem__(self, key):
        real_key = self._getkey(key)
        super().__delitem__(real_key)
        self._delkey(key)
        return

    def get(self, key, default=None):
        real_key = self._getkey(key)
        return super().get(real_key, default)

    def pop(self, key, default=MISSING):
        real_key = self._getkey(key)
        value = super().pop(real_key, default)
        self._delkey(key)
        return value

    def rename(self, oldkey, newkey):
        real_oldkey = self._getkey(oldkey)
        super().rename(real_oldkey, newkey)
        self._renamekey(oldkey, newkey)
        return

    def as_bool(self, key):
        real_key = self._getkey(key)
        return super().as_bool(real_key)

    def as_int(self, key):
        real_key = self._getkey(key)
        return super().as_int(real_key)

    def as_float(self, key):
        real_key = self._getkey(key)
        return super().as_float(real_key)

    def as_list(self, key):
        real_key = self._getkey(key)
        return super().as_list(real_key)

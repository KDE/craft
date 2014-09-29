#!/usr/bin/env python

class PackageObjectBase(object):

    def __init__(self, category=None, subpackage=None, package=None, enabled=False):
        self.category = category
        self.subpackage = subpackage
        self.package = package
        self.enabled = enabled

    def __eq__(self, other):
        #print("eq", type(other), other)
        if isinstance(other, PackageObjectBase):
            if other.package == self.package and other.category == self.category and other.subpackage == self.subpackage:
                return True
        if isinstance(other, str):
            if other == self.package:
                return True
            if other == self.category + "/" + self.package:
                return True
            if self.subpackage and other == self.category + "/" + self.subpackage + "/" + self.package:
                return True
        return False

    def __str__(self):
        if not self.category or not self.package:
            return ""
        ret = self.category
        if self.subpackage: ret += "/" + self.subpackage
        ret += "/" + self.package
        return ret

    def __bool__(self):
        #print("bool:", self.enabled)
        return self.enabled

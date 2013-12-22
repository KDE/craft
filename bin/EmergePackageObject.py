#!/usr/bin/env python

class PackageObjectBase(object):
    category=None
    package=None
    version=None
    target=None
    enabled=False

    def __init__(self, category=None, subpackage=None, package=None, version=None, target=None, enabled=False):
        self.category = category
        self.subpackage = subpackage
        self.package = package
        self.version = version
        self.target = target
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
        ret += "/" + self.package + ":" + str(self.target)
        return ret

    def __bool__(self):
        #print("bool:", self.enabled)
        return self.enabled

if __name__ == '__main__':
    p = PackageObjectBase(category="kde", subpackage="kdeedu", package="kalgebra", enabled=True)
    q = PackageObjectBase(category="kde", subpackage="kdeedu", package="kalgebra", enabled=False)
    l=[p]
    if not p in l:
        print("failed to find p in l")
    if not q in l:
        print("failed to find q in l")
    if not "kalgebra" in l:
        print("failed to find \"kalgebra\" in l")
    if not "kde/kalgebra" in l:
        print("failed to find \"kde/kalgebra\" in l")
    if not "kde/kdeedu/kalgebra" in l:
        print("failed to find \"kde/kdeedu/kalgebra\" in l")
    if not p or q:
        print("package enabling fails")
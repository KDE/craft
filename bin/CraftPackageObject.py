#!/usr/bin/env python
from collections import OrderedDict

from CraftDebug import craftDebug


class PackageObjectBase(object):
    PortageInstance = None

    def __init__(self, category=None, subpackage=None, package=None, version = None):
        self.category = category
        self.subpackage = subpackage
        self.package = package
        self._version = version

    def fullName(self):
        if self.subpackage:
            return "/".join((self.category,self.subpackage,self.package))
        else:
            return "/".join((self.category,self.package))

    @property
    def version(self):
        if not self._version:
            self._version = PackageObjectBase.PortageInstance.getNewestVersion(self.category, self.package)
        return self._version

    def _readChildren(self, category, package):
        craftDebug.log.debug("solving package {self}")
        subinfo = PackageObjectBase.PortageInstance._getSubinfo(category, package)

        if subinfo is None:
            return OrderedDict(), OrderedDict()

        return subinfo.runtimeDependencies, subinfo.buildDependencies


    def __eq__(self, other):
        #print("eq", type(other), other)
        if isinstance(other, PackageObjectBase):
            if other.package == self.package and other.category == self.category and other.subpackage == self.subpackage:
                return True
        if isinstance(other, str):
            if other == self.package:
                return True
            if other == self.fullName():
                return True
        return False

    def __str__(self):
        return self.fullName()

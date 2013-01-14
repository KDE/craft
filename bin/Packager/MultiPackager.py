#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#

from Packager.PackagerFactory import *

class MultiPackager(object):
    def __init__(self, packagerType=None):
        utils.debug( "MultiPackager __init__ %s" %packagerType, 2 )
        self.packagers = PackagerFactory(self, packagerType)

    def createPackage(self):
        result = True
        for packager in self.packagers:
            if not packager.createPackage():
                result = False
        return result

    def make_package(self):
        return self.createPackage()

# Regex:
# Binary package for GNU regex.
# see http://gnuwin32.sourceforge.net/packages/regex.htm
# for more information and the Source Code according to this package

import info

class subinfo(info.infoclass):

    def setTargets( self ):
        self.targets['2.7'] = \
                'http://downloads.sourceforge.net/project/gnuwin32/regex/2.7/regex-2.7-bin.zip'
        self.targetDigests[ '2.7' ] = "0532975f880a6d6dea71a48968709ee36b934b32"
        self.defaultTarget = '2.7'

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        BinaryPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()

# Regex:
# Binary package for GNU regex compiled for Win32
# http://sourceforge.net/projects/gnuwin32/files/regex-Spencer/3.8/
# for more information and the Source Code according to this package see:
# http://gnuwin32.sourceforge.net/packages/regex-spencer.htm

import info

class subinfo(info.infoclass):

    def setTargets( self ):
        version = '3.8'
        self.targets[version] = \
                '''http://downloads.sourceforge.net/project/gnuwin32/regex-Spencer/3.8/regex-spencer-3.8-lib.zip
                   http://downloads.sourceforge.net/project/gnuwin32/regex-Spencer/3.8/regex-spencer-3.8-bin.zip'''
        self.defaultTarget = '3.8'

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        BinaryPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()

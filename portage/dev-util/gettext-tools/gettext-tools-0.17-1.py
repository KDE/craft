import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.17'] = 'http://winkde.org/pub/kde/ports/win32/repository/win32libs/gettext-tools-0.17-bin.tar.bz2'
        self.defaultTarget = '0.17'

    def setDependencies( self ):
        self.hardDependencies['win32libs-bin/gettext'] = 'default'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = "dev-utils"
        BinaryPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()

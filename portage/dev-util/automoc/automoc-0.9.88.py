import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.9.88'] = "http://www.winkde.org/pub/kde/ports/win32/repository/other/automoc4.exe"
        self.defaultTarget = '0.9.88'
        ## \todo specific a target independent install path option
        self.targetInstallPath['0.9.88'] = 'bin'

from Package.BinaryPackageBase import *
        
class Package(BinaryPackageBase):
    def __init__(self ):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = 'dev-utils'
        BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()

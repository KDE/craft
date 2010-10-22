import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['9.0release'] = "http://kdab.com/~andy/runtime-wince-release.zip"
        self.targets['9.0debug'] = "http://kdab.com/~andy/runtime-wince-debug.zip"
        if EmergeBase().buildType() == "Debug":
            self.defaultTarget = '9.0debug'
        else:
            self.defaultTarget = '9.0release'

    def setBuildOptions( self ):
        self.disableHostBuild = True
        self.disableTargetBuild = False


from Package.BinaryPackageBase import *
        
class Package(BinaryPackageBase):
    def __init__(self):
        self.subinfo = subinfo()
        BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()

import info


class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets[ 'gitHEAD' ] = 'https://github.com/Snorenotify/SnoreGrowl.git'
        self.shortDescription = "SnoreGrowl is a library providing Growl network notifications"
        self.homepage = "https://github.com/Snorenotify/SnoreGrowl"
        self.defaultTarget = 'gitHEAD'


    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'



from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)

        



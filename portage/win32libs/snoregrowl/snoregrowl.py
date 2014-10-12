import info


class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets[ 'gitHEAD' ] = 'https://github.com/Snorenotify/SnoreGrowl.git'
        
        for ver in ['0.4.0']:
            self.targets[ver] = 'https://github.com/Snorenotify/SnoreGrowl/archive/v%s.tar.gz' % ver
            self.archiveNames[ver] = "snoregrowl-%s.tar.gz" % ver
            self.targetInstSrc[ver] = 'SnoreGrowl-%s' % ver
        self.targetDigests['0.4.0'] = '16b84d2fb673438c8250cefd95f7e4c145e4cf22'
        
        self.shortDescription = "SnoreGrowl is a library providing Growl network notifications"
        self.homepage = "https://github.com/Snorenotify/SnoreGrowl"
        self.defaultTarget = '0.4.0'


    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'



from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)

        



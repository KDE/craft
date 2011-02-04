import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'http://github.com/segfault87/Konstruktor.git'
        self.defaultTarget = 'gitHEAD'
        self.shortDescription = "a full-featured LEGO(r) CAD"
        #self.homepage = "http://konstruktor.influx.kr/"

    def setDependencies( self ):
        self.dependencies['virtual/kde-runtime']    = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()

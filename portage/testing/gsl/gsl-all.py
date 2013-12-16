import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = "[git]https://github.com/ampl/gsl.git"
        self.shortDescription = 'GNU Scientific Library'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.hardDependencies['virtual/bin-base'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()

import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = "[git]https://github.com/ampl/gsl.git"
        self.svnTargets['1.16'] = "[git]https://github.com/ampl/gsl.git||709cc572279e4a56b0e218b834f202c1b3f757af"
        self.shortDescription = 'GNU Scientific Library'
        self.defaultTarget = '1.16'

    def setDependencies( self ):
        self.hardDependencies['virtual/bin-base'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()

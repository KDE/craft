import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:scratch/sengels/kcwsh'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.shortDescription = "a cmd wrapper for konsole"
        self.buildDependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DBUILD_GUI_TEST=OFF "

if __name__ == '__main__':
    Package().execute()

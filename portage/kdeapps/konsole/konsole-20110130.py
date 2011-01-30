import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'git://git.kde.org/konsole'
        self.svnTargets['winport'] = 'git://git.kde.org/konsole|winport|'
        self.defaultTarget = 'winport'

    def setDependencies( self ):
        self.dependencies['virtual/kde-runtime'] = 'default'
        self.dependencies['testing/kcwsh'] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DBUILD_doc=OFF "

if __name__ == '__main__':
    Package().execute()

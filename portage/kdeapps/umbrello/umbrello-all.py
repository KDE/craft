import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['4.7'] = "branches/KDE/4.7/kdesdk#norecursive;branches/KDE/4.7/kdesdk/umbrello#main;branches/KDE/4.7/kdesdk/cmake"
        self.svnTargets['svnHEAD'] = "trunk/KDE/kdesdk#norecursive;trunk/KDE/kdesdk/umbrello#main;trunk/KDE/kdesdk/cmake"
        self.defaultTarget = 'svnHEAD'
        #for testing
        self.svnTargets['gitHEAD'] = "git://nohost/nopath"

    def setDependencies( self ):
        self.dependencies['virtual/kde-runtime'] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.onlyBuildTargets = 'umbrello'

if __name__ == '__main__':
    Package().execute()



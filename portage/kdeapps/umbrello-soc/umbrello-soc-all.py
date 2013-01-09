import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['svnHead'] = 'branches/work/soc-umbrello'
        self.defaultTarget = 'svnHead'

    def setDependencies( self ):
        self.dependencies['virtual/kde-runtime'] = 'default'
        self.dependencies['win32libs/boost'] = 'default'
        #self.hardDependencies['win32libs/zip'] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()

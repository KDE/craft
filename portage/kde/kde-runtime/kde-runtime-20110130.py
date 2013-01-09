import info
import compiler
class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:kde-runtime'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['kde/kdelibs'] = 'default'
        self.dependencies['kde/kactivities'] = 'default'
        self.dependencies['kdesupport/oxygen-icons'] = 'default'
        self.dependencies['win32libs/libssh'] = 'default'
        self.dependencies['kde/kactivities'] = 'default'
        self.dependencies['kde/kdepimlibs'] = 'default'
        self.dependencies['kde/nepomuk-core'] = 'default'
        if compiler.isMinGW_WXX():
            self.dependencies['win32libs/libbfd'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()

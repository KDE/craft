import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:skrooge'
        self.svnTargets['0.9.1'] = "[git]kde:skrooge|master|e00a80e33c563e0c01"
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['libs/qt'] = 'default'
        self.dependencies['kdesupport/qca'] = 'default'
        self.dependencies['virtual/kde-runtime'] = 'default'
        self.dependencies['win32libs-bin/libopensp'] = 'default'
        # missing: kdelibs

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()

import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = "[git]kde:calligra"
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.hardDependencies['win32libs-bin/lcms2'] = 'default'
        self.hardDependencies['win32libs-bin/libwpd'] = 'default'
        self.hardDependencies['win32libs-bin/libwpg'] = 'default'
        self.hardDependencies['win32libs-bin/openjpeg'] = 'default'
        self.hardDependencies['win32libs-bin/libfftw'] = 'default'
        self.hardDependencies['virtual/kdepimlibs'] = 'default'
        self.hardDependencies['virtual/kde-runtime'] = 'default'
        self.hardDependencies['kdesupport/eigen2'] = 'default'
        self.hardDependencies['kdesupport/poppler'] = 'default'
        self.softDependencies['kdesupport/qca'] = 'default'
        self.softDependencies['testing/gsl'] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()

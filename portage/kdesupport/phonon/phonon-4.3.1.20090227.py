import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['libs/qt'] = 'default'
        self.hardDependencies['kdesupport/automoc'] = 'default'

    def setTargets( self ):
        self.svnTargets['_4.1.0'] = 'tags/phonon/4.1.0'    # tagged version, also in qt4.4.0
        self.svnTargets['_4.2.0'] = 'tags/phonon/4.2.0'    # tagged version
        self.svnTargets['_4.3.0'] = 'tags/phonon/4.3.0'
        self.svnTargets['_4.3.1'] = 'tags/phonon/4.3.1'
        self.svnTargets['_4.2'] = 'branches/phonon/4.2'
        for i in ['4.3.0', '4.3.1', '4.3.2', '4.3.3', '4.3.4', '4.3']:
            self.svnTargets[ i ] = 'tags/kdesupport-for-4.3/kdesupport/phonon'
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/phonon'
        self.defaultTarget = 'svnHEAD'
        self.options.configure.defines = "-DPHONON_BUILD_EXAMPLES=OFF -DPHONON_BUILD_TESTS=OFF"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()

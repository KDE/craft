import info
from Package.CMakePackageBase import *


class subinfo( info.infoclass ):
    def setDependencies( self ):
        self.dependencies['kdesupport/phonon'] = 'default'

    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:phonon-directshow'
        self.shortDescription = "the DirectShow based phonon multimedia backend"
        self.defaultTarget = 'gitHEAD'

class Package( CMakePackageBase ):
    def __init__( self, **args ):
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = ' -DPHONON_BUILD_PHONON4QT5=ON -DPHONON_BUILDSYSTEM_DIR=\"%s\" ' % (os.path.join(emergeRoot(),'share','phonon','buildsystem').replace('\\','/'))


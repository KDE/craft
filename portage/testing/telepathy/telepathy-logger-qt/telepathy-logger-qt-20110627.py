import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'kde:telepathy-logger-qt.git'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['libs/qt'] = 'default'
        self.dependencies['testing/glib-src'] = 'default'
        #self.dependencies['testing/dbus-python'] = 'default'


from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.make.supportsMultijob = False
        self.supportsNinja = False
        self.subinfo.options.configure.defines = "-DPYTHON_EXECUTABLE=\"C:/python27/python.exe\" -DENABLE_EXAMPLES=OFF -DENABLE_TESTS=OFF -DDISABLE_WERROR=ON"

if __name__ == '__main__':
    Package().execute()

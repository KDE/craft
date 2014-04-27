import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'git://anongit.freedesktop.org/telepathy/telepathy-qt4'
        self.patchToApply[ 'gitHEAD' ] = ("telepathy-qt-20130713.patch",1)
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['libs/qt'] = 'default'
        #self.dependencies['testing/dbus-python'] = 'default'


from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )
        self.subinfo.options.make.supportsMultijob = False
        self.supportsNinja = False
        self.subinfo.options.configure.defines = "-DPYTHON_EXECUTABLE=\"C:/python27/python.exe\" -DENABLE_EXAMPLES=OFF -DENABLE_TESTS=OFF -DDISABLE_WERROR=ON"

if __name__ == '__main__':
    Package().execute()

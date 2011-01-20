import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['libs/qt'] = 'default'
        self.dependencies['win32libs-bin/libbzip2'] = 'default'

    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'git://git.kde.org/kdewin-installer'
        self.defaultTarget = 'gitHEAD'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.make.supportsMultijob = False

    def configure(self):
        if self.buildTarget == 'amarokHEAD':
            self.subinfo.configure.defines = " -DBUILD_FOR_AMAROK=ON"
        return CMakePackageBase.configure(self)

if __name__ == '__main__':
    Package().execute()

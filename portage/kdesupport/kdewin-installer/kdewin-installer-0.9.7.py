import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['libs/qt'] = 'default'
        self.hardDependencies['win32libs/libbzip2'] = 'default'

    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/kdewin-installer'
        self.svnTargets['amarokHEAD'] = 'trunk/kdesupport/kdewin-installer'
        self.defaultTarget = 'svnHEAD'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        #help(self)

    def configure(self):
        if self.buildTarget == 'amarokHEAD':
            self.subinfo.configure.defines = " -DBUILD_FOR_AMAROK=ON"
        return CMakePackageBase.configure(self)

if __name__ == '__main__':
    Package().execute()

import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdegraphics#norecursive;trunk/KDE/kdegraphics/libs'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.dependencies['win32libs-bin/expat'] = 'default'
        self.dependencies['win32libs-bin/jpeg'] = 'default'
        self.dependencies['win32libs-bin/exiv2'] = 'default'
        self.dependencies['win32libs-bin/lcms'] = 'default'

from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.onlyBuildTargets='libs'
        self.subinfo.options.configure.defines='-DBUILD_LIBS=On'

if __name__ == '__main__':
    Package().execute()

import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdewebdev'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.dependencies['kde/kdelibs'] = 'default'
        self.dependencies['kde/kdepimlibs'] = 'default'
        self.dependencies['kde/kdebase-runtime'] = 'default'
        self.softDependencies['kde/kdevplatform'] = 'default'
        
from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        # if you want to build quanta, you need to build kdevplatform as well - this is not build by default!!!
        self.subinfo.options.configure.defines = ""
        self.subinfo.options.configure.defines += "-DBUILD_kfilereplace=OFF "
        self.subinfo.options.configure.defines += "-DBUILD_kxsldbg=OFF "
        self.subinfo.options.configure.defines += "-DBUILD_kommander=OFF "

if __name__ == '__main__':
    Package().execute()

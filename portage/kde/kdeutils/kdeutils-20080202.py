import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdeutils'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.dependencies['kde/kdebase-runtime'] = 'default'
        self.dependencies['kde/kdepimlibs'] = 'default'
        self.dependencies['win32libs-bin/libgmp'] = 'default'
        self.dependencies['win32libs-bin/libzip'] = 'default'
        self.dependencies['gnuwin32/libarchive'] = 'default'

from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        #        self.subinfo.options.configure.defines += "-DBUILD_kwallet=OFF "
        #        self.subinfo.options.configure.defines += "-DBUILD_doc=OFF"

if __name__ == '__main__':
    Package().execute()


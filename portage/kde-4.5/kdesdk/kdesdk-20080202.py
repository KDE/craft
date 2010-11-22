# -*- coding: iso-8859-15 -*-
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'branches/KDE/4.5/kdesdk'
        for ver in ['0', '1', '2', '3', '4']:
            self.targets['4.5.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.5.' + ver + '/src/kdesdk-4.5.' + ver + '.tar.bz2'
            self.targetInstSrc['4.5.' + ver] = 'kdesdk-4.5.' + ver
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.dependencies['kde-4.5/kdebase-runtime'] = 'default'
        self.dependencies['win32libs-bin/boost'] = 'default'
        self.dependencies['dev-util/zip'] = 'default'
        
from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        #        self.subinfo.options.configure.defines = "-DBUILD_kate=OFF "
        #        self.subinfo.options.configure.defines += "-DBUILD_kapptemplate=OFF "
        #        self.subinfo.options.configure.defines += "-DBUILD_kbugbuster=OFF "
        #        self.subinfo.options.configure.defines += "-DBUILD_kcachegrind=OFF "
        #        self.subinfo.options.configure.defines += "-DBUILD_kdeaccounts-plugin=OFF "
        #        self.subinfo.options.configure.defines += "-DBUILD_kdepalettes=OFF "
        #        self.subinfo.options.configure.defines += "-DBUILD_strigi-analyzer=OFF "
        #        self.subinfo.options.configure.defines += "-DBUILD_kioslave=OFF "
        #        self.subinfo.options.configure.defines += "-DBUILD_kmtrace=OFF "
        #        self.subinfo.options.configure.defines += "-DBUILD_kprofilemethod=OFF "
        #        self.subinfo.options.configure.defines += "-DBUILD_kuiviewer=OFF "
        #        self.subinfo.options.configure.defines += "-DBUILD_poxml=OFF "
        #        self.subinfo.options.configure.defines += "-DBUILD_scripts=OFF "
        #        self.subinfo.options.configure.defines += "-DBUILD_umbrello=OFF "
        #        self.subinfo.options.configure.defines += "-DBUILD_doc=OFF "

if __name__ == '__main__':
    Package().execute()

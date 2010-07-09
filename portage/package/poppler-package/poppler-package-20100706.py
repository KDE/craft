# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = "git://git.freedesktop.org/git/poppler/poppler|master"
        self.defaultTarget = 'gitHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['win32libs-bin/freetype'] = 'default'
        self.hardDependencies['win32libs-bin/openjpeg'] = 'default'
        self.hardDependencies['win32libs-bin/lcms'] = 'default'
        self.hardDependencies['win32libs-bin/zlib'] = 'default'
        self.hardDependencies['win32libs-bin/jpeg'] = 'default'
        self.hardDependencies['win32libs-bin/libpng'] = 'default'
        self.hardDependencies['win32libs-bin/libxml2'] = 'default'
        self.hardDependencies['win32libs-bin/expat'] = 'default'
        self.hardDependencies['win32libs-bin/dbus'] = 'default'
        self.hardDependencies['data/poppler-data'] = 'default'
        self.hardDependencies['libs/qt'] = 'default'
        pass
    
class MainPackage(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

    def execute( self ):
        (command, option) = self.getAction()
        if command == "install":
            print "*Installation*"
            for dep in self.subinfo.hardDependencies:
                self.pac = portage.getPackageInstance(dep.split("/")[0],dep.split("/")[1])
                print "getting install directory:", self.pac.installDir()
                utils.copySrcDirToDestDir( self.pac.installDir(), self.installDir() )
        if command == "package":
                    self.runAction("package")
        return True

		
if __name__ == '__main__':
    MainPackage().execute()

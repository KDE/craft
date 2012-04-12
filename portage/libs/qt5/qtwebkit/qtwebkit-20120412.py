# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets( self ):       
        self.svnTargets['gitHEAD'] = "[git]git://gitorious.org/qtwebkit/qt5-module.git" 

        self.defaultTarget = "gitHEAD"

    def setDependencies( self ):
        self.dependencies['libs/qtbase'] = 'default'
        self.dependencies['win32libs-sources/icu-src'] = 'default'
        self.dependencies['win32libs-bin/pthreads'] = 'default'
        self.buildDependencies['gnuwin32/flex'] = 'default'
        self.buildDependencies['gnuwin32/bison'] = 'default'
        self.buildDependencies['gnuwin32/gperf'] = 'default'
        

from Package.Qt5CorePackageBase import *

class Package( Qt5CorePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        Qt5CorePackageBase.__init__( self )
        os.putenv("QMAKEPATH",os.path.join(self.sourceDir(),"Tools","qmake"))
        os.putenv("WEBKITOUTPUTDIR",self.imageDir())
        self.subinfo.options.configure.defines = " \"QT_CONFIG += icu\" "
                
if __name__ == '__main__':
    Package().execute()

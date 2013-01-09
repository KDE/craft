# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets( self ):       
        self.svnTargets['gitHEAD'] = "[git]git://gitorious.org/qt/qtwebkit.git|stable"
        self.patchToApply['gitHEAD'] = [("qtwebkit-20130109.patch",1)]

        self.defaultTarget = "gitHEAD"

    def setDependencies( self ):
        self.dependencies['libs/qtbase'] = 'default'
        self.dependencies['libs/qtdeclarative'] = 'default'
        self.dependencies['libs/qtsvg'] = 'default' 
        self.dependencies['win32libs/pthreads'] = 'default'
        self.dependencies['win32libs/sqlite'] = 'default'
        self.buildDependencies['gnuwin32/flex'] = 'default'
        self.buildDependencies['gnuwin32/bison'] = 'default'
        self.buildDependencies['gnuwin32/gperf'] = 'default'
        self.buildDependencies['dev-util/ruby'] = 'default'
        self.buildDependencies['dev-util/pkg-config'] = 'default'
        

from Package.Qt5CorePackageBase import *

class Package( Qt5CorePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        Qt5CorePackageBase.__init__( self )
        os.putenv("SQLITE3SRCDIR",os.getenv("KDEROOT"))

if __name__ == '__main__':
    Package().execute()

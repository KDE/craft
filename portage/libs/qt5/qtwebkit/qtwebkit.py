# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )
        for ver in self.versionInfo.tarballs():
            self.patchToApply[ ver ] = ("qtwebkit-20130109.patch" , 1)
            
        for ver in self.versionInfo.branches():
            self.patchToApply[ ver ] = ("qtwebkit-20130109.patch" , 1)
            
        for ver in self.versionInfo.tags():
            self.patchToApply[ ver ] = ("qtwebkit-20130109.patch" , 1)

    def setDependencies( self ):
        self.dependencies['win32libs/sqlite'] = 'default'
        self.dependencies['libs/qtbase'] = 'default'
        self.dependencies['libs/qtscript'] = 'default'
        self.dependencies['libs/qtdeclarative'] = 'default'
        self.dependencies['libs/qtquick1'] = 'default'
        self.buildDependencies['dev-util/ruby'] = 'default'
        self.buildDependencies['dev-util/winflexbison'] = 'default'
        self.buildDependencies['gnuwin32/gperf'] = 'default'
        

from Package.Qt5CorePackageBase import *
class Package( Qt5CorePackageBase ):
    def __init__( self, **args ):
        Qt5CorePackageBase.__init__( self )
        os.putenv("SQLITE3SRCDIR",EmergeStandardDirs.emergeRoot())
        if compiler.isMinGW():
            self.subinfo.options.configure.defines = """ "QMAKE_CXXFLAGS += -g0 -O3" """


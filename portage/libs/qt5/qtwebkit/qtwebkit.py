# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        for ver in self.versionInfo.branches():
            self.patchToApply[ ver ] = [("build-with-mysql.diff", 1),
                                         ("disable-icu-test.diff", 1)]

        branchRegEx = re.compile("\d\.\d\.\d")
        for ver in self.versionInfo.tarballs():
            branch = branchRegEx.findall(ver)[0][:-2]
            del self.targets[ver]
            if ver in self.targetInstSrc:
                del self.targetInstSrc[ver]
            self.svnTargets[ver] = self.svnTargets[branch]
            self.patchToApply[ver] = self.patchToApply[branch]

        for ver in self.versionInfo.tags():
            branch = branchRegEx.findall(ver)[0][:-2]
            self.svnTargets[ver] = self.svnTargets[ branch ]
            self.patchToApply[ ver ] = self.patchToApply[ branch ]

    def setDependencies( self ):
        self.dependencies['win32libs/sqlite'] = 'default'
        self.dependencies['win32libs/icu'] = 'default'
        self.dependencies['libs/qtbase'] = 'default'
        self.dependencies['libs/qtscript'] = 'default'
        self.dependencies['libs/qtdeclarative'] = 'default'
        self.dependencies['libs/qtmultimedia'] = 'default'
        self.dependencies['libs/qtwebchannel'] = 'default'
        self.buildDependencies['dev-util/ruby'] = 'default'
        self.buildDependencies['dev-util/winflexbison'] = 'default'
        self.buildDependencies['gnuwin32/gperf'] = 'default'
        

from Package.Qt5CorePackageBase import *
class Package( Qt5CorePackageBase ):
    def __init__( self, **args ):
        Qt5CorePackageBase.__init__( self )
        utils.putenv("SQLITE3SRCDIR",CraftStandardDirs.craftRoot())
        self.subinfo.options.configure.defines = ""
        if OsUtils.isWin():
            self.subinfo.options.configure.defines += """ "QT_CONFIG+=no-pkg-config" """
        if compiler.isMinGW():
            self.subinfo.options.configure.defines += """ "QMAKE_CXXFLAGS += -g0 -O3" """


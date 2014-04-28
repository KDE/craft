# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultVersions("http://download.qt-project.org/official_releases/qt/${VERSION_MAJOR}.${VERSION_MINOR}/${VERSION}/submodules/${PACKAGE_NAME}-opensource-src-${VERSION}.tar.xz",
                                    "http://download.qt-project.org/official_releases/qt/${VERSION_MAJOR}.${VERSION_MINOR}/${VERSION}/submodules/${PACKAGE_NAME}-opensource-src-${VERSION}.tar.xz.sha1",
                                    "${PACKAGE_NAME}-opensource-src-${VERSION}",
                                    "[git]git://gitorious.org/qt/${PACKAGE_NAME}.git" )
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
        self.buildDependencies['gnuwin32/gperf'] = 'default'
        

from Package.Qt5CorePackageBase import *

class Package( Qt5CorePackageBase ):
    def __init__( self, **args ):
        Qt5CorePackageBase.__init__( self )
        os.putenv("SQLITE3SRCDIR",emergeRoot())
        self.subinfo.options.make.supportsMultijob = False


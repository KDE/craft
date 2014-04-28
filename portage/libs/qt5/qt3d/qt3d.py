# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets( self ):       
        self.versionInfo.setDefaultVersions("http://download.qt-project.org/official_releases/qt/${VERSION_MAJOR}.${VERSION_MINOR}/${VERSION}/submodules/${PACKAGE_NAME}-opensource-src-${VERSION}.tar.xz",
                                    "http://download.qt-project.org/official_releases/qt/${VERSION_MAJOR}.${VERSION_MINOR}/${VERSION}/submodules/${PACKAGE_NAME}-opensource-src-${VERSION}.tar.xz.sha1",
                                    "${PACKAGE_NAME}-opensource-src-${VERSION}",
                                    "[git]git://gitorious.org/qt/${PACKAGE_NAME}.git" )

    def setDependencies( self ):
        self.dependencies['libs/qtbase'] = 'default'
        self.dependencies['libs/qtdeclarative'] = 'default'


from Package.Qt5CorePackageBase import *

class Package( Qt5CorePackageBase ):
    def __init__( self, **args ):
        Qt5CorePackageBase.__init__( self )
        

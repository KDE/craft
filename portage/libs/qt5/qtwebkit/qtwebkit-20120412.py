# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets( self ):       
        self.versionInfo.setupDefaultVersions(__file__)
        for ver in self.versionInfo.tarballs():
            self.targets[ver] = 'http://download.qt-project.org/official_releases/qt/%s/%s/submodules/%s-opensource-src-%s.zip' % ( ver[0:3], ver, self.versionInfo.packageName(), ver)
            self.targetDigestUrls[ver] = 'http://download.qt-project.org/official_releases/qt/%s/%s/submodules/%s-opensource-src-%s.zip.sha1' % (ver[0:3], ver, self.versionInfo.packageName(), ver)
            self.targetInstSrc[ver] = '%s-opensource-src-%s' % ( self.versionInfo.packageName(), ver)
            self.patchToApply[ ver ] = ("qtwebkit-20130109.patch" , 1)
            
        for ver in self.versionInfo.branches():
            self.svnTargets[ver] = '[git]git://gitorious.org/qt/%s.git|%s' % ( self.versionInfo.packageName(), ver)
            self.patchToApply[ ver ] = ("qtwebkit-20130109.patch" , 1)
            
        for ver in self.versionInfo.tags():
            self.svnTargets[ver] = '[git]git://gitorious.org/qt/%s.git||%s' % ( self.versionInfo.packageName(), ver)
            self.patchToApply[ ver ] = ("qtwebkit-20130109.patch" , 1)
            
        self.defaultTarget = self.versionInfo.defaultTarget()

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
        self.subinfo = subinfo()
        Qt5CorePackageBase.__init__( self )
        os.putenv("SQLITE3SRCDIR",os.getenv("KDEROOT"))
        self.subinfo.options.make.supportsMultijob = False

if __name__ == '__main__':
    Package().execute()

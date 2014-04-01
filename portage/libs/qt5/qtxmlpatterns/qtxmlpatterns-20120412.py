# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets( self ):       
        self.setupDefaultVersions(__file__)
        self.svnTargets['gitHEAD'] = '[git]git://gitorious.org/qt/%s.git|dev' % self.package
        self.svnTargets[self.defaultBranch()] = '[git]git://gitorious.org/qt/%s.git|%s' % ( self.package, self.defaultBranch())
        self.targets[self.defaultTag()] = 'http://download.qt-project.org/official_releases/qt/5.2/%s/submodules/%s-opensource-src-%s.zip' % ( self.defaultTag(), self.package, self.defaultTag())
        self.targetDigestUrls[self.defaultTag()] = 'http://download.qt-project.org/official_releases/qt/5.2/%s/submodules/%s-opensource-src-%s.zip.sha1' % (self.defaultTag(), self.package, self.defaultTag())
        self.targetInstSrc[self.defaultTag()] = '%s-opensource-src-%s' % ( self.package, self.defaultTag())


        self.defaultTarget = self.defaultBranch()

    def setDependencies( self ):
        self.dependencies['libs/qtbase'] = 'default'


from Package.Qt5CorePackageBase import *

class Package( Qt5CorePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        Qt5CorePackageBase.__init__( self )        
       

        
if __name__ == '__main__':
    Package().execute()

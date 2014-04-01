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
        self.dependencies['libs/qtactiveqt'] = 'default'
        self.dependencies['libs/qtdeclarative'] = 'default'
        self.dependencies['libs/qtgraphicaleffects'] = 'default'
        self.dependencies['libs/qtimageformats'] = 'default'
        self.dependencies['libs/qtquick1'] = 'default'
        self.dependencies['libs/qtscript'] = 'default'
        self.dependencies['libs/qtsvg'] = 'default'
        self.dependencies['libs/qttools'] = 'default'
        self.dependencies['libs/qtwebkit'] = 'default'
        self.dependencies['libs/qtxmlpatterns'] = 'default'
        self.dependencies['libs/qtwinextras'] = 'default'
        
        
        

from Package.VirtualPackageBase import *

class Package( VirtualPackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        VirtualPackageBase.__init__( self )


if __name__ == '__main__':
    Package().execute()

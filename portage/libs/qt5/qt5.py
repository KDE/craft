import info


class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in self.versionInfo.tarballs():
            self.targets[ver] = 'http://download.qt-project.org/official_releases/qt/%s/%s/submodules/%s-opensource-src-%s.zip' % ( ver[0:3], ver, self.versionInfo.packageName(), ver)
            self.targetDigestUrls[ver] = 'http://download.qt-project.org/official_releases/qt/%s/%s/submodules/%s-opensource-src-%s.zip.sha1' % (ver[0:3], ver, self.versionInfo.packageName(), ver)
            self.targetInstSrc[ver] = '%s-opensource-src-%s' % ( self.versionInfo.packageName(), ver)
            
        for ver in self.versionInfo.branches():
            self.svnTargets[ver] = '[git]git://gitorious.org/qt/%s.git|%s' % ( self.versionInfo.packageName(), ver)
            
        for ver in self.versionInfo.tags():
            self.svnTargets[ver] = '[git]git://gitorious.org/qt/%s.git||%s' % ( self.versionInfo.packageName(), ver)
            

        self.defaultTarget = self.versionInfo.defaultTarget()

    def setDependencies( self ):
        self.dependencies['libs/qtbase'] = 'default'
        self.dependencies['libs/qtactiveqt'] = 'default'
        self.dependencies['libs/qtdeclarative'] = 'default'
        self.dependencies['libs/qtgraphicaleffects'] = 'default'
        self.dependencies['libs/qtimageformats'] = 'default'
        self.dependencies['libs/qtmultimedia'] = 'default'
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
        VirtualPackageBase.__init__( self )



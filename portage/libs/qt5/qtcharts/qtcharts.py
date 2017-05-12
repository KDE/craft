# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets( self ):       
        self.versionInfo.setDefaultValues( )
        branchRegEx = re.compile("\d\.\d\.\d")
        for ver in self.versionInfo.tarballs():
            if CraftVersion(ver) < CraftVersion("5.7"):
                branch = branchRegEx.findall(ver)[0][:-2]
                del self.targets[ver]
                if ver in self.targetInstSrc:
                    del self.targetInstSrc[ver]
                self.svnTargets[ver] = self.svnTargets[branch]

    def setDependencies( self ):
        self.dependencies['libs/qtbase'] = 'default'


from Package.Qt5CorePackageBase import *

class Package( Qt5CorePackageBase ):
    def __init__( self, **args ):
        Qt5CorePackageBase.__init__( self )

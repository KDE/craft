import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdevplatform'
        self.svnTargets['0.9.94'] = 'tags/kdevplatform/0.9.94'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
    
from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()

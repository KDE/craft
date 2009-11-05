import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svn'] = 'tags/kdepim/pe5.20091103/kdebase'
        self.defaultTarget = 'svn'
    
    def setDependencies( self ):
        self.hardDependencies['enterprise5/kdelibs'] = 'default'
        self.hardDependencies['kdesupport/oxygen-icons'] = 'default'

from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()

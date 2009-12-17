import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['20091111'] = 'tags/kdepim/pe5.20091111/kdebase/runtime'
        self.svnTargets['20091123'] = 'tags/kdepim/pe5.20091123/kdebase/runtime'
        self.svnTargets['20091201'] = 'tags/kdepim/pe5.20091201/kdebase/runtime'
        self.defaultTarget = '20091201'
    
    def setDependencies( self ):
        self.hardDependencies['enterprise5/kdelibs-e5'] = 'default'
        self.hardDependencies['kdesupport/oxygen-icons'] = 'default'
        self.hardDependencies['win32libs-sources/libssh-src'] = 'default'

from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()

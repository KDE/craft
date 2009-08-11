import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['0.11.1'] = " https://opende.svn.sourceforge.net/svnroot/opende/tags/0.11.1"
        self.svnTargets['svnHEAD'] = " https://opende.svn.sourceforge.net/svnroot/opende/trunk"
        self.defaultTarget = '0.11.1'

from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        
    def unpack(self):
        CMakePackageBase.unpack(self)
        src = os.path.join(self.packageDir(),'CMakeLists.txt')
        dst = os.path.join(self.sourceDir(),'CMakeLists.txt')
        utils.copyFile(src,dst)
        return True
        
if __name__ == '__main__':
    Package().execute()

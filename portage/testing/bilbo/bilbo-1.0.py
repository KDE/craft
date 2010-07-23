import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = False
        self.targets['1.0'] = 'http://bilbo.gnufolks.org/packages/bilbo-1.0-src.tar.gz'
        self.targetInstSrc['1.0'] = 'bilbo'
        self.targetDigests['1.0'] = '91a285337b4fdd0a938d79edfbddda2f13142995'        
        self.defaultTarget = '1.0'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdepimlibs'] = 'default'
        self.hardDependencies['dev-util/gettext-tools'] = 'default'
        
from Package.CMakePackageBase import *
                
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)        
        	
if __name__ == '__main__':
    Package().execute()

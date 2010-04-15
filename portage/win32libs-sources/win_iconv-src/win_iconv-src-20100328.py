import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'http://win-iconv.googlecode.com/svn/trunk'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *        
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        
if __name__ == '__main__':
    Package().execute()

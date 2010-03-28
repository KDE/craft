import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'http://win-iconv.googlecode.com/svn/trunk'
        self.defaultTarget = 'svnHEAD'
        self.patchToApply['svnHEAD'] = ('win_iconv-src-20100328.diff', 0)
    
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *        
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        
if __name__ == '__main__':
    Package().execute()

import base
import os
import utils
import info
import sys

from Source.GitSource import *
from BuildSystem.QMakeBuildSystem import *

class subinfo(info.infoclass):
    def setTargets( self ):
        """ """
        self.svnTargets['svnHEAD'] = "git://github.com/mxcl/liblastfm.git"
        self.defaultTarget = 'svnHEAD'
        
    def setDependencies( self ):
        self.hardDependencies['dev-util/ruby'] = 'default'
        pass
        
class Package(GitSource,QMakeBuildSystem):
    def __init__( self, **args ):
        GitSource.__init__( self )
        QMakeBuildSystem.__init__( self )
        self.subinfo = subinfo()
        self.createCombinedPackage = True
        self.noClean = False
        self.noCopy = False
        
    #def configureOptions(self):
    #    return os.path.join(self.sourcedir,"src","lastfm.pro");

    def configureTool(self):
        return "ruby configure --release --prefix " + "../../../" 
        # absolute pathes does not work
        #self.rootdir.replace( "\\", "/" )

    #def configure(self, buildType=None, customOptions=""):
    #    #utils.copySrcDirToDestDir(self.sourcedir, self.builddir)
    #    return QMakeBuildSystem.configure(self, buildType, customOptions)
        
    def make_package( self ):
        self.instsrcdir = ""

        self.doPackaging( "liblastfm", os.path.basename(sys.argv[0]).replace("liblastfm-src-", "").replace(".py", ""), True )
        return True
  
if __name__ == '__main__':
    Package().execute()

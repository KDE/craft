import os
import shutil
import re
import utils
import info

# #########################################################################################
# ATTENTION: currently the only libraries that are built are boost.python libs
# that implies that the bin package requires the lib package as well to be used for compilation
# #########################################################################################

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.34.1'] = 'http://downloads.sourceforge.net/boost/boost_1_34_1.tar.bz2'
        self.targets['1.35.0'] = 'http://downloads.sourceforge.net/boost/boost_1_35_0.tar.bz2'
        self.targets['1.37.0'] = 'http://downloads.sourceforge.net/boost/boost_1_37_0.tar.bz2'
        self.targetInstSrc['1.34.1'] = 'boost_1_34_1'
        self.targetInstSrc['1.35.0'] = 'boost_1_35_0'
        self.targetInstSrc['1.37.0'] = 'boost_1_37_0'
        self.defaultTarget = '1.37.0'
    
    def setDependencies( self ):
        self.hardDependencies['dev-util/bjam'] = 'default'
        
from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

    def libsToBuild( self ):
        libs = " --with-python --with-program_options "
        return libs
        
    def configure( self, unused1=None, unused2=""):
        return True
        
    def make(self, unused=''):
        self.enterSourceDir()
        
        toolset = ""
        if self.compiler == "mingw" or self.compiler == "mingw4":
            toolset = "gcc"
        else:
            toolset = "msvc"
            
        cmd = "bjam --toolset=%s --prefix=%s --build-type=complete install " % \
                (toolset,
                self.imageDir())
                
        cmd += self.libsToBuild()
        print "command: ", cmd
        utils.system( cmd )
        return True
        
    def cleanImage( self ):
        return True

    def install( self ):

        # copy runtime libraries to the bin folder
        self.enterImageDir()
        cmd = "mkdir bin && move lib\\*.dll bin"
        print "command: ", cmd
        utils.system( cmd )
        return True

    def make_package( self ):
        return self.doPackaging( "boost", self.buildTarget, True )

if __name__ == '__main__':
    Package().execute()

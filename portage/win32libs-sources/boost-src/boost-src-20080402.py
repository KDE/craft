import os
import shutil
import re
import utils
import info
import platform

# #########################################################################################
# ATTENTION: currently the only libraries that are built are boost.python libs
# that implies that the bin package requires the lib package as well to be used for compilation
# #########################################################################################

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.34.1'] = 'http://downloads.sourceforge.net/boost/boost_1_34_1.tar.bz2'
        self.targets['1.35.0'] = 'http://downloads.sourceforge.net/boost/boost_1_35_0.tar.bz2'
        self.targets['1.37.0'] = 'http://downloads.sourceforge.net/boost/boost_1_37_0.tar.bz2'
        self.svnTargets['1.40.0'] = "git://gitorious.org/boost/cmake.git|1.40.0|"
        self.svnTargets['1.41.0'] = "git://gitorious.org/boost/cmake.git"
        self.targetInstSrc['1.34.1'] = 'boost_1_34_1'
        self.targetInstSrc['1.35.0'] = 'boost_1_35_0'
        self.targetInstSrc['1.37.0'] = 'boost_1_37_0'
        self.targetInstSrc['1.41.0'] = 'boost_1_41_0'
        
        if not platform.isCrossCompilingEnabled():
            self.defaultTarget = '1.41.0'
        else:
            self.patchToApply['1.40.0'] = ("boost-src-20100709", 1)
            self.defaultTarget = '1.40.0'
        
        #disables due to cmake boost does not support stlport yet
        #self.patchToApply['1.41.0'] = ("boost-src-20100428.patch", 1)
    
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        #disables due to cmake boost does not support stlport yet
        #if platform.isCrossCompilingEnabled():
        #    self.hardDependencies['win32libs-sources/stlport-src'] = 'default'


from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        
        projects = ""
        
        if self.isHostBuild():
            projects += "program_options"

        # only enable python for standard win32 builds, as x64 has problems with symbols and wince isn't supported
        if not platform.isCrossCompilingEnabled() and platform.buildArchitecture() == "x86":
            projects += ";python"
            
        self.subinfo.options.configure.defines =  "-DBUILD_PROJECTS=%s " % projects
        self.subinfo.options.configure.defines += "-DENABLE_STATIC=ON -DENABLE_STATIC_RUNTIME=ON " + \
                                                  "-DBOOST_RUNTIME_INSTALL_DIR=bin " + \
                                                  "-DINSTALL_VERSIONED=ON "
                                                 
        if self.buildType() == "Debug":
            self.subinfo.options.configure.defines += "-DENABLE_DEBUG=ON -DENABLE_RELEASE=OFF "
        else:
            self.subinfo.options.configure.defines += "-DENABLE_DEBUG=OFF -DENABLE_RELEASE=ON "
        CMakePackageBase.__init__(self)

        
        
#    def libsToBuild( self ):
#        libs = " --with-python --with-program_options "
#        return libs
#        
#    def configure( self, unused1=None, unused2=""):
#        return True
#        
#    def make(self, unused=''):
#        self.enterSourceDir()
#        
#        toolset = ""
#        if self.compiler == "mingw" or self.compiler == "mingw4":
#            toolset = "gcc"
#        else:
#            toolset = "msvc"
#            
#        cmd = "bjam --toolset=%s --prefix=%s --build-type=complete install " % \
#                (toolset,
#                self.imageDir())
#                
#        cmd += self.libsToBuild()
#        
#        if self.hasTargetPlatform():
#            self.setupCrossToolchain()
            # This is needed to find some wcecompat files (e.g. errno.h) included by some openssl headers
            # but we make sure to add it at the very end so it doesn't disrupt the rest of the Qt build
#            os.putenv( "INCLUDE", os.getenv("INCLUDE") + ";" + os.path.join( self.rootdir, "include", "wcecompat" ) )
        
#        print "command: ", cmd
#        utils.system( cmd )
#        return True
        
#    def cleanImage( self ):
#        return True

#    def install( self ):

        # copy runtime libraries to the bin folder
#        self.enterImageDir()
#        cmd = "mkdir bin && move lib\\*.dll bin"
#        print "command: ", cmd
#        utils.system( cmd )
#        return True

#    def make_package( self ):
#        return self.doPackaging( "boost", self.buildTarget, True )

if __name__ == '__main__':
    Package().execute()

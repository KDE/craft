import os.path
import re
import traceback
import shutil
import utils
import info
import platform

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
            self.patchToApply['1.40.0'] = ("boost-src-20100712.patch", 1)
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

    def install( self ):
        """ copy runtime libraries to the bin folder """

        # The Cmake variant of Boost names the libraries gcc44 in case they are compiled
        # with MinGW4. FindBoost.cmake expects mgw44 named dlls on windows systems though.
        # To enable FindBoost to find the installed Boost package without special options
        # Dll files also get installed into the the bin dir with the expected name.
        # To increase compatibility with different ways of finding boost the
        # Dlls are copied and the default installation remains untouched.
        if not CMakePackageBase.install( self ):
            return False

        DLL = re.compile(r".*\.[dD][lL][lL]$")

        try:
            if not os.path.exists(os.path.join(self.imageDir(), "bin")):
                os.mkdir(os.path.join(self.imageDir(), "bin"))
            for f in sum([[os.path.join(dp, f) for f in fns if DLL.match(f)]
                for dp, _, fns in os.walk(os.path.join(self.imageDir(), "lib"))], []):
                shutil.copy(f, os.path.join(self.imageDir(), "bin" ,
                               os.path.basename(f).replace("gcc44", "mgw44")))
        except:
            traceback.print_exc()
            utils.die("Error installing boost-src")
        return True

#    def make_package( self ):
#        return self.doPackaging( "boost", self.buildTarget, True )

if __name__ == '__main__':
    Package().execute()

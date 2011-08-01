import shutil
import info
import compiler
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['2.7.7', '2.7.8']:
            self.targets[ver] = 'ftp://xmlsoft.org/libxml2/libxml2-' + ver + '.tar.gz'
            self.targetInstSrc[ver] = 'libxml2-%s/win32' % ver
            self.patchToApply[ver] = ( 'libxml2-2.7.8-20110801.diff', 1 )
            
        self.targetDigests['2.7.7'] = '8592824a2788574a172cbddcdc72f734ff87abe3'
        self.targetDigests['2.7.8'] = '859dd535edbb851cc15b64740ee06551a7a17d40'
        self.shortDescription = "XML C parser and toolkit (runtime and applications)"

        self.defaultTarget = '2.7.8'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['win32libs-bin/zlib'] = 'default'
        self.dependencies['win32libs-bin/win_iconv'] = 'default'

    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = False

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.make.supportsMultijob = False
        
        mergeDir = self.mergeDestinationDir()
        prefix = mergeDir
        if mergeDir.endswith("\\"):
          prefix = mergeDir[0:-1]
        self.subinfo.options.configure.defines = (" prefix=%s " % prefix + \
                                                  "include=%s " % os.path.join(mergeDir,"include") + \
                                                  "lib=%s " % os.path.join(mergeDir,"lib") +\
                                                  "zlib=yes ")
        if os.getenv("EMERGE_BUILDTYPE") == "Debug":
            self.subinfo.options.configure.defines += " debug=yes"

        if compiler.isMinGW():
            self.subinfo.options.configure.defines += " compiler=mingw"
        elif compiler.isMSVC():
            self.subinfo.options.configure.defines += " compiler=msvc"
            
    def configure(self):          
        self.enterSourceDir()
        cmd  = "cscript configure.js"
        cmd += self.subinfo.options.configure.defines
        if utils.verbose() >= 1:
            print cmd
        os.system(cmd) and utils.die(
                "command: %s failed" % (cmd))
        return True
          

    def make(self):
        self.enterSourceDir()
        cmd = self.makeProgramm
        return self.system( cmd )
        
    def install(self):
        self.enterSourceDir()
        cmd = self.makeProgramm
        return self.system( cmd , "install" )
          


if __name__ == '__main__':
    Package().execute()


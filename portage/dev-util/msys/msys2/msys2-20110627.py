import info


class subinfo(info.infoclass):
    def setTargets( self ):
        if emergePlatform.buildArchitecture() == "x86":
            self.targets[ "base" ] = "http://downloads.sourceforge.net/sourceforge/msys2/msys2-base-i686-20131112.tar.xz"
        else:
            self.targets[ "base" ] = "http://downloads.sourceforge.net/sourceforge/msys2/msys64-base-x86_64-20131113.tar.xz"
            self.targetDigests['base'] = 'b907866161f92b8de2e9ff072e285479eb03afb6'
        self.defaultTarget = "base"


    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'

    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        BinaryPackageBase.__init__(self)        
        self.shell = MSysShell()

    def unpack(self):
        if not BinaryPackageBase.unpack(self):
          return False
        if emergePlatform.buildArchitecture() == "x64":
           shutil.move(os.path.join( self.imageDir(), "msys64"), os.path.join( self.imageDir(), "msys"))
        else:
           shutil.move(os.path.join( self.imageDir(), "msys32"), os.path.join( self.imageDir(), "msys"))
        utils.applyPatch(self.imageDir() , os.path.join(self.packageDir(), 'cd_currentDir.diff'), '0')
        utils.copyFile(os.path.join(self.packageDir(),"msys.bat"),os.path.join(self.rootdir,"dev-utils","bin","msys.bat"))
        return True
    
    def qmerge(self):
        if not BinaryPackageBase.qmerge(self):
           return False
        self.shell.execute(".","echo Firstrun")#start and restart msys before first use
        self.shell.execute(".","pacman -Syu --noconfirm")
        self.shell.execute(".","pacman -S base-devel --noconfirm")
        return True
       
if __name__ == '__main__':
    Package().execute()

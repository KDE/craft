import info


class subinfo(info.infoclass):
    def setTargets( self ):
        ver = "20130619"
        self.targets[ ver ] = "http://downloads.sourceforge.net/sourceforge/msys2/%s-msys2-alpha-%s.tar.xz" % (emergePlatform.buildArchitecture(), ver)       
        self.targetDigests['20130619'] = '79dd1c7da9168cc0969db22d5e4f9ad7ac953282'
        self.defaultTarget = ver


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
            shutil.move(os.path.join( self.imageDir(), "cross64"), os.path.join( self.imageDir(), "msys"))
        else:
            shutil.move(os.path.join( self.imageDir(), "cross32"), os.path.join( self.imageDir(), "msys"))
        utils.applyPatch(self.imageDir() , os.path.join(self.packageDir(), 'cd_currentDir.diff'), '0')
        utils.copyFile(os.path.join(self.packageDir(),"msys.bat"),os.path.join(self.rootdir,"dev-utils","bin","msys.bat"))
        return True
    
    def install(self):
        #self.shell.execute
        return True
       
if __name__ == '__main__':
    Package().execute()

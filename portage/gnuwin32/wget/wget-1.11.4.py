import info

# because the python http implementation do not support proxies 
# a local copy of wget is used for downloading
# the all inclusive wget binary is taken from http://users.ugent.be/~bpuype/wget/
# and do not have the multiple dll installation problem normal gnuwin32 package have

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['dummy'] = 'empty'
        self.defaultTarget = 'dummy'
        
    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = "dev-utils"
        self.subinfo.options.install.installPath = "bin"
        BinaryPackageBase.__init__(self)
        self.localwget = os.path.join(self.packageDir(),'wget.exe')

    def fetch(self):
        return True
        
    def unpack(self):
        dest = os.path.join(self.installDir(),'wget.exe')
        if not os.path.exists(self.installDir()):
            os.makedirs(self.installDir())
        return utils.copyFile(self.localwget,os.path.join(self.installDir(),'wget.exe'))
            
if __name__ == '__main__':
    Package().execute()

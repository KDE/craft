import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.60'] = """
            http://the.earth.li/~sgtatham/putty/latest/x86/pscp.exe
            http://the.earth.li/~sgtatham/putty/latest/x86/plink.exe
            http://the.earth.li/~sgtatham/putty/latest/x86/psftp.exe
            http://the.earth.li/~sgtatham/putty/latest/x86/pageant.exe
        """
        self.targetInstallPath['0.60'] = "bin"
        self.defaultTarget = '0.60'

from Package.BinaryPackageBase import *        
        
class Package(BinaryPackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = 'dev-utils'
        self.subinfo.options.package.withCompiler = False
        BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()




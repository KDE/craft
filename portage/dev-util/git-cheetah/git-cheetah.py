import os

from Package.BinaryPackageBase import *
import info


class subinfo( info.infoclass ):
    def setTargets( self ):
        arch = "x86"
        if os.path.exists(os.getenv("SystemDrive")+"/Program Files (x86)"):
              arch = 'x64'
        self.targets[ '20110703' ] = 'http://downloads.sourceforge.net/kde-windows/git-cheetah-%s-20110703-bin.tar.bz2' % arch
        self.targetDigestUrls[ '20110703' ] = 'http://downloads.sourceforge.net/kde-windows/git-cheetah-%s-20110703-bin.tar.bz2.sha1' % arch

        self.defaultTarget = '20110703'



    def setDependencies( self ):
        if not utils.varAsBool( emergeSettings.get("General",'EMERGE_ENABLE_IMPLICID_BUILDTIME_DEPENDENCIES', "False" )):
            self.buildDependencies[ 'gnuwin32/wget' ] = 'default'
        self.runtimeDependencies[ 'win32libs/expat' ] = 'default'


class Package(BinaryPackageBase):
  def __init__(self):
    BinaryPackageBase.__init__( self )
    self.subinfo.options.merge.destinationPath = 'dev-utils'
    
    def qmerge(self):
        if not BinaryPackageBase.qmerge(self):
            return False
        utils.system("regsvr32 -s -n -i:machine %s" % utils.deSubstPath(os.path.join(self.mergeDestinationDir() , "bin" , "git_shell_ext.dll" )))
        return True
        
    def unmerge(self):
        utils.system("regsvr32 -u -s -n -i:machine %s" % utils.deSubstPath(os.path.join(self.mergeDestinationDir() , "bin" , "git_shell_ext.dll" )))
        return BinaryPackageBase.unmerge(self)

if __name__ == '__main__':
    Package().execute()

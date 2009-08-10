import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.9.6'] = "http://www.winkde.org/pub/kde/ports/win32/installer/kdewin-packager.exe"
        self.defaultTarget = '0.9.6'

from Package.BinaryPackageBase import *
        
class Package(BinaryPackageBase):
  def __init__(self ):
    self.subinfo = subinfo()
    self.subinfo.options.merge.destinationPath = 'dev-utils'
    BinaryPackageBase.__init__( self )

  def install(self ):
    if not BinaryPackageBase.install( self ):
        return False
    
    utils.createDir( os.path.join(self.installDir(),'bin') )
    utils.moveFile( os.path.join(self.installDir(),'kdewin-packager.exe'), os.path.join(self.installDir(),'bin','kdewin-packager.exe') )
    return False

if __name__ == '__main__':
    Package().execute()

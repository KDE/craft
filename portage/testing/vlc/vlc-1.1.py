from Package.BinaryPackageBase import *
import info
import shutil
import os

# currently only needed from kdenetwork

class subinfo(info.infoclass):
    def setTargets( self ):    
        self.targets[ '1.1.0-20100129'] = """http://nightlies.videolan.org/build/win32/trunk-20100129-1616/vlc-1.1.0-git-20100129-1616-win32.7z"""

        self.defaultTarget = '1.1.0-20100129'
        self.targetInstSrc['1.1.0-20100129'] = "vlc-1.1.0-git-20100129-1616"
       

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
 

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    self.subinfo.options.merge.ignoreBuildType = True
    BinaryPackageBase.__init__( self )
    
    
  def install( self ):
    shutil.move( os.path.join( self.installDir() , self.subinfo.targetInstSrc[ self.subinfo.buildTarget ]) , os.path.join( self.installDir(), "bin" ) )
    shutil.move( os.path.join( self.installDir() , "bin" , "sdk" ) , os.path.join( self.installDir(),"include"))
    return True 
    
if __name__ == '__main__':
    Package().execute()

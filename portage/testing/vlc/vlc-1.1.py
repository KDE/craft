from Package.BinaryPackageBase import *
import info
import shutil
import os

# currently only needed from kdenetwork

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['20100226-0002']:
            self.targets[ ver ]  = "http://nightlies.videolan.org/build/win32/trunk-%s/vlc-1.1.0-git-%s-win32.7z" % (ver , ver )
            self.targetInstSrc[ver] = "vlc-1.1.0-git-%s" % (ver)
        
        
        self.defaultTarget = '20100226-0002'  
       

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
 

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    self.subinfo.options.merge.ignoreBuildType = True
    BinaryPackageBase.__init__( self )
    
    
  def install( self ):
    shutil.move( os.path.join( self.installDir() , self.subinfo.targetInstSrc[ self.subinfo.buildTarget ]) , os.path.join( self.installDir(), "bin" ) )
    shutil.move( os.path.join( self.installDir() , "bin" , "sdk" , "include") , os.path.join( self.installDir(), "include" ) ) 
    shutil.move( os.path.join( self.installDir() , "bin" , "sdk" , "lib") , os.path.join( self.installDir(), "lib" ) ) 
    return True 
    
if __name__ == '__main__':
    Package().execute()

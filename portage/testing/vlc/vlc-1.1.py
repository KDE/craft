from Package.BinaryPackageBase import *
import info
import shutil
import os
import re
import urllib

# currently only needed from kdenetwork


class subinfo(info.infoclass):
    def setTargets( self ):                
        self.targets[ "noDebug" ]  = "http://nightlies.videolan.org/build/win32/last/vlc-1.1.0-git-%s-win32.7z" % ( self.getVer() )
        self.targetInstSrc[ "noDebug" ] = "vlc-1.1.0-git-%s" % ( self.getVer() )
        
        self.targets[ self.getVer() ]  = "http://nightlies.videolan.org/build/win32/last/vlc-1.1.0-git-%s-win32-debug.7z" % ( self.getVer() )
        self.targetInstSrc[ self.getVer()] = "vlc-1.1.0-git-%s" % ( self.getVer() )        
        
        self.defaultTarget = self.getVer() 
       

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
        
    def getVer( self ):
        if( hasattr( self , "ver" ) ) :
          return self.ver
        else:
          fh = urllib.urlopen("http://nightlies.videolan.org/build/win32/last/")
          m = re.search( '\d\d\d\d\d\d\d\d-\d\d\d\d'  , fh.read() )
          fh.close()
          self.ver = m.group(0)
          return self.ver
        
class Package(BinaryPackageBase):
  def __init__(self):  
    self.subinfo = subinfo()    
    self.subinfo.options.merge.ignoreBuildType = True
    BinaryPackageBase.__init__( self )
    
    
  def install( self ):
    shutil.move( os.path.join( self.installDir() , self.subinfo.targetInstSrc[ self.subinfo.buildTarget ]) , os.path.join( self.installDir(), "bin" ) )
    shutil.move( os.path.join( self.installDir() , "bin" , "sdk" , "include") , os.path.join( self.installDir(), "include" ) ) 
    os.makedirs( os.path.join( self.installDir() , "share" , "applications" , "kde4" ) )
    shutil.copy(os.path.join( self.packageDir() ,"vlc.desktop" ), os.path.join( self.installDir() , "share" , "applications" , "kde4" ) )
    self.createImportLibs( "libvlc")
    self.createImportLibs( "libvlccore")
    return True 
    
if __name__ == '__main__':
    Package().execute()

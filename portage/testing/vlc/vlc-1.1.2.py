from Package.BinaryPackageBase import *
import info
import shutil
import os
import re
import urllib

# currently only needed from kdenetwork


class subinfo(info.infoclass):
  def setTargets( self ):    
    self.vlcBaseUrl = 'http://nightlies.videolan.org/build/win32/last/'
    self.vlcTagName = 'vlc-1.2.0-git-'
    self.targets[ self.vlcTagName + self.getVer() ]  =  self.vlcBaseUrl + self.vlcTagName + self.getVer() + "-win32.7z" 
    self.targetInstSrc[ self.vlcTagName + self.getVer() ] = self.vlcTagName + self.getVer()    
    
    self.targets[ self.vlcTagName + self.getVer() +"-debug" ]  = self.vlcBaseUrl + self.vlcTagName + self.getVer() + "-win32-debug.7z"
    self.targetInstSrc[ self.vlcTagName + self.getVer() +"-debug" ] = self.vlcTagName +  self.getVer()      
    
    self.targets[ 'vlc-1.1.2'] = "http://downloads.sourceforge.net/sourceforge/vlc/vlc-1.1.2-win32.7z"
    self.targetDigests['vlc-1.1.2'] = '2c66818b0686841c565b90f20075c9d6aca3ad57'
    self.targetInstSrc[ 'vlc-1.1.2' ] = "vlc-1.1.2"
    
    self.defaultTarget = 'vlc-1.1.2'
    

  def setDependencies( self ):
    self.hardDependencies['gnuwin32/wget'] = 'default'
    
  def getVer( self ):
    if( hasattr( self , "ver" ) ) :
      return self.ver
    else:
      try:
        fh = urllib.urlopen("http://nightlies.videolan.org/build/win32/last/" , timeout = 10)
      except:
        return " Nightlys Unavailible "
      m = re.search( '\d\d\d\d\d\d\d\d-\d\d\d\d'  , fh.read() )
      fh.close()
      self.ver = m.group(0)
      return self.ver

class Package(BinaryPackageBase):
  def __init__(self):  
    self.subinfo = subinfo()    
    self.subinfo.options.merge.ignoreBuildType = True
    self.subinfo.options.package.packSources = False
    self.subinfo.options.package.withCompiler = None
    BinaryPackageBase.__init__( self )
    
    
  def install( self ):
    shutil.move( os.path.join( self.installDir() , self.subinfo.targetInstSrc[ self.subinfo.buildTarget ]) , os.path.join( self.installDir(), "bin" ) )
    shutil.move( os.path.join( self.installDir() , "bin" , "sdk" , "include") , os.path.join( self.installDir(), "include" ) ) 
    shutil.rmtree( os.path.join( self.installDir() , "bin" , "sdk" ) )
    os.makedirs( os.path.join( self.installDir() , "share" , "applications" , "kde4" ) )
    utils.wgetFile( "http://git.videolan.org/?p=vlc.git;a=blob_plain;f=share/vlc.desktop" , os.path.join( self.installDir() , "share" , "applications" , "kde4" ) , "vlc.desktop"  )
    self.createImportLibs( "libvlc")
    self.createImportLibs( "libvlccore")
    return True 
    
if __name__ == '__main__':
    Package().execute()

from Package.BinaryPackageBase import *
import info
import shutil
import os
import re
import urllib2

# currently only needed from kdenetwork


class subinfo(info.infoclass):
  def setTargets( self ):    
    self.vlcArch = "32"
    if( emergePlatform.buildArchitecture() == 'x64' ):
        self.vlcArch = "64"
    self.vlcBaseUrl = 'http://nightlies.videolan.org/build/win'+self.vlcArch+'/last/'
    self.vlcTagName = 'vlc-1.2.0-git-'

    self.targets[ self.vlcTagName + self.getVer() ]  =  self.vlcBaseUrl + self.vlcTagName + self.getVer() + "-win32.7z" 
    self.targetInstSrc[ self.vlcTagName + self.getVer() ] = self.vlcTagName + self.getVer()    
    
    self.targets[ self.vlcTagName + self.getVer() +"-debug" ]  = self.vlcBaseUrl + self.vlcTagName + self.getVer() + "-win32-debug.7z"
    self.targetInstSrc[ self.vlcTagName + self.getVer() +"-debug" ] = self.vlcTagName +  self.getVer()      
    
    releaseTag = 'vlc-1.1.4'
    self.targets[ releaseTag] = "http://downloads.sourceforge.net/sourceforge/vlc/"+releaseTag+"-win32.7z"
    self.targetInstSrc[ releaseTag ] = releaseTag
    
    if( emergePlatform.buildArchitecture() == 'x64' ):
        self.defaultTarget = self.vlcTagName + self.getVer()
    else:
        self.defaultTarget = 'vlc-1.1.4'
    

  def setDependencies( self ):
    self.hardDependencies['gnuwin32/wget'] = 'default'
    
  def getVer( self ):
    if( hasattr( self , "ver" ) ) :
      return self.ver
    else:
      try:
        fh = urllib2.urlopen(self.vlcBaseUrl , timeout = 10)
        
      except Exception, e:
        return "Nightlys Unavailible:"+str(e)
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

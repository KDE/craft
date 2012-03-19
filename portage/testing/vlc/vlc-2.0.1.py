from Package.BinaryPackageBase import *
import info
import shutil
import os
import re
import urllib.request, urllib.error, urllib.parse
import compiler

_VLC_VER = None

class subinfo(info.infoclass):
  def setTargets( self ):
    self.vlcArch = "32"
    self.vlcTagName = '1.2.0-rc1-'
    if( emergePlatform.buildArchitecture() == 'x64' ):
        self.vlcArch = "64"        
    self.vlcBaseUrl = 'http://nightlies.videolan.org/build/win'+self.vlcArch+'/last/'
    self.vlcTagName = '2.1.0-git-%s' % self.getVer() 
    

    self.targets[ self.vlcTagName ]  =  "%svlc-%s-%s-win%s.7z" % (self.vlcBaseUrl, self.vlcTagName, self.getVer(),self.vlcArch  )
    
    self.targetInstSrc[ self.vlcTagName ] = "vlc-%s-%s" % (self.vlcTagName,self.getVer())

    self.targets[ self.vlcTagName +"-debug" ]  = "%svlc-%s-%s-win%s-debug.7z" % (self.vlcBaseUrl, self.vlcTagName, self.getVer(),self.vlcArch  )
    self.targetInstSrc[ self.vlcTagName + "-debug" ] = "vlc-%s-%s" % (self.vlcTagName,self.getVer())
    for releaseTag in [ '1.1.11','2.0.0','2.0.1']:
        self.targets[ releaseTag ] = "http://downloads.sourceforge.net/sourceforge/vlc/vlc-"+releaseTag+"-win32.7z"
        self.targetInstSrc[ releaseTag ] = 'vlc-' + releaseTag
        self.targetDigestUrls[ releaseTag ] = "http://downloads.sourceforge.net/sourceforge/vlc/vlc-"+releaseTag+"-win32.7z.sha1"
    self.shortDescription = "an open-source multimedia framework"

    if compiler.isMinGW_W64():
      self.defaultTarget = self.vlcTagName +"-debug" 
    else:
      self.defaultTarget = releaseTag


  def setDependencies( self ):
    self.buildDependencies['virtual/bin-base'] = 'default'

  def getVer( self ):
    global _VLC_VER
    if _VLC_VER != None :
      return _VLC_VER
    else:
      try:
        fh = urllib.request.urlopen(self.vlcBaseUrl , timeout = 10)
      except Exception as e:
        return "Nightlys Unavailible:"+str(e)
      m = re.search( "\d\d\d\d\d\d\d\d-\d\d\d\d"  , str(fh.read(),'UTF-8' ))
      fh.close()
      _VLC_VER = m.group(0)
      return _VLC_VER 

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    self.subinfo.options.package.packSources = False
    self.subinfo.options.package.packageName = 'vlc'
    BinaryPackageBase.__init__( self )


  def install( self ):
    shutil.move( os.path.join( self.installDir() , self.subinfo.targetInstSrc[ self.subinfo.buildTarget ]) , os.path.join( self.installDir(), "bin" ) )
    shutil.move( os.path.join( self.installDir() , "bin" , "sdk" , "include") , os.path.join( self.installDir(), "include" ) )
    shutil.move( os.path.join( self.installDir() , "bin" , "sdk" , "lib") , os.path.join( self.installDir(), "lib" ) )
    shutil.copy( os.path.join( self.imageDir() , "lib" ,"libvlc.dll.a" ) , os.path.join( self.imageDir() , "lib" ,"libvlc.lib" ))
    shutil.copy( os.path.join( self.imageDir() , "lib" ,"libvlccore.dll.a" ) , os.path.join( self.imageDir() , "lib" ,"libvlccore.lib" ))
    shutil.rmtree( os.path.join( self.installDir() , "bin" , "sdk" ) )
    os.makedirs( os.path.join( self.installDir() , "share" , "applications" , "kde4" ) )
    #utils.wgetFile( "http://git.videolan.org/?p=vlc.git;a=blob_plain;f=share/vlc.desktop" , os.path.join( self.installDir() , "share" , "applications" , "kde4" ) , "vlc.desktop"  )
    return True

if __name__ == '__main__':
    Package().execute()

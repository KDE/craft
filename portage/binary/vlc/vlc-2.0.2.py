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
    if( emergePlatform.buildArchitecture() == 'x64' ):
        self.vlcArch = "64"        
    self.vlcBaseUrl = 'http://nightlies.videolan.org/build/win'+self.vlcArch+'/last/'
    self.vlcTagName = 'vlc-2.2.0-git' 
    

    self.targets[ self.vlcTagName ]  =  "%svlc-%s-win%s.7z" % (self.vlcBaseUrl, self.vlcTagName,self.vlcArch  )
    
    self.targetInstSrc[ self.vlcTagName ] = "vlc-%s" % (self.vlcTagName)

    self.targets[ self.vlcTagName +"-debug" ]  = "%svlc-%s-win%s-debug.7z" % (self.vlcBaseUrl, self.vlcTagName,self.vlcArch  )
    self.targetInstSrc[ self.vlcTagName + "-debug" ] = "vlc-%s" % (self.vlcTagName)
    for releaseTag in [ '1.1.11','2.0.0','2.0.1','2.0.2','2.0.5','2.0.6', '2.0.8', '2.1.0','2.1.1']:
        self.targets[ releaseTag ] = "http://download.videolan.org/pub/videolan/vlc/%s/win%s/vlc-%s-win%s.7z" % ( releaseTag ,self.vlcArch,releaseTag , self.vlcArch )
        self.targetInstSrc[ releaseTag ] = 'vlc-' + releaseTag
        self.targetDigestUrls[ releaseTag ] = "http://download.videolan.org/pub/videolan/vlc/%s/win%s/vlc-%s-win%s.7z.sha1" % ( releaseTag ,self.vlcArch,releaseTag , self.vlcArch )
    for releaseTag in [ '2.0.2','2.0.5','2.0.6','2.1.0' ]:
        self.patchToApply[ releaseTag ] = [("vlc-%s.diff" % (releaseTag),1)]
    self.shortDescription = "an open-source multimedia framework"
    
    self.defaultTarget = '2.1.1'


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
    ver2 = self.subinfo.buildTarget.split('.')
    if not (int(ver2[0]) >= 2 and int(ver2[0]) >= 1):
      shutil.copy( os.path.join( self.installDir() , "lib" ,"libvlc.dll.a" ) , os.path.join( self.installDir() , "lib" ,"libvlc.lib" ))
      shutil.copy( os.path.join( self.installDir() , "lib" ,"libvlccore.dll.a" ) , os.path.join( self.installDir() , "lib" ,"libvlccore.lib" ))
    shutil.rmtree( os.path.join( self.installDir() , "bin" , "sdk" ) )
    os.makedirs( os.path.join( self.installDir() , "share" , "applications" , "kde4" ) )
    shutil.copy( os.path.join( self.packageDir() ,  "vlc.desktop" ) , os.path.join( self.installDir() , "share" , "applications" , "kde4" , "vlc.desktop" ))
    return True

if __name__ == '__main__':
    Package().execute()

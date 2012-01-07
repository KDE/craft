from Package.BinaryPackageBase import *
import info
import shutil
import os
import re
import urllib2
import compiler

_VLC_VER = None

class subinfo(info.infoclass):
  def setTargets( self ):
    self.vlcArch = "32"
    if( emergePlatform.buildArchitecture() == 'x64' ):
        self.vlcArch = "64"
    self.vlcBaseUrl = 'http://nightlies.videolan.org/build/win'+self.vlcArch+'/last/'
    self.vlcTagName = '1.3.0-'

    self.targets[ self.vlcTagName + self.getVer() ]  =  self.vlcBaseUrl + 'vlc-' + self.vlcTagName + self.getVer() + "-win" + self.vlcArch + ".7z"
    self.targetInstSrc[ self.vlcTagName + self.getVer() ] = 'vlc-' + self.vlcTagName + self.getVer()

    self.targets[ self.vlcTagName + self.getVer() +"-debug" ]  = self.vlcBaseUrl +  'vlc-' + self.vlcTagName + self.getVer() + "-win" + self.vlcArch + "-debug.7z"
    self.targetInstSrc[ self.vlcTagName + self.getVer() + "-debug" ] = 'vlc-' + self.vlcTagName +  self.getVer()

    releaseTag = '1.1.11'
    self.targets[ releaseTag ] = "http://downloads.sourceforge.net/sourceforge/vlc/vlc-"+releaseTag+"-win32.7z"
    self.targetInstSrc[ releaseTag ] = 'vlc-' + releaseTag
    self.targetDigests['1.1.11'] = '5d95a0e55c1d30f21e6dd4aa2fb1744a3ab694ac'
    self.shortDescription = "an open-source multimedia framework"

    if compiler.isMinGW_W64():
        self.defaultTarget = self.vlcTagName + self.getVer() +"-debug" 
    else:
        self.defaultTarget = releaseTag


  def setDependencies( self ):
    self.buildDependencies['virtual/bin-base'] = 'default'

  def getVer( self ):
    global _VLC_VER
    if _VLC_VER != None:
        return _VLC_VER

    try:
        fh = urllib2.urlopen(self.vlcBaseUrl , timeout = 10)
    except Exception, e:
        return "Nightlys Unavailible:"+str(e)

    m = re.search( '\d\d\d\d\d\d\d\d-\d\d\d\d'  , fh.read() )
    fh.close()
    if m == None:
        _VLC_VER = ""
    else:
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
    utils.wgetFile( "http://git.videolan.org/?p=vlc.git;a=blob_plain;f=share/vlc.desktop" , os.path.join( self.installDir() , "share" , "applications" , "kde4" ) , "vlc.desktop"  )
    return True

if __name__ == '__main__':
    Package().execute()

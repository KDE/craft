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
    self.vlcTagName = '1.2.0-git-'

    self.targets[ self.vlcTagName + self.getVer() ]  =  self.vlcBaseUrl + 'vlc-' + self.vlcTagName + self.getVer() + "-win32.7z"
    self.targetInstSrc[ self.vlcTagName + self.getVer() ] = 'vlc-' + self.vlcTagName + self.getVer()

    self.targets[ self.vlcTagName + self.getVer() +"-debug" ]  = self.vlcBaseUrl +  'vlc-' + self.vlcTagName + self.getVer() + "-win32-debug.7z"
    self.targetInstSrc[ self.vlcTagName + self.getVer() +"-debug" ] = 'vlc-' + self.vlcTagName +  self.getVer()

    releaseTag = '1.1.5'
    self.targets[ releaseTag ] = "http://downloads.sourceforge.net/sourceforge/vlc/vlc-"+releaseTag+"-win32.7z"
    self.targetInstSrc[ releaseTag ] = 'vlc-' + releaseTag
    self.targetDigests['1.1.5'] = 'c2da2e2a530d9558fcf9da46fa34920c66d9f2ef'
    self.shortDescription = "an open-source multimedia framework"
    if( emergePlatform.buildArchitecture() == 'x64' ):
        self.defaultTarget = self.vlcTagName + self.getVer()
    else:
        self.defaultTarget = '1.1.5'


  def setDependencies( self ):
    self.buildDependencies['virtual/bin-base'] = 'default'

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

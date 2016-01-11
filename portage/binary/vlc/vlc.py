import shutil
import os
import re

from Package.BinaryPackageBase import *
import info
import compiler

class subinfo(info.infoclass):
  vlc_ver = None
  
  def setTargets( self ):
    self.vlcArch = "32"
    if compiler.isX64():
        self.vlcArch = "64"        
    self.vlcBaseUrl = 'http://nightlies.videolan.org/build/win'+self.vlcArch+'/last/'
    self.vlcTagName = '3.0.0-git' 
    self.gitVer = utils.getNightlyVersionsFromUrl(self.vlcBaseUrl, "\d\d\d\d\d\d\d\d-\d\d\d\d" )[0]
    

    self.targets[ self.vlcTagName ]  =  "%svlc-%s-%s-win%s.7z" % (self.vlcBaseUrl, self.vlcTagName, self.gitVer, self.vlcArch  )
    self.targetInstSrc[ self.vlcTagName ] = "vlc-%s-%s" % (self.vlcTagName, self.gitVer)
    self.patchToApply[ self.vlcTagName ] = [("vlc-2.1.5.diff" ,1)]
    
    self.targets[ self.vlcTagName +"-debug" ]  = "%svlc-%s-%s-win%s-debug.7z" % (self.vlcBaseUrl, self.vlcTagName, self.gitVer, self.vlcArch  )
    self.targetInstSrc[ self.vlcTagName + "-debug" ] = "vlc-%s-%s" % (self.vlcTagName,self.gitVer)
    self.patchToApply[ self.vlcTagName + "-debug" ] = [("vlc-2.1.5.diff" ,1)]
    
    for releaseTag in [  '2.2.0', '2.2.1']:
        self.targets[ releaseTag ] = "http://download.videolan.org/pub/videolan/vlc/%s/win%s/vlc-%s-win%s.7z" % ( releaseTag ,self.vlcArch,releaseTag , self.vlcArch )
        self.targetInstSrc[ releaseTag ] = 'vlc-' + releaseTag
        self.targetDigestUrls[ releaseTag ] = "http://download.videolan.org/pub/videolan/vlc/%s/win%s/vlc-%s-win%s.7z.sha1" % ( releaseTag ,self.vlcArch,releaseTag , self.vlcArch )
        self.patchToApply[ releaseTag ] = [("vlc-2.1.5.diff" ,1)]
    self.shortDescription = "an open-source multimedia framework"
    
    self.defaultTarget = '2.2.1'


  def setDependencies( self ):
    self.buildDependencies['virtual/bin-base'] = 'default'

class Package(BinaryPackageBase):
  def __init__(self):
    BinaryPackageBase.__init__( self )
    self.subinfo.options.package.packageName = 'vlc'
    self.subinfo.options.package.packSources = False


  def install( self ):
    utils.copyDir(   self.sourceDir() , os.path.join( self.imageDir(), "bin" ) )
    if compiler.isMinGW():
      utils.deleteFile(os.path.join( self.imageDir(), "bin", "libgcc_s_seh-1.dll" ) )
    shutil.move( os.path.join( self.imageDir() , "bin" , "sdk" , "include") , os.path.join( self.imageDir(), "include" ) )
    shutil.move( os.path.join( self.imageDir() , "bin" , "sdk" , "lib") , os.path.join( self.imageDir(), "lib" ) )
    ver2 = self.subinfo.buildTarget.split('.')
    if not (int(ver2[0]) >= 2 and int(ver2[0]) >= 1):
      utils.copyFile( os.path.join( self.imageDir() , "lib" ,"libvlc.dll.a" ) , os.path.join( self.imageDir() , "lib" ,"libvlc.lib" ))
      utils.copyFile( os.path.join( self.imageDir() , "lib" ,"libvlccore.dll.a" ) , os.path.join( self.imageDir() , "lib" ,"libvlccore.lib" ))
    shutil.rmtree( os.path.join( self.imageDir() , "bin" , "sdk" ) )
    os.makedirs( os.path.join( self.imageDir() , "share" , "applications") )
    utils.copyFile( os.path.join( self.packageDir() ,  "vlc.desktop" ) , os.path.join( self.imageDir() , "share" , "applications", "vlc.desktop" ))
    return True


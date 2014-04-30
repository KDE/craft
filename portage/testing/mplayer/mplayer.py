# -*- coding: utf-8 -*-
import os

from Package.BinaryPackageBase import *
import info


class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://kovensky.project357.com/builds/mplayer/git/"""

        for version in ['20091013-314c6fc-2e061e0','20100211']:
            self.targets[ version ] = repoUrl+version+"/mplayer.exe"
        self.defaultTarget = '20100211'

    def setDependencies( self ):
        self.dependencies['virtual/bin-base'] = 'default'

class Package(BinaryPackageBase):
  def __init__(self):
    BinaryPackageBase.__init__( self )
    self.subinfo.options.package.withCompiler = None
    self.subinfo.options.package.packSources = False
    self.subinfo.options.merge.ignoreBuildType = True

  def install( self ):
    if(not os.path.exists(os.path.join( self.imageDir(), "bin" , "mplayer" ))):
      os.makedirs( os.path.join( self.imageDir(), "bin" , "mplayer" ))
    shutil.move( os.path.join( self.imageDir() , "mplayer.exe" ) , os.path.join( self.imageDir(), "bin" , "mplayer" , "mplayer.exe" ) )
    return True


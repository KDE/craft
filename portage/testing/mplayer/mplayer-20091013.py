# -*- coding: utf-8 -*-
from Package.BinaryPackageBase import *
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://kovensky.project357.com/builds/mplayer/git/"""
        
        for version in ['20091013-314c6fc-2e061e0','20100211']:
            self.targets[ version ] = repoUrl+version+"/mplayer.exe"            
        self.defaultTarget = '20100211'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    self.subinfo.options.merge.ignoreBuildType = True
    self.subinfo.options.package.packSources = False
    self.subinfo.options.package.withCompiler = None
    BinaryPackageBase.__init__( self )
    
  def install( self ):
    os.makedirs( os.path.join( self.imageDir(), "bin" , "mplayer" ))
    shutil.move( os.path.join( self.imageDir() , "mplayer.exe" ) , os.path.join( self.imageDir(), "bin" , "mplayer" , "mplayer.exe" ) )
    return True

if __name__ == '__main__':
    Package().execute()
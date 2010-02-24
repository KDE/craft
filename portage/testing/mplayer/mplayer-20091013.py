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
    self.subinfo.options.install.installPath = "bin/mplayer"

    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
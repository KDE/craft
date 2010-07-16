from Package.BinaryPackageBase import *
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for ver in ['1.0.8', '1.0.8-1', '1.0.8-2']:
            self.targets[ ver ] = self.getPackage( repoUrl, "redland", ver )

        #self.targetDigests['1.0.8-2'] = ['06a4856aa41efec0c812d50c57f49fdf0ab7dfbf',
        #                                 '3f20e15a2c42676fced3bf3a779ff8b1b277ea24']
        self.defaultTarget = '1.0.8-2'

    def setDependencies( self ):
        self.hardDependencies['win32libs-bin/iconv'] = 'default'
        self.hardDependencies['win32libs-bin/libcurl'] = 'default'
        self.hardDependencies['win32libs-bin/libxml2'] = 'default'
        self.hardDependencies['win32libs-bin/libxslt'] = 'default'
        self.hardDependencies['win32libs-bin/openssl'] = 'default'
        self.hardDependencies['win32libs-bin/pcre'] = 'default'
        self.hardDependencies['win32libs-bin/sqlite'] = 'default'
        self.hardDependencies['gnuwin32/wget'] = 'default'
        
    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()

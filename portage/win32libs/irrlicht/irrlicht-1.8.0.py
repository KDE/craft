from Package.CMakePackageBase import *
import info
import shutil
import os

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in [ '1.8' ]:
            self.targets[ ver ] = \
                'http://downloads.sourceforge.net/project/irrlicht/Irrlicht%20SDK/'+ver+'/irrlicht-'+ver+'.zip'
            self.targetInstSrc[ ver ] = 'irrlicht-' + ver + '/source/Irrlicht'
        self.patchToApply['1.8'] = ('irrlicht-1.8-20130411.diff', 3)
        self.targetDigests['1.8'] = 'a24c2183e3c7dd909f92699c373a68382958b09d'
        self.shortDescription = 'lightning fast realtime 3D engine'
        self.defaultTarget = '1.8'

    def setDependencies( self ):
        self.hardDependencies['win32libs/jpeg'] = 'default'
        self.hardDependencies['win32libs/libpng'] = 'default'
        self.hardDependencies['win32libs/libbzip2'] = 'default'
        self.buildDependencies['virtual/bin-base'] = 'default'


class Package(CMakePackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    CMakePackageBase.__init__( self )


if __name__ == '__main__':
    Package().execute()

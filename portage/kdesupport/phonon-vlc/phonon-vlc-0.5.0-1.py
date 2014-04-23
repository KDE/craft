# -*- coding: utf-8 -*-

import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies( self ):
        self.dependencies['kdesupport/phonon'] = 'default'
        self.dependencies['binary/vlc'] = 'default'
        if compiler.isMSVC() or compiler.isIntel():
            self.dependencies['kdesupport/kdewin'] = 'default'

    def setTargets( self ):
      for ver in ['0.7.0']:
        self.targets[ ver ] = "http://download.kde.org/stable/phonon/phonon-backend-vlc/%s/src/phonon-backend-vlc-%s.tar.xz" % ( ver ,ver )
        self.targetInstSrc[ ver ] = "phonon-backend-vlc-%s" % ver 
        
      for ver in ['0.7.1']:
        self.targets[ ver ] = "http://download.kde.org/stable/phonon/phonon-backend-vlc/%s/phonon-backend-vlc-%s.tar.xz" % ( ver ,ver )
        self.targetInstSrc[ ver ] = "phonon-backend-vlc-%s" % ver 
        
      self.targetDigests['0.7.0'] = '8ebf032d7a87064e1307ff3f421aef2b07088681'
      self.targetDigests['0.7.1'] = '6f8e8abae12fdafc63b911b185cb335c65d59450'
      
      self.patchToApply['0.7.0'] = [("use-kdewin-also-for-intel-compiler.diff", 1), # upstream
                                    ("0002-FindLIBVLC-Detect-libvlc-s-version-even-if-pkg-confi.patch", 1)] # upstream
      
      self.svnTargets['gitHEAD'] = '[git]kde:phonon-vlc'
      
      self.shortDescription = "the vlc based phonon multimedia backend"
      self.defaultTarget = 'gitHEAD'


class Package( CMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = ' -DCMAKE_CXX_FLAGS=-DWIN32  -DPHONON_BUILD_PHONON4QT5=ON -DPHONON_BUILDSYSTEM_DIR=\"%s\" ' % (os.path.join(os.getenv('KDEROOT'),'share','phonon','buildsystem').replace('\\','/'))

if __name__ == '__main__':
    Package().execute()

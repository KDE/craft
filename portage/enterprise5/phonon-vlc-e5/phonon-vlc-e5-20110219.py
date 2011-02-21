# -*- coding: utf-8 -*-
import info
import os
import compiler
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies( self ):
        self.dependencies['enterprise5/phonon-e5'] = 'default'
        self.runtimeDependencies['testing/vlc'] = 'default'
        if compiler.isMSVC():
            self.dependencies['enterprise5/kdewin-e5'] = 'default'

    def setTargets( self ):
      self.targets['0.3.1'] = "http://download.kde.org/download.php?url=stable/phonon-backend-vlc/0.3.1/src/phonon-backend-vlc-0.3.1.tar.bz2"
      self.targetInstSrc['0.3.1'] = "phonon-backend-vlc-0.3.1"
      self.targetDigests['0.3.1'] = 'b94dddc6f37924c101a8bab7b7a184b7d6b42d96'
      self.patchToApply['0.3.1'] = ("phonon-backend-vlc-0.3.1-20101223.diff", 1)
      self.svnTargets['gitHEAD'] = '[git]kde:phonon-vlc'
      self.shortDescription = "the vlc based phonon multimedia backend"
      self.defaultTarget = '0.3.1'


class Package( CMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = \
                '-DPHONON_BUILDSYSTEM_DIR=\"%s\" ' % os.path.join(
                        os.getenv('KDEROOT'), 'share',
                        'phonon-buildsystem').replace('\\','/')

if __name__ == '__main__':
    Package().execute()

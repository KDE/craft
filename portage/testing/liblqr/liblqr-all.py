# -*- coding: utf-8 -*-
import info

from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.defaultTarget = '0.4.2'
        self.shortDescription = "liblqr is a seam-carving C/C++ library called Liquid Rescale that aims to resize pictures non-uniformly while preserving their features, i.e. avoiding distortion of the important parts."
        
        self.svnTargets['gitHEAD'] = 'http://repo.or.cz/w/liblqr.git'        
        
        for ver in ['0.4.2']:
            self.targets[ver] = "http://liblqr.wdfiles.com/local--files/en:download-page/liblqr-1-%s.tar.bz2" % (ver)
            self.targetInstSrc[ver] = "liblqr-1-%s" % ver
        
        self.targetDigests['0.4.2'] = '69639f7dc56a084f59a3198f3a8d72e4a73ff927'
        
        self.patchToApply['0.4.2'] = ('liblqr-1-0.4.2.diff', 1)
        
    
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        # self.buildDependencies['dev-util/doxygen'] = 'default' # only needed if building docs
        self.dependencies['testing/glib-src'] = 'default'
        

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()

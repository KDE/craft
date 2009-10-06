# -*- coding: utf-8 -*-
import base
import os
import sys
import info
import utils

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/extragear/graphics/digikam'
        self.targets['0.10.0'] = 'http://digikam3rdparty.free.fr/0.10.x-releases/digikam-0.10.0.tar.bz2'
        self.targetInstSrc['0.10.0'] = 'digikam-0.10.0'
        for ver in ['beta1', 'beta3', 'beta4', 'beta5']:
            self.targets['1.0.0-' + ver] = 'http://downloads.sourceforge.net/project/digikam/digikam/1.0.0-' + ver + '/digikam-1.0.0-' + ver + '.tar.bz2'
            self.targetInstSrc['1.0.0-' + ver] = 'digikam-1.0.0-' + ver
        
        self.svnTargets['branch-0.10.0'] = 'branches/extragear/graphics/digikam/0.10.0-trunk'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
        self.hardDependencies['kde/kdegraphics'] = 'default'
        self.hardDependencies['win32libs-bin/lcms'] = 'default'
        self.hardDependencies['win32libs-bin/gettext'] = 'default'
        self.hardDependencies['dev-util/gettext-tools'] = 'default'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "digikam"
        self.subinfo = subinfo()

    def unpack( self ):
        if self.buildTarget in ['0.10.0', '1.0.0-beta1', '1.0.0-beta3', '1.0.0-beta4', '1.0.0-beta5']:
            if( not base.baseclass.unpack( self ) ):
                return False
            else:
                return True
        else:
            return self.kdeSvnUnpack()

    def compile( self ):
        self.kdeCustomDefines = "-DENABLE_GPHOTO2=OFF"
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if not self.buildTarget == 'svnHEAD':
            return self.doPackaging( "digikam", self.buildTarget, True )
        else:
            return self.doPackaging( "digikam" )


if __name__ == '__main__':		
    subclass().execute()

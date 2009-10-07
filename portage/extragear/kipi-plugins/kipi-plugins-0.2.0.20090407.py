# -*- coding: utf-8 -*-
import base
import os
import sys
import info
import utils

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/extragear/graphics/kipi-plugins'
        for ver in ['0.2.0', '0.3.0', '0.5.0', '0.6.0', '0.7.0']:
            self.targets[ ver ] = "http://downloads.sourceforge.net/project/kipi/kipi-plugins/" + ver + "/kipi-plugins-" + ver + ".tar.bz2"
            self.targetInstSrc[ ver ] = 'kipi-plugins-' + ver
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
        self.hardDependencies['kde/kdegraphics'] = 'default'
        self.hardDependencies['win32libs-bin/gettext'] = 'default'
        self.hardDependencies['dev-util/gettext-tools'] = 'default'
        self.hardDependencies['win32libs-bin/expat'] = 'default'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "kipi-plugins"
        self.subinfo = subinfo()

    def unpack( self ):
        if self.buildTarget in ['0.2.0', '0.3.0', '0.5.0', '0.6.0', '0.7.0']:
            ret = base.baseclass.unpack( self )
            if self.buildTarget == '0.7.0':
                self.system( "cd %s && patch -p0 < %s" % ( self.workdir, os.path.join( self.packagedir, "kipi-twain-stable.diff" ) ) )
            return ret
        else:
            return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if not self.buildTarget == 'svnHEAD':
            return self.doPackaging( "kipi-plugins", self.buildTarget, True )
        else:
            return self.doPackaging( "kipi-plugins" )


if __name__ == '__main__':		
    subclass().execute()

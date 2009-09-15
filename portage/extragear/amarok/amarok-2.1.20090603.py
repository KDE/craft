# -*- coding: utf-8 -*-
import base
import os
import sys
import info
import utils

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['2.1.1'] = 'tags/amarok/2.1.1/amarok'
        for rel in ['2.0', '2.0.1.1', '2.1']:
            self.targets[ rel ] = 'ftp://ftp.kde.org/pub/kde/stable/amarok/' + rel + '/src/amarok-' + rel + '.tar.bz2'
            self.targetInstSrc[ rel ] = 'amarok-' + rel
        self.svnTargets['master'] = 'git://gitorious.org/amarok/amarok.git'
        self.defaultTarget = 'master'
    
    def setDependencies( self ):
        self.hardDependencies['kdesupport/taglib'] = 'default'
        self.hardDependencies['kdesupport/taglib-extras'] = 'default'
        self.hardDependencies['kdesupport/phonon'] = 'default'
        self.hardDependencies['kde/kdelibs'] = 'default'
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
        self.hardDependencies['testing/mysql-server'] = 'default'
        self.hardDependencies['testing/mysql-embedded'] = 'default'
        # this is only a runtime dependency: keep that in mind for later!!!!
        self.hardDependencies['testing/qtscriptgenerator'] = 'default'
        self.hardDependencies['win32libs-bin/gettext'] = 'default'
        self.hardDependencies['dev-util/gettext-tools'] = 'default'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "amarok"
        self.subinfo = subinfo()

    def unpack( self ):
        if self.buildTarget not in ['master']:
            if self.buildTarget in ['2.0', '2.0.1.1', '2.1']:
                if( not base.baseclass.unpack( self ) ):
                    return False
                    
                if self.buildTarget == '1.90':
                    src = os.path.join( self.workdir, self.instsrcdir )

                    cmd = "cd %s && patch -p0 < %s" % \
                          ( src, os.path.join( self.packagedir , "amarok-beta1.diff" ) )
                    if utils.verbose() >= 1:
                        print cmd
    #                self.system( cmd ) or die( "patch" )
                return True
            else:
                return self.kdeSvnUnpack()
        else:
            return base.baseclass.unpack( self )

    def compile( self ):
        if self.buildTarget in ['master']:
            self.kde.sourcePath = self.svndir

        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if self.buildTarget in ['master']:
            self.kde.sourcePath = self.svndir

        if not self.buildTarget == 'svnHEAD':
            return self.doPackaging( "amarok", self.buildTarget, True )
        else:
            return self.doPackaging( "amarok" )


if __name__ == '__main__':		
    subclass().execute()

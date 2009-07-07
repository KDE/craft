# -*- coding: utf-8 -*-
import base
import info
import shutil
import os

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

    def setTargets( self ):
        self.targets['HEAD'] = 'http://winkde.org/pub/kde/ports/win32/repository/other/jom-20090611-bin.tar.bz2'
        self.targetInstSrc['HEAD'] = 'jom'
        self.defaultTarget = 'HEAD'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instdestdir = "dev-utils"
        self.subinfo = subinfo()

    def unpack( self ):
        return base.baseclass.unpack( self )

    def install(self):
        res = base.baseclass.install( self )
        srcdir = os.path.join( os.path.join(self.workdir, "bin"), "jom.exe" )
        destdir = os.path.join( self.imagedir, "bin" )
        if not os.path.exists( self.imagedir ):
            os.mkdir( self.imagedir )
        if not os.path.exists( destdir ):
            os.mkdir( destdir )
        shutil.copy( srcdir, os.path.join( destdir, "jom.exe" ) )
        return res

if __name__ == '__main__':
    subclass().execute()

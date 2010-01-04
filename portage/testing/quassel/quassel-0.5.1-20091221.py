# -*- coding: utf-8 -*-
import info
import os
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'git://git.quassel-irc.org/quassel.git'
        self.defaultTarget = 'gitHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdelibs'] = 'default'
    

class Package( CMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = ""
        self.subinfo.options.configure.defines += " -DWITH_KDE=ON"

    def unpack( self ):
        if not CMakePackageBase.unpack( self ):
            return False
       #  self.source.shell.execute(os.environ["KDEROOT"],"pexport"sos.path.join( os.environ["SYSTEMROOT"], "System32" , "dbghelp.dll" ) )
     #Advapi32.dll
     #Secur32.dll
    #dbgHelp.h
        self.source.shell.execute( self.sourceDir(), "git", "reset --hard" )
        utils.applyPatch( self.sourceDir(), os.path.join( self.packageDir(), "quassel.diff" ), 1 )

        return True
      


if __name__ == '__main__':
    Package().execute()

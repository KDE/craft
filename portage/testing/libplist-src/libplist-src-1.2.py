# -*- coding: utf-8 -*-
import info
import os
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'git://github.com/JonathanBeck/libplist.git'
        self.defaultTarget = 'gitHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['win32libs-bin/libxml2'] = 'default'
        self.hardDependencies['virtual/base'] = 'default'
    
class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

    def unpack( self ):
        if not CMakePackageBase.unpack( self ):
            return False
        self.source.shell.execute( self.sourceDir(), "git", "reset --hard" )
        utils.applyPatch( self.sourceDir(), os.path.join( self.packageDir(), "mingw.diff" ), 1 )
        return True
        
if __name__ == '__main__':
    Package().execute()

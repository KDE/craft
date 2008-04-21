import base
import utils
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'branches/ktorrent/windows_port'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdelibs'] = 'default'
        self.hardDependencies['kdesupport/qca'] = 'default'
        self.hardDependencies['testing/libgmp-src'] = 'default'
    
class subclass(base.baseclass):
    def __init__(self):
        self.buildType = "Debug"
        base.baseclass.__init__( self, "" )
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        return self.doPackaging( "ktorrent", self.buildTarget, True )

if __name__ == '__main__':
    subclass().execute()

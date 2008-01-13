import base
import utils
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['4.0.0'] = 'tags/KDE/4.0.0/kdeedu'
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdeedu'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdebase'] = 'default'
        
        self.softDependencies['kdesupport/eigen'] = 'default'
        self.softDependencies['win32libs-sources/cfitsio-src'] = 'default'
        self.softDependencies['win32libs-sources/libnova-src'] = 'default'
        self.softDependencies['win32libs-sources/openbabel-src'] = 'default'
    
class subclass(base.baseclass):
    def __init__(self):
        base.baseclass.__init__( self, "" )
        self.instsrcdir = "kdeedu"
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        self.kdeCustomDefines = "-DBUILD_doc=OFF"
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        return self.doPackaging( "kdeedu", os.path.basename(sys.argv[0]).replace("kdeedu-", "").replace(".py", ""), True )

if __name__ == '__main__':
    subclass().execute()

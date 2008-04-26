import base
import os
import sys
import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

    def setTargets( self ):
        self.targets['1.4.0'] = 'http://developer.kde.org/~wheeler/files/src/taglib-1.4.tar.gz'
        self.targetInstSrc['1.4.0'] = 'taglib-1.4'
        self.targets['1.5.0'] = 'http://developer.kde.org/~wheeler/files/src/taglib-1.5.tar.gz'
        self.targetInstSrc['1.5.0'] = 'taglib-1.5'
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/taglib'
        self.defaultTarget = 'svnHEAD'

class subclass(base.baseclass):
    def __init__(self):
        base.baseclass.__init__( self, "" )
        self.instsrcdir = "taglib"
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if self.buildTarget == "svnHEAD":
            self.instdestdir = "kde"
            return self.doPackaging( "taglib", os.path.basename(sys.argv[0]).replace("taglib-", ""), True )
        else:
            return self.doPackaging( "taglib", self.buildTarget, True )

if __name__ == '__main__':
    subclass().execute()

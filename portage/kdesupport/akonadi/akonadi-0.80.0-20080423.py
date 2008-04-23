import base
import os
import sys
import info

#DEPEND = """
#virtual/base
#"""

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/akonadi'
        self.defaultTarget = 'svnHEAD'

class subclass(base.baseclass):
    def __init__(self):
        base.baseclass.__init__( self, "" )
        self.instsrcdir = "akonadi"
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
            return self.doPackaging( "akonadi", os.path.basename(sys.argv[0]).replace("akonadi-", ""), True )
        else:
            return self.doPackaging( "taglib", self.buildTarget, True )

if __name__ == '__main__':
    subclass().execute()

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
        if self.traditional:
            self.instdestdir = "kde"
            return self.doPackaging( "taglib", "1.4.0-3", True )
        else:
            return self.doPackaging( "taglib", os.path.basename(sys.argv[0]).replace("taglib-", "").replace(".py", ""), True )

if __name__ == '__main__':
    subclass().execute()

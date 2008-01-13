import base
import os
import sys
import info

#DEPEND = """
#virtual/base
#libs/qt
#"""

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['lib/qt'] = 'default'

    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/qca'
        self.defaultTarget = 'svnHEAD'

class subclass(base.baseclass):
    def __init__(self):
        base.baseclass.__init__( self, "" )
        self.instsrcdir = "qca"
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
            return self.doPackaging( "qca", "2.0.0-4", True )
        else:
            return self.doPackaging( "qca", os.path.basename(sys.argv[0]).replace("qca-", "").replace(".py", ""), True )

if __name__ == '__main__':
    subclass().execute()

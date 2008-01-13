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
        self.hardDependencies['libs/qt'] = 'default'

    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/qimageblitz'
        self.defaultTarget = 'svnHEAD'

class subclass(base.baseclass):
    def __init__(self):
        base.baseclass.__init__( self, "" )
        self.instsrcdir = "qimageblitz"
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
            return self.doPackaging( "qimageblitz", "4.0.0-3", True )
        else:
            return self.doPackaging( "qimageblitz", os.path.basename(sys.argv[0]).replace("qimageblitz-", "").replace(".py", ""), True )

if __name__ == '__main__':
    subclass().execute()

import os
import sys
import base
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
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/kdewin32'
        self.defaultTarget = 'svnHEAD'

class subclass(base.baseclass):
    def __init__(self):
        base.baseclass.__init__( self, "" )
        self.instsrcdir = "kdewin32"
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
            return self.doPackaging( "kdewin32", "0.3.5-1", True )
        else:
            return self.doPackaging( "kdewin32", os.path.basename(sys.argv[0]).replace("kdewin32-", "").replace(".py", ""), True )
if __name__ == '__main__':
    subclass().execute()

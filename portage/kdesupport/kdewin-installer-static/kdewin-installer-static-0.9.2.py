import base
import utils
from utils import die
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
        self.hardDependencies['libs/qt-static'] = 'default'
        self.hardDependencies['dev-util/upx'] = 'default'

    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/kdewin-installer'
        self.defaultTarget = 'svnHEAD'

class subclass(base.baseclass):
    def __init__(self):
        base.baseclass.__init__( self, "" )
        self.instsrcdir = "kdewin-installer"
        self.buildType = "Release"
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
        return self.doPackaging( "kdewin-installer", os.path.basename(sys.argv[0]).replace("kdewin-installer-", "").replace(".py", ""), True )

if __name__ == '__main__':
    subclass().execute()
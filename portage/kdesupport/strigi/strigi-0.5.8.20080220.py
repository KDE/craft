import base
import os
import sys
import info

#currently build without clucene...
class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['libs/qt'] = 'default'
        self.hardDependencies['kdesupport/kdewin32'] = 'default'
        self.hardDependencies['kdesupport/clucene-core'] = 'default'

    def setTargets( self ):
        self.svnTargets['0.5.7'] = 'tags/strigi/strigi/0.5.7'
        self.svnTargets['0.5.8'] = 'tags/strigi/strigi/0.5.8'
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/strigi'
        self.defaultTarget = 'svnHEAD'

class subclass(base.baseclass):
    def __init__(self):
        base.baseclass.__init__( self, "" )
        self.instsrcdir = "strigi"
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
        if self.buildTarget == "svnHEAD":
            return self.doPackaging( "strigi", os.path.basename(sys.argv[0]).replace("strigi-", ""), True )
        else:
            return self.doPackaging( "strigi", self.buildTarget, True )

if __name__ == '__main__':
    subclass().execute()

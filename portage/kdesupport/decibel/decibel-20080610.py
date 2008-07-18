import base
import os
import sys
import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['libs/qt'] = 'default'
        self.hardDependencies['kdesupport/tapioca-qt'] = 'default'
        self.hardDependencies['kdesupport/telepathy-qt'] = 'default'

    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/decibel'
        self.defaultTarget = 'svnHEAD'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "decibel"
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
            return self.doPackaging( "decibel", "20080610", True )
        else:
            return self.doPackaging( "decibel", os.path.basename(sys.argv[0]).replace("decibel-", "").replace(".py", ""), True )

if __name__ == '__main__':
    subclass().execute()

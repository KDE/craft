import base
import os
import sys
import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['kdesupport/automoc'] = 'default'
        self.hardDependencies['libs/qt'] = 'default'

    def setTargets( self ):
        self.svnTargets['0.80'] = 'tags/akonadi/0.80/'
        self.svnTargets['0.81'] = 'tags/akonadi/0.81/'
        self.svnTargets['0.82'] = 'tags/akonadi/0.82/'
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/akonadi'
        self.defaultTarget = 'svnHEAD'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
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
            return self.doPackaging( "akonadi", os.path.basename(sys.argv[0]).replace("akonadi-", ""), True )
        else:
            return self.doPackaging( "akonadi", self.buildTarget, True )

if __name__ == '__main__':
    subclass().execute()

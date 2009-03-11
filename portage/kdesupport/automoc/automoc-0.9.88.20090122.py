import base
import utils
import sys
import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['libs/qt'] = 'default'

    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/automoc'
        self.svnTargets['0.9.83'] = 'tags/automoc4/0.9.83'
        self.svnTargets['0.9.84'] = 'tags/automoc4/0.9.84'
        self.svnTargets['0.9.87'] = 'tags/automoc4/0.9.87'
        self.svnTargets['0.9.88'] = 'tags/automoc4/0.9.88'
        self.defaultTarget = 'svnHEAD'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "automoc"
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if self.buildTarget == "svnHEAD":
            return self.doPackaging( "automoc" )
        else:
            return self.doPackaging( "automoc", self.buildTarget, True )

if __name__ == '__main__':
    subclass().execute()

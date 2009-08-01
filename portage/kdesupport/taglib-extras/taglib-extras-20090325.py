import base
import utils
import sys
import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['kdesupport/taglib'] = 'default'
        self.hardDependencies['kde/kdelibs'] = 'default'

    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/taglib-extras'
        for i in ['4.3.0', '4.3.1', '4.3.2', '4.3.3', '4.3.4', '4.3']:
            self.svnTargets[ i ] = 'tags/kdesupport-for-4.3/kdesupport/taglib-extras'
        self.defaultTarget = 'svnHEAD'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "taglib-extras"
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
#        self.kdeCustomDefines = "-DWITH_KDE=ON"
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if self.buildTarget == "svnHEAD":
            return self.doPackaging( "taglib-extras", utils.cleanPackageName( sys.argv[0], "taglib-extras" ), True )
        else:
            return self.doPackaging( "taglib-extras", self.buildTarget, True )

if __name__ == '__main__':
    subclass().execute()

import base
import utils
import sys
import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

    def setTargets( self ):
        self.targets['1.4.0'] = 'http://developer.kde.org/~wheeler/files/src/taglib-1.4.tar.gz'
        self.targetInstSrc['1.4.0'] = 'taglib-1.4'
        self.targets['1.5.0'] = 'http://developer.kde.org/~wheeler/files/src/taglib-1.5.tar.gz'
        self.targetInstSrc['1.5.0'] = 'taglib-1.5'
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/taglib'
        for i in ['4.3.0', '4.3.1', '4.3.2', '4.3.3', '4.3.4', '4.3']:
            self.svnTargets[ i ] = 'tags/kdesupport-for-4.3/kdesupport/taglib'
        self.defaultTarget = 'svnHEAD'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "taglib"
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        self.kdeCustomDefines = ""
#        self.kdeCustomDefines += " -DBUILD_TESTS=ON"
#        self.kdeCustomDefines += " -DBUILD_EXAMPLES=ON"
#        self.kdeCustomDefines += " -DNO_ITUNES_HACKS=ON"
        self.kdeCustomDefines += " -DWITH_ASF=ON"
        self.kdeCustomDefines += " -DWITH_MP4=ON"

        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if self.buildTarget == "svnHEAD":
            return self.doPackaging( "taglib" )
        else:
            return self.doPackaging( "taglib", self.buildTarget, True )

if __name__ == '__main__':
    subclass().execute()

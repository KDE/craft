import sys
import base
import utils
import os
import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['libs/qt'] = 'default'
        self.hardDependencies['kdesupport/automoc'] = 'default'

    def setTargets( self ):
        self.svnTargets['_4.1.0'] = 'tags/phonon/4.1.0'    # tagged version, also in qt4.4.0
        self.svnTargets['_4.2.0'] = 'tags/phonon/4.2.0'    # tagged version
        self.svnTargets['_4.3.0'] = 'tags/phonon/4.3.0'
        self.svnTargets['_4.3.1'] = 'tags/phonon/4.3.1'
        self.svnTargets['_4.2'] = 'branches/phonon/4.2'
        for i in ['4.3.0', '4.3.1', '4.3.2', '4.3.3', '4.3.4', '4.3']:
            self.svnTargets[ i ] = 'tags/kdesupport-for-4.3/kdesupport/phonon'
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/phonon'
        self.defaultTarget = 'svnHEAD'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "phonon"
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        if self.compiler == "mingw":
            """
            For microsoft compilers the DirectX SDK is needed if you want to
            compile the DirectShow 9 backend.
            """
            os.environ["DXSDK_DIR"] = os.path.join( self.rootdir, "include", "mingw" )
        self.kdeCustomDefines="-DPHONON_BUILD_EXAMPLES=OFF -DPHONON_BUILD_TESTS=OFF"
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if self.buildTarget == "svnHEAD":
            return self.doPackaging( "phonon" )
        else:
            return self.doPackaging( "phonon", self.buildTarget, True )

if __name__ == '__main__':
    subclass().execute()

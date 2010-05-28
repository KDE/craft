import sys
import base
import utils
import os
import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['libs/qt'] = 'default'
        self.hardDependencies['enterprise5/automoc-e5'] = 'default'

    def setTargets( self ):
        self.svnTargets['4.1.0'] = 'tags/phonon/4.1.0'    # tagged version, also in qt4.4.0
        self.svnTargets['4.2.0'] = 'tags/phonon/4.2.0'    # tagged version
        self.svnTargets['4.3.0'] = 'tags/phonon/4.3.0'
        self.svnTargets['4.3.1'] = 'tags/phonon/4.3.1'
        self.svnTargets['4.2'] = 'branches/phonon/4.2'
        self.svnTargets['20091111'] = 'tags/kdepim/pe5.20091111/kdesupport/phonon'
        self.svnTargets['20091123'] = 'tags/kdepim/pe5.20091123/kdesupport/phonon'
        self.svnTargets['20091201'] = 'tags/kdepim/pe5.20091201/kdesupport/phonon'
        self.svnTargets['20100101'] = 'tags/kdepim/enterprise5.0.20100101.1068602/kdesupport/phonon'
        self.svnTargets['20100115'] = 'tags/kdepim/enterprise5.0.20100115.1075215/kdesupport/phonon'
        self.svnTargets['20100122'] = 'tags/kdepim/enterprise5.0.20100122.1078631/kdesupport/phonon'
        self.svnTargets['20100129'] = 'tags/kdepim/enterprise5.0.20100129.1082020/kdesupport/phonon'
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/phonon'
        self.svnTargets['20100205'] = 'tags/kdepim/enterprise5.0.20100205.1085631/kdesupport/phonon'
        self.svnTargets['20100212'] = 'tags/kdepim/enterprise5.0.20100212.1089060/kdesupport/phonon'
        self.svnTargets['20100219'] = 'tags/kdepim/enterprise5.0.20100219.1092868/kdesupport/phonon'
        self.svnTargets['20100226'] = 'tags/kdepim/enterprise5.0.20100226.1096279/kdesupport/phonon'
        self.svnTargets['20100305'] = 'tags/kdepim/enterprise5.0.20100305.1099232/kdesupport/phonon'
        self.svnTargets['20100312'] = 'tags/kdepim/enterprise5.0.20100312.1102371/kdesupport/phonon'
        self.svnTargets['20100319'] = 'tags/kdepim/enterprise5.0.20100319.1105074/kdesupport/phonon'
        self.svnTargets['20100326'] = 'tags/kdepim/enterprise5.0.20100326.1107645/kdesupport/phonon'
        self.svnTargets['20100401'] = 'tags/kdepim/enterprise5.0.20100401.1110042/kdesupport/phonon'
        self.svnTargets['20100409'] = 'tags/kdepim/enterprise5.0.20100409.1112952/kdesupport/phonon'
        self.svnTargets['20100507'] = 'tags/kdepim/enterprise5.0.20100507.1123982/kdesupport/phonon'
        self.svnTargets['20100528'] = 'tags/kdepim/enterprise5.0.20100528.1131643/kdesupport/phonon'
        self.defaultTarget = '20100528'

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

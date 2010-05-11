import base
import utils
import sys
import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base']            = 'default'
        self.hardDependencies['libs/qt']               = 'default'
        self.hardDependencies['kdesupport/clucene-core'] = 'default'
        self.hardDependencies['win32libs-sources/redland-src']   = 'default'

    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/soprano'
        self.svnTargets['2.0.0']  = 'tags/soprano/2.0.0'
        self.svnTargets['2.0.1']  = 'tags/soprano/2.0.1'
        self.svnTargets['2.0.2']  = 'tags/soprano/2.0.2'
        self.svnTargets['2.0.3']  = 'tags/soprano/2.0.3'
        self.svnTargets['2.0.99'] = 'tags/soprano/2.0.99'
        self.svnTargets['2.1']    = 'tags/soprano/2.1'
        self.svnTargets['2.1.1']  = 'tags/soprano/2.1.1'
        self.svnTargets['2.1.64'] = 'tags/soprano/2.1.64'
        self.svnTargets['2.1.65'] = 'tags/soprano/2.1.65'
        self.svnTargets['2.1.67'] = 'tags/soprano/2.1.67'
        self.svnTargets['2.2']    = 'tags/soprano/2.2'
        self.svnTargets['2.2.1']  = 'tags/soprano/2.2.1'
        self.svnTargets['2.2.2']  = 'tags/soprano/2.2.2'
        self.svnTargets['20091111'] = 'tags/kdepim/pe5.20091111/kdesupport/soprano'
        self.svnTargets['20091123'] = 'tags/kdepim/pe5.20091123/kdesupport/soprano'
        self.svnTargets['20091201'] = 'tags/kdepim/pe5.20091201/kdesupport/soprano'
        self.svnTargets['20100101'] = 'tags/kdepim/enterprise5.0.20100101.1068602/kdesupport/soprano'
        self.svnTargets['20100115'] = 'tags/kdepim/enterprise5.0.20100115.1075215/kdesupport/soprano'
        self.svnTargets['20100122'] = 'tags/kdepim/enterprise5.0.20100122.1078631/kdesupport/soprano'
        self.svnTargets['20100129'] = 'tags/kdepim/enterprise5.0.20100129.1082020/kdesupport/soprano'
        self.svnTargets['20100205'] = 'tags/kdepim/enterprise5.0.20100205.1085631/kdesupport/soprano'
        self.svnTargets['20100212'] = 'tags/kdepim/enterprise5.0.20100212.1089060/kdesupport/soprano'
        self.svnTargets['20100219'] = 'tags/kdepim/enterprise5.0.20100219.1092868/kdesupport/soprano'
        self.svnTargets['20100226'] = 'tags/kdepim/enterprise5.0.20100226.1096279/kdesupport/soprano'
        self.svnTargets['20100305'] = 'tags/kdepim/enterprise5.0.20100305.1099232/kdesupport/soprano'
        self.svnTargets['20100312'] = 'tags/kdepim/enterprise5.0.20100312.1102371/kdesupport/soprano'
        self.svnTargets['20100319'] = 'tags/kdepim/enterprise5.0.20100319.1105074/kdesupport/soprano'
        self.svnTargets['20100326'] = 'tags/kdepim/enterprise5.0.20100326.1107645/kdesupport/soprano'
        self.svnTargets['20100401'] = 'tags/kdepim/enterprise5.0.20100401.1110042/kdesupport/soprano'
        self.svnTargets['20100409'] = 'tags/kdepim/enterprise5.0.20100409.1112952/kdesupport/soprano'
        self.svnTargets['20100507'] = 'tags/kdepim/enterprise5.0.20100507.1123982/kdesupport/soprano'
        self.defaultTarget = '20100507'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "soprano"
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if not self.buildTarget == 'svnHEAD':
            return self.doPackaging( "soprano", self.buildTarget, True )
        else:
            return self.doPackaging( "soprano", utils.cleanPackageName( sys.argv[0], "soprano" ), True )

if __name__ == '__main__':
    subclass().execute()

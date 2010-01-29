import base
import utils
import sys
import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['libs/qt'] = 'default'

    def setTargets( self ):
        self.svnTargets['0.0.5'] = 'tags/qimageblitz/0.0.5'
        self.svnTargets['20091111'] = 'tags/kdepim/pe5.20091111/kdesupport/qimageblitz'
        self.svnTargets['20091123'] = 'tags/kdepim/pe5.20091123/kdesupport/qimageblitz'
        self.svnTargets['20091201'] = 'tags/kdepim/pe5.20091201/kdesupport/qimageblitz'
        self.svnTargets['20100101'] = 'tags/kdepim/enterprise5.0.20100101.1068602/kdesupport/qimageblitz'
        self.svnTargets['20100115'] = 'tags/kdepim/enterprise5.0.20100115.1075215/kdesupport/qimageblitz'
        self.svnTargets['20100122'] = 'tags/kdepim/enterprise5.0.20100122.1078631/kdesupport/qimageblitz'
        self.svnTargets['20100129'] = 'tags/kdepim/enterprise5.0.20100129.1082020/kdesupport/qimageblitz'
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/qimageblitz'
        self.defaultTarget = '20100129'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "qimageblitz"
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        return self.doPackaging( "qimageblitz", self.buildTarget, True )

if __name__ == '__main__':
    subclass().execute()

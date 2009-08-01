import base
import utils
import sys
import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base']            = 'default'
        self.hardDependencies['libs/qt']                 = 'default'
        self.hardDependencies['kdesupport/clucene-core'] = 'default'
        #not good for 4.2 branch...
        #self.hardDependencies['win32libs-bin/redland']   = 'default'

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
        for i in ['4.3.0', '4.3.1', '4.3.2', '4.3.3', '4.3.4', '4.3']:
            self.svnTargets[ i ] = 'tags/kdesupport-for-4.3/kdesupport/soprano'
        self.defaultTarget = 'svnHEAD'

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

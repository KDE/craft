import sys
import base
import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['libs/qt'] = 'default'
        self.hardDependencies['win32libs-sources/libpng-src'] = 'default'
        self.hardDependencies['win32libs-bin/zlib'] = 'default'

    def setTargets( self ):
        self.svnTargets['0.3.9'] = 'tags/kdewin32/0.3.9'
        self.svnTargets['20091111'] = 'tags/kdepim/pe5.20091111/kdesupport/kdewin'
        self.svnTargets['20091123'] = 'tags/kdepim/pe5.20091123/kdesupport/kdewin'
        self.svnTargets['20091201'] = 'tags/kdepim/pe5.20091201/kdesupport/kdewin'
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/kdewin'
        self.defaultTarget = '20091201'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "kdewin"
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        return self.doPackaging( "kdewin", self.buildTarget, True )

if __name__ == '__main__':
    subclass().execute()

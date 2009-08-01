import base
import utils
import sys
import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['libs/qt'] = 'default'
        self.hardDependencies['kdesupport/clucene-core'] = 'default'
        self.hardDependencies['win32libs-bin/exiv2'] = 'default'
        self.hardDependencies['win32libs-bin/iconv'] = 'default'
        self.hardDependencies['win32libs-bin/libbzip2'] = 'default'
        self.hardDependencies['win32libs-bin/libxml2'] = 'default'
        self.hardDependencies['win32libs-bin/zlib'] = 'default'

    def setTargets( self ):
        self.svnTargets['0.5.7'] = 'tags/strigi/strigi/0.5.7'
        self.svnTargets['0.5.8'] = 'tags/strigi/strigi/0.5.8'
        self.svnTargets['0.5.9'] = 'tags/strigi/strigi/0.5.9'
        self.svnTargets['0.5.10'] = 'tags/strigi/strigi/0.5.10'
        self.svnTargets['0.5.11'] = 'tags/strigi/strigi/0.5.11'
        self.svnTargets['0.6.3']  = 'tags/strigi/strigi/0.6.3'
        self.svnTargets['0.6.4']  = 'tags/strigi/strigi/strigi-0.6.4'
        self.svnTargets['0.6.5']  = 'tags/strigi/strigi/0.6.5'
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/strigi'
        for i in ['4.3.0', '4.3.1', '4.3.2', '4.3.3', '4.3.4', '4.3']:
            self.svnTargets[ i ] = 'tags/kdesupport-for-4.3/kdesupport/strigi'
        self.defaultTarget = 'svnHEAD'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "strigi"
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if self.buildTarget == "svnHEAD":
            return self.doPackaging( "strigi" )
        else:
            return self.doPackaging( "strigi", self.buildTarget, True )

if __name__ == '__main__':
    subclass().execute()

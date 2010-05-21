import base
import utils
import sys
import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['libs/qt'] = 'default'
        self.hardDependencies['kdesupport/clucene-core'] = 'default'
        self.hardDependencies['win32libs-sources/exiv2-src'] = 'default'
        self.hardDependencies['win32libs-sources/libbzip2-src'] = 'default'
        self.hardDependencies['win32libs-bin/iconv'] = 'default'
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
        self.svnTargets['20091111'] = 'tags/kdepim/pe5.20091111/kdesupport/strigi'
        self.svnTargets['20091123'] = 'tags/kdepim/pe5.20091123/kdesupport/strigi'
        self.svnTargets['20091201'] = 'tags/kdepim/pe5.20091201/kdesupport/strigi'
        self.svnTargets['20100101'] = 'tags/kdepim/enterprise5.0.20100101.1068602/kdesupport/strigi'
        self.svnTargets['20100115'] = 'tags/kdepim/enterprise5.0.20100115.1075215/kdesupport/strigi'
        self.svnTargets['20100122'] = 'tags/kdepim/enterprise5.0.20100122.1078631/kdesupport/strigi'
        self.svnTargets['20100129'] = 'tags/kdepim/enterprise5.0.20100129.1082020/kdesupport/strigi'
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/strigi'
        self.svnTargets['20100205'] = 'tags/kdepim/enterprise5.0.20100205.1085631/kdesupport/strigi'
        self.svnTargets['20100212'] = 'tags/kdepim/enterprise5.0.20100212.1089060/kdesupport/strigi'
        self.svnTargets['20100219'] = 'tags/kdepim/enterprise5.0.20100219.1092868/kdesupport/strigi'
        self.svnTargets['20100226'] = 'tags/kdepim/enterprise5.0.20100226.1096279/kdesupport/strigi'
        self.svnTargets['20100305'] = 'tags/kdepim/enterprise5.0.20100305.1099232/kdesupport/strigi'
        self.svnTargets['20100312'] = 'tags/kdepim/enterprise5.0.20100312.1102371/kdesupport/strigi'
        self.svnTargets['20100319'] = 'tags/kdepim/enterprise5.0.20100319.1105074/kdesupport/strigi'
        self.svnTargets['20100326'] = 'tags/kdepim/enterprise5.0.20100326.1107645/kdesupport/strigi'
        self.svnTargets['20100401'] = 'tags/kdepim/enterprise5.0.20100401.1110042/kdesupport/strigi'
        self.svnTargets['20100409'] = 'tags/kdepim/enterprise5.0.20100409.1112952/kdesupport/strigi'
        self.svnTargets['20100507'] = 'tags/kdepim/enterprise5.0.20100507.1123982/kdesupport/strigi'
        self.svnTargets['20100521'] = 'tags/kdepim/enterprise5.0.20100521.1129114/kdesupport/strigi'
        self.defaultTarget = '20100521'

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

import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['libs/qt'] = 'default'

    def setTargets( self ):
        self.svnTargets['20100101'] = 'tags/kdepim/enterprise5.0.20100101.1068602/kdesupport/attica'
        self.svnTargets['20100115'] = 'tags/kdepim/enterprise5.0.20100115.1075215/kdesupport/attica'
        self.svnTargets['20100122'] = 'tags/kdepim/enterprise5.0.20100122.1078631/kdesupport/attica'
        self.svnTargets['20100129'] = 'tags/kdepim/enterprise5.0.20100129.1082020/kdesupport/attica'
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/attica'
        self.svnTargets['20100205'] = 'tags/kdepim/enterprise5.0.20100205.1085631/kdesupport/attica'
        self.svnTargets['20100212'] = 'tags/kdepim/enterprise5.0.20100212.1089060/kdesupport/attica'
        self.svnTargets['20100219'] = 'tags/kdepim/enterprise5.0.20100219.1092868/kdesupport/attica'
        self.svnTargets['20100226'] = 'tags/kdepim/enterprise5.0.20100226.1096279/kdesupport/attica'
        self.svnTargets['20100305'] = 'tags/kdepim/enterprise5.0.20100305.1099232/kdesupport/attica'
        self.svnTargets['20100312'] = 'tags/kdepim/enterprise5.0.20100312.1102371/kdesupport/attica'
        self.svnTargets['20100319'] = 'tags/kdepim/enterprise5.0.20100319.1105074/kdesupport/attica'
        self.svnTargets['20100326'] = 'tags/kdepim/enterprise5.0.20100326.1107645/kdesupport/attica'
        self.svnTargets['20100401'] = 'tags/kdepim/enterprise5.0.20100401.1110042/kdesupport/attica'
        self.svnTargets['20100409'] = 'tags/kdepim/enterprise5.0.20100409.1112952/kdesupport/attica'
        self.svnTargets['20100507'] = 'tags/kdepim/enterprise5.0.20100507.1123982/kdesupport/attica'
        self.svnTargets['20100528'] = 'tags/kdepim/enterprise5.0.20100528.1131643/kdesupport/attica'
        self.svnTargets['20100604'] = 'tags/kdepim/enterprise5.0.20100604.1134428/kdesupport/attica'
        self.svnTargets['20100611'] = 'tags/kdepim/enterprise5.0.20100611.1136974/kdesupport/attica'
        self.svnTargets['20100618'] = 'tags/kdepim/enterprise5.0.20100618.1139547/kdesupport/attica'
        self.svnTargets['20100625'] = 'tags/kdepim/enterprise5.0.20100625.1142603/kdesupport/attica'
        self.svnTargets['20100701'] = 'tags/kdepim/enterprise5.0.20100701.1144979/kdesupport/attica'
        self.defaultTarget = '20100701'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()

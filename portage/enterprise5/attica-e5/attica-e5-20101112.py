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
        self.svnTargets['20100709'] = 'tags/kdepim/enterprise5.0.20100709.1148001/kdesupport/attica'
        self.svnTargets['20100716'] = 'tags/kdepim/enterprise5.0.20100716.1150616/kdesupport/attica'
        self.svnTargets['20100723'] = 'tags/kdepim/enterprise5.0.20100723.1153624/kdesupport/attica'
        self.svnTargets['20100730'] = 'tags/kdepim/enterprise5.0.20100730.1157241/kdesupport/attica'
        self.svnTargets['20100805'] = 'tags/kdepim/enterprise5.0.20100805.1159431/kdesupport/attica'
        self.svnTargets['20100813'] = 'tags/kdepim/enterprise5.0.20100813.1163234/kdesupport/attica'
        self.svnTargets['20100820'] = 'tags/kdepim/enterprise5.0.20100820.1165957/kdesupport/attica'
        self.svnTargets['20100827'] = 'tags/kdepim/enterprise5.0.20100827.1168749/kdesupport/attica'
        self.svnTargets['20100903'] = 'tags/kdepim/enterprise5.0.20100903.1171282/kdesupport/attica'
        self.svnTargets['20100910'] = 'tags/kdepim/enterprise5.0.20100910.1173808/kdesupport/attica'
        self.svnTargets['20100917'] = 'tags/kdepim/enterprise5.0.20100917.1176291/kdesupport/attica'
        self.svnTargets['20100927'] = 'tags/kdepim/enterprise5.0.20100927.1180225/kdesupport/attica'
        self.svnTargets['20101001'] = 'tags/kdepim/enterprise5.0.20101001.1181557/kdesupport/attica'
        self.svnTargets['20101008'] = 'tags/kdepim/enterprise5.0.20101008.1183806/kdesupport/attica'
        self.svnTargets['20101015'] = 'tags/kdepim/enterprise5.0.20101015.1186246/kdesupport/attica'
        self.svnTargets['20101022'] = 'tags/kdepim/enterprise5.0.20101022.1188481/kdesupport/attica'
        self.svnTargets['20101029'] = 'tags/kdepim/enterprise5.0.20101029.1191061/kdesupport/attica'
        self.svnTargets['20101112'] = 'tags/kdepim/enterprise5.0.20101112.1196098/kdesupport/attica'
        self.defaultTarget = '20101112'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()

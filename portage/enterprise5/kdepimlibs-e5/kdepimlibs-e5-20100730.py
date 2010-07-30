import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['20091111'] = 'tags/kdepim/pe5.20091111/kdepimlibs'
        self.svnTargets['20091123'] = 'tags/kdepim/pe5.20091123/kdepimlibs'
        self.svnTargets['20091201'] = 'tags/kdepim/pe5.20091201/kdepimlibs'
        self.svnTargets['20100101'] = 'tags/kdepim/enterprise5.0.20100101.1068602/kdepimlibs'
        self.svnTargets['20100115'] = 'tags/kdepim/enterprise5.0.20100115.1075215/kdepimlibs'
        self.svnTargets['20100122'] = 'tags/kdepim/enterprise5.0.20100122.1078631/kdepimlibs'
        self.svnTargets['20100129'] = 'tags/kdepim/enterprise5.0.20100129.1082020/kdepimlibs'
        self.svnTargets['20100205'] = 'tags/kdepim/enterprise5.0.20100205.1085631/kdepimlibs'
        self.svnTargets['20100212'] = 'tags/kdepim/enterprise5.0.20100212.1089060/kdepimlibs'
        self.svnTargets['20100219'] = 'tags/kdepim/enterprise5.0.20100219.1092868/kdepimlibs'
        self.svnTargets['20100226'] = 'tags/kdepim/enterprise5.0.20100226.1096279/kdepimlibs'
        self.svnTargets['20100305'] = 'tags/kdepim/enterprise5.0.20100305.1099232/kdepimlibs'
        self.svnTargets['20100312'] = 'tags/kdepim/enterprise5.0.20100312.1102371/kdepimlibs'
        self.svnTargets['20100319'] = 'tags/kdepim/enterprise5.0.20100319.1105074/kdepimlibs'
        self.svnTargets['20100326'] = 'tags/kdepim/enterprise5.0.20100326.1107645/kdepimlibs'
        self.svnTargets['20100401'] = 'tags/kdepim/enterprise5.0.20100401.1110042/kdepimlibs'
        self.svnTargets['20100409'] = 'tags/kdepim/enterprise5.0.20100409.1112952/kdepimlibs'
        self.svnTargets['20100507'] = 'tags/kdepim/enterprise5.0.20100507.1123982/kdepimlibs'
        self.svnTargets['20100528'] = 'tags/kdepim/enterprise5.0.20100528.1131643/kdepimlibs'
        self.svnTargets['20100604'] = 'tags/kdepim/enterprise5.0.20100604.1134428/kdepimlibs'
        self.svnTargets['20100611'] = 'tags/kdepim/enterprise5.0.20100611.1136974/kdepimlibs'
        self.svnTargets['20100618'] = 'tags/kdepim/enterprise5.0.20100618.1139547/kdepimlibs'
        self.svnTargets['20100625'] = 'tags/kdepim/enterprise5.0.20100625.1142603/kdepimlibs'
        self.svnTargets['20100701'] = 'tags/kdepim/enterprise5.0.20100701.1144979/kdepimlibs'
        self.svnTargets['20100709'] = 'tags/kdepim/enterprise5.0.20100709.1148001/kdepimlibs'
        self.svnTargets['20100716'] = 'tags/kdepim/enterprise5.0.20100716.1150616/kdepimlibs'
        self.svnTargets['20100723'] = 'tags/kdepim/enterprise5.0.20100723.1153624/kdepimlibs'
        self.svnTargets['20100730'] = 'tags/kdepim/enterprise5.0.20100730.1157241/kdepimlibs'
        self.defaultTarget = '20100730'
    
    def setDependencies( self ):
        self.hardDependencies['enterprise5/kdelibs-e5'] = 'default'
        self.hardDependencies['enterprise5/akonadi-e5'] = 'default'
        self.hardDependencies['win32libs-sources/cyrus-sasl-src'] = 'default'
        self.hardDependencies['win32libs-sources/boost-src'] = 'default'
        self.hardDependencies['win32libs-sources/libical-src'] = 'default'
        self.hardDependencies['contributed/gpg4win-dev'] = 'default'
        if compiler.isMinGW():
            self.hardDependencies['testing/openldap-src'] = 'default'

from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()

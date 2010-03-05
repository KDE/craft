import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['20091111'] = 'tags/kdepim/pe5.20091111/kdebase/runtime'
        self.svnTargets['20091123'] = 'tags/kdepim/pe5.20091123/kdebase/runtime'
        self.svnTargets['20091201'] = 'tags/kdepim/pe5.20091201/kdebase/runtime'
        self.svnTargets['20100101'] = 'tags/kdepim/enterprise5.0.20100101.1068602/runtime'
        self.svnTargets['20100115'] = 'tags/kdepim/enterprise5.0.20100115.1075215/runtime'
        self.svnTargets['20100122'] = 'tags/kdepim/enterprise5.0.20100122.1078631/runtime'
        self.svnTargets['20100129'] = 'tags/kdepim/enterprise5.0.20100129.1082020/runtime'
        self.svnTargets['20100205'] = 'tags/kdepim/enterprise5.0.20100205.1085631/runtime'
        self.svnTargets['20100212'] = 'tags/kdepim/enterprise5.0.20100212.1089060/runtime'
        self.svnTargets['20100219'] = 'tags/kdepim/enterprise5.0.20100219.1092868/runtime'
        self.svnTargets['20100226'] = 'tags/kdepim/enterprise5.0.20100226.1096279/runtime'
        self.svnTargets['20100305'] = 'tags/kdepim/enterprise5.0.20100305.1099232/runtime'
        self.defaultTarget = '20100305'
    
    def setDependencies( self ):
        self.hardDependencies['enterprise5/kdelibs-e5'] = 'default'
        self.hardDependencies['kdesupport/oxygen-icons'] = 'default'
        self.hardDependencies['win32libs-sources/libssh-src'] = 'default'

from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()

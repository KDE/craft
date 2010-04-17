import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base']            = 'default'
        self.hardDependencies['libs/qt']                 = 'default'
        self.hardDependencies['kdesupport/clucene-core'] = 'default'
        self.hardDependencies['win32libs-bin/redland']   = 'default'

    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/soprano'
        self.svnTargets['2.0.0']  = 'tags/soprano/2.0.0'
        self.svnTargets['2.0.1']  = 'tags/soprano/2.0.1'
        self.svnTargets['2.0.2']  = 'tags/soprano/2.0.2'
        self.svnTargets['2.0.3']  = 'tags/soprano/2.0.3'
        self.svnTargets['2.0.99'] = 'tags/soprano/2.0.99'
        self.svnTargets['2.1']    = 'tags/soprano/2.1'
        self.svnTargets['2.1.1']  = 'tags/soprano/2.1.1'
        self.svnTargets['2.1.67'] = 'tags/soprano/2.1.67'
        self.svnTargets['2.2']    = 'tags/soprano/2.2'
        self.svnTargets['2.2.1']  = 'tags/soprano/2.2.1'
        self.svnTargets['2.2.2']  = 'tags/soprano/2.2.2'
        self.svnTargets['2.2.4']  = 'tags/soprano/2.2.4'
        self.svnTargets['2.3.0']  = 'tags/soprano/2.3.0'
        for i in ['4.3.0', '4.3.1', '4.3.2', '4.3.3', '4.3.4', '4.3']:
            self.svnTargets[ i ] = 'tags/kdesupport-for-4.3/kdesupport/soprano'
        for i in ['4.4.0', '4.4.1', '4.4.2', '4.4.3', '4.4.4', '4.4']:
            self.svnTargets[ i ] = 'tags/kdesupport-for-4.4/kdesupport/soprano'
        self.defaultTarget = 'svnHEAD'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines="-DSOPRANO_DISABLE_SESAME2_BACKEND=YES"

if __name__ == '__main__':
    Package().execute()

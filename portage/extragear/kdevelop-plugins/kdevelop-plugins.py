import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['master'] = ''
        self.defaultTarget = 'master'
        self.shortDescription = 'kdevelop languages and other plugins'

    def setDependencies( self ):
        self.dependencies['extragear/kdev-python'] = 'default'
        self.dependencies['extragear/kdev-ruby'] = 'default'
        self.dependencies['extragear/kdev-php'] = 'default'
        self.dependencies['extragear/kdev-qmljs'] = 'default'
#        self.dependencies['extragear/kdev-clang'] = 'default'


from Package.VirtualPackageBase import *

class Package( VirtualPackageBase ):
    def __init__( self ):
        VirtualPackageBase.__init__( self )


import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = ''
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['libs/qtbase'] = 'default'
        self.dependencies['libs/qtactiveqt'] = 'default'
        self.dependencies['libs/qtdeclarative'] = 'default'
        self.dependencies['libs/qtgraphicaleffects'] = 'default'
        self.dependencies['libs/qtimageformats'] = 'default'
        self.dependencies['libs/qtjsbackend'] = 'default'
        self.dependencies['libs/qtquick1'] = 'default'
        self.dependencies['libs/qtscript'] = 'default'
        self.dependencies['libs/qtsvg'] = 'default'
        self.dependencies['libs/qttools'] = 'default'
        self.dependencies['libs/qtwebkit'] = 'default'
        self.dependencies['libs/qtxmlpatterns'] = 'default'
        
        
        

from Package.VirtualPackageBase import *

class Package( VirtualPackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        VirtualPackageBase.__init__( self )


if __name__ == '__main__':
    Package().execute()

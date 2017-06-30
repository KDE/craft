import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

    def setDependencies( self ):
        self.dependencies['libs/qtbase'] = 'default'
        self.dependencies['libs/qtactiveqt'] = 'default'
        self.dependencies['libs/qtdeclarative'] = 'default'
        self.dependencies['libs/qtgraphicaleffects'] = 'default'
        self.dependencies['libs/qtimageformats'] = 'default'
        self.dependencies['libs/qtmultimedia'] = 'default'
        self.dependencies['libs/qtscript'] = 'default'
        self.dependencies['libs/qtsvg'] = 'default'
        self.dependencies['libs/qttools'] = 'default'
        self.dependencies['libs/qtwebkit'] = 'default'
        self.dependencies['libs/qtwebchannel'] = 'default'
        self.dependencies['libs/qtxmlpatterns'] = 'default'
        self.dependencies['libs/qtwinextras'] = 'default'
        self.dependencies['libs/qtquickcontrols'] = 'default'
        self.dependencies['libs/qtquickcontrols2'] = 'default'
        self.dependencies['libs/qtserialport'] = 'default'




from Package.VirtualPackageBase import *

class Package( VirtualPackageBase ):
    def __init__( self ):
        VirtualPackageBase.__init__( self )


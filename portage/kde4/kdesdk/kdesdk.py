import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['gitHEAD'] = ''
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        #self.dependencies['kde/cervisia'] = 'default'#only builds on unix
        self.dependencies['kde/dolphin-plugins'] = 'default'
        self.dependencies['kde/kapptemplate'] = 'default'
        self.dependencies['kde/kcachegrind'] = 'default'
#        self.dependencies['kde/kde-dev-scripts'] = 'default'
#        self.dependencies['kde/kde-dev-utils'] = 'default'
        self.dependencies['kde/kdesdk-kioslaves'] = 'default'
        self.dependencies['kde/kdesdk-strigi-analyzers'] = 'default'
        #self.dependencies['kde/kdesdk-thumbnailers'] = 'default' # only po thumbnailers which dont build
        self.dependencies['kde/kompare'] = 'default'
        self.dependencies['kde/lokalize'] = 'default'
        self.dependencies['kde/okteta'] = 'default'
        self.dependencies['kde/poxml'] = 'default'
        self.dependencies['kde/umbrello'] = 'default'

#        self.dependencies['kde/kde-baseapps'] = 'default'
#        self.dependencies['win32libs/boost'] = 'default'
        self.shortDescription = "KDE software development package (umbrello, okteta)"

from Package.VirtualPackageBase import *

class Package(VirtualPackageBase):
    def __init__( self ):
        VirtualPackageBase.__init__( self )


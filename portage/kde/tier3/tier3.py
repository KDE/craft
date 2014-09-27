import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = ''
        self.defaultTarget = 'gitHEAD'
        self.shortDescription = 'kf5 tier3'

    def setDependencies( self ):
        self.dependencies['frameworks/kactivities'] = 'default'
        self.dependencies['frameworks/kbookmarks'] = 'default'
        self.dependencies['frameworks/kcmutils'] = 'default'
        self.dependencies['frameworks/kconfigwidgets'] = 'default'
        self.dependencies['frameworks/kdeclarative'] = 'default'
        self.dependencies['frameworks/kded'] = 'default'
        self.dependencies['frameworks/kdesignerplugin'] = 'default'
        self.dependencies['frameworks/kdewebkit'] = 'default'
        self.dependencies['frameworks/kemoticons'] = 'default'
        self.dependencies['frameworks/khtml'] = 'default'
        self.dependencies['frameworks/kiconthemes'] = 'default'
        self.dependencies['frameworks/kinit'] = 'default'
        self.dependencies['frameworks/kio'] = 'default'
        self.dependencies['frameworks/kjsembed'] = 'default'
        self.dependencies['frameworks/kmediaplayer'] = 'default'
        self.dependencies['frameworks/knewstuff'] = 'default'
        self.dependencies['frameworks/knotifications'] = 'default'
        self.dependencies['frameworks/knotifyconfig'] = 'default'
        self.dependencies['frameworks/kparts'] = 'default'
        self.dependencies['frameworks/kross'] = 'default'
        self.dependencies['frameworks/krunner'] = 'default'
        self.dependencies['frameworks/kservice'] = 'default'
        self.dependencies['frameworks/ktexteditor'] = 'default'
        self.dependencies['frameworks/ktextwidgets'] = 'default'
        self.dependencies['frameworks/kwallet'] = 'default'
        self.dependencies['frameworks/kxmlgui'] = 'default'
        self.dependencies['frameworks/plasma'] = 'default'

from Package.VirtualPackageBase import *

class Package( VirtualPackageBase ):
    def __init__( self ):
        VirtualPackageBase.__init__( self )

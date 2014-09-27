import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:kdev-qmljs'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.shortDescription = "qml / javascript support for kdevelop"
        self.buildDependencies['virtual/base'] = 'default'
        # python interpreter is needed?!?
        self.buildDependencies['dev-util/gettext-tools'] = 'default'
        self.dependencies['win32libs/gettext'] = 'default'
        self.dependencies['frameworks/threadweaver'] = 'default'
        self.dependencies['kde/ktexteditor'] = 'default'
        self.dependencies['kde/kdeclarative'] = 'default'
        self.dependencies['frameworks/ki18n'] = 'default'
        self.dependencies['kde/kdelibs4support'] = 'default'
        self.dependencies['extragear/kdevplatform'] = 'default'
        self.dependencies['extragear/kdevelop'] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )


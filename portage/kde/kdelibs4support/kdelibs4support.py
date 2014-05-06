import info
import kdedefaults as kd
from EmergeConfig import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues("http://download.kde.org/unstable/frameworks/${VERSION}/kde4support-${VERSION}.tar.xz",
                                            "http://download.kde.org/unstable/frameworks/${VERSION}/kde4support-${VERSION}.tar.xz.sha1",
                                            "${PACKAGE_NAME}-${VERSION}",
                                            "[git]kde:${PACKAGE_NAME}" )
        self.shortDescription = "Porting aid from KDELibs4"

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.buildDependencies['dev-util/extra-cmake-modules'] = 'default'
        self.buildDependencies["win32libs/automoc"] = "default"
        self.dependencies['kdesupport/kdewin'] = 'default'
        self.dependencies["kde/kcompletion"] = 'default'
        self.dependencies["kde/kconfig"] = 'default'
        self.dependencies["kde/kconfigwidgets"] = 'default'
        self.dependencies["kde/kcrash"] = 'default'
        self.dependencies["kde/kdesignerplugin"] = 'default'
        self.dependencies["kde/kglobalaccel"] = 'default'
        self.dependencies["kde/kdoctools"] = 'default'
        self.dependencies["kde/kemoticons"] = 'default'
        self.dependencies["kde/kguiaddons"] = 'default'
        self.dependencies["kde/ki18n"] = 'default'
        self.dependencies["kde/kiconthemes"] = 'default'
        self.dependencies["kde/kio"] = 'default'
        self.dependencies["kde/knotifications"] = 'default'
        self.dependencies["kde/kparts"] = 'default'
        self.dependencies["kde/kservice"] = 'default'
        self.dependencies["kde/ktextwidgets"] = 'default'
        self.dependencies["kde/kunitconversion"] = 'default'
        self.dependencies["kde/kwidgetsaddons"] = 'default'
        self.dependencies["kde/kwindowsystem"] = 'default'
        self.dependencies["kde/kxmlgui"] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )

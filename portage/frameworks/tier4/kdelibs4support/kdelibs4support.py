import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( tarballUrl = "http://download.kde.org/stable/frameworks/${VERSION_MAJOR}.${VERSION_MINOR}/portingAids/${PACKAGE_NAME}-${VERSION}.tar.xz",
                                           tarballDigestUrl = "http://download.kde.org/stable/frameworks/${VERSION_MAJOR}.${VERSION_MINOR}/portingAids/${PACKAGE_NAME}-${VERSION}.tar.xz.sha1")



    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies['data/docbook-dtd42'] = 'default'
        self.runtimeDependencies['kdesupport/kdewin'] = 'default'
        self.runtimeDependencies["frameworks/kcompletion"] = 'default'
        self.runtimeDependencies["frameworks/kconfig"] = 'default'
        self.runtimeDependencies["frameworks/kconfigwidgets"] = 'default'
        self.runtimeDependencies["frameworks/kcrash"] = 'default'
        self.runtimeDependencies["frameworks/kdesignerplugin"] = 'default'
        self.runtimeDependencies["frameworks/kglobalaccel"] = 'default'
        self.runtimeDependencies['frameworks/kded'] = 'default'
        self.runtimeDependencies["frameworks/kdoctools"] = 'default'
        self.runtimeDependencies["frameworks/kemoticons"] = 'default'
        self.runtimeDependencies["frameworks/kguiaddons"] = 'default'
        self.runtimeDependencies["frameworks/ki18n"] = 'default'
        self.runtimeDependencies["frameworks/kiconthemes"] = 'default'
        self.runtimeDependencies["frameworks/kinit"] = 'default'
        self.runtimeDependencies["frameworks/kio"] = 'default'
        self.runtimeDependencies["frameworks/kitemmodels"] = 'default'
        self.runtimeDependencies["frameworks/knotifications"] = 'default'
        self.runtimeDependencies["frameworks/kparts"] = 'default'
        self.runtimeDependencies["frameworks/kservice"] = 'default'
        self.runtimeDependencies["frameworks/ktextwidgets"] = 'default'
        self.runtimeDependencies["frameworks/kunitconversion"] = 'default'
        self.runtimeDependencies["frameworks/kwidgetsaddons"] = 'default'
        self.runtimeDependencies["frameworks/kwindowsystem"] = 'default'
        self.runtimeDependencies["frameworks/kxmlgui"] = 'default'


from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )
        # this package is currently not portable due to hardcoded paths in the kdewin defines
        self.subinfo.options.package.disableBinaryCache = True


    


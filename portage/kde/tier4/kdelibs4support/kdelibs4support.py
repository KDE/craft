import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )


    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.dependencies['data/docbook-dtd42'] = 'default'
        self.dependencies['kdesupport/kdewin'] = 'default'
        self.dependencies["kde/kcompletion"] = 'default'
        self.dependencies["frameworks/kconfig"] = 'default'
        self.dependencies["frameworks/kconfigwidgets"] = 'default'
        self.dependencies["kde/kcrash"] = 'default'
        self.dependencies["kde/kdesignerplugin"] = 'default'
        self.dependencies["frameworks/kglobalaccel"] = 'default'
        self.dependencies["kde/kdoctools"] = 'default'
        self.dependencies["kde/kemoticons"] = 'default'
        self.dependencies["frameworks/kguiaddons"] = 'default'
        self.dependencies["frameworks/ki18n"] = 'default'
        self.dependencies["kde/kiconthemes"] = 'default'
        self.dependencies["kde/kinit"] = 'default'
        self.dependencies["kde/kio"] = 'default'
        self.dependencies["frameworks/kitemmodels"] = 'default'
        self.dependencies["kde/knotifications"] = 'default'
        self.dependencies["kde/kparts"] = 'default'
        self.dependencies["kde/kservice"] = 'default'
        self.dependencies["kde/ktextwidgets"] = 'default'
        self.dependencies["kde/kunitconversion"] = 'default'
        self.dependencies["frameworks/kwidgetsaddons"] = 'default'
        self.dependencies["frameworks/kwindowsystem"] = 'default'
        self.dependencies["kde/kxmlgui"] = 'default'


from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


    


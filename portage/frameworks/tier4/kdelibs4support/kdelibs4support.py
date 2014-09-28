import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )


    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.dependencies['data/docbook-dtd42'] = 'default'
        self.dependencies['kdesupport/kdewin'] = 'default'
        self.dependencies["frameworks/kcompletion"] = 'default'
        self.dependencies["frameworks/kconfig"] = 'default'
        self.dependencies["frameworks/kconfigwidgets"] = 'default'
        self.dependencies["frameworks/kcrash"] = 'default'
        self.dependencies["frameworks/kdesignerplugin"] = 'default'
        self.dependencies["frameworks/kglobalaccel"] = 'default'
        self.dependencies["frameworks/kdoctools"] = 'default'
        self.dependencies["frameworks/kemoticons"] = 'default'
        self.dependencies["frameworks/kguiaddons"] = 'default'
        self.dependencies["frameworks/ki18n"] = 'default'
        self.dependencies["frameworks/kiconthemes"] = 'default'
        self.dependencies["frameworks/kinit"] = 'default'
        self.dependencies["frameworks/kio"] = 'default'
        self.dependencies["frameworks/kitemmodels"] = 'default'
        self.dependencies["frameworks/knotifications"] = 'default'
        self.dependencies["frameworks/kparts"] = 'default'
        self.dependencies["frameworks/kservice"] = 'default'
        self.dependencies["frameworks/ktextwidgets"] = 'default'
        self.dependencies["frameworks/kunitconversion"] = 'default'
        self.dependencies["frameworks/kwidgetsaddons"] = 'default'
        self.dependencies["frameworks/kwindowsystem"] = 'default'
        self.dependencies["frameworks/kxmlgui"] = 'default'


from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


    


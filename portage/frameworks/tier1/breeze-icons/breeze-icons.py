import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = "Breeze icon theme."

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

        self.subinfo.options.configure.args = " -DBINARY_ICONS_RESOURCE=ON"

    def install(self):
        if OsUtils.isWin() or OsUtils.isMac():
            dest = os.path.join(self.installDir(), "bin", "data")
            if not os.path.exists(dest):
                os.makedirs(dest)
            utils.copyFile(os.path.join(self.buildDir(), "icons", "breeze-icons.rcc"),
                           os.path.join(dest, "icontheme.rcc"))
            return True
        else:
            return CMakePackageBase.install(self)

#
# copyright (c) 2012 Hannah von Reth <vonreth@kde.org>
#
# definitions for the qt5 modules

from BuildSystem.QMakeBuildSystem import *
from CraftStandardDirs import CraftStandardDirs


class Qt5CoreBuildSystem(QMakeBuildSystem):
    def __init__(self):
        QMakeBuildSystem.__init__(self)

    def install(self, options=""):
        """implements the make step for Qt projects"""
        imageDir = self.imageDir()
        # Since 5.9.3 we don't apply the patch to Qt anymore which would accept a absolute path
        if self.qtVer >= CraftVersion("5.9.3") or CraftCore.settings.getboolean("QtSDK", "Enabled", False):
            if os.path.splitdrive(imageDir)[0] == os.path.splitdrive(self.buildDir())[0]:
                imageDir = os.path.splitdrive(imageDir)[1]
        options += f" INSTALL_ROOT={imageDir} install"
        if not QMakeBuildSystem.install(self, options):
            return False

        self._fixInstallPrefix()

        if OsUtils.isWin():
            if os.path.exists(os.path.join(self.installDir(), "bin", "mkspecs")):
                utils.moveFile(os.path.join(self.installDir(), "bin", "mkspecs"),
                               os.path.join(self.installDir(), "mkspecs"))
        return True

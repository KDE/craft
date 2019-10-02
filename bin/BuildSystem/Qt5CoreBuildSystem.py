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
        options += f" INSTALL_ROOT={os.path.splitdrive(self.imageDir())[1]} " + self.makeOptions(self.subinfo.options.install.args)
        if not QMakeBuildSystem.install(self, options):
            return False
        self._fixInstallPrefix()

        if OsUtils.isWin():
            if os.path.exists(os.path.join(self.installDir(), "bin", "mkspecs")):
                utils.moveFile(os.path.join(self.installDir(), "bin", "mkspecs"),
                               os.path.join(self.installDir(), "mkspecs"))
        return True

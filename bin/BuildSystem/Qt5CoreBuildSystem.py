#
# copyright (c) 2012 Hannah von Reth <vonreth@kde.org>
#
# definitions for the qt5 modules

from BuildSystem.QMakeBuildSystem import *


class Qt5CoreBuildSystem(QMakeBuildSystem):
    def __init__(self):
        QMakeBuildSystem.__init__(self)

    def install(self, options=""):
        """implements the make step for Qt projects"""
        imageDir = self.imageDir()
        if craftSettings.getboolean("QtSDK", "Enabled", False):
            if os.path.splitdrive(imageDir)[0] == os.path.splitdrive(self.buildDir())[0]:
                imageDir = imageDir[2:]
        options += f" INSTALL_ROOT={imageDir} install"
        if not QMakeBuildSystem.install(self, options):
            return False
        if OsUtils.isWin():
            badPrefix = os.path.join(self.installDir(), CraftStandardDirs.craftRoot()[3:])
        else:
            badPrefix = os.path.join(self.installDir(), CraftStandardDirs.craftRoot()[1:])
        if os.path.exists(badPrefix) and not os.path.samefile(self.installDir(), badPrefix):
            utils.mergeTree(badPrefix, self.installDir())
        if craftSettings.getboolean("QtSDK", "Enabled", False):
            qtDir = os.path.join(craftSettings.get("QtSDK", "Path"), craftSettings.get("QtSDK", "Version"),
                                 craftSettings.get("QtSDK", "Compiler"))
            # drop the drive letter and the first slash [3:]
            path = os.path.join(self.installDir(), qtDir[3:])
            if os.path.exists(path):
                utils.mergeTree(path, self.installDir())
                utils.rmtree(os.path.join(self.installDir(), craftSettings.get("QtSDK", "Path")[3:]))

        if OsUtils.isWin():
            if os.path.exists(os.path.join(self.installDir(), "bin", "mkspecs")):
                utils.moveFile(os.path.join(self.installDir(), "bin", "mkspecs"),
                               os.path.join(self.installDir(), "mkspecs"))
        return True

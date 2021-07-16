#
# copyright (c) 2012 Hannah von Reth <vonreth@kde.org>
#
# definitions for the qt5 modules

from BuildSystem.QMakeBuildSystem import *
from CraftStandardDirs import CraftStandardDirs


class Qt5CoreBuildSystem(QMakeBuildSystem):
    def __init__(self):
        QMakeBuildSystem.__init__(self)
        self.subinfo.options.dynamic.registerOption("featureArguments", Arguments(), permanent=False)


    def _qtCoreEnv(self):
        env = {}
        if CraftCore.compiler.isMacOS:
            # we need mac's version of libtool here
            env["PATH"] = os.pathsep.join(["/usr/bin/", os.environ["PATH"]])
        return env

    def configure(self, configureDefines=""):
        # not using  QMakeBuildSystem.configure here due to the special way of passing feature arguments
        # for Qt's configure system in modules other than qtbase
        self.enterBuildDir()
        args = ["qmake", "-makefile", self.configureSourceDir(), self.configureOptions(configureDefines)]
        if self.subinfo.options.dynamic.featureArguments:
            args += ["--", self.subinfo.options.dynamic.featureArguments]
        with utils.ScopedEnv(self._qtCoreEnv()):
            return utils.system(Arguments(args))

    def make(self):
        with utils.ScopedEnv(self._qtCoreEnv()):
            return super().make()

    def install(self, options=""):
        """implements the make step for Qt projects"""
        with utils.ScopedEnv(self._qtCoreEnv()):
            options = Arguments([options, f"INSTALL_ROOT={os.path.splitdrive(self.imageDir())[1]}"])
            if not super().install(options):
                return False
            self._fixInstallPrefix()

            if OsUtils.isWin():
                if os.path.exists(os.path.join(self.installDir(), "bin", "mkspecs")):
                    utils.moveFile(os.path.join(self.installDir(), "bin", "mkspecs"),
                                os.path.join(self.installDir(), "mkspecs"))
            return True

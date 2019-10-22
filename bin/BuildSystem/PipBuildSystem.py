import shutil

from BuildSystem.BuildSystemBase import *


class PipBuildSystem(BuildSystemBase):
    def __init__(self):
        BuildSystemBase.__init__(self, "pip")
        self.python2 = True
        self.python3 = True


    def _getPython2(self):
        if CraftPackageObject.get("dev-utils/python2").isInstalled:
            return "python2"
        python2 = CraftCore.cache.findApplication("python2.7")
        if CraftCore.compiler.isWindows:
                if not python2 and ("Paths", "PYTHON27") in CraftCore.settings:
                    python2 = CraftCore.cache.findApplication("python", CraftCore.settings.get("Paths", "PYTHON27"))
        if not python2:
            CraftCore.log.critical(f"Please have a look on {CraftCore.settings.iniPath} and make sure that\n"
                                   "\t[Paths]\n"
                                   "\tPYTHON27\n"
                                   "Points to a valid Python installation.")
            return None
        return python2

    def _getPython3(self):
        if CraftPackageObject.get("dev-utils/python3").isInstalled:
            return "python3"
        return sys.executable

    @property
    def _pythons(self):
        pythons = []
        if self.python2:
            pythons.append(("2", self._getPython2()))
        if self.python3:
            pythons.append(("3", self._getPython3()))
        return pythons

    def venvDir(self, ver):
        return Path(CraftCore.standardDirs.etcDir()) / "virtualenv" / ver

    def make(self):
        if self.subinfo.svnTarget():
            for ver, python in self._pythons:
                if not utils.system([python, "setup.py", "sdist"], cwd=self.sourceDir()):
                    return False
        return True

    def install(self):
        ok = True
        for ver, python in self._pythons:
            command = [python, "-m", "pip", "install", "--upgrade"]
            if not self.venvDir(ver).exists():
                command += ["--user"]
            if self.subinfo.svnTarget():
                command += ["-e", self.sourceDir()]
            else:
                command += [self.package.name]
            ok = ok and utils.system(command)
        return ok

    def runTest(self):
        return False

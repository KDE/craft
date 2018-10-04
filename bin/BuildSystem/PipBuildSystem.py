import shutil

from BuildSystem.BuildSystemBase import *


class PipBuildSystem(BuildSystemBase):
    def __init__(self):
        BuildSystemBase.__init__(self, "pip")
        self.python2 = True
        self.python3 = True

    def configure(self):
        return True

    def make(self):
        return True

    def install(self):
        ok = True

        pythons = {}  # dict: major version -> path
        if self.python2 and ("Paths", "PYTHON27") in CraftCore.settings:
            pythons[2] = CraftCore.settings.get("Paths", "PYTHON27")
        if self.python3:
            pythons[3] = CraftCore.settings.get("Paths", "PYTHON")

        args = []

        for pythonMajorVersion, pythonPath in pythons.items():
            for app, path in [("pip", os.path.join(pythonPath, "Scripts")),
                              (f"pip{pythonMajorVersion}", pythonPath),
                              ("pip", pythonPath)]:
                if not path.endswith(os.path.sep):
                    path += os.path.sep
                CraftCore.log.debug(f"Looking for {app} in {path}")
                pipExe = shutil.which(app, path=path)
                if pipExe:
                    break

            if not pipExe:
                CraftCore.log.warning(
                    "Could not find 'pip' executable for Python install: {0}, skipping install".format(pythonPath))
                return False

            command = [pipExe, "install", "--upgrade"] + args + [self.package.name]
            ok = ok and utils.system(command)
        return ok

    def runTest(self):
        return False

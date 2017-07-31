from CraftDebug import craftDebug
from BuildSystem.BuildSystemBase import *

import shutil


class PipBuildSystem(BuildSystemBase):
    def __init__(self):
        BuildSystemBase.__init__(self, "pip")
        self.python2 = True
        self.python3 = True
        self.allowExternal = False

    def configure(self):
        return True

    def make(self):
        return True

    def install(self):
        ok = True

        pythons = {}  # dict: major version -> path
        if self.python2 and ("Paths", "PYTHON27") in craftSettings:
            pythons[2] = craftSettings.get("Paths", "PYTHON27")
        if self.python3:
            pythons[3] = craftSettings.get("Paths", "PYTHON")

        args = ""
        if self.allowExternal:
            args += " --allow-all-external "

        for pythonMajorVersion, pythonPath in pythons.items():
            pipExe = shutil.which("pip", path=os.path.join(pythonPath, "Scripts"))
            if not pipExe:
                pipExe = shutil.which("pip%s" % pythonMajorVersion,
                                      path=pythonPath)  # Unix systems may append the major version to the name
            if not pipExe:
                pipExe = shutil.which("pip", path=pythonPath)  # Chocolatey installs pip.exe next to python.exe

            if not pipExe:
                craftDebug.log.warning(
                    "Could not find 'pip' executable for Python install: {0}, skipping install".format(pythonPath))
                return False

            command = "\"%s\" install --upgrade %s %s" % (pipExe, args, self.subinfo.package)
            ok = ok and utils.system(command)
        return ok

    def runTest(self):
        return False

import EmergeDebug
from BuildSystem.BuildSystemBase import *

class PipBuildSystem(BuildSystemBase):
    def __init__( self):
        BuildSystemBase.__init__(self, "pip")
        self.python2 = True
        self.python3 = True
        self.allowExternal = False

    def configure( self ):
        return True

    def make( self ):
        return True

    def install( self ):
        ok = True
        pythons = []
        if self.python2 and ("Paths","PYTHON27") in emergeSettings:
            pythons.append(emergeSettings.get("Paths","PYTHON27"))
        if self.python3:
            pythons.append(emergeSettings.get("Paths","PYTHON"))

        args = ""
        if self.allowExternal:
            args += " --allow-all-external "
        for path in pythons:
            pipExe = os.path.join(path, "Scripts", "pip.exe")
            if not os.path.exists(pipExe):
                pipExe = os.path.join(path, "pip.exe") # Chocolatey installs pip.exe next to python.exe

            command = "\"%s\" install --upgrade %s %s" % (pipExe, args, self.subinfo.package)
            ok = ok and utils.system(command)
        return ok


    def runTest( self ):
        return False

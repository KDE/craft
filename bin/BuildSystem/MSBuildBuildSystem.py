from BuildSystem.BuildSystemBase import *


class MSBuildBuildSystem(BuildSystemBase):
    def __init__(self):
        BuildSystemBase.__init__(self, "msbuild")
        self.msbuildTargets = ["Rebuild"]
        self.buildTypes = {"Release" : "Release", "RelWithDebInfo" : "Release", "Debug" : "Debug" }

    def configure(self, defines=""):
        return True

    def make(self):
        self.enterSourceDir()
        buildType =self.buildTypes[self.buildType()]
        defines = self.subinfo.options.configure.args or ""
        for target in self.msbuildTargets:
            if not utils.system(f"msbuild /m /t:{target} \"{self.subinfo.options.configure.projectFile}\""
                                f" /p:Configuration={buildType}"
                                f" /tv:{CraftCore.compiler.getInternalVersion()}.0 /property:PlatformToolset=v{CraftCore.compiler.getMsvcPlatformToolset()}"
                                f" {defines}"):
                return False
        return True

    def install(self, buildDirs=None, installHeaders=True):
        if not buildDirs:
            buildDirs = [self.sourceDir()]

        self.cleanImage()

        for dir in ["bin", "lib", "include"]:
            if not os.path.exists(os.path.join(self.installDir(), dir)):
                os.makedirs(os.path.join(self.installDir(), dir))

        for dir in buildDirs:
            for root, dirs, files in os.walk(dir):
                for f in files:
                    path = os.path.join(root, f)
                    if f.endswith((".pdb", ".lib")):
                        utils.copyFile(path, os.path.join(self.imageDir(), "lib", f), linkOnly=False)
                    elif f.endswith((".dll", ".exe")):
                        utils.copyFile(path, os.path.join(self.imageDir(), "bin", f), linkOnly=False)
                    elif installHeaders and f.endswith(".h"):
                        utils.copyFile(path, os.path.join(self.imageDir(), "include", f), linkOnly=False)
        return True

    def unittest(self):
        return True

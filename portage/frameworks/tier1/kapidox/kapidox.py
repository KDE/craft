from CraftDebug import craftDebug
import info
import shutil


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "Scripts and data for building API documentation (dox) in a standard format and style."
        

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/cmake"] = "default"
        self.runtimeDependencies["dev-util/doxygen"] = "default"
        self.runtimeDependencies["python-modules/pyyaml"] = "default"
        self.runtimeDependencies["python-modules/jinja2"] = "default"
        self.runtimeDependencies["python-modules/doxyqml"] = "default"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )
        #the shims are not portable
        self.subinfo.options.package.disableBinaryCache = True

        if not ("Paths","Python27") in craftSettings:
            craftDebug.log.critical("Please make sure Paths/Python27 is set in your kdesettings.ini")

        # this program needs python 2.7
        pythonPath = shutil.which("python", path=craftSettings.get("Paths","PYTHON27",""))
        if pythonPath:
            self.subinfo.options.configure.defines = " -DPYTHON_EXECUTABLE=%s" % pythonPath.replace("\\","/")

    def configure(self):
        if not ("Paths","Python27") in craftSettings:
            craftDebug.log.critical("Please make sure Paths/Python27 is set in your kdesettings.ini")
        return CMakeBuildSystem.configure(self)
    
    def install(self):
        if not CMakeBuildSystem.install(self):
            return False
        python = os.path.join(craftSettings.get("Paths","PYTHON27"), "python.exe")
        binPath = os.path.join(self.imageDir(), "bin")
        for script in ["depdiagram-generate", "depdiagram-generate-all", "depdiagram-prepare", "kapidox_generate"]:
            if not utils.createShim(os.path.join(binPath, f"{script}.exe"),
                                    python,
                                    args=os.path.join(CraftStandardDirs.craftRoot(), "Scripts", script),
                                    useAbsolutePath=True):
                return False
        return True

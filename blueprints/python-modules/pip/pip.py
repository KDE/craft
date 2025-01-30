import io
import subprocess

import info
import utils
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = ""
        self.defaultTarget = "master"

    def setDependencies(self):
        self.buildDependencies["core/cacert"] = None
        self.buildDependencies["python-modules/virtualenv"] = None


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def make(self):
        for ver, python in self._pythons:
            # if its installed we get the help text if not we get an empty string
            with io.StringIO() as tmp:
                utils.system([python, "-m", "pip"], stdout=tmp, stderr=subprocess.DEVNULL)
                if tmp.getvalue():
                    return True

                if not utils.system([python, "-m", "ensurepip"]):
                    return False
        return True

    def install(self):
        if not CraftCore.compiler.isWindows:
            return super.install()

        # Run "pip install pip" to install the lateste version
        # We can't use the install step from PipBuildSystem,
        # because installing pip itself causes issues when --prefix is used
        # See https://github.com/pypa/pip/issues/11349
        # TODO: re-evaluate when we use a newer python in libs/python
        command = [
            python,
            "-m",
            "pip",
            "install",
            "--upgrade",
            "--upgrade-strategy",
            "only-if-needed",
            "pip"
        ]

        return utils.system(command)

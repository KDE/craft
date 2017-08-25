import io

import info
import shells
from Package.MaybeVirtualPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        ver = "20161025"
        arch = "i686"
        if craftCompiler.isX64():
            arch = "x86_64"
        # don't set an actual version  instead of base. Msys must be manually updated so doing a craft update of msys wil break things.
        self.targets["base"] = f"http://repo.msys2.org/distrib/{arch}/msys2-base-{arch}-{ver}.tar.xz"
        self.defaultTarget = "base"

    def setDependencies(self):
        self.runtimeDependencies["virtual/bin-base"] = "default"
        self.runtimeDependencies["dev-util/python3"] = "default"

    def msysInstallShim(self, installDir):
        return utils.createShim(os.path.join(installDir, "dev-utils", "bin", "msys.exe"),
                                os.path.join(installDir, "dev-utils", "bin", "python3.exe"),
                                args=os.path.join(CraftStandardDirs.craftBin(), "shells.py"))


from Package.BinaryPackageBase import *


class MsysPackage(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
        self.shell = shells.BashShell()

    def install(self):
        if craftCompiler.isX64():
            utils.copyDir(os.path.join(self.sourceDir(), "msys64"), os.path.join(self.installDir(), "msys"))
        else:
            utils.copyDir(os.path.join(self.sourceDir(), "msys32"), os.path.join(self.installDir(), "msys"))
        return True

    def qmerge(self):
        if not self.subinfo.msysInstallShim(self.installDir()):
            return False
        if not BinaryPackageBase.qmerge(self):
            return False
        msysDir = os.path.join(CraftStandardDirs.craftRoot(), "msys")
        # start and restart msys before first use
        if not self.shell.execute(".", "echo Firstrun") and utils.system("autorebase.bat", cwd=msysDir):
            return False

        def queryForUpdate():
            out = io.BytesIO()
            if not self.shell.execute(".", "pacman -Sy --noconfirm --force"):
                raise Exception()
            self.shell.execute(".", "pacman -Qu --noconfirm", out=out, err=subprocess.PIPE)
            out = out.getvalue()
            return out != b""

        try:
            while queryForUpdate():
                if not self.shell.execute(".", "pacman -Su --noconfirm --force") and \
                        utils.system("autorebase.bat", cwd=msysDir):
                    return False
        except Exception as e:
            print(e)
            return False
        return (self.shell.execute(".", "pacman -S base-devel --noconfirm --force --needed") and
                utils.system("autorebase.bat", cwd=msysDir))


class VirtualPackage(VirtualPackageBase):
    def __init__(self):
        VirtualPackageBase.__init__(self)

    def install(self):
        if not VirtualPackageBase.install(self):
            return False
        return self.subinfo.msysInstallShim(self.installDir())


class Package(MaybeVirtualPackageBase):
    def __init__(self):
        self.skipCondition = ("Paths", "Msys") not in craftSettings
        MaybeVirtualPackageBase.__init__(self, condition=self.skipCondition, classA=MsysPackage, classB=VirtualPackage)

        if not self.skipCondition:
            # override the install method
            def install():
                craftDebug.log.info(f"Using manually installed msys {CraftStandardDirs.msysDir()}")
                return self.baseClass.install(self)

            setattr(self, "install", install)

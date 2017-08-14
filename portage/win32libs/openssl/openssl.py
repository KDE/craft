import info


class subinfo(info.infoclass):
    def setTargets(self):
        def addTarget(baseUrl, ver):
            self.targets[ver] = f'{baseUrl}openssl-{ver}.tar.gz'
            self.targetInstSrc[ver] = f'openssl-{ver}'
            self.targetDigestUrls[ver] = ([f'{baseUrl}openssl-{ver}.tar.gz.sha256'], CraftHash.HashAlgorithm.SHA256)

        # older versions  -> inside old/major.minor.patch/
        for ver in ['1.0.2a', '1.0.2c', '1.0.2d', '1.0.2j']:
            dir = re.search(r"\d+\.\d+.\d+", ver).group(0)
            baseUrl = f'ftp://ftp.openssl.org/source/old/{dir}/'
            addTarget(baseUrl, ver)

        # latest versions -> inside source/
        for ver in ["1.1.0d"]:
            baseUrl = 'ftp://ftp.openssl.org/source/'
            addTarget(baseUrl, ver)

        self.description = "The OpenSSL runtime environment"

        self.defaultTarget = '1.0.2j'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/perl"] = "default"
        if craftCompiler.isMinGW():
            self.buildDependencies["dev-util/msys"] = "default"
            self.runtimeDependencies["win32libs/zlib"] = "default"
        elif craftCompiler.isMSVC():
            self.buildDependencies["dev-util/nasm"] = "default"


from Package.CMakePackageBase import *


class PackageCMake(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.staticBuild = False

    def compile(self):
        os.chdir(self.sourceDir())
        cmd = ""
        if craftCompiler.isX64():
            config = "VC-WIN64A"
        else:
            config = "VC-WIN32"

        if not self.system("perl Configure %s" % config, "configure"):
            return False

        if craftCompiler.isX64():
            if not self.system("ms\do_win64a.bat", "configure"):
                return False
        else:
            if not self.system("ms\do_nasm.bat", "configure"):
                return False

        if self.staticBuild:
            cmd = r"nmake -f ms\nt.mak"
        else:
            cmd = r"nmake -f ms\ntdll.mak"

        return self.system(cmd)

    def install(self):
        src = self.sourceDir()
        dst = self.imageDir()

        if not os.path.isdir(dst):
            os.mkdir(dst)
        if not os.path.isdir(os.path.join(dst, "bin")):
            os.mkdir(os.path.join(dst, "bin"))
        if not os.path.isdir(os.path.join(dst, "lib")):
            os.mkdir(os.path.join(dst, "lib"))
        if not os.path.isdir(os.path.join(dst, "include")):
            os.mkdir(os.path.join(dst, "include"))

        if self.staticBuild:
            outdir = "out32"
        else:
            outdir = "out32dll"

        if not self.staticBuild:
            shutil.copy(os.path.join(src, outdir, "libeay32.dll"), os.path.join(dst, "bin"))
            shutil.copy(os.path.join(src, outdir, "ssleay32.dll"), os.path.join(dst, "bin"))
        shutil.copy(os.path.join(src, outdir, "libeay32.lib"), os.path.join(dst, "lib"))
        shutil.copy(os.path.join(src, outdir, "ssleay32.lib"), os.path.join(dst, "lib"))
        utils.copyDir(os.path.join(src, "inc32"), os.path.join(dst, "include"))

        return True


from Package.AutoToolsPackageBase import *


class PackageMSys(AutoToolsPackageBase):
    def __init__(self):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.make.supportsMultijob = False
        self.subinfo.options.package.packageName = 'openssl'
        self.subinfo.options.package.packSources = False
        if craftCompiler.isX64():
            self.platform = "mingw64"
        else:
            self.platform = "mingw"
        self.supportsCCACHE = False

        self.subinfo.options.useShadowBuild = False

        # target install needs perl with native path on configure time
        self.subinfo.options.configure.args = " shared zlib-dynamic enable-camellia enable-idea enable-mdc2 enable-tlsext enable-rfc3779"

    def make(self, dummyBuildType=None):
        return self.shell.execute(self.sourceDir(), self.makeProgram, "depend") and \
               AutoToolsPackageBase.make(self, dummyBuildType)

    def install(self):
        self.enterSourceDir()
        self.shell.execute(self.sourceDir(), self.makeProgram,
                           "INSTALLTOP=%s install_sw" % (self.shell.toNativePath(self.imageDir())))
        self.shell.execute(os.path.join(self.imageDir(), "lib"), "chmod", "-R 664 .")
        self.shell.execute(os.path.join(self.imageDir(), "lib", "engines"), "chmod", " -R 755 .")
        self.shell.execute(os.path.join(self.imageDir(), "bin"), "chmod", " -R 755 .")
        shutil.move(os.path.join(self.imageDir(), "lib", "libcrypto.dll.a"),
                    os.path.join(self.imageDir(), "lib", "libeay32.dll.a"))
        shutil.move(os.path.join(self.imageDir(), "lib", "libssl.dll.a"),
                    os.path.join(self.imageDir(), "lib", "ssleay32.dll.a"))
        return True


if craftCompiler.isMinGW():
    class Package(PackageMSys):
        pass
else:
    class Package(PackageCMake):
        pass

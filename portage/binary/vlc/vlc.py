import shutil

import info
from Package.BinaryPackageBase import *


class subinfo(info.infoclass):
    vlc_ver = None

    def setTargets(self):
        vlcArch = "32"
        if craftCompiler.isX64():
            vlcArch = "64"
        vlcBaseUrl = "http://nightlies.videolan.org/build/win" + vlcArch + "/last/"
        vlcTagName = "3.0.0"

        for ver in utils.utilsCache.getNightlyVersionsFromUrl(vlcBaseUrl, r"\d\d\d\d\d\d\d\d-\d\d\d\d"):
            self.targets[vlcTagName + "-git"] = "%svlc-%s-%s-git-win%s.7z" % (vlcBaseUrl, vlcTagName, ver, vlcArch)
            self.targetInstSrc[vlcTagName + "-git"] = "vlc-%s-git" % (vlcTagName)
            self.patchToApply[vlcTagName + "-git"] = [("vlc-2.1.5.diff", 1)]

            self.targets[vlcTagName + "-debug-git"] = "%s/vlc-%s-%s-git-win%s-debug.7z" % (
            vlcBaseUrl, vlcTagName, ver, vlcArch)
            self.targetInstSrc[vlcTagName + "-debug-git"] = "vlc-%s-git" % (vlcTagName)
            self.patchToApply[vlcTagName + "-debug-git"] = [("vlc-2.1.5.diff", 1)]

        for releaseTag in ["2.2.0", "2.2.1", "2.2.4", "2.2.6"]:
            self.targets[releaseTag] = "http://download.videolan.org/pub/videolan/vlc/%s/win%s/vlc-%s-win%s.7z" % (
            releaseTag, vlcArch, releaseTag, vlcArch)
            self.targetInstSrc[releaseTag] = "vlc-" + releaseTag
            self.targetDigestUrls[
                releaseTag] = "http://download.videolan.org/pub/videolan/vlc/%s/win%s/vlc-%s-win%s.7z.sha1" % (
            releaseTag, vlcArch, releaseTag, vlcArch)
            self.patchToApply[releaseTag] = [("vlc-2.1.5.diff", 1)]
        self.description = "an open-source multimedia framework"

        self.defaultTarget = "2.2.6"

    def setDependencies(self):
        self.buildDependencies["virtual/bin-base"] = "default"


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.package.packageName = "vlc"
        self.subinfo.options.package.packSources = False

    def install(self):
        utils.copyDir(self.sourceDir(), os.path.join(self.installDir(), "bin"))
        if craftCompiler.isMinGW():
            utils.deleteFile(os.path.join(self.installDir(), "bin", "libgcc_s_seh-1.dll"))
        shutil.move(os.path.join(self.installDir(), "bin", "sdk", "include"),
                    os.path.join(self.installDir(), "include"))
        shutil.move(os.path.join(self.installDir(), "bin", "sdk", "lib"), os.path.join(self.installDir(), "lib"))
        ver2 = self.subinfo.buildTarget.split(".")
        if not (int(ver2[0]) >= 2 and int(ver2[0]) >= 1):
            utils.copyFile(os.path.join(self.installDir(), "lib", "libvlc.dll.a"),
                           os.path.join(self.installDir(), "lib", "libvlc.lib"))
            utils.copyFile(os.path.join(self.installDir(), "lib", "libvlccore.dll.a"),
                           os.path.join(self.installDir(), "lib", "libvlccore.lib"))
        shutil.rmtree(os.path.join(self.installDir(), "bin", "sdk"))
        os.makedirs(os.path.join(self.installDir(), "share", "applications"))
        utils.copyFile(os.path.join(self.packageDir(), "vlc.desktop"),
                       os.path.join(self.installDir(), "share", "applications", "vlc.desktop"))
        return True

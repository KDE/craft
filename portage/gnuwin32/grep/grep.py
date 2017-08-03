import info


class subinfo(info.infoclass):
    def setTargets(self):
        for t in ('2.5.1a', '2.5.4'):
            self.targets[t] = ["http://downloads.sourceforge.net/sourceforge/gnuwin32/grep-%s-bin.zip" % t,
                               "http://downloads.sourceforge.net/sourceforge/gnuwin32/grep-%s-dep.zip" % t]
            self.targetInstallPath[t] = "dev-utils"
        self.targetDigests['2.5.4'] = ['56f41d351b3ed8ac671df4dd3bbd4c4d3b9190a2',
                                       '6dc3a0d1a1751c731fb680a01650a1396c76648c']
        self.defaultTarget = '2.5.4'

    def setDependencies(self):
        self.runtimeDependencies["virtual/bin-base"] = "default"


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def install(self):
        if not BinaryPackageBase.install(self):
            return False

        manifestDir = os.path.join(self.imageDir(), "manifest")
        if os.path.exists(manifestDir):
            for file in os.listdir(manifestDir):
                if file.endswith('.mft'):
                    os.remove(os.path.join(manifestDir, file))
        return True

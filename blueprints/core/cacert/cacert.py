import info

def find_all(path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            result.append(os.path.join(root, name))
    return result

class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2023-01-10", "2023-12-12"]:
            self.targets[ver] = f"https://files.kde.org/craft/curl.haxx.se/cacert-{ver}.zip"
            self.targetInstallPath[ver] = "etc/certs"
        self.targetDigests["2023-01-10"] = (
            ["d31764d1cf86e457199e820d5f0880933e6b0058afa7b5db19f8a526a6634a18"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.targetDigests["2023-12-12"] = (
            ["e7d3215c9e1273056e7beea4f84d2c7b22b22ff0b15c5c88ce2e3f857e6a45ea"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.webpage = "https://curl.haxx.se/docs/caextract.html"
        self.defaultTarget = "2023-12-12"


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.package.disableBinaryCache = True

    def fetch(self):
        with utils.ScopedEnv({"SSL_CERT_FILE": None, "REQUESTS_CA_BUNDLE": None}):
            return super().fetch()

    def qmerge(self, dbOnly=False):
        if not super().qmerge(dbOnly):
            return False

        etcDir = CraftCore.standardDirs.etcDir()
        certsDir = os.path.join(etcDir, 'certs')
        cacertFile = os.path.join(etcDir, 'cacert.pem')
        filenames = find_all(certsDir)
        with open(cacertFile, 'w') as outfile:
            for fname in filenames:
                CraftCore.debug.trace("Adding content of '%s' to '%s'" % (fname, cacertFile))
                with open(fname) as infile:
                    outfile.write(infile.read())
        return True

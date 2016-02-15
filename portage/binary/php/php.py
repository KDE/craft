# -*- coding: utf-8 -*-
import tempfile

import info
import utils


class subinfo(info.infoclass):
    def setTargets( self ):
        ver = "7.0.3"
        self.targets[ver]  ="http://windows.php.net/downloads/releases/php-%s-Win32-VC14-%s.zip" % (ver, compiler.architecture())
        self.targetDigestUrls[ver] = ("http://windows.php.net/downloads/releases/sha1sum.txt", EmergeHash.HashAlgorithm.SHA1)

        self.defaultTarget = ver

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.merge.destinationPath = "dev-utils/php";
        self.subinfo.options.merge.ignoreBuildType = True

    def install( self ):
        if not BinaryPackageBase.install(self):
            return False
        # TODO: ouch
        with open(os.path.join( self.installDir(), "php.ini-development"), "rt+") as ini:
            with open(os.path.join( self.installDir(), "php.ini"), "wt+") as out:
                ext_dir = re.compile("^; extension_dir = \"ext\".*$")
                curl = re.compile("^;extension=php_curl.dll.*$")
                for line in ini:
                    if ext_dir.match(line) :
                        line = "extension_dir = \"ext\"\n"
                    elif curl.match(line):
                        line = "extension=php_curl.dll\n"
                    out.write(line)
        return True

    def qmerge(self):
        if not BinaryPackageBase.qmerge(self):
            return False
        utils.createBat(os.path.join(self.rootdir,"dev-utils","bin","php.bat"), "%s %%*" % os.path.join( EmergeStandardDirs.emergeRoot(), "dev-utils", "php", "php.exe" ))
        return True


#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
# Packager base

import io

from CraftBase import *

from Utils import CraftHash
from Utils.CraftManifest import *

from CraftDebug import deprecated


class PackagerBase(CraftBase):
    """ provides a generic interface for packagers and implements basic package creating stuff """

    @InitGuard.init_once
    def __init__(self):
        CraftBase.__init__(self)
        self.whitelist_file = []
        self.blacklist_file = []
        self.defines = {}
        self.ignoredPackages = []

    def preArchive(self):
        utils.abstract()

    def archiveDir(self):
        return os.path.join(self.buildRoot(), "archive")

    def symbolsDir(self):
        """return absolute path to the symbol directory in imageDir
        """
        return os.path.join(self.imageDir(), 'symbols')

    @property
    def isDebugSymbolDumpingEnabled(self):
        return CraftCore.settings.getboolean("Packager", "DebugSymbolDumping", False)

    # """ create a package """
    def createPackage(self):
        utils.abstract()

    def internalPostInstall(self):
        if not super().internalPostInstall():
            return False

        if self.isDebugSymbolDumpingEnabled:
            for root, dirs, files in os.walk(self.imageDir()):
                for file in files:
                    if self.isBinary(file):
                        self._dumpSymbols(file)

        return True

    # Loosely based on https://chromium.googlesource.com/chromium/chromium/+/34599b0bf7a14ab21a04483c46ecd9b5eaf86704/components/breakpad/tools/generate_breakpad_symbols.py#92
    def _dumpSymbols(self, binaryFile):
        CraftCore.log.debug('%s: dump symbols' % binaryFile)

        with io.BytesIO() as out:
            utils.system(['dump_syms', binaryFile], stdout=out)

            outBytes = out.getvalue()
            firstLine = str(outBytes.splitlines()[0], 'utf-8')
            CraftCore.log.debug('Module line: %s' % firstLine)
            regex = "^MODULE [^ ]+ [^ ]+ ([0-9aA-fF]+) (.*)"
            CraftCore.log.debug('regex: %s' % regex)
            moduleLine = re.match(regex, firstLine)
            CraftCore.log.debug('regex: %s' % moduleLine)
            outputPath = os.path.join(self.symbolsDir(), moduleLine.group(2),
                                 moduleLine.group(1))

            utils.createDirectory(outputPath)

            symbolFileBasename = moduleLine.group(2).replace(".pdb", "")
            symbolFile = os.path.join(outputPath, "%s.sym" % symbolFileBasename)

            with open(symbolFile, 'wb') as outputFile:
                outputFile.write(outBytes)

            CraftCore.log.debug('%s: written symbol dump to: %s' % (binaryFile, symbolFile))



    def _generateManifest(self, destDir, archiveName, manifestLocation=None, manifestUrls=None):
        if not manifestLocation:
            manifestLocation = destDir
        manifestLocation = os.path.join(manifestLocation, "manifest.json")
        archiveFile = os.path.join(destDir, archiveName)

        name = archiveName if not os.path.isabs(archiveName) else os.path.relpath(archiveName, destDir)

        manifest = CraftManifest.load(manifestLocation, urls=manifestUrls)
        entry = manifest.get(str(self))
        entry.addFile(name, CraftHash.digestFile(archiveFile, CraftHash.HashAlgorithm.SHA256), version=self.version)

        manifest.dump(manifestLocation)

    @property
    def shortcuts(self) -> []:
        """ Return a list of shortcuts we want installe"""
        out = []
        if "shortcuts" in self.defines:
            out  += self.defines["shortcuts"]
        return out



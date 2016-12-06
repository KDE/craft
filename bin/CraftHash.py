from enum import Enum
import os
import hashlib
import re

from CraftDebug import craftDebug


class HashAlgorithm(Enum):
    SHA1 = 1
    SHA224 = 2
    SHA256 = 3
    SHA512 = 4
    MD5 = 5  # deprecated

    def stringPrefix(self):
        return "[%s]" % self.name

    def fileEnding(self):
        return "." + self.name.lower()

    @classmethod
    def fileEndings(cls):
        out = dict()
        for _, val in cls.__members__.items():
            out[val] = val.fileEnding()
        return out

    @classmethod
    def getAlgorithmFromFile(cls, file):
        _, ext = os.path.splitext()
        return cls.__getattr__(ext[1:].upper())

    @classmethod
    def getAlgorithmFromPrefix(cls, hash):
        for alg in re.findall("\[.*\]", hash):
            return cls.__getattr__(alg[1:-1])
        return None


def digestFile(filepath, algorithm=HashAlgorithm.SHA256):
    """ digests a file """
    blockSize = 65536
    with open(filepath, "rb") as hashFile:
        hash = getattr(hashlib, algorithm.name.lower())()
        buffer = hashFile.read(blockSize)
        while len(buffer) > 0:
            hash.update(buffer)
            buffer = hashFile.read(blockSize)
        return hash.hexdigest()


def checkFilesDigests(downloaddir, filenames, digests=None, digestAlgorithm=HashAlgorithm.SHA1):
    """check digest of (multiple) files specified by 'filenames' from 'downloaddir'"""
    if type(digests) == list:
        digestList = digests
    else:
        digestList = [digests]

    for digests, filename in zip(digestList, filenames):
        craftDebug.log.debug("checking digest of: %s" % filename)
        pathName = os.path.join(downloaddir, filename)
        if digests == None:
            for digestAlgorithm, digestFileEnding in HashAlgorithm.fileEndings().items():
                digestFileName = pathName + digestFileEnding
                if not os.path.exists(digestFileName):
                    digestFileName, _ = os.path.splitext(pathName)
                    digestFileName += digestFileEnding
                    if not os.path.exists(digestFileName):
                        continue
                currentHash = digestFile(pathName, digestAlgorithm)
                with open(digestFileName, "rt+") as f:
                    data = f.read()
                if not re.findall(currentHash, data):
                    craftDebug.log.error("%s hash for file %s (%s) does not match (%s)" % (
                    digestAlgorithm.name, pathName, currentHash, data))
                    return False
                    # digest provided in digests parameter
        else:
            currentHash = digestFile(pathName, digestAlgorithm)
            if len(digests) != len(currentHash) or digests.find(currentHash) == -1:
                craftDebug.log.error("%s hash for file %s (%s) does not match (%s)" % (
                digestAlgorithm.name, pathName, currentHash, digests))
                return False
    return True


def createDigestFiles(path, algorithms=None):
    """creates a sha1 diget file"""
    if algorithms == None:
        algorithms = HashAlgorithm.__members__.values()
    for algorithm in algorithms:
        digets = digestFile(path, algorithm)
        with open(path + algorithm.fileEnding(), "wt+") as f:
            f.write("%s\n" % digets)


def printFilesDigests(downloaddir, filenames, buildTarget, algorithm=HashAlgorithm.SHA256):
    out = ""
    for filename in filenames:
        if not filename == "":
            out += "'%s'," % digestFile(os.path.join(downloaddir, filename), algorithm)
    if not out == "":
        print("self.targetDigests['%s'] = ([%s], CraftHash.%s)" % (buildTarget, out[:-1], algorithm))


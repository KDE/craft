import hashlib
import os
import re
from enum import Enum

from CraftCore import CraftCore


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
        _, ext = os.path.splitext(file)
        return cls.__getitem__(ext[1:].upper())

    @classmethod
    def getAlgorithmFromPrefix(cls, hash):
        for alg in re.findall(r"\[.*\]", hash):
            return cls.__getitem__(alg[1:-1])
        return None


def digestString(string: str, algorithm=HashAlgorithm.SHA256) -> str:
    hash = getattr(hashlib, algorithm.name.lower())()
    hash.update(bytes(string, "UTF-8"))
    return hash.hexdigest()


def digestFile(filepath, algorithm=HashAlgorithm.SHA256):
    """digests a file"""
    blockSize = 65536
    hash = getattr(hashlib, algorithm.name.lower())()
    if os.path.islink(filepath):
        hash.update(os.readlink(filepath).encode("utf-8"))
    else:
        with open(filepath, "rb") as hashFile:
            buffer = hashFile.read(blockSize)
            while len(buffer) > 0:
                hash.update(buffer)
                buffer = hashFile.read(blockSize)
    return hash.hexdigest()


def checkFilesDigests(downloaddir, filenames, digests=None, digestAlgorithm=HashAlgorithm.SHA1):
    """check digest of (multiple) files specified by 'filenames' from 'downloaddir'"""
    if isinstance(digests, list):
        digestList = digests
    else:
        digestList = [digests]

    for digests, filename in zip(digestList, filenames):
        pathName = os.path.join(downloaddir, filename)
        CraftCore.log.debug(f"checking digest of: {pathName}")
        if digests is None:
            for (
                digestAlgorithm,
                digestFileEnding,
            ) in HashAlgorithm.fileEndings().items():
                digestFileName = pathName + digestFileEnding
                if not os.path.exists(digestFileName):
                    digestFileName, _ = os.path.splitext(pathName)
                    digestFileName += digestFileEnding
                    if not os.path.exists(digestFileName):
                        continue
                currentHash = digestFile(pathName, digestAlgorithm)
                try:
                    with open(digestFileName, "rt", encoding="UTF-8") as f:
                        data = f.read()
                except UnicodeDecodeError:
                    with open(digestFileName, "rb") as f:
                        CraftCore.log.error(f"Failed to decode digests file {digestFileName}: {f.read(100)}...")
                    return False
                if not re.findall(currentHash, data):
                    CraftCore.log.error("%s hash for file %s (%s) does not match (%s)" % (digestAlgorithm.name, pathName, currentHash, data))
                    return False
                    # digest provided in digests parameter
        else:
            currentHash = digestFile(pathName, digestAlgorithm)
            if len(digests) != len(currentHash) or digests.find(currentHash) == -1:
                CraftCore.log.error("%s hash for file %s (%s) does not match (%s)" % (digestAlgorithm.name, pathName, currentHash, digests))
                return False
    return True


def createDigestFiles(path, algorithms=None):
    """creates a sha1 diget file"""
    if algorithms is None:
        algorithms = [HashAlgorithm.SHA256]
    for algorithm in algorithms:
        digets = digestFile(path, algorithm)
        with open(str(path) + algorithm.fileEnding(), "wt", encoding="UTF-8") as f:
            f.write("%s\n" % digets)


def printFilesDigests(downloaddir, filenames, buildTarget, algorithm=HashAlgorithm.SHA256):
    digests = []
    for filename in filenames:
        if not filename == "":
            digests.append(digestFile(os.path.join(downloaddir, filename), algorithm))
    if digests:
        CraftCore.log.info(f"Digests for {buildTarget}: ({digests}, CraftHash.{algorithm})")

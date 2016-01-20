import os
import sys
import unittest
import random
import tempfile
import contextlib
import io
import collections
import EmergeHash
import EmergeDebug
import EmergeTestBase

class EmergeHashTest(EmergeTestBase.EmergeTestBase):

    def setUp(self):
        super().setUp()
        random.seed(42)
        data = ""
        for i in range(0, 1000):
            data += str(random.random())
        self.tmpDir = tempfile.TemporaryDirectory()
        #self.tmpDir = collections.namedtuple("tmp", ["name"])
        #self.tmpDir.name = "R:/tmp"
        self.tmpFile = os.path.join(self.tmpDir.name, "tmpFile")
        with open(self.tmpFile, "wt+") as tmpFIle:
            tmpFIle.write(data)


    def tearDown(self):
        del self.tmpDir
        super().tearDown()


    def hashTest(self, hash, algorithm):
        path, name = os.path.split(self.tmpFile)
        self.assertEquals(EmergeHash.checkFilesDigests(path, [name], hash, algorithm), True)


class TestAPI(EmergeHashTest):

    def test_MD5(self):
        self.hashTest("953700da7dfea74714b08f8a7cf69151", EmergeHash.HashAlgorithm.MD5)

    def test_SHA1(self):
        self.hashTest("25f0187fc5e189518dc489bcc97daa93973d7d1e", EmergeHash.HashAlgorithm.SHA1)

    def test_SHA224(self):
        self.hashTest("deef4b9f1cf9e7bdfa34ba05521740a7fdf3e1570b704a3d4088cec2", EmergeHash.HashAlgorithm.SHA224)

    def test_SHA256(self):
        self.hashTest("4fc1e96dc5ecf625efe228fce1b0964b6302cfa4d4fb2bb8d16c665d23f6ff30", EmergeHash.HashAlgorithm.SHA256)

    def test_SHA512(self):
        self.hashTest(
            "70f8f3087b51217d16e860915a06a5208eb51fb2264c10815d395feb834f63cc28fb9abed6c681b7475fbfb3dcd1afc713b16789ea951d27ab34e8d637cc27f4",
            EmergeHash.HashAlgorithm.SHA512)

    def test_printFilesDigests(self):
        path, name = os.path.split(self.tmpFile)
        log = io.StringIO()
        with contextlib.redirect_stdout(log):
            EmergeHash.printFilesDigests(path, [name], "test", EmergeHash.HashAlgorithm.SHA256)
        self.assertEquals("self.targetDigests['test'] = (['4fc1e96dc5ecf625efe228fce1b0964b6302cfa4d4fb2bb8d16c665d23f6ff30'], EmergeHash.HashAlgorithm.SHA256)\n",
                          log.getvalue())

    def test_createDigestFiles(self):
        # TODO: check file content
        EmergeHash.createDigestFiles(self.tmpFile)
        for algorithms in EmergeHash.HashAlgorithm.__members__.values():
            self.assertEquals(os.path.exists(self.tmpFile + algorithms.fileEnding()), True)
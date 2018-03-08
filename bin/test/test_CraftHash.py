import io
import os
import random
import tempfile

import CraftTestBase
from CraftCore import CraftCore
from Utils import CraftHash


class CraftHashTest(CraftTestBase.CraftTestBase):
    def setUp(self):
        super().setUp()
        random.seed(42)
        data = ""
        for i in range(0, 1000):
            data += str(random.random())
        self.tmpDir = tempfile.TemporaryDirectory()
        # self.tmpDir = collections.namedtuple("tmp", ["name"])
        # self.tmpDir.name = "R:/tmp"
        self.tmpFile = os.path.join(self.tmpDir.name, "tmpFile")
        with open(self.tmpFile, "wt+") as tmpFIle:
            tmpFIle.write(data)

    def tearDown(self):
        del self.tmpDir
        super().tearDown()

    def hashTest(self, hash, algorithm):
        path, name = os.path.split(self.tmpFile)
        self.assertEquals(CraftHash.checkFilesDigests(path, [name], hash, algorithm), True)


class TestAPI(CraftHashTest):
    def test_MD5(self):
        self.hashTest("953700da7dfea74714b08f8a7cf69151", CraftHash.HashAlgorithm.MD5)

    def test_SHA1(self):
        self.hashTest("25f0187fc5e189518dc489bcc97daa93973d7d1e", CraftHash.HashAlgorithm.SHA1)

    def test_SHA224(self):
        self.hashTest("deef4b9f1cf9e7bdfa34ba05521740a7fdf3e1570b704a3d4088cec2", CraftHash.HashAlgorithm.SHA224)

    def test_SHA256(self):
        self.hashTest("4fc1e96dc5ecf625efe228fce1b0964b6302cfa4d4fb2bb8d16c665d23f6ff30",
                      CraftHash.HashAlgorithm.SHA256)

    def test_SHA512(self):
        self.hashTest(
            "70f8f3087b51217d16e860915a06a5208eb51fb2264c10815d395feb834f63cc28fb9abed6c681b7475fbfb3dcd1afc713b16789ea951d27ab34e8d637cc27f4",
            CraftHash.HashAlgorithm.SHA512)

    def test_printFilesDigests(self):
        path, name = os.path.split(self.tmpFile)
        log = io.StringIO()
        oldLog = CraftCore.debug._handler.stream
        CraftCore.debug._handler.stream = log
        CraftHash.printFilesDigests(path, [name], "test", CraftHash.HashAlgorithm.SHA256)
        self.assertEquals(
            "Digests for test: (['4fc1e96dc5ecf625efe228fce1b0964b6302cfa4d4fb2bb8d16c665d23f6ff30'], CraftHash.HashAlgorithm.SHA256)\n", log.getvalue())
        CraftCore.debug._handler.stream = oldLog

    def test_createDigestFiles(self):
        # TODO: check file content
        algorithms = CraftHash.HashAlgorithm.__members__.values()
        CraftHash.createDigestFiles(self.tmpFile, algorithms=algorithms)
        for algorithm in algorithms:
            self.assertEquals(os.path.exists(self.tmpFile + algorithm.fileEnding()), True)


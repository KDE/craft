import os
import sys
import unittest
import random
import tempfile
import contextlib
import importlib

import EmergeDebug
import EmergeTestBase
import EmergeConfig
import portage

class EmergeHashTest(EmergeTestBase.EmergeTestBase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()


    def portageTest(self, compiler, architecture):
        EmergeConfig.emergeSettings.set("General", "KDECOMPILER", compiler)
        EmergeConfig.emergeSettings.set("General", "Architecture", architecture)

        importlib.reload(portage)#clear cache
        installable = portage.PortageInstance.getInstallables()
        for _p in installable:
            portage.PortageInstance.getPackageInstance( _p.category, _p.package)



class TestAPI(EmergeHashTest):

    def test_mingw_x86(self):
        self.portageTest("mingw4", "x86")

    def test_mingw_x64(self):
        self.portageTest("mingw4", "x64")

    def test_msvc2015_x86(self):
        self.portageTest("msvc2015", "x86")

    def test_msvc2015_x64(self):
        self.portageTest("msvc2015", "x64")

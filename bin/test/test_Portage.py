import os
import sys
import unittest
import random
import tempfile
import contextlib
import importlib

import CraftDebug
import CraftTestBase
import CraftConfig
import portage

class CraftPortageTest(CraftTestBase.CraftTestBase):

    def portageTest(self, compiler, architecture):
        CraftConfig.craftSettings.set("General", "KDECOMPILER", compiler)
        CraftConfig.craftSettings.set("General", "Architecture", architecture)

        importlib.reload(portage)#clear cache
        installable = portage.PortageInstance.getInstallables()
        for _p in installable:
            portage.PortageInstance.getPackageInstance( _p.category, _p.package)



class TestAPI(CraftPortageTest):

    def test_mingw_x86(self):
        self.portageTest("mingw4", "x86")

    def test_mingw_x64(self):
        self.portageTest("mingw4", "x64")

    def test_msvc2015_x86(self):
        self.portageTest("msvc2015", "x86")

    def test_msvc2015_x64(self):
        self.portageTest("msvc2015", "x64")

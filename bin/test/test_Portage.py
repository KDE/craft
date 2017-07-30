import os
import sys
import unittest
import random
import tempfile
import contextlib
import importlib

from CraftDebug import craftDebug
import CraftTestBase
import CraftConfig
import portage

class CraftPortageTest(CraftTestBase.CraftTestBase):

    def portageTest(self, compiler):
        CraftConfig.craftSettings.set("General", "ABI", compiler)

        importlib.reload(portage)#clear cache
        installable = portage.PortageInstance.getInstallables()
        for _p in installable:
            portage.PortageInstance.getPackageInstance( _p.category, _p.package)



class TestAPI(CraftPortageTest):

    def test_mingw_x86(self):
        self.portageTest("windows-mingw_86-gcc")

    def test_mingw_x64(self):
        self.portageTest("windows-mingw_64-gcc")

    def test_msvc2015_x86(self):
        self.portageTest("windows-msvc2015_86-cl")

    def test_msvc2015_x64(self):
        self.portageTest("windows-msvc2015_64-cl")

# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2023 Julius Künzel <jk.kdedev@smartlab.uber.space>

import io
import os
from pathlib import Path

import utils
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore
from Source.SourceBase import SourceBase


class DirSource(SourceBase):
    """existing directory as source"""

    def __init__(self, package: CraftPackageObject):
        CraftCore.debug.trace("DirSource.__init__ called")
        super().__init__(package=package)

    def sourceDir(self, dummyIndex=0) -> Path:
        if ("ContinuousIntegration", "SourceDir") in CraftCore.settings:
            CraftCore.log.warning(
                "WARNING: [ContinuousIntegration]SourceDir and the --src-dir option are deprecated and will soon be removed. Use the srcDir option of a blueprint instead eg. --options myapp.srcDir=/path/to/source"
            )
            srcPath = Path(CraftCore.settings.get("ContinuousIntegration", "SourceDir"))
        else:
            srcPath = Path(self.subinfo.options.dynamic.srcDir)

        if not srcPath.is_absolute():
            CraftCore.log.error("Error: Please provide an absolute path as source dir")
            return None
        return srcPath

    def sourceRevision(self):
        CraftCore.debug.trace("DirSource.sourceRevision called")
        if os.path.exists(self.sourceDir() / ".git"):
            with io.StringIO() as tmp:
                if utils.system(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=self.sourceDir(), stdout=tmp):
                    return tmp.getvalue().strip()
        return "latest"

    def fetch(self):
        CraftCore.debug.trace("DirSource.fetch called")
        return True

    def unpack(self):
        CraftCore.debug.trace("DirSource.unpack called")
        self.enterBuildDir()

        CraftCore.log.debug(f"cleaning {self.buildDir()}")
        self.cleanBuild()

        return True

    def getUrls(self):
        CraftCore.debug.printOut(f"No remote URL using dir from srcDir option: {self.sourceDir()}")
        return True

    def createPatch(self):
        CraftCore.log.error("DirSource does not support creating patches.")
        return False

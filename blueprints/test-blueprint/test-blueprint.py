# -*- coding: utf-8 -*-
# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2023 Julius Künzel <jk.kdedev@smartlab.uber.space>

import info
from CraftCore import CraftCore
from Package.VirtualPackageBase import VirtualPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "This blueprint is made to be used by craft's automated tests only"

    def registerOptions(self):
        self.options.dynamic.registerOption("name", "Something")
        self.options.dynamic.registerOption("thetruth", False)


class Package(VirtualPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def make(self):
        CraftCore.log.warning("This blueprint does nothing. It is designed to be used by the automated tests only.")
        return True

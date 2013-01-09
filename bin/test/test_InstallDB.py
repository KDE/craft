#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 by Intevation GmbH
# All rights reserved.
#
# Authors:
# Andre Heinecke <aheinecke@intevation.de>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of Intevation GmbH nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#


""" Functional tests for InstallDB """

import os
import sys
import unittest

test_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(test_dir, os.pardir))
os.environ["KDEROOT"] = test_dir

import InstallDB

tmp_dir = os.path.join(test_dir, "tmp")

class DatabaseTest(unittest.TestCase):

    def setUp(self):
        if not os.path.isdir(tmp_dir):
            os.mkdir(tmp_dir)
        self.db = InstallDB.InstallDB(os.path.join(tmp_dir, "test.db"))

    def tearDown(self):
        os.remove(os.path.join(tmp_dir, "test.db"))
        os.rmdir(tmp_dir)

class TestAPI(DatabaseTest):

    def test_addInstalled(self):
        package = self.db.addInstalled( 'win32libs', 'dbus-src', '1.4.0', 'release' )
        package.addFiles( dict().fromkeys( [ 'test', 'test1', 'test2' ], 'empty hash' ) )
        package.install()
        self.assertEquals( self.db.isInstalled( 'win32libs', 'dbus-src', '1.4.0',
            'release'), True)

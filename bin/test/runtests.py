#!/usr/bin/env python3
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

"""
Main entry point for the craft test suite.

Just run this file as a python script to execute all tests
"""
import sys

# enable warnings
if not sys.warnoptions:
    import os
    import warnings

    warnings.simplefilter("default")  # Change the filter in this process
    os.environ["PYTHONWARNINGS"] = "default"  # Also affect subprocesses

import optparse
import os
import platform
import unittest

xml_report = True
try:
    import xmlrunner
except ImportError:
    xml_report = False


def fallbackTestAbi():
    if os.name == "posix":
        if platform.system() == "Darwin":
            return "macos-clang-x86_64"
        elif platform.system() == "FreeBSD":
            return "freebsd-gcc-x86_64"
        else:
            return "linux-gcc-x86_64"
    else:
        return "windows-cl-msvc2019-x86_64"


thisdir = os.path.dirname(__file__)
sys.path.append(os.path.join(thisdir, os.pardir))

# allow fallback to settings template
os.environ["CRAFT_TEST"] = "True"
# also set fallback ABI for that case
if "CRAFT_TEST_ABI" not in os.environ:
    os.environ["CRAFT_TEST_ABI"] = fallbackTestAbi()
from CraftCore import CraftCore


def main():
    """Run all the tests in the craft test suite"""

    parser = optparse.OptionParser(epilog='A "JUnitTestResults.xml" file will be generated (only) if unittest-xml-reporting is installed.')
    parser.set_defaults(verbosity=1)
    parser.add_option("-v", "--verbose", action="store_const", const=3, dest="verbosity")
    parser.add_option("-t", "--target", action="store", dest="target", default=None)
    parser.add_option("--blueprint-root", action="store", dest="blueprintRoot", default=None)
    opts, rest = parser.parse_args()

    CraftCore.debug.setVerbose(opts.verbosity)
    os.environ["CRAFT_TEST_VERBOSITY"] = str(opts.verbosity)
    if opts.blueprintRoot:
        os.environ["CRAFT_TEST_BLUEPRINTS_ROOT"] = opts.blueprintRoot

    loader = unittest.TestLoader()
    if not opts.target:
        suite = loader.discover(start_dir=thisdir)
    else:
        suite = loader.loadTestsFromName(opts.target)
    if xml_report:
        with open("JUnitTestResults.xml", "wb") as output:
            runner = xmlrunner.XMLTestRunner(verbosity=opts.verbosity + 1, output=output)
            result = runner.run(suite)
    else:
        runner = unittest.TextTestRunner(verbosity=opts.verbosity + 1)
        result = runner.run(suite)

    sys.exit(not result.wasSuccessful())


if __name__ == "__main__":
    main()

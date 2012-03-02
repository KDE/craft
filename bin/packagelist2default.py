#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2010, Intevation GmbH
# All rights reserved.
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
"""Tool to convert packagelists as used by the emerge server into
   default targets for a branch.

   Use with care as it will override the default targets in the source
   files. And will indiscriminately overwrite the default targets
   for all conditions!

   This is a temporary solution to reproduce buildserver builds
   without using the emerge server
"""
__author__  = "Andre Heinecke <aheinecke@intevation.de>"
__license__ = "New-style BSD"

import getopt
import os
import sys
import re

#Calculate the portage root relative to the directory of this script
PORTAGE_ROOT=os.path.join(os.path.dirname(sys.argv[0]), "..", "portage")

DEFAULT_TARGET_RE = re.compile(r"(\s*self\.defaultTarget.*\s*=\s*)(.*)\s*$")

def traverse(directory, whitelist = lambda f: True):
    '''
        Traverse through a directory tree and return every
        dirname and filename that the function whitelist returns as true
    '''
    dirs = [ directory ]
    while dirs:
        mypath = dirs.pop()
        for f in os.listdir(mypath):
            f = os.path.join(mypath, f)
            if os.path.isdir(f):
                dirs.append(f)
            elif os.path.isfile(f) and whitelist(f):
                yield f

def findPortage(category, package):
    pdir = os.path.join(PORTAGE_ROOT, category)
    candidate = None
    for fname in traverse(pdir, lambda f: f.endswith("py") and \
            os.path.basename(f).startswith(package)):
        if candidate == None:
            candidate = fname
        else:
            # take the exact match first
            if os.path.join(pdir, package) == os.path.dirname(fname):
                candidate = fname
    if not candidate:
        print("Could not find portage file for %s %s\n\
Looking in %s" % (category, package, pdir), file=sys.stderr)
        sys.exit(1)
    return candidate

def setDefaultTarget(line):
    category, package, target, patchlevel = line.split(",")
    if target== "" or None:
        return
    portage_file_name = findPortage(category, package)

    output = ""
    with open(portage_file_name, "r") as portage_file:
        for l in portage_file.readlines(True):
            match = DEFAULT_TARGET_RE.match(l)
            if not match:
                output += l
                continue
            current_default = \
                    match.groups()[1].replace('"', '').replace("'", "")
            output += l.replace(current_default, target)
    with open(portage_file_name, "w") as portage_file:
        portage_file.write(output)

def main():
    if len(sys.argv) != 2:
        print("usage: packagelist2default.py <packagelist>", file=sys.stderr)
        sys.exit(1)

    packagelist = sys.argv[1]
    if not os.path.isfile(packagelist):
        print("Error no such file: %s " % packagelist, file=sys.stderr)
        sys.exit(1)

    with open(packagelist, "r") as plptr:
        for line in plptr.readlines():
            if line.startswith("#") or not len(line.strip()):
                continue
            else:
                setDefaultTarget(line)

if __name__ == '__main__':
    main()

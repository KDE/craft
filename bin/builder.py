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

"""Emerge tends to die at the first error it finds. If you look
   at the dependencies graph you'll see that many parts of the
   system are independent and are able to be build independent.
   If we made an unattended long running clean build we does not
   want Emerge to die that fast. We want to build as much as possible
   like the way 'make -k' works. We _really_ want this kind of
   builds to grantee that a given svn revision builds cleanly from
   stretch.

   $ python bin\builder.py enterprise5/kdepim-e5 >> control.log 2>&1

   implements this functionality. 
"""   

__author__  = "Sascha L. Teichmann <sascha.teichmann@intevation.de>"
__license__ = "New-style BSD"

import getopt
import os.path
import sys

import portage

from dependencies import DependenciesTree

DEFAULT_COMMAND = "python %s %%(category)s/%%(package)s" % \
    os.path.join(os.getenv("KDEROOT", os.curdir), "bin", "emerge.py")

class Builder(object):

    def __init__(self, command, tries = 1):
        self.command       = command
        self.tries         = tries
        self.build_status  = {}

    def recursiveBuild(self, node):

        name = str(node)
        try:
            return self.build_status[name]
        except KeyError:
            pass

        all_okay = True

        # build the children
        for child in node.children:
            okay = self.recursiveBuild(child)
            if not okay: all_okay = False

        # only build node if all of its children are built correctly
        if all_okay:
            for t in range(self.tries):
                exit_status = os.system(self.command % {
                    'category': node.category,
                    'package' : node.package,
                    'version' : node.version,
                    'tag'     : node.tag })
                if exit_status == 0: break
            all_okay = exit_status == 0

        self.build_status[name] = all_okay
        return all_okay

    def build(self, dep_tree):
        for root in dep_tree.roots:
            self.recursiveBuild(root)

def main():
    try:
        opts, args = getopt.getopt(
            sys.argv[1:], "c:t:", ["command=", "tries="])
    except getopt.GetoptError, err:
        print >> sys.stderr, str(err)
        sys.exit(1)

    if len(args) < 1:
        print >> sys.stderr, "missing package"
        sys.exit(1)

    command = DEFAULT_COMMAND

    tries = 1

    for o, a in opts:
        if o in ("-c", "--command"):
            command = a
        elif o in ("-t", "--tries"):
            tries = max(1, abs(int(a)))

    packageList, categoryList = portage.getPackagesCategories(args[0])

    dep_tree = DependenciesTree()

    for category, package in zip(categoryList, packageList):
        dep_tree.addDependencies(category, package)

    builder = Builder(command, tries)

    builder.build(dep_tree)

if __name__ == '__main__':
    main()

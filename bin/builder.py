#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# copyright 2010 by Intevation GmbH

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
__license__ = "GNU General Public License (GPL)"

import getopt
import os.path
import sys

import portage

from dependencies import DependenciesTree

DEFAULT_COMMAND = "python %s %%(category)s/%%(package)s" % \
    os.path.join(os.getenv("KDEROOT", os.curdir), "bin", "emerge.py")

class Builder(object):

    def __init__(self, command):
        self.command       = command
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
            exit_status = os.system(self.command % {
                'category': node.category,
                'package' : node.package,
                'version' : node.version,
                'tag'     : node.tag })
            all_okay = exit_status == 0

        self.build_status[name] = all_okay
        return all_okay

    def build(self, dep_tree):
        for root in dep_tree.roots:
            self.recursiveBuild(root)

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "c:", ["command="])
    except getopt.GetoptError, err:
        print >> sys.stderr, str(err)
        sys.exit(1)

    if len(args) < 1:
        print >> sys.stderr, "missing package"
        sys.exit(1)

    command = DEFAULT_COMMAND

    for o, a in opts:
        if o in ("-c", "--command"):
            command = a

    packageList, categoryList = portage.getPackagesCategories(args[0])

    dep_tree = DependenciesTree()

    for category, package in zip(categoryList, packageList):
        dep_tree.addDependencies(category, package)

    builder = Builder(command)

    builder.build(dep_tree)

if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
# Copyright Hannah von Reth <vonreth@kde.org>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

from CraftCore import CraftCore
from Blueprints.CraftPackageObject import *
from options import *

def resolvePackage(packageNames : [str], version : str=None) -> [CraftPackageObject]:
    package = CraftPackageObject(None)
    def resolveChildren(child):
        if child.isCategory():
            for c in child.children.values():
                resolveChildren(c)
        else:
            if version:
                UserOptions.addPackageOption(child, "version", version)
            package.children[child.name] = child

    for packageName in packageNames:
        child = CraftPackageObject.get(packageName)
        if not child:
            raise BlueprintNotFoundException(packageName)
        resolveChildren(child)
    return package


def setOption(packageNames : [str], option : str) -> bool:
    if "=" not in option:
        CraftCore.log.error(f"Invalid option {args.set}")
        return False
    key, value = option.split("=", 1)
    for name in packageNames:
        package = CraftPackageObject.get(name)
        if not package:
            raise BlueprintNotFoundException(name)
        options = UserOptions.get(package)
        if not options.setOption(key, value):
            return False
        CraftCore.log.info(f"[{package}]\n{key}={getattr(options, key)}")
    return True

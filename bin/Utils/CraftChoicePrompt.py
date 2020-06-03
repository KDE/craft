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

import os
import sys

from collections import OrderedDict

# HACK for direct invocation, better provide a test scrip
if __name__ == "__main__":
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


import utils
import getpass

from CraftCore import CraftCore

def promptForChoice(title: str, choices : [], default : str=None):
    simpleMode = not isinstance(choices[0], tuple)
    if simpleMode:
        choices = OrderedDict.fromkeys(choices)
    else:
        choices = OrderedDict(choices)
    if not default:
        default = list(choices.keys())[0]

    selections = [f"[{index}] {value}" for index, value in enumerate(choices.keys())]
    promp = f"{', '.join(selections)} (Default is {default}): "

    utils.notify("Craft needs your attention", promp, log=False)

    CraftCore.debug.new_line()
    if CraftCore.settings.getboolean("ContinuousIntegration", "Enabled", False):
        CraftCore.log.info(title)
        CraftCore.log.info(f"[ContinuousIntegration]Enabled = True: returning default: {default}")
        return default if simpleMode else choices[default]

    while (True):
        CraftCore.log.info(title)
        choice = input(promp)
        CraftCore.log.debug(f"The user entered: {choice}")
        try:
            choiceInt = int(choice)
        except:
            choiceInt = -1
        if choice == "":
            out = default if simpleMode else choices[default]
            break
        elif choiceInt >= 0 and choiceInt < len(choices):
            out = list(choices.items())[choiceInt][0 if simpleMode else 1]
            break
        elif choice in choices:
            out = choice if simpleMode else choices[choice]
            break
    CraftCore.log.debug(f"Returning: {out}")
    return out

def promptForPassword(message: str, key: str=None):
    if CraftCore.settings.getboolean("ContinuousIntegration", "Enabled", True):
        if key:
            key = f"CRAFT_SECRET_{key}"
            if key in os.environ:
                return os.environ[key]
        CraftCore.log.info(f"[ContinuousIntegration] Enabled = True: Please set the environment variable {key}")
        raise Exception("Password prompts for CI are not supported by Craft.")
    else:
        utils.notify("Craft needs your attention", message, log=False)

        CraftCore.debug.new_line()
        password = getpass.getpass(prompt=message+": ", stream=None)
        return password

if __name__ == "__main__":
    print(promptForChoice("Test1, simple no default", ["Foo", "Bar"]))
    print(promptForChoice("Test2, simple default", ["Foo", "Bar"], "Bar"))
    print(promptForChoice("Test3, touple no default", [("Foo", True), ("Bar", False)]))
    print(promptForChoice("Test4, touple default", [("Foo", True), ("Bar", False)], "Bar"))

import threading
import time

import utils

from CraftCore import CraftCore

def promptForChoice(title, choices, default=None):
    if not default:
        if isinstance(choices[0], tuple):
            default, _ = choices[0]
        else:
            default = choices[0]
    selection = ", ".join(["[{index}] {value}".format(index=index,
                                                        value=value[0] if isinstance(value, tuple) else value)
                            for index, value in enumerate(choices)])
    promp = "{selection} (Default is {default}): ".format(selection=selection,
                                                            default=default[0] if isinstance(default,
                                                                                            tuple) else default)

    print()
    while (True):
        print(title)
        choice = input(promp)
        try:
            choiceInt = int(choice)
        except:
            choiceInt = -1
        if choice == "":
            for choice in choices:
                if isinstance(choice, tuple):
                    key, val = choice
                else:
                    key = val = choice
                if key == default:
                    return val
        elif choiceInt in range(len(choices)):
            if isinstance(choices[choiceInt], tuple):
                return choices[choiceInt][1]
            else:
                return choices[choiceInt]

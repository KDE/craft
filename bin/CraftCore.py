import importlib
import logging
import os
import sys

# Add imports that cause a cyclic dependency in a not taken branch to make code completion work
if False:
    from .CraftCompiler import CraftCompiler
    from .CraftDebug import CraftDebug
    from .CraftStandardDirs import CraftStandardDirs
    from .CraftConfig import CraftConfig
    from .Utils.CraftCache import CraftCache
    from .InstallDB import InstallDB


# TODO: a more optimal solution would be to initialize all singletons in a
# __init__.py but that would require massive refactoring as everything in bin/
# is not part of a module which could use such a __init__.py
class AutoImport(object):
    def __init__(self, name : str, module : str, className : str=None, function=None, member : str=None) -> None:
        self.name = name
        self.module = module
        self.className = className or module
        self.function = function
        self.member = member

    def __getattribute__(self, name : str):
        _name = super().__getattribute__("name")
        _module = super().__getattribute__("module")
        _className = super().__getattribute__("className")
        _function = super().__getattribute__("function")
        _member= super().__getattribute__("member")

        if _member:
            # initialize with a member of another object
            source = getattr(CraftCore, _name)
            out = getattr(source, _member)
            setattr(CraftCore, _member, out)
            return getattr(out, name)
        else:
            mod = importlib.import_module(_module)
            cls = getattr(mod, _className)
            if _function:
                func = getattr(cls, _function)
                instance = func()
            else:
                instance = cls()
            setattr(CraftCore, _name, instance)
            return instance.__getattribute__(name)

    def __str__(self):
        # force replacement
        self.__getattribute__
        # TODO: find out why how self was replaced ....
        return self.__str__()

class State(object):
    def __init__(self):
        # targets directly passed to craft
        self.directTargets = []

class CraftCore(object):
    debug = AutoImport("debug", "CraftDebug")  # type: CraftDebug
    # log will be replaced once debug is loaded
    log = AutoImport("debug", "CraftDebug", member="log") # type: logging.Logger
    standardDirs = AutoImport("standardDirs", "CraftStandardDirs")  # type: CraftStandardDirs
    settings = AutoImport("settings", "CraftConfig")  # type: CraftConfig
    cache = AutoImport("cache", "Utils.CraftCache", "CraftCache", "_loadInstance")  # type: CraftCache
    compiler = AutoImport("compiler", "CraftCompiler")  # type: CraftCompiler
    installdb = AutoImport("installdb", "InstallDB")  # type: InstallDB

    # information about the current internal state of Craft
    state = State()

# make sure our environment is setup
import CraftSetupHelper
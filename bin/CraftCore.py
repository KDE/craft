import importlib
import logging
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
# is not part of a module wich could use such a __init__.py
class AutoImport(object):
    def __init__(self, name : str, module : str, className : str=None, function=None) -> None:
        self.name = name
        self.module = module
        self.className = className or module
        self.function = function

    def __getattribute__(self, name : str):
        _name = super().__getattribute__("name")
        _module = super().__getattribute__("module")
        _className = super().__getattribute__("className")
        _function = super().__getattribute__("function")

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
    log = None  # type: logging.Logger
    standardDirs = AutoImport("standardDirs", "CraftStandardDirs")  # type: CraftStandardDirs
    settings = AutoImport("settings", "CraftConfig")  # type: CraftConfig
    cache = AutoImport("cache", "Utils.CraftCache", "CraftCache", "_loadInstance")  # type: CraftCache
    compiler = AutoImport("compiler", "CraftCompiler")  # type: CraftCompiler
    installdb = AutoImport("installdb", "InstallDB")  # type: InstallDB

    # information about the current internal state of Craft
    state = State()

    @classmethod
    def registerObjectAlias(cls, name : str, source : str, obj : str) -> None:
        """
        Allow to make a property of a singleton available through CraftCore
        """
        if not hasattr(cls, source):
            print(f"Unknown soruce {source}, please call CraftCore.registerInstance first", file=sys.stderr)
            exit(1)
        if not hasattr(cls, name):
            print(f"Unknown property name {name}, please define  CraftCore.{name}", file=sys.stderr)
            exit(1)
        if not hasattr(cls, name):
            print(f"Unknown property {source.__class__}.{name}", file=sys.stderr)
            exit(1)
        if not getattr(cls, name):
            setattr(cls, name, getattr(getattr(cls, source), obj))

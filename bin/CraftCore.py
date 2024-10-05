import importlib
from typing import Optional

# Add imports that cause a cyclic dependency in a not taken branch to make code completion work
if False:
    from .CraftCompiler import CraftCompiler  # noqa: F401
    from .CraftConfig import CraftConfig  # noqa: F401
    from .CraftDebug import CraftDebug  # noqa: F401
    from .CraftStandardDirs import CraftStandardDirs  # noqa: F401
    from .InstallDB import InstallDB  # noqa: F401
    from .Utils.CraftCache import CraftCache  # noqa: F401


# TODO: a more optimal solution would be to initialize all singletons in a
# __init__.py but that would require massive refactoring as everything in bin/
# is not part of a module which could use such a __init__.py
# TODO: remove once we require python 3.7
# "Circular imports involving absolute imports with binding a submodule to a name are now supported. (Contributed by Serhiy Storchaka in bpo-30024.)"
class AutoImport(object):
    def __init__(
        self,
        name: str,
        module: str,
        className: Optional[str] = None,
        function=None,
        member: Optional[str] = None,
    ) -> None:
        self.name = name
        self.module = module
        self.className = className or module
        self.function = function
        self.member = member

    def __getattribute__(self, name: str):
        _name = super().__getattribute__("name")
        _module = super().__getattribute__("module")
        _className = super().__getattribute__("className")
        _function = super().__getattribute__("function")
        _member = super().__getattribute__("member")

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
    debug: "CraftDebug" = AutoImport("debug", "CraftDebug")
    # log will be replaced once debug is loaded
    log = AutoImport("debug", "CraftDebug", member="log")
    standardDirs: "CraftStandardDirs" = AutoImport("standardDirs", "CraftStandardDirs")
    settings: "CraftConfig" = AutoImport("settings", "CraftConfig")
    cache: "CraftCache" = AutoImport("cache", "Utils.CraftCache", "CraftCache", "_loadInstance")
    compiler: "CraftCompiler" = AutoImport("compiler", "CraftCompiler")
    installdb: "InstallDB" = AutoImport("installdb", "InstallDB")

    # information about the current internal state of Craft
    state = State()


# make sure our environment is setup
import CraftSetupHelper  # noqa: F401,E402

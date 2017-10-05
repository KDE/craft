import logging
import sys

class CraftCore(object):
    debug = None
    log = None
    standardDirs = None
    settings = None

    @classmethod
    def registerInstance(cls, name : str, _class : type) -> None:
        """
        Register a singleton with CraftCore
        """
        if not hasattr(cls, name):
            print(f"Unknown instance name {name}, please define  CraftCore.{name}", file=sys.stderr)
            exit(1)
        if not getattr(cls, name):
            setattr(cls, name, _class())

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

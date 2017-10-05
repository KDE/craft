import logging
import sys

class CraftCore(object):
    debug = None
    standardDirs = None
    settings = None

    @classmethod
    def registerInstance(cls, name : str, _class : type) -> None:
        if not hasattr(cls, name):
            print(f"Unknown instance name {name}, please define  CraftCore.{name}", file=sys.stderr)
            exit(1)
        if not getattr(cls, name):
            setattr(cls, name, _class())

    @staticmethod
    def log() -> logging.Logger:
        return CraftCore.debug.log()

import subprocess

from CraftCore import CraftCore


class Arguments(object):
    def __init__(self, args: [str] = None):
        self.__args = []
        self.__legacyString = None
        if args:
            if isinstance(args, str):
                self.__legacyString = ""
            self.append(args)

    def __setLegacy(self):
        if self.__legacyString is None:
            self.__legacyString = subprocess.list2cmdline([str(x) for x in self.__args])

    def toSetting(self):
        return str(self)

    @staticmethod
    def fromSetting(data: str):
        return Arguments(data)

    def append(self, other):
        if not other:
            return self
        if self.__legacyString is not None:

            def join(rhs: str, lhs: str):
                if not rhs:
                    return lhs
                return " ".join([rhs.rstrip(), lhs.lstrip()])

            if isinstance(other, str):
                self.__legacyString = join(self.__legacyString, other)
            elif isinstance(other, list):
                self.__legacyString = join(self.__legacyString, subprocess.list2cmdline([str(x) for x in other]))
            elif isinstance(other, Arguments):
                if other.__legacyString is not None:
                    self.__legacyString = join(self.__legacyString, other.__legacyString)
                else:
                    self.__legacyString = join(self.__legacyString, subprocess.list2cmdline(other.__args))
            else:
                raise Exception("error unsupported argumen" + other)
        else:
            if isinstance(other, Arguments):
                if other.__legacyString is not None:
                    self.__setLegacy()
                    self.append(other)
                else:
                    self.__args += other.__args
            elif isinstance(other, list):
                for x in other:
                    self.append(x)
            else:
                self.__args.append(other)
            return self

    def __add__(self, other):
        out = Arguments(self)
        if not other:
            return out
        if isinstance(other, str):
            out.__setLegacy()
        out.append(other)
        return out

    def __str__(self):
        if self.__legacyString is not None:
            return self.__legacyString
        return subprocess.list2cmdline([str(x) for x in self.__args])

    def get(self):
        if self.__legacyString:
            return self.__legacyString
        else:
            return self.__args

    @staticmethod
    def formatCommand(command: [str], args):
        tmp = Arguments(command) + args
        return tmp.get()


import subprocess

class Arguments(object):
    def __init__(self, args:[str]=None):
        self.__args = []
        self.__legacyString = None
        if args:
            if isinstance(args, str):
                self.__legacyString = ""
            self.append(args)

    def __setLegacy(self):
        if self.__legacyString is None:
            self.__legacyString = subprocess.list2cmdline(self.__args)

    def append(self, other):
        if self.__legacyString is not None:
            if isinstance(other, str):
                if not other.startswith(" "):
                    self.__legacyString += " "
                self.__legacyString += other
            elif isinstance(other, list):
                self.__legacyString += " " + subprocess.list2cmdline([str(x) for x in other])
            elif isinstance(other, Arguments):
                self.__legacyString += " " + subprocess.list2cmdline(other.__args)
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
        if isinstance(other, str):
            self.__setLegacy()
        self.append(other)
        return self

    def __str__(self):
        if self.__legacyString is not None:
            return self.__legacyString
        return subprocess.list2cmdline(self.__args)

    def get(self):
        if self.__legacyString:
            return self.__legacyString           
        else:
            return self.__args

    @staticmethod
    def formatCommand(command:[str], args):
        if args.__legacyString:
            return subprocess.list2cmdline(command) + " " + args.__legacyString.strip()
        return command + args.__args

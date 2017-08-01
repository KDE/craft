import argparse
import os
import platform
import re
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request


class CraftBootstrap(object):
    def __init__(self, kdeRoot, branch):
        self.kdeRoot = kdeRoot
        self.branch = branch
        with open(os.path.join(kdeRoot, f"craft-{branch}", "kdesettings.ini"), "rt+") as ini:
            self.settings = ini.read().splitlines()

    @staticmethod
    def isWin():
        return os.name == 'nt'

    @staticmethod
    def isUnix():
        return os.name == 'posix'

    @staticmethod
    def isFreeBSD():
        return CraftBootstrap.isUnix() and platform.system() == 'FreeBSD'

    @staticmethod
    def isMac():
        return CraftBootstrap.isUnix() and platform.system() == 'Darwin'

    @staticmethod
    def isLinux():
        return CraftBootstrap.isUnix() and platform.system() == 'Linux'

    @staticmethod
    def printProgress(percent):
        width, _ = shutil.get_terminal_size((80, 20))
        width -= 20  # margin
        times = int(width / 100 * percent)
        sys.stdout.write("\r[{progress}{space}]{percent}%".format(progress="#" * times, space=" " * (width - times),
                                                                  percent=percent))
        sys.stdout.flush()

    @staticmethod
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

    @staticmethod
    def promptShortPath():
        drivePatern = re.compile("^[A-Z](:|:\\\\)?$", re.IGNORECASE)

        def promptDriveLetter(purpose, default):
            while (True):
                print(f"Enter drive for {purpose}")
                drive = input(f"[Possibilities A-Z] (Default is {default}):")
                if drive == "":
                    return default
                if drivePatern.match(drive):
                    if len(drive) == 1:
                        return drive + ":"
                    return drive[:2]

        return {"RootDrive": promptDriveLetter("the build root", "R:"),
                "GitDrive": promptDriveLetter("the location where the git checkouts are located", "Q:")}

    def setSettignsValue(self, section, key, value):
        reKey = re.compile(r"^\s*{key}\s*=.*$".format(key=key), re.IGNORECASE)
        reSection = re.compile(r"^\[(.*)\]$".format(section=section))
        inSection = False
        for i, line in enumerate(self.settings):
            sectionMatch = reSection.match(line)
            if sectionMatch:
                inSection = sectionMatch.group(1) == section
            elif inSection and reKey.match(line):
                self.settings[i] = f"{key} = {value}"

    def writeSettings(self):
        os.makedirs(os.path.join(self.kdeRoot, "etc"))
        with open(os.path.join(self.kdeRoot, "etc", "kdesettings.ini"), "wt+") as out:
            out.write("\n".join(self.settings))

    @staticmethod
    def downloadFile(url, destdir, filename=None):
        if not os.path.exists(destdir):
            os.makedirs(destdir)

        if not filename:
            _, _, path, _, _, _ = urllib.parse.urlparse(url)
            filename = os.path.basename(path)

        print("Starting to download %s to %s" % (url, os.path.join(destdir, filename)))
        if os.path.exists(os.path.join(destdir, filename)):
            return True

        def dlProgress(count, blockSize, totalSize):
            if totalSize != -1:
                percent = int(count * blockSize * 100 / totalSize)
                CraftBootstrap.printProgress(percent)
            else:
                sys.stdout.write(("\r%s bytes downloaded" % (count * blockSize)))
                sys.stdout.flush()

        urllib.request.urlretrieve(url, filename=os.path.join(destdir, filename), reporthook=dlProgress)
        print()
        return os.path.exists(os.path.join(destdir, filename))


def run(args, command):
    script = os.path.join(args.prefix, f"craft-{args.branch}", "bin", "craft.py")
    command = f"{sys.executable} {script} {command}"
    print(f"Execute: {command}")
    if not subprocess.run(f"{command}", shell=True).returncode == 0:
        exit(1)


def getArchitecture():
    return CraftBootstrap.promptForChoice("Select architecture", [("x86", "32"),
                                                                  ("x64", "64")], "x64")


def getABI():
    if CraftBootstrap.isWin():
        platform = "windows"
        abi, compiler = CraftBootstrap.promptForChoice("Select compiler",
                                                       [("Mingw-w64", ("mingw", "gcc")),
                                                        ("Microsoft Visual Studio 2015", ("msvc2015", "cl")),
                                                        ("Microsoft Visual Studio 2017", ("msvc2017", "cl"))],
                                                       "Microsoft Visual Studio 2015")
        abi += f"_{getArchitecture()}"

    elif CraftBootstrap.isUnix():
        if CraftBootstrap.isMac():
            platform = "macos"
            compiler = "clang"
            abi = "64"
        else:
            if CraftBootstrap.isLinux():
                platform = "linux"
            elif CraftBootstrap.isFreeBSD():
                platform = "freebsd"
            compiler = CraftBootstrap.promptForChoice("Select compiler",
                                                      ["gcc", "clang"])
            abi = getArchitecture()

    return f"{platform}-{abi}-{compiler}"


def getIgnores():
    if CraftBootstrap.isWin():
        return ""

    ignores = "gnuwin32/.*;dev-util/.*;binary/.*;kdesupport/kdewin"
    print(f"On your OS we blacklist the following packages.\n"
          f"  {ignores}")
    print("On Unix systems we recommend to get third party libraries from your distributions package manager.")
    ignores += CraftBootstrap.promptForChoice("Do you want to blacklist the win32libs category?",
                                              [("Yes", ";win32libs/.*"), ("No", "")])
    print(
        "Craft can provide you with the whole Qt5 SDK, but you can also use Qt5 development packages provided by the distribution.")
    ignores += CraftBootstrap.promptForChoice("Do you want to blacklist Qt5?",
                                              [("Yes", ";libs/qt5/.*"), ("No", "")],
                                              default="No")
    print(f"Your blacklist.\n"
          f"Ignores: {ignores}")

    return ignores


def setUp(args):
    if not os.path.exists(args.prefix):
        os.makedirs(args.prefix)

    print("Welcome to the Craft setup wizard!")

    abi = getABI()
    if CraftBootstrap.isWin():
        print("Windows has problems with too long commands.")
        print("For that reason we mount Craft directories to drive letters.")
        print("It just maps the folder to a drive letter you will assign.")
        shortPath = CraftBootstrap.promptShortPath()

    ignores = getIgnores()

    CraftBootstrap.downloadFile(f"https://github.com/KDE/craft/archive/{args.branch}.zip",
                                os.path.join(args.prefix, "download"),
                                f"craft-{args.branch}.zip")
    shutil.unpack_archive(os.path.join(args.prefix, "download", f"craft-{args.branch}.zip"), args.prefix)

    boot = CraftBootstrap(args.prefix, args.branch)
    boot.setSettignsValue("Paths", "Python", os.path.dirname(sys.executable).replace("\\", "/"))
    boot.setSettignsValue("General", "ABI", abi)
    boot.setSettignsValue("Portage", "Ignores", ignores)

    if CraftBootstrap.isWin():
        boot.setSettignsValue("ShortPath", "Enabled", "True")
        for key, value in shortPath.items():
            boot.setSettignsValue("ShortPath", key, value)
    else:
        boot.setSettignsValue("ShortPath", "Enabled", "False")
        boot.setSettignsValue("Compile", "MakeProgram", "make")

    boot.writeSettings()

    verbosityFlag = "-vvv" if args.verbose else ""
    run(args, f"--no-cache {verbosityFlag} craft")
    shutil.rmtree(os.path.join(args.prefix, f"craft-{args.branch}"))
    print("Setup complete")
    print()
    print("Please run the following command to get started:")
    if CraftBootstrap.isWin():
        print(f"  {args.prefix}/craft/craftenv.ps1")
    else:
        print(f"  source {args.prefix}/craft/craftenv.sh")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="CraftSetupHelper")
    parser.add_argument("--root", action="store", help="Deprecated: use prefix instead.")
    parser.add_argument("--prefix", action="store", default=os.getcwd(), help="The installation directory.")
    parser.add_argument("--branch", action="store", default="master", help="The branch to install")
    parser.add_argument("--verbose", action="store_true", help="The verbosity.")
    parser.add_argument("--version", action="version", version="%(prog)s master")

    args = parser.parse_args()
    if args.root:
        args.prefix = args.root

    setUp(args)

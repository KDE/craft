import argparse
import configparser
import os
import sys
import re
import subprocess
import urllib.parse
import urllib.request
import shutil
import platform

class CraftBootstrap(object):
    def __init__(self, kdeRoot, branch):
        self.kdeRoot = kdeRoot
        self.branch = branch
        with open(os.path.join(kdeRoot, f"craft-{branch}", "kdesettings.ini"),  "rt+") as ini:
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
    def promptForChoice(title, choices, default):
        print(title)
        promp = "%s (Default is %s): " %(", ".join(["[%d] %s" % (i, val) for i, val in enumerate(choices)]), default)
        while(True):
            choice = input(promp)
            try:
                choiceInt = int(choice)
            except:
                choiceInt = -1
            if choice == "":
                return default
            elif choiceInt in range(len(choices)):
                return choices[choiceInt]

    @staticmethod
    def promptShortPath():
        drivePatern = re.compile("^[A-Z](:|:\\\\)?$", re.IGNORECASE)
        def promptDriveLetter(purpose, default):
            while(True):
                drive = input("Enter drive for %s [Possibilities A-Z] (Default is %s): " % (purpose, default))
                if drive == "":
                    return default
                if drivePatern.match(drive):
                    if len(drive) == 1:
                        return drive + ":"
                    return drive[:2]
        return { "RootDrive" : promptDriveLetter("the build root", "R:"),
                 "GitDrive" : promptDriveLetter("the location where the git checkouts are located", "Q:")}



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
            out.write(os.linesep.join(self.settings))

    @staticmethod
    def downloadFile(url, destdir, filename = None):
        if not os.path.exists(destdir):
            os.makedirs(destdir)

        if not filename:
            _, _, path, _, _, _ = urllib.parse.urlparse( url )
            filename = os.path.basename( path )

        print("Starting to download %s to %s" % (url, os.path.join( destdir, filename )))
        if os.path.exists(os.path.join( destdir, filename )):
            return True

        def dlProgress(count, blockSize, totalSize):
            if totalSize != -1:
                percent = int(count * blockSize * 100 / totalSize)
                CraftBootstrap.printProgress(percent)
            else:
                sys.stdout.write(("\r%s bytes downloaded" % (count * blockSize)))
                sys.stdout.flush()

        urllib.request.urlretrieve(url, filename =  os.path.join( destdir, filename ), reporthook=dlProgress)
        print()
        return os.path.exists(os.path.join( destdir, filename ))

def run(args, command):
    script = os.path.join(args.root, f"craft-{args.branch}", "bin", "craft.py")
    command = f"{sys.executable} {script} {command}"
    print(f"Execute: {command}")
    if not subprocess.run(f"{command}").returncode == 0:
        exit(1)

def getArchitecture():
    return CraftBootstrap.promptForChoice("Select Architecture", ["32", "64"], "64")

def getABI():
    if CraftBootstrap.isWin():
        platform = "windows"
        abi = CraftBootstrap.promptForChoice("Select Compiler",
                                                  ["Mingw-w64", "Microsoft Visual Studio 2015", "Microsoft Visual Studio 2017"],
                                                   "Microsoft Visual Studio 2015")
        compiler = "cl"
        if abi == "Mingw-w64":
            abi = "mingw"
            compiler = "gcc"
        elif abi == "Microsoft Visual Studio 2015":
            abi = "msvc2015"
        else:
            abi = "msvc2017"
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
            compiler = CraftBootstrap.promptForChoice("Select Compiler",
                                                      ["gcc", "clang"],
                                                      "gcc")
            abi = getArchitecture()

    return f"{platform}-{abi}-{compiler}"

def setUp(args):
    if not os.path.exists(args.root):
        os.makedirs(args.root)

    abi = getABI()
    if CraftBootstrap.isWin():
        print("Windows has problems with too long commands.")
        print("For that reason we mount Craft directories to drive letters.")
        print("It just maps the folder to a drive letter you will assign.")
        shortPath = CraftBootstrap.promptShortPath()

    CraftBootstrap.downloadFile(f"https://github.com/KDE/craft/archive/{args.branch}.zip", os.path.join(args.root, "download"),
                                 f"craft-{args.branch}.zip")
    shutil.unpack_archive(os.path.join(args.root, "download", f"craft-{args.branch}.zip"), args.root)

    boot = CraftBootstrap(args.root, args.branch)
    boot.setSettignsValue("Paths", "Python", os.path.dirname(sys.executable).replace("\\", "/"))
    boot.setSettignsValue("General", "ABI", abi)

    if CraftBootstrap.isWin():
        boot.setSettignsValue("ShortPath", "Enabled", "True")
        for key, value in shortPath.items():
            boot.setSettignsValue("ShortPath", key, value)
    else:
        boot.setSettignsValue("ShortPath", "Enabled", "False")


    boot.writeSettings()

    verbosityFlag = "-vvv" if args.verbose else ""
    run(args, f"--no-cache {verbosityFlag} craft")
    shutil.rmtree(os.path.join(args.root, f"craft-{args.branch}"))
    print("Setup complete")
    if CraftBootstrap.isWin():
        print(f"Please run {args.root}/craft/craftenv.ps1")
    else:
        print(f"Please source {args.root}/craft/craftenv.sh")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="SetupHelper")
    parser.add_argument("--root", action="store", default=os.getcwd())
    parser.add_argument("--branch", action="store", default="master")
    parser.add_argument("--verbose", action="store_true")

    args = parser.parse_args()
    setUp(args)


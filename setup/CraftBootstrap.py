import argparse
import configparser
import os
import sys
import re
import subprocess
import urllib.parse
import urllib.request
import shutil

class CraftBootstrap(object):
    def __init__(self, kdeRoot, branch):
        self.kdeRoot = kdeRoot
        self.branch = branch
        with open(os.path.join(kdeRoot, f"craft-{branch}", "kdesettings.ini"),  "rt+") as ini:
            self.settings = ini.read()

    @staticmethod
    def isWin():
        return os.name == 'nt'

    @staticmethod
    def isUnix():
        return os.name == 'posix'

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
        return { "EMERGE_ROOT_DRIVE" : promptDriveLetter("the build root", "R:"),
                 "EMERGE_GIT_DRIVE" : promptDriveLetter("the location where the git checkouts are located", "Q:")}



    def setSettignsValue(self, key, value):
        regex = re.compile("^\s*%s\s*=.*$" % key, re.MULTILINE | re.IGNORECASE )
        self.settings = regex.sub("%s = %s" % (key, value), self.settings)

    def writeSettings(self):
        os.makedirs(os.path.join(self.kdeRoot, "etc"))
        with open(os.path.join(self.kdeRoot, "etc", "kdesettings.ini"), "wt+") as out:
            out.write(self.settings)

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
    script = os.path.join(args.root, f"craft-{args.branch}", "craftenv.ps1")
    print(f"Execute: powershell {script} {command}")
    if not subprocess.run(f"powershell {script} {command}").returncode == 0:
        exit(1)


def setUp(args):
    if not os.path.exists(args.root):
        os.makedirs(args.root)
    architecture = CraftBootstrap.promptForChoice("Select Architecture", ["x86", "x64"], "x86")

    compiler = CraftBootstrap.promptForChoice("Select Compiler", ["Mingw-w64", "Microsoft Visual Studio 2015"],
                                               "Mingw-w64")
    if compiler == "Mingw-w64":
        compiler = "mingw4"
    else:
        compiler = "msvc2015"

    if CraftBootstrap.isWin():
        print("Windows has problems with too long commands.")
        print("For that reason we mount Craft directories to drive letters.")
        print("It just maps the folder to a drive letter you will assign.")
        shortPath = CraftBootstrap.promptShortPath()

    CraftBootstrap.downloadFile(f"https://github.com/KDE/craft/archive/{args.branch}.zip", os.path.join(args.root, "download"),
                                 f"craft-{args.branch}.zip")
    shutil.unpack_archive(os.path.join(args.root, "download", f"craft-{args.branch}.zip"), args.root)

    boot = CraftBootstrap(args.root, args.branch)
    boot.setSettignsValue("Python", os.path.dirname(sys.executable).replace("\\", "/"))
    boot.setSettignsValue("Architecture", architecture)
    boot.setSettignsValue("KDECompiler", compiler)

    if CraftBootstrap.isWin():
        boot.setSettignsValue("EMERGE_USE_SHORT_PATH", "True")
        for key, value in shortPath.items():
            boot.setSettignsValue(key, value)
    else:
        boot.setSettignsValue("EMERGE_USE_SHORT_PATH", "False")


    boot.writeSettings()

    craftDir = os.path.join(args.root, "craft")
    verbosityFlag = "-vvv" if args.verbose else ""
    run(args, f"craft --no-cache {verbosityFlag} git")
    run(args, f"git clone --progress --branch={args.branch} kde:craft {craftDir}")
    shutil.rmtree(os.path.join(args.root, f"craft-{args.branch}"))
    print("Setup complete")
    print(f"Please run {args.root}/craft/craftenv.ps1")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="SetupHelper")
    parser.add_argument("--root", action="store")
    parser.add_argument("--branch", action="store")
    parser.add_argument("--verbose", action="store_true")

    args = parser.parse_args()
    setUp(args)


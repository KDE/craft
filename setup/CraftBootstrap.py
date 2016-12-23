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
    def __init__(self, kdeRoot):
        self.kdeRoot = kdeRoot
        with open(os.path.join(kdeRoot, "craft-master", "kdesettings.ini"),  "rt+") as ini:
            self.settings = ini.read()

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

        width, _ =  shutil.get_terminal_size((80,20))
        def dlProgress(count, blockSize, totalSize):
            percent = int(count * blockSize * 100 / totalSize)
            times = int((width - 20)/100 * percent)
            sys.stdout.write(("\r%s%3d%%" % ("#" * times, percent)))
            sys.stdout.flush()

        urllib.request.urlretrieve(url, filename =  os.path.join( destdir, filename ), reporthook= dlProgress)
        print()
        return os.path.exists(os.path.join( destdir, filename ))

def run(args, command):
    print("Execute: powershell %s %s" % (os.path.join(args.root, "craft-master", "kdeenv.ps1"), command))
    subprocess.check_call("powershell %s %s" % (os.path.join(args.root, "craft-master", "kdeenv.ps1"), command))


def setUp(args):
    if not os.path.exists(args.root):
        os.makedirs(args.root)
    if args.architecture:
        architecture = args.architecture
    else:
        architecture = CraftBootstrap.promptForChoice("Select Architecture", ["x86", "x64"], "x86")

    if args.compiler:
        compiler = args.compiler
    else:
        compiler = CraftBootstrap.promptForChoice("Select Compiler", ["Mingw-w64", "Microsoft Visual Studio 2015"],
                                               "Mingw-w64")
    if compiler == "Mingw-w64":
        compiler = "mingw4"
    else:
        compiler = "msvc2015"

    if not args.noShortPath:
        print("Windows has problems with too long commands.")
        print("For that reason we mount Craft directories to drive letters.")
        print("It just maps the folder to a drive letter you will assign.")
        shortPath = CraftBootstrap.promptShortPath()

    CraftBootstrap.downloadFile("https://github.com/KDE/craft/archive/master.zip", os.path.join(args.root, "download"),
                                 "craft.zip")
    shutil.unpack_archive(os.path.join(args.root, "download", "Craft.zip"), args.root)

    boot = CraftBootstrap(args.root)
    boot.setSettignsValue("Python", os.path.dirname(sys.executable).replace("\\", "/"))
    boot.setSettignsValue("Architecture", architecture)
    boot.setSettignsValue("KDECompiler", compiler)

    if not args.noShortPath:
        boot.setSettignsValue("EMERGE_USE_SHORT_PATH", "True")
        for key, value in shortPath.items():
            boot.setSettignsValue(key, value)
    else:
        boot.setSettignsValue("EMERGE_USE_SHORT_PATH", "False")


    boot.writeSettings()
    if args.set:
        writeSettings(args)

    run(args, "craft --ci-mode %s git" % ("-vvv" if args.verbose else ""))
    run(args, "git clone kde:craft %s" % os.path.join(args.root, "craft"))
    shutil.rmtree(os.path.join(args.root, "craft-master"))
    print("Setup complete")
    print("Please run %s/craft/kdeenv.ps1" % args.root)


def writeSettings(args):
    settings = configparser.ConfigParser()
    ini = os.path.join(args.root, "etc", "kdesettings.ini")
    if not os.path.exists(ini):
        os.makedirs(os.path.dirname(ini))
        shutil.copy(os.path.join(args.root, "craft", "kdesettings.ini"), ini)
    settings.read(ini)

    for setting in args.values:
        section, key = setting.split("/", 1)
        key, value = key.split("=", 1)
        if section not in settings.sections():
            settings.add_section(section)
        settings.set(section, key, value)

    with open(ini, 'wt+') as configfile:
        settings.write(configfile)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="SetupHelper")
    parser.add_argument("--root", action="store")
    parser.add_argument("--compiler", action="store")
    parser.add_argument("--architecture", action="store")
    parser.add_argument("--no-short-path", action="store_true", dest="noShortPath")
    parser.add_argument("--no-bootstrap", action="store_true", dest="noBootstrap")
    parser.add_argument("--set", action="store_true")
    parser.add_argument("--verbose", action="store_true")

    parser.add_argument("values", nargs = argparse.REMAINDER)

    args = parser.parse_args()

    if not args.noBootstrap:
        setUp(args)
    elif args.set:
        writeSettings(args)



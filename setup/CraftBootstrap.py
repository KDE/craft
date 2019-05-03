import argparse
import configparser
import os
import platform
import re
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request

if not platform.machine().endswith("64"):
    print(f"Craft requires a 64bit operating system. You are using: {platform.machine()}")
    exit(1)

class CraftBootstrap(object):
    def __init__(self, craftRoot, branch, dryRun):
        self.craftRoot = craftRoot
        self.branch = branch
        self.dryRun = dryRun

        if not dryRun:
            with open(os.path.join(craftRoot, f"craft-{branch}", "CraftSettings.ini.template"), "rt", encoding="UTF-8") as ini:
                self.settings = ini.read().splitlines()
        else:
            with open(dryRun, "rt", encoding="UTF-8") as ini:
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

    def setSettignsValue(self, section, key, value):
        reKey = re.compile(r"^[\#;]?\s*{key}\s*=.*$".format(key=key), re.IGNORECASE)
        reSection = re.compile(r"^\[(.*)\]$".format(section=section))
        inSection = False
        for i, line in enumerate(self.settings):
            sectionMatch = reSection.match(line)
            if sectionMatch:
                inSection = sectionMatch.group(1) == section
            elif inSection and reKey.match(line):
                self.settings[i] = f"{key} = {value}"
                return
        print(f"Unable to locate\n"
              f"\t[{section}]\n"
              f"\t{key}")
        exit(1)

    def writeSettings(self):
        if not os.path.isdir(os.path.join(self.craftRoot, "etc")):
            os.makedirs(os.path.join(self.craftRoot, "etc"), exist_ok=True)
        if not self.dryRun:
            with open(os.path.join(self.craftRoot, "etc", "CraftSettings.ini"), "wt+") as out:
                out.write("\n".join(self.settings))
        else:
            with open(self.dryRun + ".dry_run", "wt+") as out:
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
    root = os.path.join(args.prefix, "craft")
    if not os.path.isdir(root):
        root = os.path.join(args.prefix, f"craft-{args.branch}")
    script = os.path.join(root, "bin", "craft.py")
    command = [sys.executable, script] + command
    commandStr = " ".join(command)
    print(f"Execute: {commandStr}")
    if not args.dry_run:
        if not subprocess.run(command).returncode == 0:
            exit(1)

def getABI():
    if CraftBootstrap.isWin():
        platform = "windows"
        abi, compiler = CraftBootstrap.promptForChoice("Select compiler",
                                                       [("Mingw-w64", ("mingw", "gcc")),
                                                        ("Microsoft Visual Studio 2017", ("msvc2017", "cl")),
                                                        ("Microsoft Visual Studio 2019 (Experimental)", ("msvc2019", "cl")),
                                                        ], "Microsoft Visual Studio 2017")
        abi += f"_64"

    elif CraftBootstrap.isUnix():
        if CraftBootstrap.isMac():
            platform = "macos"
            compiler = "clang"
        else:
            if CraftBootstrap.isLinux():
                platform = "linux"
            elif CraftBootstrap.isFreeBSD():
                platform = "freebsd"
            compiler = CraftBootstrap.promptForChoice("Select compiler",
                                                      ["gcc", "clang"])
        abi = "64"

    return f"{platform}-{abi}-{compiler}"

def setUp(args):
    if not args.dry_run and not os.path.exists(args.prefix):
        os.makedirs(args.prefix)
        for d in os.listdir(args.prefix):
            if d != "downloads":#generated by the windows script
                print("Error: you are trying to install Craft into an non empty directory")
                exit(1)


    print("Welcome to the Craft setup wizard!")

    abi = getABI()

    installShortCut = False
    if CraftBootstrap.isWin():
        installShortCut = CraftBootstrap.promptForChoice("Do you want to install a StartMenu entry",
                                                         [("Yes", True), ("No", False)],
                                                         default="Yes")
    if not args.dry_run:
        if args.localDev:
            shutil.copytree(args.localDev, os.path.join(args.prefix, f"craft-{args.branch}"),
                            ignore=shutil.ignore_patterns(".git"))
            print("Getting code from local {}".format(args.localDev))
        else:
            CraftBootstrap.downloadFile(f"https://github.com/KDE/craft/archive/{args.branch}.zip",
                                        os.path.join(args.prefix, "download"),
                                        f"craft-{args.branch}.zip")
            shutil.unpack_archive(os.path.join(args.prefix, "download", f"craft-{args.branch}.zip"), args.prefix)

    boot = CraftBootstrap(args.prefix, args.branch, args.dry_run)
    boot.setSettignsValue("Paths", "Python", os.path.dirname(sys.executable))
    boot.setSettignsValue("General", "ABI", abi)
    py = shutil.which("py")
    if py:
        py2 = subprocess.getoutput(f"""{py} -2 -c "import sys; print(sys.executable)" """)
        if os.path.isfile(py2):
            boot.setSettignsValue("Paths", "Python27", os.path.dirname(py2))

    if CraftBootstrap.isWin():
        boot.setSettignsValue("Compile", "MakeProgram", "mingw32-make" if "mingw" in abi else "jom")
    else:
        boot.setSettignsValue("Compile", "MakeProgram", "make")

    boot.writeSettings()

    cmd = []
    if args.verbose:
        cmd.append("-vvv")
    cmd += ["craft"]
    run(args, cmd)
    if not args.dry_run:
        shutil.rmtree(os.path.join(args.prefix, f"craft-{args.branch}"))
    if installShortCut:
        run(args, ["craft-startmenu-entry"])

    # install toast notifications
    run(args, ["dev-utils/snoretoast"])

    print("Setup complete")
    print()
    print("Please run the following command to get started:")
    path = os.path.join(args.prefix, "craft", "craftenv")
    if CraftBootstrap.isWin():
        print(f"  {path}.ps1")
    else:
        print(f"  source {path}.sh")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="CraftSetupHelper")
    parser.add_argument("--root", action="store", help="Deprecated: use prefix instead.")
    parser.add_argument("--prefix", action="store", default=os.getcwd(), help="The installation directory.")
    parser.add_argument("--branch", action="store", default="master", help="The branch to install")
    parser.add_argument("--verbose", action="store_true", help="The verbosity.")
    parser.add_argument("--dry-run", action="store", help="Configure the passed CraftSettings.ini and exit.")
    parser.add_argument("--version", action="version", version="%(prog)s master")
    parser.add_argument("--localDev", action="store", help="Path to a local directory to use instead of fetching from github")

    args = parser.parse_args()
    if args.root:
        args.prefix = args.root

    setUp(args)

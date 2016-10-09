import os
import sys
import re
import subprocess
import urllib.parse
import urllib.request
import shutil

class EmergeBootstrap(object):
    def __init__(self, kdeRoot):
        self.kdeRoot = kdeRoot
        with open(os.path.join(kdeRoot, "emerge", "kdesettings.ini"),  "rt+") as ini:
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



if __name__ == "__main__":
    kdeRoot = sys.argv[1]
    os.chdir(kdeRoot)

    architecture = EmergeBootstrap.promptForChoice("Select Architecture", ["x86", "x64"], "x86")
    compiler = EmergeBootstrap.promptForChoice("Select Compiler", ["Mingw-w64", "Microsoft Visual Studio 2015"], "Mingw-w64")
    if compiler == "Mingw-w64":
        compiler = "mingw4"
    else:
        compiler = "msvc2015"

    print("Windows has problems with too long commands.")
    print("For that reason we mount emerge directories to drive letters.")
    print("It just maps the folder to a drive letter you will assign.")
    shortPath = EmergeBootstrap.promptShortPath()

    EmergeBootstrap.downloadFile("https://github.com/KDE/emerge/archive/master.zip", os.path.join(kdeRoot, "download"), "emerge.zip")
    shutil.unpack_archive(os.path.join(kdeRoot, "download", "emerge.zip" ), kdeRoot)
    shutil.move(os.path.join(kdeRoot,"emerge-master" ), os.path.join(kdeRoot,"emerge" ))
    os.chdir(os.path.join(kdeRoot,"emerge" ))

    boot = EmergeBootstrap(kdeRoot)
    boot.setSettignsValue("Python", os.path.dirname(sys.executable).replace("\\", "/"))
    boot.setSettignsValue("Architecture", architecture)
    boot.setSettignsValue("KDECompiler", compiler)

    boot.setSettignsValue("EMERGE_USE_SHORT_PATH", "True")
    for key, value in shortPath.items():
        boot.setSettignsValue(key, value)
    boot.writeSettings()
    subprocess.call("%s emerge git" % os.path.join(kdeRoot, "emerge", "kdeenv.bat"))
    os.chdir(kdeRoot)
    shutil.rmtree( os.path.join(kdeRoot, "emerge") )
    subprocess.check_call("%s clone kde:emerge %s" % (os.path.join(kdeRoot, "dev-utils", "bin", "git"), os.path.join(kdeRoot, "emerge")))
    print("Setup complete")
    print("Please run %s/emerge/kdeenv.ps1" % kdeRoot)



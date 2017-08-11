import shutil

import info
from Package.CMakePackageBase import *


# do not forget to update CMakeLists.txt!


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["1.1"] = ["http://people.freedesktop.org/~hadess/shared-mime-info-1.1.tar.xz",
                               "http://ftp.gnome.org/pub/gnome/sources/glib/2.24/glib-2.24.0.tar.bz2"]
        self.targetInstSrc["1.1"] = "shared-mime-info-1.1"
        self.targetDigests['1.1'] = ['752668b0cc5729433c99cbad00f21241ec4797ef',
                                     '32714e64fff52d18db5f077732910215790e0c5b']
        self.description = "common mimetype library"
        self.defaultTarget = '1.1'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["win32libs/gettext"] = "default"
        self.runtimeDependencies["win32libs/libxml2"] = "default"
        self.runtimeDependencies["gnuwin32/sed"] = "default"


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        # adjust some vars for proper compile
        GLIB_VER = "2.24.0"
        self.glibDir = os.path.join(self.sourceDir(), "..", "glib-" + GLIB_VER);
        self.subinfo.options.configure.args = " -DGLIB_DIR=%s " % self.glibDir.replace("\\", "/")

    def sedFile(self, directory, fileName, sedcommand):
        """ runs the given sed command on the given file """
        olddir = os.getcwd()
        try:
            os.chdir(directory)
            backup = "%s.orig" % fileName
            if (os.path.isfile(backup)):
                os.remove(backup)

            command = "sed -i.orig %s %s" % (sedcommand, fileName)

            utils.system(command)
        finally:
            os.chdir(olddir)

    def unpack(self):
        if (not CMakePackageBase.unpack(self)):
            return False;
        # rename config.h and glibconfig.h.win32 in glib to
        # avoid config.h confusion
        p = re.compile('.*\.[ch]$')
        sedcmd = r"""-e "s/config.h/config.h.win32/" """
        directory = os.path.join(self.glibDir, "glib")
        if (os.path.exists(directory)):
            for root, dirs, files in os.walk(directory, topdown=False):
                print(root)
                for name in files:
                    if (p.match(name)):
                        self.sedFile(root, name, sedcmd)

        # we have an own cmake script - copy it to the right place
        src = os.path.join(self.packageDir(), "CMakeLists.txt")
        dst = os.path.join(self.sourceDir(), "CMakeLists.txt")
        shutil.copy(src, dst)
        src = os.path.join(self.packageDir(), "FindLibintl.cmake")
        dst = os.path.join(self.sourceDir(), "FindLibintl.cmake")
        shutil.copy(src, dst)

        src = os.path.join(self.packageDir(), "FindKDEWin.cmake")
        dst = os.path.join(self.sourceDir(), "FindKDEWin.cmake")
        shutil.copy(src, dst)

        src = os.path.join(self.packageDir(), "CheckMingwVersion.cmake")
        dst = os.path.join(self.sourceDir(), "CheckMingwVersion.cmake")
        shutil.copy(src, dst)

        src = os.path.join(self.packageDir(), "config.h.cmake")
        dst = os.path.join(self.sourceDir(), "config.h.cmake")
        shutil.copy(src, dst)

        src = os.path.join(self.packageDir(), "dirent.c")
        dst = os.path.join(self.sourceDir(), "dirent.c")
        shutil.copy(src, dst)

        src = os.path.join(self.packageDir(), "unistd.c")
        dst = os.path.join(self.sourceDir(), "unistd.c")
        shutil.copy(src, dst)

        if not os.path.exists(os.path.join(self.sourceDir(), "headers")):
            os.makedirs(os.path.join(self.sourceDir(), "headers"))

        src = os.path.join(self.packageDir(), "dirent.h")
        dst = os.path.join(self.sourceDir(), "headers", "dirent.h")
        shutil.copy(src, dst)

        src = os.path.join(self.packageDir(), "unistd.h")
        dst = os.path.join(self.sourceDir(), "headers", "unistd.h")
        shutil.copy(src, dst)

        utils.applyPatch(self.glibDir, os.path.join(self.packageDir(), "glib-x64.diff"), 0)

        return True

    def install(self):
        if not CMakePackageBase.install(self):
            return False
        if craftCompiler.isMinGW():
            manifest = os.path.join(self.packageDir(), "update-mime-database.exe.manifest")
            executable = os.path.join(self.installDir(), "bin", "update-mime-database.exe")
            utils.embedManifest(executable, manifest)
        return True

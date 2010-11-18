# -*- coding: utf-8 -*-
# kdepim-ce-package.py :
# This package will create a CAB Installer that can be used to install
# Software on Windows CE based on the filename patterns in whitelist.txt

__author__  = "Andre Heinecke <aheinecke@intevation.de>"
__license__ = "GNU General Public License (GPL)"

import info
import compiler
import re
import utils
import os
import shutil
import fileinput
import subprocess

from string import Template
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['de'] = ""
        self.targets['en'] = ""
        self.defaultTarget = 'de'

    def setBuildOptions( self ):
        self.disableHostBuild = True
        self.disableTargetBuild = False

    def setDependencies( self ):
        self.hardDependencies['testing/wincetools'] = 'kdepimcetools'
        self.hardDependencies['testing/setupdll-wince'] = 'default'
        self.hardDependencies['kde/kdepim'] = 'default'
        self.hardDependencies['testing/pinentry-qt'] = 'default'
        if not self.buildTarget == 'en':
            self.hardDependencies['enterprise5/l10n-wce-e5'] = 'default'

class MainPackage(CMakePackageBase):
    def __init__(self):
        self.subinfo = subinfo()
        if not compiler.isMSVC():
            utils.die("Only Microsoft Visual Studio is currently "+
                       "supported for packaging for WinCE.")
        CMakePackageBase.__init__( self )
        self.whitelist = []
        # Add here files that should be loaded into the high memory slots
        self.loader_executables = [ "bin\\kmail-mobile.exe",
                                    "bin\\kaddressbook-mobile.exe",
                                    "bin\\korganizer-mobile.exe",
                                    "bin\\notes-mobile.exe",
                                    "bin\\tasks-mobile.exe" ]
        # Icons for the Start Menu
        self.menu_icons = [ "contacts-90.png",
                            "mail-90.png",
                            "notes-90.png",
                            "organizer-90.png",
                            "tasks-90.png" ]
    def execute(self):
        (command, option) = self.getAction()
        if self.isHostBuild(): return True
        if command == "compile":
            whitelist = "whitelist.txt"
            whitelist = os.path.join(self.packageDir(), whitelist)
            utils.info("Reading whitelist from %s" % whitelist)
            self.read_whitelist(whitelist)
            if self.buildTarget == 'de':
                whitelist = "whitelist_de.txt"
                whitelist = os.path.join(self.packageDir(), whitelist)
                utils.info("Reading additonal locale whitelist from %s" %\
                        whitelist)
                self.read_whitelist(whitelist)
            utils.info("Copying files")
            self.copy_files()
            return True
        if command == "install":
            self.createCab(self.generateCabIni())
            return True
        return self.runAction(command) == 0

    def whitelisted(self, pathname):
        ''' Return true if pathname matches a pattern in self.whitelist '''
        for pattern in self.whitelist:
            if pattern.search(pathname):
                return True
        return False

    def read_whitelist(self, fname):
        ''' Read regular expressions from fname '''
        if not os.path.isfile(fname):
            utils.die("Whitelist not found at: %s" % \
                     os.path.abspath(fname))
            return False
        for line in fileinput.input(fname):
            # Cleanup white spaces / line endings
            line = line.splitlines()
            line = line[0].rstrip()
            if line.startswith("#") or len(line) == 0:
                continue
            try:
                exp = re.compile(re.escape(os.path.join(self.rootdir,
                          os.environ["EMERGE_TARGET_PLATFORM"])+ os.path.sep)\
                          + line)
                self.whitelist.append(exp)
                utils.debug("%s added to whitelist as %s" % (line,
                    exp.pattern), 2)
            except:
                utils.debug("%s is not a valid regexp" % line, 1)

    def copy_files(self):
        '''
            Copy the binaries for the Package from kderoot to the image
            directory
        '''
        wm_root = os.path.join(self.rootdir,
                os.environ["EMERGE_TARGET_PLATFORM"]) + os.path.sep
        utils.createDir(self.workDir())
        utils.debug("Copying from %s to %s ..." % (wm_root,
            self.workDir()), 1)
        uniquebasenames = []
        unique_names = []
        duplicates = []

        #FIXME do this in the gpg-wce-dev portage
        windir = os.path.join(wm_root, "windows")
        if not os.path.isdir(windir):
            os.mkdir(windir)
        libgcc_src = os.path.join(wm_root, "bin", "libgcc_s_sjlj-1.dll")
        libgcc_tgt = os.path.join(wm_root, "windows", "libgcc_s_sjlj-1.dll")
        utils.copyFile(libgcc_src, libgcc_tgt)

        for entry in self.traverse(wm_root, self.whitelisted):
            if os.path.basename(entry) in uniquebasenames:
                utils.debug("Found duplicate filename: %s" % \
                        os.path.basename(entry), 2)
                duplicates.append(entry)
            else:
                unique_names.append(entry)
                uniquebasenames.append(os.path.basename(entry))

        for entry in unique_names:
            entry_target = entry.replace(wm_root,
                    os.path.join(self.workDir()+"\\"))
            if not os.path.exists(os.path.dirname(entry_target)):
                utils.createDir(os.path.dirname(entry_target))
            shutil.copy(entry, entry_target)
            utils.debug("Copied %s to %s" % (entry, entry_target),2)
        dups=0
        for entry in duplicates:
            entry_target = entry.replace(wm_root,
                    os.path.join(self.workDir()+"\\"))
            entry_target = "%s_dup%d" % (entry_target, dups)
            dups += 1
            if not os.path.exists(os.path.dirname(entry_target)):
                utils.createDir(os.path.dirname(entry_target))
            shutil.copy(entry, entry_target)
            utils.debug("Copied %s to %s" % (entry, entry_target), 2)

        # Handle special cases
        pinentry = os.path.join(wm_root, "bin", "pinentry-qt.exe")
        utils.copyFile(pinentry, os.path.join(self.workDir(), "bin",
                "pinentry.exe"))

        #The Kolab icon is in hicolor but we only package oxygen for CE
        kolabicon = os.path.join(wm_root, "share", "icons", "hicolor",
                                 "64x64", "apps", "kolab.png")
        utils.copyFile(kolabicon, os.path.join(self.workDir(), "share",
                       "icons", "oxygen", "64x64", "apps", "kolab.png"))

        # Drivers need to be installed in the Windows direcotry
        gpgcedev = os.path.join(wm_root, "bin", "gpgcedev.dll")
        if not os.path.isdir(os.path.join(self.workDir(), "windows")):
            os.mkdir(os.path.join(self.workDir(), "windows"))

        # Create an empty file for DBus and his /etc/dbus-1/session.d
        dbus_session_d = os.path.join(self.workDir(), "etc", "dbus-1",
                "session.d")
        if not os.path.exists(dbus_session_d): os.mkdir(dbus_session_d)
        f = open(os.path.join(dbus_session_d, "stub"), "w")
        f.close()
        # Rename applications that should be started by the loader
        for f in self.loader_executables:
            path2file = os.path.join(wm_root, f)
            if not os.path.isfile(path2file):
                utils.debug("Createloaderfiles: Could not find %s at %s " % \
                        (f, path2file))
                continue
            realpath = path2file.replace(f, os.path.splitext(f)[0] +
                    "-real.exe")
            shutil.copy(path2file, realpath.replace(wm_root,
                    os.path.join(self.workDir()+"\\")))
            customloader = path2file.replace(f, os.path.splitext(f)[0] +
                    "-loader.exe")
            defaultloader = os.path.join(wm_root, "bin", "himemce.exe")
            path2file = path2file.replace(wm_root,
                    os.path.join(self.workDir()+"\\"))
            if os.path.isfile(customloader):
                shutil.copy(customloader, path2file)
            elif os.path.isfile(defaultloader):
                shutil.copy(defaultloader, path2file)
            else:
                utils.die("Trying to use the custom loader but no loader \
found in: %s \n Please ensure that package wincetools is installed" %\
                os.path.join(wm_root, "bin"))
        # Add start menu icons to the Package
        for f in self.menu_icons:
            path2file = os.path.join(self.packageDir(), "icons", f)
            if os.path.isfile(path2file):
                utils.copyFile(path2file, os.path.join(self.workDir(),
                    "share", "icons"))
            else:
                utils.debug("Failed to copy %s not a file: %s" % path2file, 1)

        # Configure localization
        if self.buildTarget == 'de':
            confdir = os.path.join(self.workDir(), "share", "config")
            if not os.path.isdir(confdir):
                os.makedirs(confdir)
            with open(os.path.join(confdir, "kdeglobals"),"w") as f:
                f.write('[Locale]\n')
                f.write('Country=de\n')
                f.write('Language=de\n')

    def traverse(self, directory, whitelist = lambda f: True):
        '''
            Traverse through a directory tree and return every
            filename that the function whitelist returns as true
        '''
        dirs = [ directory ]
        while dirs:
            path = dirs.pop()
            for f in os.listdir(path):
                f = os.path.join(path, f)
                if os.path.isdir(f):
                    dirs.append(f)
                elif os.path.isfile(f) and whitelist(f):
                    yield f

    def createCab(self, cab_ini):
        ''' Create a cab file from cab_ini using Microsoft Cabwizard '''
        cabwiz = os.path.join(os.getenv("TARGET_SDKDIR"), "..", "Tools",
                              "CabWiz", "Cabwiz.exe")
        output = os.getenv("EMERGE_PKGDSTDIR", os.path.join(self.imageDir(),
                           "packages"))
        if not os.path.exists(output):
            utils.createDir(output)
        elif not os.path.isdir(output):
            utils.die("Outputpath %s can not be accessed." % output)
        args = [cabwiz, cab_ini, "/dest", output, "/compress"]
        utils.debug("Calling Microsoft Cabwizard: %s" % cabwiz, 2)
        retcode = subprocess.call(args)
        return retcode == 0

    def generateCabIni(self):
        '''
            Package specific configuration data that is used as input for 
            MS Cab Wizard
        '''
        with open(
            os.path.join(self.packageDir(), "cab_template.inf"),"r") as f:
            cabtemplate = Template(f.read())

        sourcedisknames = {}
        sourcediskfiles = []
        files           = {}

        for f in self.traverse(self.workDir()):
            dir_id = sourcedisknames.setdefault(
                os.path.dirname(f), len(sourcedisknames)+1)
            sourcediskfiles.append("%s=%d" % (os.path.basename(f), dir_id))
            files.setdefault(dir_id, []).append(os.path.basename(f))


        destinationdirs = [
            (d.endswith("windows") and "a%d = 0,\\%s"
                    or "a%d = 0,%%CE1%%\\Kontact-Mobile%s") % (
                dir_id, d.replace(self.workDir(), ""))
                for d, dir_id in sourcedisknames.iteritems()]

        sourcedisknames = ["%d=,,,%s" % (dir_id, d) 
            for d, dir_id in sourcedisknames.iteritems()]

        rn = "\r\n".join

        sections = []
        for dir_id in files.iterkeys():
            sections.append("[a%d]\r\n" % dir_id)
            for f in files.get(dir_id):
                sections.append("%s,%s,,0\r\n" % (re.sub("_dup[0-9]+","",f), f))
       # sections = ["[a%d]\r\n%s,%s,,0" % (dir_id, rn(replace(fs)), fs)
       #     for dir_id, fs in files.iteritems()]
        sectionnames = ["a%d" % dir_id for dir_id in files.iterkeys()]

        with open(os.path.join(self.workDir(), "..", "Kontact-Mobile.inf"),
                "wb") as output:
            print >> output, cabtemplate.substitute(
               SOURCEDISKNAMES = rn(sourcedisknames),
               SOURCEDISKFILES = rn(sourcediskfiles),
               DESTINATIONDIRS = rn(destinationdirs),
               SECTIONS        = "".join(sections),
               SECTIONNAMES    = ", ".join(sectionnames))
            return output.name

if __name__ == '__main__':
    MainPackage().execute()

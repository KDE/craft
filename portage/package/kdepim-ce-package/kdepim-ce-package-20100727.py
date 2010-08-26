# -*- coding: utf-8 -*-
# kdepim-ce-package.py :
# This package will create a CAB Installer that can be used to install
# Software on Windows CE based on the filename patterns in whitelist.txt

# TODO: Make the WinCE build dir configurable currently WM65 is hardcoded

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
        self.targets['0'] = ""
        self.defaultTarget = '0'

    def setBuildOptions( self ):
        self.disableHostBuild = True
        self.disableTargetBuild = False

    def setDependencies( self ):
        self.hardDependencies['kde/kdepim'] = 'default'

class MainPackage(CMakePackageBase):
    def __init__(self):
        self.subinfo = subinfo()
        if not compiler.isMSVC():
            utils.die("Only Microsoft Visual Studio is currently "+
                       "supported for packaging for WinCE.")
        CMakePackageBase.__init__( self )
        self.whitelist = []

    def execute(self):
        (command, option) = self.getAction()
        if command == "compile":
            whitelist = "whitelist.txt"
            whitelist = os.path.join(self.packageDir(), whitelist)
            utils.info("Reading whitelist from %s" % whitelist)
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
                          "WM65")+ os.path.sep) + line)
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
        wm_root = os.path.join(self.rootdir, "WM65") + os.path.sep
        utils.createDir(self.workDir())
        utils.debug("Copying from %s to %s ..." % (wm_root,
            self.workDir()), 1)
        uniquebasenames = []
        unique_names = []
        duplicates = []

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

        # Create an empty file for DBus and his /etc/dbus-1/session.d
        dbus_session_d = os.path.join(self.workDir(), "etc", "dbus-1",
                "session.d")
        os.mkdir(dbus_session_d)
        f = open(os.path.join(dbus_session_d, "stub"), "w")
        f.close()

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

        destinationdirs = ["a%d = 0,%%InstallDir%%%s" % (
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

        with open(os.path.join(self.workDir(), "Kontact-Mobile.inf"), "wb") \
            as output:
            print >> output, cabtemplate.substitute(
               SOURCEDISKNAMES = rn(sourcedisknames),
               SOURCEDISKFILES = rn(sourcediskfiles),
               DESTINATIONDIRS = rn(destinationdirs),
               SECTIONS        = "".join(sections),
               SECTIONNAMES    = ", ".join(sectionnames))
            return output.name

if __name__ == '__main__':
    MainPackage().execute()

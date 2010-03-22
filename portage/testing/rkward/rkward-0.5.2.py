# -*- coding: utf-8 -*-
import base
import utils
import os
import sys
import info
import xml.dom.minidom
import subprocess

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'http://rkward.svn.sourceforge.net/svnroot/rkward/trunk/rkward'
        # no "release" targets defined, yet. Releases up to RKWard 0.5.2 (current) had an additional dependency on PHP, which we do not provide
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.hardDependencies['testing/r-base'] = 'default'
        self.hardDependencies['kde/kdebase-runtime'] = 'default'

# TODO:
# - Move files out of the way that are already provided by dependencies:
#     - lib\R\library\R.css
#     - share\apps\katepart\syntax\r.xml
#     - When to do this? Safely possible within install, or can that go directly into KDEROOT at times?
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()

    # What is the recommended way to fetch SVN sources from a repository that is not on the KDE SVN server?
    def fetch( self ):
        ok = utils.svnFetch (self.subinfo.svnTargets['svnHEAD'], self.svndir)
        # This is plainly wrong, but somehow ok is False even though the checkout/update succeeded. Why?
        return True

    def realSvnPath( self ):
        return os.path.join (self.svndir, "rkward")

    def unpack( self ):
        utils.cleanDirectory( self.workdir )	# side-effect of creating the dir, if needed
        return True

    def compile( self ):
        self.kde.sourcePath = self.realSvnPath()
        return self.kde.kdeCompile(" -DR_EXECUTABLE=" + self.rootdir + "/lib/R/bin/R.exe")

    def install( self ):
        return self.kde.kdeInstall()

    def getSvnVersion( self ):
        svninfo = subprocess.Popen(['svn', 'info', '--xml', self.realSvnPath()], shell=True, stdout=subprocess.PIPE).communicate()[0]
        doc = xml.dom.minidom.parseString(svninfo)
        latestcommit = doc.getElementsByTagName("commit")[0]
        rev = latestcommit.getAttribute("revision")
        if rev == "":
            rev = "-unknown"
        return "svn" + rev

    def make_package( self ):
        # I'm sure this is not the right way to do it, but then, what is the right way?
        self.kde.kdesvndir = ""
        self.kde.kdeSvnPath = self.realSvnPath # NOTE: We are assinging the function, here, not the return value.

        if not self.buildTarget == 'svnHEAD':
            return self.doPackaging( "rkward", self.buildTarget, True )
        else:
            return self.doPackaging( "rkward", self.getSvnVersion(), True )

if __name__ == '__main__':
    subclass().execute()

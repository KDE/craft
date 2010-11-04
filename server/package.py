# copyright 2009 Patrick Spendrin <ps_ml@gmx.de>
# License: BSD

import os
import sys
import subprocess
import time     # for sleep
from datetime import datetime

# our own headers
from notifications import *
import common

def die( message ):
    log.write( message )
    print >> sys.stderr, "package.py fatal error: %s" % message
    exit( 1 )

class BuildError( Exception ):
    """ this exception handles the error reporting """
    
    def __init__( self, packageName, message, logfile ):
        self.packageName = packageName
        self.messageText = message
        self.logfile = logfile
        self.revision = False
        self.enabled = True
        print "Error:", self.messageText
        
    def __str__( self ):
        log = file( self.logfile, 'rb' )
        logtext = log.readlines()[-20:]
        log.close()
        return "Error:" + "".join( logtext )

class package:
    """ one object for each package to be build 
        it contains all the information needed to build """
        
    def __init__( self, category, packagename, target, patchlevel ):
        self.category = category
        self.packageName = packagename
        self.cleanPackageName = category + "_" + packagename
        if target:
            self.target = "--target=%s " % target
        else:
            self.target = ""
        self.patchlevel = patchlevel
        self.revision = None
        self.generalSettings = common.settings.getSection( 'General', { 'package': self.cleanPackageName,
                                                                        'pkgdstdir': packageroot,
                                                                        'logdstdir': logroot } )
                                                    
        self.logfile = outfile % (self.generalSettings["platform"], self.cleanPackageName)
        log = file( self.logfile, 'wb+' )
        log.close()
        self.notifications = { 'email': EmailNotification( self.category, self.packageName, self.logfile ),
                               'dashboard': DashboardNotification( self.category, self.packageName, self.logfile ),
                               'logupload': LogUploadNotification( self.category, self.packageName, self.logfile ) }

        self.enabled = True
    
    def timeStamp( self ):
        datetime.now().strftime("%m/%d/%Y %H:%M")
        log = file( self.logfile, 'ab+' )
        log.write( datetime.now().strftime("%m/%d/%Y %H:%M") )
        log.close()

    def getRevision( self ):
        """ runs emerge --print-revision for a specific package and returns the output """
        ## this function must replaced in case we are using the emerge API directly
        if not self.revision:
            tempfile = file( os.path.join( logroot, "rev.tmp" ), "wb+" )
            tempfile.close()
            if not self.system( "--print-revision %s%s/%s" % ( self.target, self.category, self.packageName ), os.path.join( logroot, "rev.tmp" ) ):
                return ""
            tempfile = file( os.path.join( logroot, "rev.tmp" ), "rb+" )
            self.revision = tempfile.readline()
            tempfile.close()
            os.remove( os.path.join( logroot, "rev.tmp" ) )
        return self.revision
        
    def system( self, cmdstring, logfile ):
        """ runs an emerge command """
        cmdstring = emerge + " " + cmdstring
        fstderr = file( logfile + ".tmp", 'wb+' )
        p = subprocess.Popen( cmdstring, shell=True, stdout=fstderr, stderr=fstderr )
        ret = p.wait()
        log = file( logfile, 'ab+' )
        fstderr.seek( os.SEEK_SET )
        for line in fstderr:
            log.write( line )
        fstderr.close()
        log.close()
        return ( ret == 0 )

    def emerge( self, cmd, addParameters = "" ):
        """ runs an emerge call """
        print "running:", cmd, self.packageName
        if self.enabled and not self.system( "--" + cmd + addParameters + " %s%s/%s" % ( self.target, self.category, self.packageName ), self.logfile ):
            self.enabled = False
            raise BuildError( self.cleanPackageName, "%s " % self.cleanPackageName + cmd + " FAILED", self.logfile )
        
    def fetch( self ):
        """ fetches and unpacks; make sure that all packages are fetched & unpacked 
            correctly before they are used """
        self.timestamp()
        self.emerge( "fetch" )
        
    def build( self ):
        """ builds and installs packages locally """
        self.timestamp()
        self.emerge( "unpack" )
        self.emerge( "compile", " -i" )
        self.emerge( "install" )
        self.emerge( "manifest" )
        self.emerge( "qmerge" )
        
    def test( self ):
        """ runs unittests and submits them to cdash server """
        self.timestamp()
        self.emerge( "test" )

    def package( self ):
        """ packages into subdirectories of the normal directory - this helps to keep the directory clean """
        if not self.enabled:
            return

        self.timestamp()
        os.environ["EMERGE_PKGDSTDIR"] = os.path.join( self.generalSettings["pkgdstdir"], self.cleanPackageName )
        
        if not os.path.exists( os.environ["EMERGE_PKGDSTDIR"] ):
            os.mkdir( os.environ["EMERGE_PKGDSTDIR"] )
        
        self.emerge( "package", " --patchlevel=%s" % self.patchlevel )
        
        # cleanup behind us
        del os.environ["EMERGE_PKGDSTDIR"]
        
    def upload( self ):
        """ uploads packages to winkde server """
        if not self.enabled:
            return

        self.timestamp()
        print "running: upload", self.packageName
        upload = common.Uploader( logfile=self.logfile )
        
        pkgdir = os.path.join( self.generalSettings["pkgdstdir"], self.cleanPackageName )
        if os.path.exists( pkgdir ):
            """ if there is a directory at the specified location, upload files that can be found there """
            os.chdir( pkgdir )
            filelist = os.listdir( pkgdir )
            
            ret = 0
            for entry in filelist:
                upload.upload( os.path.join( pkgdir, entry ) )
            
            if not ret == 0:
                raise BuildError( self.cleanPackageName, "%s " % self.cleanPackageName + " upload FAILED\n", self.logfile )
        else:
            log = file( self.logfile, 'ab+' )
            log.write( "Package directory doesn't exist:\n"
                       "Package directory is %s" % pkgdir )


general = common.settings.getSection( "General" )

if "logdstdir" in general:
    logroot = general["logdstdir"]
else:
    logroot = os.path.join( general["kderoot"], "tmp", common.isodate, "logs" )
if "pkgdstdir" in general:
    packageroot = general["pkgdstdir"]
else:
    packageroot = os.path.join( general["kderoot"], "tmp", common.isodate, "packages" )
if not os.path.exists( logroot ):
    os.makedirs( logroot )
if not os.path.exists( packageroot ):
    os.makedirs( packageroot )

outfile = os.path.join( logroot, "log-%s-%s.txt" )
emerge = os.path.join( general["kderoot"], "emerge", "bin", "emerge.py" )

packagelist = []
if len(sys.argv) <= 1:
    print "please add the path to the packagelist file as only argument"
    time.sleep(6)
    exit( 0 )
    
packagefile = file( sys.argv[1] )
for line in packagefile:
    if not line.startswith( '#' ):
        entry = line.strip().split( ',' )
        packagelist.append( package( entry[0], entry[1], entry[2], entry[3] ) )
packagefile.close()

common.Uploader().executeScript("prepare")
for entry in packagelist:
    try:
        entry.fetch()
        entry.getRevision()
    except BuildError:
        entry.enabled = False
        for i in entry.notifications:
            if i == 'dashboard': continue
            entry.notifications[i].error = True
            entry.notifications[i].run()

for entry in packagelist:
    try:
        enabled = entry.enabled
        entry.build()
    except BuildError:
        entry.enabled = False
        for i in entry.notifications:
            entry.notifications[i].error = True
    finally:
        for i in entry.notifications:
            if enabled: entry.notifications[i].run( entry.getRevision() )

for entry in packagelist:
    try:
        enabled = entry.enabled
        entry.package()
    except BuildError:
        entry.enabled = False
        for i in entry.notifications:
            if i == 'dashboard': continue
            entry.notifications[i].error = True
            if enabled: entry.notifications[i].run( entry.getRevision() )

for entry in packagelist:
    try:
        enabled = entry.enabled
        entry.upload()
    except BuildError:
        entry.enabled = False
        for i in entry.notifications:
            if i == 'dashboard': continue
            entry.notifications[i].error = True
            if enabled: entry.notifications[i].run( entry.getRevision() )
common.Uploader().executeScript("finish")

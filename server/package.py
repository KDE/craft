import os
import sys
import subprocess
import smtplib
import datetime
from email.mime.text import MIMEText

def die( message ):
    log.write( message )
    print >> sys.stderr, "package.py fatal error: %s" % message
    exit( 1 )

class BuildError(Exception):
    """ this exception handles the error reporting """
    
    def __init__( self, packageName, message, logfile ):
        self.packageName = packageName
        self.messageText = message
        self.logfile = logfile
        self.revision = False
        print "Error:", self.messageText
        
    def __str__( self ):
        log = file( self.logfile, 'rb' )
        logtext = log.readlines()[-20:]
        log.close()
        return "Error:" + "".join( logtext )
        
    def sendNotification( self, revision=False ):
        """ this is used to send emails to """
        if "EMERGE_SERVER_SERVER" in os.environ and \
           "EMERGE_SERVER_SENDER" in os.environ and \
           "EMERGE_SERVER_RECEIVERS" in os.environ and \
           "EMERGE_SERVER_PASS" in os.environ:
            server = os.environ["EMERGE_SERVER_SERVER"]
            sender = os.environ["EMERGE_SERVER_SENDER"]
            pw = os.environ["EMERGE_SERVER_PASS"]
            receivers = os.environ["EMERGE_SERVER_RECEIVERS"].split(',')
            self.revision = revision
            self.email( server, sender, pw, receivers )
        
    def email( self, server, sender, pw, receivers ):
        """ send an email"""
        log = file( self.logfile, 'rb' )
        logtext = log.readlines()[-20:]
        log.close()

        # Create a text/plain message
        msg = MIMEText( self.messageText + """\n
        """ + "".join( logtext ) )

        # me == the sender's email address
        # you == the recipient's email address
        subject = 'Build error in %s on %s' % ( self.packageName, os.environ["KDECOMPILER"] )
        if self.revision:
            subject += ' in revision %s' % self.revision.strip()

        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = receivers[0]
        
        server = smtplib.SMTP( server )
        # server.set_debuglevel(True) # set debuglevel to see that mail can be sent

        server.starttls()

        server.login( sender, pw )

        server.sendmail( sender, receivers, msg.as_string() )
        server.quit()


class package:
    """ one object for each package to be build 
        it contains all the information needed to build """
        
    def __init__( self, packagename, target, patchlevel ):
        self.packageName = packagename
        if target:
            self.target = "--target=%s " % target
        else:
            self.target = ""
        self.patchlevel = patchlevel
        self.logfile = outfile % packagename.replace( '/', '_' )
        if os.path.exists( self.logfile ):
            os.remove( self.logfile )
        self.enabled = True
    
    def getRevision( self ):
        """ runs emerge --print-revision for a specific package and returns the output """
        ## this function must replaced in case we are using the emerge API directly
        revision = ""
        tempfile = file( os.path.join( logroot, "rev.tmp" ), "wb+" )
        tempfile.close()
        if not self.system( "--print-revision %s%s" % ( self.target, self.packageName ), os.path.join( logroot, "rev.tmp" ) ):
            return ""
        tempfile = file( os.path.join( logroot, "rev.tmp" ), "rb+" )
        revision = tempfile.readline()
        tempfile.close()
        os.remove( os.path.join( logroot, "rev.tmp" ) )
        return revision
        
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
        if self.enabled and not self.system( "--" + cmd + addParameters + " %s%s" % ( self.target, self.packageName ), self.logfile ):
            self.enabled = False
            raise BuildError( self.packageName, "%s " % self.packageName + cmd + " FAILED", self.logfile )
        
    def fetch( self ):
        """ fetches and unpacks; make sure that all packages are fetched & unpacked 
            correctly before they are used """
        self.emerge( "fetch" )
        
    def build( self ):
        """ builds and installs packages locally """
        self.emerge( "unpack" )
        self.emerge( "compile", " -i" )
        self.emerge( "install" )
        self.emerge( "manifest" )
        self.emerge( "qmerge" )
        
    def test( self ):
        """ runs unittests and submits them to cdash server """
        self.emerge( "test" )

    def package( self ):
        """ packages into subdirectories of the normal directory - this helps to keep the directory clean """
        if not self.enabled:
            return

        if "EMERGE_PKGDSTDIR" in os.environ:
            outputBase = os.environ["EMERGE_PKGDSTDIR"]
            oldDstDir = os.environ["EMERGE_PKGDSTDIR"]
        else:
            oldDstDir = ""
            outputBase = packageroot
        os.environ["EMERGE_PKGDSTDIR"] = os.path.join( outputBase, self.packageName.replace( '/', '_' ) )
        
        if not os.path.exists( os.environ["EMERGE_PKGDSTDIR"] ):
            os.mkdir( os.environ["EMERGE_PKGDSTDIR"] )
        
        self.emerge( "package", " --patchlevel=%s" % self.patchlevel )
        os.environ["EMERGE_PKGDSTDIR"] = oldDstDir
        
    def upload( self ):
        """ uploads packages to winkde server """
        if not self.enabled:
            return
        print "uploading"
        if "EMERGE_PKGDSTDIR" in os.environ:
            outputBase = os.environ["EMERGE_PKGDSTDIR"]
            oldDstDir = os.environ["EMERGE_PKGDSTDIR"]
        else:
            oldDstDir = ""
            outputBase = packageroot
        pkgdir = os.path.join( outputBase, self.packageName.replace( '/', '_' ) )
        if os.path.exists( pkgdir ) and \
           "EMERGE_SERVER_UPLOAD_SERVER" in os.environ and\
           "EMERGE_SERVER_UPLOAD_DIR" in os.environ:
            """ if there is a directory at the specified location, upload files that can be found there """
            os.chdir( pkgdir )
            filelist = os.listdir( pkgdir )
            
            for entry in os.listdir( pkgdir ):
                """ check that all things that are uploaded are files """
                if os.path.isdir( entry ):
                    filelist.remove( entry )

            cmdstring = "psftp " + os.environ["EMERGE_SERVER_UPLOAD_SERVER"]
            ret = 0
            fstderr = file( self.logfile + ".tmp", 'wb+' )
            p = subprocess.Popen( cmdstring, shell=True, stdin=subprocess.PIPE, stdout=fstderr, stderr=fstderr )
            
            fstderr.write( "cd " + os.environ["EMERGE_SERVER_UPLOAD_DIR"] + "\r\n" )
            fstderr.flush()
            p.stdin.write( "cd " + os.environ["EMERGE_SERVER_UPLOAD_DIR"] + "\r\n" )

            fstderr.write( "mput " + " ".join( filelist ) + "\r\n" )
            fstderr.flush()
            p.stdin.write( "mput " + " ".join( filelist ) + "\r\n" )
            
            fstderr.write( "quit\r\n" )
            fstderr.flush()
            p.stdin.write( "quit\r\n" )
            ret = p.wait()
            log = file( self.logfile, 'ab+' )
            fstderr.seek( os.SEEK_SET )
            for line in fstderr:
                log.write( line )
            fstderr.close()
            log.close()
            if not ret == 0:
                raise BuildError( self.packageName, "%s " % self.packageName + " upload FAILED\n", self.logfile )
        else:
            log = file( self.logfile, 'ab+' )
            log.write("Package directory doesn't exist or EMERGE_SERVER_UPLOAD_SERVER or EMERGE_SERVER_UPLOAD_DIR are not set:\n"
                      "Package directory is %s" % pkgdir )
        os.environ["EMERGE_PKGDSTDIR"] = oldDstDir


isodate = str( datetime.date.today() ).replace('-', '')
logroot = os.path.join( os.environ["KDEROOT"], "tmp", isodate, "logs" )
packageroot = os.path.join( os.environ["KDEROOT"], "tmp", isodate, "packages" )

if not os.path.exists( logroot ):
    os.makedirs( logroot )

outfile = os.path.join( logroot, "log-%s.txt" )
emerge = os.path.join( os.environ["KDEROOT"], "emerge", "bin", "emerge.py" )

packagelist = []
if len(sys.argv) <= 1:
    print "please add the path to the packagelist file as only argument"
    exit( 0 )
    
packagefile = file( sys.argv[1] )
for line in packagefile:
    if not line.startswith( '#' ):
        entry = line.strip().split( ',' )
        packagelist.append( package( entry[0], entry[1], entry[2] ) )
packagefile.close()

for entry in packagelist:
    try:
        entry.fetch()
    except BuildError, ( instance ):
        instance.sendNotification()

for entry in packagelist:
    try:
        entry.build()
    except BuildError, ( instance ):
        entry.enabled = False
        instance.sendNotification( entry.getRevision() )

for entry in packagelist:
    try:
        entry.package()
    except BuildError, ( instance ):
        entry.enabled = False
        instance.sendNotification( entry.getRevision() )

for entry in packagelist:
    try:
        entry.upload()
    except BuildError, ( instance ):
        instance.sendNotification( entry.getRevision() )

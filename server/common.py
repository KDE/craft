# copyright 2009; 2010 Patrick Spendrin <ps_ml@gmx.de>
# License: BSD
import os
import sys
from datetime import date, datetime
from ConfigParser import ConfigParser
import subprocess
import time

isodate = str( date.today() ).replace( '-', '' )
isodatetime = datetime.now().strftime("%Y%m%d%H%M")

class Settings:
    def __init__( self ):
        # this means emerge/server/../../etc/emergeserver.conf
        self.configpath = os.path.normpath(os.path.join(os.path.dirname(sys.argv[0]), "..", "..", "etc", "emergeserver.conf"))
        defaults = dict()
        defaults["isodate"] = isodate
        defaults["release"] = isodate
        defaults["ftpclient"] = "psftp"
        defaults["sshclient"] = "plink"
        self.parser = ConfigParser( defaults )
        self.sections = dict()
        if os.path.exists( self.configpath ):
            self.parser.read( self.configpath )
            if not self.parser.has_section('General'):
                # enable all other sections
                for sec in self.parser.sections():
                    self.sections[sec] = True
            else:
                for sec in self.parser.sections():
                    if self.parser.has_option('General', 'enable-' + sec.lower()):
                        try:
                            self.sections[sec] = self.parser.getboolean('General', 'enable-' + sec.lower())
                        except:
                            self.sections[sec] = False
                    else:
                        self.sections[sec] = True
            self.enabled = True
        else:
            self.enabled = False
            
    def getSection( self, section, additionalvars=None ):
        if self.enabled and self.sections[section]:
            return dict( self.parser.items(section, False, additionalvars) )
        else:
            return False
            
    def getOption( self, section, option, additionalvars=None ):
        if self.enabled and self.sections[section]:
            return self.parser.get(section, option, False, additionalvars )
        else:
            return False

settings = Settings()

class Uploader:
    def __init__( self, category='Upload', logfile=None ):
        self.category = category
        self.logfile = logfile
        
        self.fstderr = sys.stderr
        self.pstdin = None
        
    def ftpExecute( self, cmd ):
        self.fstderr.write( cmd + "\r\n" )
        self.fstderr.flush()
        self.pstdin.write( cmd + "\r\n" )        

    def executeScript( self, state="common" ):
        self.settings = settings.getSection( self.category )
        if not self.settings:
            print "upload disabled!"
            return False

        name = state+"-script"
        if name in self.settings:
            self.fstderr = file( 'NUL', 'wb+' )
            cmdstring = self.settings["sshclient"] + " " + self.settings["server"]
            p = subprocess.Popen( cmdstring, shell=True, stdin=subprocess.PIPE, stdout=self.fstderr, stderr=self.fstderr )
            self.pstdin = p.stdin
            p.stdin.write( self.settings[ name ] + "\n" )
            p.stdin.write( "exit\n" )
            ret = p.wait()

            return ret == 0
        else:
            print "no config for " + name + " found!"
        return True

    def upload( self, sourcefilename ):
        self.settings = settings.getSection( self.category )
        if not self.settings:
            """ return True because we're probably simply disabled and we do not want to result in an error """
            print "upload disabled!"
            return True
            
        if not ( "server" in self.settings and "directory" in self.settings ):
            print "server or directory not set"
            return False

        if os.path.isdir( sourcefilename ):
            print "sourcefile is a directory"
            return False

        cmdstring = self.settings[ "ftpclient" ] + " " + self.settings[ "server" ]
        ret = 0
        if self.logfile:
            fstderr = file( self.logfile + ".tmp", 'wb+' )
        else:
            fstderr = file( 'NUL', 'wb+' )
        p = subprocess.Popen( cmdstring, shell=True, stdin=subprocess.PIPE, stdout=fstderr, stderr=fstderr )
        self.fstderr = fstderr
        self.pstdin = p.stdin
        
        for dir in self.settings[ "directory" ].split( '/' ):
            self.ftpExecute( "cd " + dir )

        self.ftpExecute( "put " + sourcefilename )
        self.ftpExecute( "quit" )

        ret = p.wait()

        if self.logfile:
            log = file( self.logfile, 'ab+' )
            fstderr.seek( os.SEEK_SET )
            for line in fstderr:
                log.write( line )
            fstderr.close()
            log.close()

        return ret == 0

class SourceForgeUploader ( Uploader ):
    def __init__( self, packageName, packageVersion, category='SFUpload', logfile=None ):
        Uploader.__init__( self, category, logfile )
        self.category = category
        self.logfile = logfile
        if packageName.endswith("-src"):
            packageName = packageName[:-4]
        self.packageName = packageName
        self.packageVersion = packageVersion
        
        self.settings = settings.getSection( self.category )

        if not self.settings:
            self.disabled = True
        else:
            self.disabled = False

        if not ( "server" in self.settings and "directory" in self.settings ):
            print "server or directory not set"
            self.disabled = True
            return

        cmdstring = self.settings[ "ftpclient" ] + " " + self.settings[ "server" ]
        if self.logfile:
            self.fstderr = file( self.logfile + ".tmp", 'wb+' )
        else:
            self.fstderr = file( 'NUL', 'wb+' )

        self.p = subprocess.Popen( cmdstring, shell=True, stdin=subprocess.PIPE, stdout=self.fstderr, stderr=self.fstderr )
        self.pstdin = self.p.stdin

        directoryName = self.settings[ "directory" ]
        for dir in directoryName.split( '/' ):
            if dir == "":
                dir = "/"
            self.ftpExecute( "cd " + dir )

    def __del__( self ):
        if self.disabled:
            return

        self.ftpExecute( "quit" )
        self.p.wait()

        if self.logfile:
            log = file( self.logfile, 'ab+' )
            self.fstderr.seek( os.SEEK_SET )
            for line in self.fstderr:
                log.write( line )
            self.fstderr.close()
            log.close()
            
        self.ftpExecute( "mkdir " + self.packageName )
        self.ftpExecute( "chmod 775 " + self.packageName )
        self.ftpExecute( "cd " + self.packageName )
        self.ftpExecute( "mkdir " + self.packageVersion )
        self.ftpExecute( "chmod 775 " + self.packageVersion )
        self.ftpExecute( "cd " + self.packageVersion )

    def upload( self, sourcefilename ):
        if self.disabled:
            """ return True because we're probably simply disabled and we do not want to result in an error """
            print "sfupload disabled!"
            return True
            
        if os.path.isdir( sourcefilename ):
            print "sourcefile is a directory"
            return False

        self.ftpExecute( "put " + sourcefilename )
        self.ftpExecute( "chmod 664 " + os.path.basename( sourcefilename ) )

        return ret == 0

if __name__ == '__main__':
    Uploader().executeScript( "test" )
    SourceForgeUploader().upload( "win_iconv", "0.0.1", "C:\\kde\\test.cpp" )
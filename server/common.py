# copyright 2009 Patrick Spendrin <ps_ml@gmx.de>
# License: BSD
import os
import sys
from datetime import date, datetime
from ConfigParser import ConfigParser
import subprocess

isodate = str( date.today() ).replace( '-', '' )
isodatetime = datetime.now().strftime("%Y%m%d%H%M")

class Settings:
    def __init__( self ):
        # this means emerge/server/../../etc/emergeserver.conf
        self.configpath = os.path.normpath(os.path.join(os.path.dirname(sys.argv[0]), "..", "..", "etc", "emergeserver.conf"))
        defaults = dict()
        defaults["isodate"] = isodate
        defaults["ftpclient"] = "psftp"
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
        
    def upload( self, sourcefilename ):
        self.settings = settings.getSection( self.category )
        if not self.settings:
            """ return True because we're probably simply disabled and we do not want to result in an error """
            print "upload disabled!"
            return True
            
        if not ( self.settings["server"] and self.settings["directory"] ):
            print "server or directory not set"
            return False

        if os.path.isdir( sourcefilename ):
            print "sourcefile is a directory"
            return False

        cmdstring = self.settings["ftpclient"] + " " + self.settings["server"]
        ret = 0
        if self.logfile:
            fstderr = file( self.logfile + ".tmp", 'wb+' )
        else:
            fstderr = file( 'NUL', 'wb+' )
        p = subprocess.Popen( cmdstring, shell=True, stdin=subprocess.PIPE, stdout=fstderr, stderr=fstderr )
        
        for dir in self.settings["directory"].split('/'):
            p.stdin.write( "mkdir " + dir + "\r\n" )
            fstderr.write( "cd " + dir + "\r\n" )
            fstderr.flush()
            p.stdin.write( "cd " + dir + "\r\n" )

        fstderr.write( "put " + sourcefilename + "\r\n" )
        fstderr.flush()
        p.stdin.write( "put " + sourcefilename + "\r\n" )
        
        fstderr.write( "quit\r\n" )
        fstderr.flush()
        p.stdin.write( "quit\r\n" )
        ret = p.wait()

        if self.logfile:
            log = file( self.logfile, 'ab+' )
            fstderr.seek( os.SEEK_SET )
            for line in fstderr:
                log.write( line )
            fstderr.close()
            log.close()

        return ret == 0

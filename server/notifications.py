# copyright 2009 Patrick Spendrin <ps_ml@gmx.de>
# License: BSD
import os
from email.mime.text import MIMEText
import common
import smtplib
import urllib
import urllib2
import json

class Notification:
    """ this class is the base class for notifications """
    def __init__( self, category, packageName, logfile, error=False ):
        self.category = category
        self.logfile = logfile
        self.packageName = packageName
        # expect that if there is no error, there is no error ;-)
        self.error = error

        self.settings = common.settings.getSection( "Notification" )
        self.dryRun = False

    def setShortLog( self ):
        log = file( self.logfile, 'rb' )
        logtext = log.readlines()[-20:]
        log.close()
        if self.error:
            self.shortLog = "".join( logtext )
        else:
            self.shortLog = ""
    
    def run( self, revision = None ):
        pass

class EmailNotification(Notification):
    """ send an email """
    def run( self, revision = None ):
        settings = common.settings.getSection( "Email" )
        if not self.error:
            return
        if settings:
            if self.settings and self.settings["link-url"]:
                logurltext = """The full log can be found here: """ + self.settings["link-url"] + """/""" + os.path.basename( self.logfile ) + """\n\n"""
            else:
                logurltext = ""
            self.setShortLog()

            # Create a text/plain message
            msg = MIMEText( logurltext + self.shortLog )

            # me == the sender's email address
            # you == the recipient's email address
            subject = 'Build error in %s/%s on %s' % ( self.category, self.packageName, os.environ["KDECOMPILER"] )
            if revision:
                subject += ' in revision %s' % revision.strip()

            msg['Subject'] = subject
            msg['From'] = settings["sender"]
            msg['To'] = settings["receivers"]

            if not self.dryRun:
                server = smtplib.SMTP( settings["server"] )
                # server.set_debuglevel(True) # set debuglevel to see that mail can be sent

                server.starttls()

                server.login( settings["sender"], settings["password"] )

                server.sendmail( settings["sender"], settings["receivers"], msg.as_string() )
                server.quit()
            else:
                print subject
#                print msg.as_string()
            

class DashboardNotification(Notification):
    """ announce a build on a dashboard """
    def run( self, revision = None ):
        settings = common.settings.getSection( "Dashboard" )
        if settings:
            self.setShortLog()
            values = dict()
            values['accesskey'] = settings["password"]
            values['category'] = self.category
            values['name'] = self.packageName
            values['platform'] = common.settings.getOption( "General", "platform" )
            values['date'] = common.isodatetime
            values['failed'] = "0"
            if self.error:
                values['failed'] = "1"
            values['revision'] = revision
            values['log'] = self.shortLog
            if self.settings and self.settings["link-url"]:
                logurltext = self.settings["link-url"] + "/" + os.path.basename( self.logfile )
            else:
                logurltext = ""
            values['logUrl'] = logurltext
            if not self.dryRun:
                data = urllib.urlencode( values )
                req = urllib2.Request( settings["submit-url"], data )
                response = urllib2.urlopen( req )
                the_page = response.read()
            else:
                print values["logUrl"]

class LogUploadNotification( Notification ):
    """ this uploads the logfile to a server - it is no real notification """
    def run( self, revision = None ):
        settings = common.settings.getSection( "LogUpload" )
        if settings:
            self.setShortLog()
            upload = common.Uploader( category="LogUpload" )
            print "uploading logfile:", self.logfile, self.dryRun
            if not self.dryRun:
                upload.upload( self.logfile )

class StatusNotification(Notification):
    """ this writes the status of the package into a file """
    def run( self, revision = None ):
        settings = common.settings.getSection( "StatusNotes", common.settings.getSection( "General" ) )
        if settings:
            self.setShortLog()
            values = dict()
            values[ 'category' ] = self.category
            values[ 'name' ] = self.packageName
            values[ 'platform' ] = common.settings.getOption( "General", "platform" )
            values[ 'stage' ] = common.settings.getOption( "General", "stage" )
            values[ 'date' ] = common.isodatetime
            values[ 'failed' ] = "0"
            if self.error:
                values[ 'failed' ] = "1"
            values[ 'revision' ] = revision
            values[ 'log' ] = self.shortLog
            if self.settings and self.settings[ "link-url" ]:
                logurltext = self.settings[ "link-url" ] + "/" + os.path.basename( self.logfile )
            else:
                logurltext = ""
            values[ 'logUrl' ] = logurltext
            
            filename = os.path.join( settings[ 'directory' ], self.category + "_" + self.packageName + ".json" )
            if not self.dryRun:
                if not os.path.exists( settings[ 'directory' ] ):
                    os.makedirs( settings[ 'directory' ] )

                jsondump = file( filename, "w+b" )
                jsondump.write( json.dumps( values, sort_keys=True, indent=4 ) )
                jsondump.close()
            else:
                print "writing to filename:", filename
                print json.dumps( values, sort_keys=True, indent=4 )

if __name__ == '__main__':
    email = EmailNotification( "kdesupport", "automoc", __file__ )
    email.dryRun = True
    email.run()
    dashboard = DashboardNotification( "kdesupport", "automoc", __file__ )
    dashboard.dryRun = True
    dashboard.run( revision="1224" )
    logupload = LogUploadNotification( "kdesupport", "automoc", __file__ )
    logupload.dryRun = True
    logupload.run( revision="1224" )
    status = StatusNotification( "kdesupport", "automoc", __file__ )
#    status.dryRun = True
    status.run( revision="1224" )
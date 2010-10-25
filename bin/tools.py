#!/usr/bin/env python

"""
    several useful tool classes
    
    This module contains some important classes to be used in the future.
    The Tee class should be used for duplicating output on the commandline and
    into a stream.
    The Popen class fixes two important problems with executing commands.
    It requires the installation of the pywin32 packages from
    http://sourceforge.net/projects/pywin32/ to work though ( thanks to the 
    author! )
"""

__author__ = "Patrick Spendrin ( ps_ml at gmx dot de )"
__license__ = "the emerge license (BSD)"

import os
import sys
import imp
import subprocess
import __builtin__
import msvcrt
import time


try:
    import win32pipe
    import win32file
    _pywin32 = True
except:
    _pywin32 = False
    
class Tee( __builtin__.file ):
    """
        This class behaves like the unix command tee:
        everything that gets written into it, will be given out into the given
        file (the object itself) and into the stream outstream.
        Be aware that for writing to this class you should use the write
        function explicitly: print >> Tee(), "string" will not work!
    """
    def __init__( self, name=None, mode='r', bufsize=-1, outstream=sys.stdout, outfile=None ):
        self.outstream = outstream
        self.outfile = outfile
        if self.outfile is None:
            __builtin__.file.__init__( self, name, mode, bufsize )

    def write( self, inputstring ):
        print >> self.outstream, inputstring,
        if self.outfile is None:
            __builtin__.file.write( self, inputstring )
        else:
            self.outfile.write( inputstring )
            self.outfile.flush()

if _pywin32:
    class Popen( subprocess.Popen ):
        """
            This class is used to achieve two goals:
                1) the subprocess.Popen class does not use the write
                method of the file object that is given over - but rather
                the fileno() function. Thus a Tee File Object cannot be used.
                2) with the help of win32pipe.PeekNamedPipe we can check whether
                something has been written to one stream without blocking the
                running program and this way we are not dependent on any output
                in the streams.
        """

        sleeptime = .05

        def __init__( self, *args, **kwargs ):
            """
                Both output streams stdout and stderr can be set to any object
                that has a write function. Leaving stdout or stderr out will
                redirect both streams to their system equivalent (sys.stdout and
                sys.stderr).
            """
            self._bypass_stdout = False
            self._bypass_stderr = False

            if 'stdout' in kwargs and not kwargs['stdout'] is subprocess.PIPE:
                self._stdout_file = kwargs['stdout']
                kwargs['stdout'] = subprocess.PIPE
                self._bypass_stdout = True
            elif not 'stdout' in kwargs:
                self._stdout_file = sys.stdout
                kwargs['stdout'] = subprocess.PIPE
                self._bypass_stdout = True

            if 'stderr' in kwargs and not kwargs['stderr'] is subprocess.PIPE:
                self._stderr_file = kwargs['stderr']
                kwargs['stderr'] = subprocess.PIPE
                self._bypass_stderr = True
            elif not 'stderr' in kwargs:
                self._stderr_file = sys.stderr
                kwargs['stderr'] = subprocess.PIPE
                self._bypass_stderr = True

            subprocess.Popen.__init__( self, *args, **kwargs )

            if self._bypass_stdout:
                self._stdout_hdl = msvcrt.get_osfhandle( self.stdout.fileno() )
            if self._bypass_stderr:
                self._stderr_hdl = msvcrt.get_osfhandle( self.stderr.fileno() )

        def wait( self ):
            """
                This function overwrites the wait() function from subprocess
                completely. It will set up an independent loop, and connect
                the streams of the process via the write function of the object
                that has been given over.
                Before returning, the buffers of the streams are emptied and
                written into the given objects.
            """

            while self.poll() is None:
                if self._bypass_stdout:
                    cont, avail, pos = win32pipe.PeekNamedPipe( self._stdout_hdl, 1024 )
                    if avail > 0: 
                        self._stdout_file.write( win32file.ReadFile( self._stdout_hdl, avail, None )[1] )
                if self._bypass_stderr:
                    cont, avail, pos = win32pipe.PeekNamedPipe( self._stderr_hdl, 1024 )
                    if avail > 0: 
                        self._stderr_file.write( win32file.ReadFile( self._stderr_hdl, avail, None )[1] )
                time.sleep( self.sleeptime )

            # there might be some stuff left in the streams
            if self._bypass_stdout:
                for line in self.stdout: self._stdout_file.write( line )
            if self._bypass_stderr:
                for line in self.stderr: self._stderr_file.write( line )

            return self.returncode


globalVerboseLevel = int( os.getenv( "EMERGE_VERBOSE" ) )

class Verbose:
    """ 
        This class will work on the overall output verbosity 
        It defines the interface for the option parser but before the default 
        value is taken from the environment variable 
    """

    def increase( self, option, opt, value, parser ):
        """ callback function as requested by the optparse parser """
        global globalVerboseLevel
        print "increase"
        globalVerboseLevel += 1
        self.VERBOSE = str( globalVerboseLevel )

    def decrease( self, option, opt, value, parser ):
        """ callback function as requested by the optparse parser """
        global globalVerboseLevel
        print "decrease"
        if globalVerboseLevel > 0:
            globalVerboseLevel -= 1
            self.VERBOSE = str( globalVerboseLevel )

    def setVerboseLevel( self, newLevel ):
        """ set the level by hand for quick and dirty changes """
        global globalVerboseLevel
        globalVerboseLevel = newLevel

    def verbose( self ):
        """ returns the verbosity level for the application """
        global globalVerboseLevel
        return globalVerboseLevel

class Environment ( Verbose ):
    def __init__( self ):
        """ """
#        Verbose.__init__( self )
        self.KDEROOT = os.getenv( "KDEROOT" )
        self.LOGFILE = os.getenv( "EMERGE_LOGFILE" )
        self.BUILDTYPE = os.getenv( "EMERGE_BUILDTYPE" )
        self.BUILDTESTS = os.getenv( "EMERGE_BUILDTESTS" )
        self.PKG_DEST_DIR = os.getenv( "EMERGE_PKGDSTDIR" )
        self.COMPILER = os.getenv( "KDECOMPILER" )
        self.IGNORE_SUBVERSION = ".svn"
        if not self.LOGFILE:
            self.LOGFILE = '%KDEROOT%\\emerge-system.log'



    def __lshift__( self, other ):
        """ self << other """
        self.KDEROOT = other.KDEROOT
        self.LOGFILE = other.LOGFILE
        self.BUILDTYPE = other.BUILDTYPE
        self.BUILDTESTS = other.BUILDTESTS
        self.PKG_DEST_DIR = other.PKG_DEST_DIR
        self.COMPILER = other.COMPILER


class Object ( Environment ):
    def __init__( self ):
        """ """
        Environment.__init__( self )

    def inform( self, message ):
        if self.verbose() > 0:
            print "emerge info: %s" % message
        return True

    def debug( self, message, level=1 ):
        if self.verbose() > level:
            print "emerge debug: %s" % message
        return True

    def warning( self, message ):
        if self.verbose() > 0:
            print "emerge warning: %s" % message
        return True

    def error( self, message=None ):
        if not message:
            message = self.errormessage
        if self.verbose() > 0:
            print >> sys.stderr, "emerge error: %s" % message
        return False

    def die( self, message ):
        print "emerge fatal error: %s" % message
        exit( 1 )

    def system( self, cmdstring, die=False, capture_output=None ):
        if self.verbose() == 0:
            self.stderr = file( self.LOGFILE, 'wb' )
            self.stdout = sys.stderr
        else:
            self.stderr = sys.stderr
            self.stdout = sys.stdout
        if capture_output:
            self.stderr = capture_output
            self.stdout = capture_output
        if self.verbose() > 1:
            print "system() executing this: <" + cmdstring + ">"
        p = subprocess.Popen( cmdstring, shell=True, stdout=self.stdout, stderr=self.stderr )
        ret = p.wait()
        if die:
            self.die( "system failed to execute: <" + cmdstring + ">" )
        return ret

    def __import__( self, module ):
        if not os.path.isfile( module ):
            return __builtin__.__import__( module )
        else:
            sys.path.append( os.path.dirname( module ) )
            fileHdl = open( module )
            modulename = os.path.basename( module ).replace('.py', '')
            return imp.load_module( modulename.replace('.', '_'), fileHdl, module, imp.get_suffixes()[1] )

if __name__ == "__main__":
    """
        Give a short introduction on how to use Tee and Popen;
        A script will be written that can be executed afterwards and which
        will give out some stuff on stdout and stderr. This script gets
        deleted in the end.
        For some further insight:
            We first create a normal file object log and a Tee object which uses
            the log object as its output file. The outstream of the Tee object
            stays sys.stdout even though we redirect sys.stdout to the log 
            object next. That will result in stderr going to stdout and log via
            the Tee object and stdout going directly into log (as we changed
            the sys.stdout for that!!!!).
            If we would want to make stderr to go to stderr and log, we only
            need to add outstream=sys.stderr in the creation of the Tee object.
    """

    import os
    import sys
    
    if not os.path.exists( os.path.join( os.path.dirname( sys.argv[0] ), "test.py" ) ) or not '--no-write' in sys.argv:
        testfile = file( os.path.join( os.path.dirname( sys.argv[0] ), "test.py" ), 'w+' )
        content = """from time import sleep
import sys
for i in range( 100 ):
        sleep(.1)
        print "stdout: " + str(i)
        if i%5 == 0:
            print >> sys.stderr, "stderr: " + str(i)
        """
        
        testfile.write( content )
        testfile.close()
    
    command = sys.executable + " -u " + os.path.join( os.path.dirname( sys.argv[0] ), "test.py" )
    log=open( os.path.join( os.getenv( "KDEROOT" ), "tools.log" ), mode='w+b' )
    T_err = Tee( outfile=log )
    sys.stdout=log
    process = Popen( command, stderr=T_err, shell=True )
    process.wait()
    
    if not '--no-remove' in sys.argv:
        os.remove( os.path.join( os.path.dirname( sys.argv[0] ), "test.py" ) )
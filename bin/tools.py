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
import subprocess
import builtins
import msvcrt  # pylint: disable=F0401
import time

try:
    # pylint: disable=F0401
    import win32pipe
    import win32file
    _pywin32 = True
except ImportError:
    _pywin32 = False

class Tee( builtins.file ):
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
            builtins.file.__init__( self, name, mode, bufsize )

    def write( self, inputstring ):
        print(inputstring, end=' ', file=self.outstream)
        if self.outfile is None:
            builtins.file.write( self, inputstring )
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
                    _, avail, _ = win32pipe.PeekNamedPipe( self._stdout_hdl, 1024 )
                    if avail > 0:
                        self._stdout_file.write( win32file.ReadFile( self._stdout_hdl, avail, None )[1] )
                if self._bypass_stderr:
                    _, avail, _ = win32pipe.PeekNamedPipe( self._stderr_hdl, 1024 )
                    if avail > 0:
                        self._stderr_file.write( win32file.ReadFile( self._stderr_hdl, avail, None )[1] )
                time.sleep( self.sleeptime )

            # there might be some stuff left in the streams
            if self._bypass_stdout:
                for line in self.stdout:
                    self._stdout_file.write( line )
            if self._bypass_stderr:
                for line in self.stderr:
                    self._stderr_file.write( line )

            return self.returncode


def main():
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
    log = open( os.path.join( os.getenv( "KDEROOT" ), "tools.log" ), mode='w+b' )
    T_err = Tee( outfile=log )
    sys.stdout = log
    process = Popen( command, stderr=T_err, shell=True )
    process.wait()

    if not '--no-remove' in sys.argv:
        os.remove( os.path.join( os.path.dirname( sys.argv[0] ), "test.py" ) )

if __name__ == "__main__":
    main()

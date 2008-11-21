import base
import utils
import sys
import info
import os

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

    def setTargets( self ):
        self.targets['4.7.7'] = 'http://www.winkde.org/pub/kde/ports/win32/repository/external/sip-4.7.7.zip'
        self.targetInstSrc['4.7.7'] = 'sip-4.7.7'
        self.defaultTarget = '4.7.7'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()

    def configure( self ):
        builddir = os.path.join( self.workdir, self.instsrcdir )
        os.chdir( builddir )
        if self.buildType == 'Debug':
            command = "python configure.py -u"
        else:
            command = "python configure.py"
        if self.compiler == "mingw":
            command += " -p win32-g++"
        command += " CFLAGS=-I" + os.path.join(self.packagedir)
        command += " CXXFLAGS=-I" + os.path.join(self.packagedir)
        self.system( command )
        return True

    def compile( self ):
        self.configure()
        builddir = os.path.join( self.workdir, self.instsrcdir )
        os.chdir( builddir )
        if self.compiler == "mingw":
            command = "mingw32-make"
        else:
            command = "nmake"
        self.system( command )
        return True

    def install( self ):
        builddir = os.path.join( self.workdir, self.instsrcdir )
        os.chdir( builddir )
        if self.compiler == "mingw":
            self.system( "mingw32-make install" )
        else:
            self.system( "nmake install" )
        # fix problem with not copying manifest file 
        self.system( "copy " + os.path.join(builddir,"sipgen","sip.exe.manifest") + " c:\python25") 
        # install manifest file too
        return True

    def make_package( self ):
        return False

if __name__ == '__main__':
    subclass().execute()

import base
import utils
import sys
import info
import os

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

    def setTargets( self ):
        self.targets['4.4.3'] = 'http://www.winkde.org/pub/kde/ports/win32/repository/external/PyQt-win-gpl-4.4.3.zip'
        self.targetInstSrc['4.4.3'] = 'PyQt-win-gpl-4.4.3'
        self.defaultTarget = '4.4.3'
        #self.svnTargets['svnHEAD'] = 'trunk/kdesupport/taglib'
        #self.defaultTarget = 'svnHEAD'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()
        os.putenv( "QMAKESPEC", os.path.join(self.rootdir,"mkspecs","win32-"+self.compiler) )

    def configure( self ):
		builddir = os.path.join( self.workdir, self.instsrcdir )
		os.chdir( builddir )
		self.system( "set" )
		
		if self.buildType == 'Debug':
			command = "echo yes | python configure.py -u "
		else:
			command = "echo yes | python configure.py "
		# add mingw compiler
		#command += "-p plat"
		#command += " LFLAGS+=/MANIFEST"
		command += " --verbose"
		self.system( command )
		return True

    def compile( self ):
		self.configure()
		builddir = os.path.join( self.workdir, self.instsrcdir )
		os.chdir( builddir )
		command = "nmake"
		self.system( command )
		return True

    def install( self ):
		builddir = os.path.join( self.workdir, self.instsrcdir )
		os.chdir( builddir )
		self.system( "nmake install" )
		self.system( "copy " + os.path.join(builddir,"sipgen","sip.exe.manifest") + " c:\python25") 
		# install manifest file too
		return True

    def make_package( self ):
        return False

if __name__ == '__main__':
    subclass().execute()

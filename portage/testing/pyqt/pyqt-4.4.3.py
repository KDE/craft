import base
import utils
import sys
import info
import os
import sipconfig

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        #self.hardDependencies['python25'] = 'default'

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

    def unpack(self):
        base.baseclass.unpack( self ) or utils.die( "unpack failed" )		
        self.system( "copy " + os.path.join(self.workdir,self.instsrcdir,"configure.py") + " " + os.path.join(self.workdir,self.instsrcdir,"configure.py.orig") )
        self.system( "copy " + os.path.join( self.packagedir,"configure.py") + " " + os.path.join(self.workdir,self.instsrcdir,"configure.py") )
        # patch does not work for unknown reasons
        #cmd = "cd %s && patch -p0 -i %s" % ( self.instsrcdir, os.path.join( self.packagedir, "pyqt-4.4.3.patch" ) ) 
        #self.system( cmd )

        if self.buildType == 'Debug':
            # Get the SIP configuration.
            sipcfg = sipconfig.Configuration()
            py_lib_dir = sipcfg.py_lib_dir
            implib = os.path.join(py_lib_dir,"python25.lib")
            implib_d = os.path.join(py_lib_dir,"python25_d.lib")
			# new location build dir
            #implib_d = os.path.join(self.workdir,self.instsrcdir,"python25_d.lib")
            if os.path.exists(implib):
                self.system( "copy " + implib + " " + implib_d);

        return True

    def configure( self ):
		builddir = os.path.join( self.workdir, self.instsrcdir )
		os.chdir( builddir )
		
		if self.buildType == 'Debug':
			command = "echo yes | python configure.py -u "
		else:
			command = "echo yes | python configure.py "
		# add mingw compiler
		#command += "-p plat"
		command += "--verbose"
		command += " -I " + os.path.join(self.packagedir)
		# for debug library
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
		# install manifest file too
		return True

    def make_package( self ):
        return False

if __name__ == '__main__':
    subclass().execute()

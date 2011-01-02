import base
import utils
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['4.3.3'] = 'http://www.riverbankcomputing.com/Downloads/PyQt4/GPL/PyQt-win-gpl-4.3.3.zip'
        self.targetInstSrc['4.3.3'] = 'PyQt-win-gpl-4.3.3'        
        self.defaultTarget = '4.3.3'
    
    def setDependencies( self ):
        self.hardDependencies['testing/sip'] = 'default'
        
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()
        
    def unpack( self ):
        ok = base.baseclass.unpack( self )
        # remove query for acceptance of GPL
        sedcommand = r""" -e "s/resp = raw_input(\"Do you accept the terms of the license? \")/resp = \"yes\"/g" """
        utils.sedFile( os.path.join( self.workdir, self.instsrcdir ), "configure.py", sedcommand )
        # instead of using qt.conf fix it in the sources here.
        sedcommand = r""" -e "s/QLibraryInfo::location(QLibraryInfo::PrefixPath)/\"""" + self.rootdir.replace('\\', '\\\\\\\\\\\\\\\\') + """\\"/g" """
        utils.sedFile( os.path.join( self.workdir, self.instsrcdir ), "configure.py", sedcommand )
        sedcommand = r""" -e "s/QLibraryInfo::location(QLibraryInfo::HeadersPath)/\"""" + os.path.join( self.rootdir, "include" ).replace('\\', '\\\\\\\\\\\\\\\\') + """\\"/g" """
        utils.sedFile( os.path.join( self.workdir, self.instsrcdir ), "configure.py", sedcommand )
        sedcommand = r""" -e "s/QLibraryInfo::location(QLibraryInfo::LibrariesPath)/\"""" + os.path.join( self.rootdir, "lib" ).replace('\\', '\\\\\\\\\\\\\\\\') + """\\"/g" """
        utils.sedFile( os.path.join( self.workdir, self.instsrcdir ), "configure.py", sedcommand )
        sedcommand = r""" -e "s/QLibraryInfo::location(QLibraryInfo::BinariesPath)/\"""" + os.path.join( self.rootdir, "bin" ).replace('\\', '\\\\\\\\\\\\\\\\') + """\\"/g" """
        utils.sedFile( os.path.join( self.workdir, self.instsrcdir ), "configure.py", sedcommand )
        sedcommand = r""" -e "s/QLibraryInfo::location(QLibraryInfo::DataPath)/\"""" + self.rootdir.replace('\\', '\\\\\\\\\\\\\\\\') + """\\"/g" """
        utils.sedFile( os.path.join( self.workdir, self.instsrcdir ), "configure.py", sedcommand )
        sedcommand = r""" -e "s/QLibraryInfo::location(QLibraryInfo::PluginsPath)/\"""" + os.path.join( self.rootdir, "plugins" ).replace('\\', '\\\\\\\\\\\\\\\\') + """\\"/g" """
        utils.sedFile( os.path.join( self.workdir, self.instsrcdir ), "configure.py", sedcommand )
        return ok

    def compile( self ):
        cmd = 'cd %s && python configure.py -b %s -w' % ( os.path.join( self.workdir, self.instsrcdir ),
                                                                   os.path.join( self.imagedir, "bin" ) )
        if self.compiler == "mingw":
            cmd += " -p win32-g++"
        utils.system( cmd ) or utils.die( "failed to execute %1" % cmd )
        sedcommand = r""" -e "s/""" + os.path.join( self.rootdir, "tmp", "qt" ).replace('\\', '\\/') + "*\\/image-mingw\\/" + """/""" + self.rootdir.replace('\\', '\\/') + """/g" """
        utils.sedFile( os.path.join( self.workdir, self.instsrcdir ), "pyqtconfig.py", sedcommand )
        cmd = 'cd %s && %s' % ( os.path.join( self.workdir, self.instsrcdir ), self.cmakeMakeProgramm )
        utils.system( cmd ) or utils.die( "failed to execute %1" % cmd )
        return True

    def install( self ):
        cmd = 'cd %s && %s install' % ( os.path.join( self.workdir, self.instsrcdir ), self.cmakeMakeProgramm )
        utils.system( cmd ) or utils.die( "failed to execute %1" % cmd )
        return True


if __name__ == '__main__':
    subclass().execute()

import base
import utils
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['4.7.4'] = 'http://www.riverbankcomputing.com/Downloads/sip4/sip-4.7.4.zip'
        self.targetInstSrc['4.7.4'] = 'sip-4.7.4'
        self.defaultTarget = '4.7.4'

        def setDependencies( self ):
            self.hardDependencies['libs/qt'] = 'default'
        
class subclass(base.baseclass):
    def __init__( self ):
        base.baseclass.__init__( self, "" )
        self.subinfo = subinfo()

    def compile( self ):
        cmd = 'cd %s && python configure.py -b %s -e %s' % ( os.path.join( self.workdir, self.instsrcdir ),
                                                             os.path.join( self.imagedir, "bin" ), 
                                                             os.path.join( self.imagedir, "include" ) )
        if self.compiler == "mingw":
            cmd += " -p win32-g++"
        utils.system( cmd ) or utils.die( "failed to execute %1" % cmd )
        cmd = 'cd %s && %s' % ( os.path.join( self.workdir, self.instsrcdir ), self.cmakeMakeProgramm )
        utils.system( cmd ) or utils.die( "failed to execute %1" % cmd )
        sedcommand = r""" -e "s/""" + self.imagedir.replace('\\', '\\\\\\\\') + """/""" + self.rootdir.replace('\\', '\\\\\\\\') + """/g" """
        utils.sedFile( os.path.join( self.workdir, self.instsrcdir ), "sipconfig.py", sedcommand )
        return True
        
    def install( self ):
        """please be aware that unlike all the other stuff, sip installs to the python interpreter for now"""
        cmd = 'cd %s && %s install' % ( os.path.join( self.workdir, self.instsrcdir ), self.cmakeMakeProgramm )
        utils.system( cmd ) or utils.die( "failed to execute %1" % cmd )
        return True
        

if __name__ == '__main__':
    subclass().execute()

from Package.CMakePackageBase import *
import info
import compiler
import utils

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = '[git]kde:rocs'
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.hardDependencies['kde/kde-runtime'] = 'default'

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        if compiler.isMSVC2008() or compiler.isMSVC2010():
            utils.die("""
            src/Interfaces/GraphScene.h contains the static member kBorder
            and sets the initial value in the class statement. 
            This is not supported by msvc compilers, please fix it""")
       
if __name__ == '__main__':
    Package().execute()

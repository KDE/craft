import base
import utils
import sys
import os
import shutil
import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['libs/qt'] = 'default'

    def setTargets( self ):
        self.targets['0.1.0'] = 'http://qtscriptgenerator.googlecode.com/files/qtscriptgenerator-src-0.1.0.tar.gz'
        self.targetInstSrc['0.1.0'] = 'qtscriptgenerator-src-0.1.0'
        self.defaultTarget = '0.1.0'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "qtscriptgenerator"
        self.subinfo = subinfo()

    def unpack( self ):
        ret = self.kdeSvnUnpack()
        if self.buildTarget == '0.1.0':
                self.system( "cd %s && patch -p1 < %s" % ( os.path.join( self.workdir, self.instsrcdir ), os.path.join( self.packagedir, "qtscriptgenerator-cmake.diff" ) ) )
                self.system( "cd %s && patch -p1 < %s" % ( os.path.join( self.workdir, self.instsrcdir ), os.path.join( self.packagedir, "qtscriptgenerator.diff" ) ) )
        return ret

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if self.buildTarget == "svnHEAD":
            return self.doPackaging( "qtscriptgenerator", utils.cleanPackageName( sys.argv[0], "qtscriptgenerator" ), True )
        else:
            return self.doPackaging( "qtscriptgenerator", self.buildTarget, True )

if __name__ == '__main__':
    subclass().execute()

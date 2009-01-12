import base
import utils
import sys
import os
import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['kdesupport/automoc'] = 'default'
        self.hardDependencies['libs/qt'] = 'default'
        self.boostversion = "1.37"

    def setTargets( self ):
        self.svnTargets['0.80'] = 'tags/akonadi/0.80'
        self.svnTargets['0.81'] = 'tags/akonadi/0.81'
        self.svnTargets['0.82'] = 'tags/akonadi/0.82'
        self.svnTargets['1.0.0'] = 'tags/akonadi/1.0.0'
        self.svnTargets['1.0.80'] = 'tags/akonadi/1.0.80'
        self.svnTargets['1.1.0']  = 'tags/akonadi/1.1.0'
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/akonadi'
        self.defaultTarget = 'svnHEAD'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "akonadi"
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        self.kdeCustomDefines = " -DBoost_ADDITIONAL_VERSIONS=" + self.subinfo.boostversion
        self.kdeCustomDefines += " -DBOOST_INCLUDEDIR=" + os.path.join( self.rootdir, "include", "boost-" + self.subinfo.boostversion.replace(".", "_") )
        print self.kdeCustomDefines
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if self.buildTarget == "svnHEAD":
            return self.doPackaging( "akonadi", utils.cleanPackageName( sys.argv[0], "akonadi" ), True )
        else:
            return self.doPackaging( "akonadi", self.buildTarget, True )

if __name__ == '__main__':
    subclass().execute()

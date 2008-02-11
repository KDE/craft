import base
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['1.80'] = 'tags/amarok/1.80/amarok'
        self.svnTargets['svnHEAD'] = 'trunk/extragear/multimedia/amarok'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kdesupport/taglib'] = 'default'
        self.hardDependencies['dev-util/ruby'] = 'default'
        self.hardDependencies['extragear/phonon'] = 'default'
        self.hardDependencies['kde/kdelibs'] = 'default'
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
    
class subclass(base.baseclass):
    def __init__( self ):
        base.baseclass.__init__( self, "" )
        self.instsrcdir = "amarok"
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if not self.buildTarget == 'svnHEAD':
            return self.doPackaging( "amarok", self.buildTarget, True )
        else:
            return self.doPackaging( "amarok", os.path.basename(sys.argv[0]).replace("amarok-", "").replace(".py", ""), True )


if __name__ == '__main__':		
    subclass().execute()

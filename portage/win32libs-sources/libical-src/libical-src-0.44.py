import base
import utils
import os
import shutil
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'libical'
        for v in [ '0.41', '0.42', '0.43', '0.44']:
            self.targets[ v ] = 'http://downloads.sourceforge.net/freeassociation/libical-' + v + '.tar.gz'
            self.targetInstSrc[ v ] = 'libical-' + v
        self.defaultTarget = '0.44'
        self.patchToApply['0.44'] = ( 'libical-src-0.44.patch', 0 )
    
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.createCombinedPackage = True
        self.subinfo = subinfo()
    
    def unpack( self ):
        print "libical unpack called for %s" % self.subinfo.buildTarget
        # do the svn fetch/update
        if self.buildTarget == 'svnHEAD':
            repo = 'https://freeassociation.svn.sourceforge.net/svnroot/freeassociation/trunk/'
            if self.subinfo.buildTarget in self.subinfo.svnTargets.keys():
                self.svnFetch( repo + self.subinfo.svnTargets[ self.subinfo.buildTarget ] )
            else:
                return False
            utils.cleanDirectory( self.workdir )
        else:
            return base.baseclass.unpack( self )
        return True

    def compile( self ):
        if self.buildTarget == 'svnHEAD':
            if self.subinfo.buildTarget in self.subinfo.svnTargets.keys():
                self.kde.sourcePath = os.path.join( self.svndir, self.subinfo.svnTargets[ self.subinfo.buildTarget ] )
            else:
                return False
        self.kdeCustomDefines = "-DUSE_BUILTIN_TZDATA=true -DICAL_UNIX_NEWLINE=false"
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        # auto-create both import libs with the help of pexports
        self.createImportLibs( "libical" )
        self.createImportLibs( "libicalss" )
        self.createImportLibs( "libicalvcal" )

        self.doPackaging( "libical", self.buildTarget, True )

        return True

if __name__ == '__main__':
    subclass().execute()

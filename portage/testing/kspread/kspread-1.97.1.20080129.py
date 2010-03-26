import base
import os
import utils
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = "trunk/koffice"
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['win32libs-sources/lcms-src'] = 'default'
        self.hardDependencies['kde/kdelibs'] = 'default'
        self.hardDependencies['kde/kdebase'] = 'default'

        self.softDependencies['kdesupport/eigen'] = 'default'
        self.softDependencies['kdesupport/qca'] = 'default'
        self.softDependencies['testing/gsl'] = 'default'
    

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.kdeCustomDefines = ""
#        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_karbon=OFF "
        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_kpresenter=OFF "
        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_kchart=OFF "
        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_kdgantt=OFF "
        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_kexi=OFF "
        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_kivio=OFF "
        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_kounavail=OFF "
        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_kplato=OFF "
        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_krita=OFF "
        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_kword=OFF "
        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_kspread=OFF "
        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_doc=OFF "
        

    def unpack( self ):
        unp = self.kdeSvnUnpack( "trunk", "koffice" )
        # now copy the tree to workdir
        srcdir  = os.path.join( self.workdir, "koffice" )
        destdir = os.path.join( self.workdir, "kspread" )
        if not os.path.exists( destdir ):
            utils.moveSrcDirToDestDir( srcdir, destdir )
        else:
            utils.copySrcDirToDestDir( srcdir, destdir )
        return unp


    def kdeSvnPath( self ):
        return False
        
    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        return self.doPackaging( "kspread", "1.95-1", True )
		
if __name__ == '__main__':
    subclass().execute()

import base
import os
import utils
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = "trunk/koffice"
        self.svnTargets['1.9.95.8'] = "tags/koffice/1.9.95.8/koffice"
        self.svnTargets['1.9.95.9'] = "tags/koffice/1.9.95.9/koffice"
        self.targets['1.9.95.10'] = 'ftp://ftp.kde.org/pub/kde/unstable/koffice-1.9.95.10/src/koffice-1.9.95.10.tar.bz2'
        self.targetInstSrc['1.9.95.10'] = 'koffice-1.9.95.10'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
#        self.hardDependencies['win32libs-sources/lcms-src'] = 'default'
        self.hardDependencies['kde/kdelibs'] = 'default'
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
#        self.hardDependencies['kdesupport/eigen'] = 'default'
#         self.hardDependencies['kdesupport/eigen2'] = 'default'
        self.softDependencies['kdesupport/qca'] = 'default'
        self.softDependencies['testing/gsl'] = 'default'
    
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "koffice"
        self.subinfo = subinfo()
        self.kdeCustomDefines = ""
#        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_karbon=OFF "
#        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_kformula=OFF "
#        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_kpresenter=OFF "
#        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_kchart=OFF "
#        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_kdgantt=OFF "
#        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_kexi=OFF "
#        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_kivio=OFF "
#        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_kounavail=OFF "
#        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_kplato=OFF "
#        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_krita=OFF "
#        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_kword=OFF "
#        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_kspread=OFF "
#        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_doc=OFF "

    def unpack( self ):
        if self.buildTarget == '1.9.95.10':
            if( not base.baseclass.unpack( self ) ):
                return False
                
            src = os.path.join( self.workdir, self.instsrcdir )

            cmd = "cd %s && patch -p0 < %s" % \
                  ( self.workdir, os.path.join( self.packagedir , "koffice-alpha10.diff" ) )
            if utils.verbose() >= 1:
                print cmd
            self.system( cmd ) or die( "patch" )
            return True
        else:
            return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if self.buildTarget == 'svnHEAD':
            return self.doPackaging( "koffice", os.path.basename(sys.argv[0]).replace("koffice-", "").replace(".py", ""), True )
        else:
            return self.doPackaging( "koffice", self.buildTarget, True )
		
if __name__ == '__main__':
    subclass().execute()

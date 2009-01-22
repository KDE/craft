import base
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'branches/KDE/4.2/kdepimlibs'
        for ver in ['0']:
          self.targets['4.2.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.2.' + ver + '/src/kdepimlibs-4.2.' + ver + '.tar.bz2'
          self.targetInstSrc['4.2.' + ver] = 'kdepimlibs-4.2.' + ver
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde-4.2/kdelibs'] = 'default'
#        self.hardDependencies['win32libs/libical'] = 'default'
        self.hardDependencies['contributed/gpgme-qt'] = 'default'
        self.hardDependencies['kdesupport/akonadi'] = 'default'
        
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        # add env var so that boost headers are found
        path = os.path.join( self.rootdir, "win32libs" )
        os.putenv( "BOOST_ROOT", path )

        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        # generate the template file for KDELibsDependenciesInternal.cmake
        filename = os.path.join( self.imagedir, "share", "apps", "cmake", "modules", "KDEPimLibsDependencies.cmake" )
        sedcmd = "sed -e \"s/" + self.rootdir.replace("\\", "\\/") + "/[replace_this]/g\" " + filename + " > " + filename + ".template"
        self.system( sedcmd )

        return self.doPackaging( "kdepimlibs", self.buildTarget, True )

if __name__ == '__main__':
    subclass().execute()

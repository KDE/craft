import base
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'branches/KDE/4.1/kdepimlibs'
        for ver in ['0', '1', '2']:
          self.targets['4.1.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.1.' + ver + '/src/kdepimlibs-4.1.' + ver + '.tar.bz2'
          self.targetInstSrc['4.1.' + ver] = 'kdepimlibs-4.1.' + ver
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde-4.1/kdelibs'] = 'default'
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

        if not self.buildTarget == 'svnHEAD':
            return self.doPackaging( "kdepimlibs", self.buildTarget, True )
        else:
            return self.doPackaging( "kdepimlibs", os.path.basename(sys.argv[0]).replace("kdepimlibs-", "").replace(".py", ""), True )


if __name__ == '__main__':
    subclass().execute()

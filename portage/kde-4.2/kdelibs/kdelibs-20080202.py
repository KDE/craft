import base
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'branches/KDE/4.2/kdelibs'
        for ver in ['0']:
          self.targets['4.2.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.2.' + ver + '/src/kdelibs-4.2.' + ver + '.tar.bz2'
          self.targetInstSrc['4.2.' + ver] = 'kdelibs-4.2.' + ver
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kdesupport/kdewin32'] = 'default'
        self.hardDependencies['kdesupport/qimageblitz'] = 'default'
        self.hardDependencies['kdesupport/soprano'] = 'default'
        self.hardDependencies['kdesupport/strigi'] = 'default'
        self.hardDependencies['kdesupport/phonon'] = 'default'
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['dev-util/perl'] = 'default'
        self.hardDependencies['dev-util/win32libs'] = 'default'
    
class subclass(base.baseclass):
    def __init__( self, **args ):
        self.buildType = "Debug"
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()

    def unpack( self ):
        if not self.kdeSvnUnpack():
          return False;
        if self.buildTarget == "4.2.0":
          src_dir  = os.path.join( self.workdir, self.instsrcdir )
          cmd = "cd %s && patch -p0 < %s" % \
            ( src_dir, os.path.join( self.packagedir, "kdelibs_4.2.0.patch" ) )
          os.system( cmd )
        return True

    def compile( self ):
        if self.compiler == "mingw":
          self.kdeCustomDefines += " -DKDE_DISTRIBUTION_TEXT=\"MinGW 3.4.5\" "
        if self.compiler == "msvc2005":
          self.kdeCustomDefines += " -DKDE_DISTRIBUTION_TEXT=\"MS Visual Studio 2005 SP1\" "

        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def unittest( self ):
        return self.kdeTest()

    def make_package( self ):
        # generate the template file for KDELibsDependenciesInternal.cmake
        # filename = os.path.join( self.imagedir, "share", "apps", "cmake", "modules", "KDELibsDependenciesInternal.cmake" )
        # sedcmd = "sed -e \"s/" + self.rootdir.replace("\\", "\\/") + "/[replace_this]/g\" " + filename + " > " + filename + ".template"
        # self.system( sedcmd )
        return self.doPackaging( "kdelibs", self.buildTarget, True )

if __name__ == '__main__':
    subclass().execute()

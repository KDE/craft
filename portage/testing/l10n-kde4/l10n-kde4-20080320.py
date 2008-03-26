import base
import utils
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/l10n-kde4'
        self.defaultTarget = 'svnHEAD'
        self.languages = 'de'
    
    def setDependencies( self ):
        self.hardDependencies['dev-util/cmake'] = 'default'
        self.hardDependencies['testing/gettext-tools'] = 'default'
        self.hardDependencies['kdesupport/kdewin-installer'] = 'default'
        return 0
        
class subclass(base.baseclass):
    def __init__( self ):
        base.baseclass.__init__( self, "" )
        self.subinfo = subinfo()

    def unpack( self ):
        svnpath = self.kdeSvnPath()
        utils.cleanDirectory( self.workdir )
        if not self.kdeSvnUnpack( svnpath, "scripts" ):
            return False
        srcdir  = os.path.join( self.kdesvndir, svnpath, "scripts" )
        destdir = os.path.join( self.workdir, "scripts" )
        utils.copySrcDirToDestDir( srcdir, destdir )
        for pkg in self.subinfo.languages.split():
            if not self.kdeSvnUnpack( svnpath, pkg ):
                return False
            srcdir  = os.path.join( self.kdesvndir, svnpath, pkg )
            destdir = os.path.join( self.workdir, pkg )
            utils.copySrcDirToDestDir( srcdir, destdir )
        # revpath is not available in msys
        return True

    def preconfigure( self ):
        path = self.workdir
        cmd = os.path.join( path, "scripts", "autogen.sh" )
        args = self.subinfo.languages
        self.msys.msysExecute( path, cmd, args )
        return True
               
    def configure( self ):
        for pkg in self.subinfo.languages.split():
            defines = "-DCMAKE_INCLUDE_PATH=%s/include -DCMAKE_LIBRARY_PATH=%s/lib -DCMAKE_INSTALL_PREFIX=%s" % \
                      ( self.rootdir, self.rootdir, self.rootdir )
            # does not work because source dir does not fit
            #defines = self.kdeDefaultDefines()
            workdir = os.path.join( self.workdir, pkg )
            if not os.path.exists( workdir ):
                os.mkdir( workdir )
            cmd = "cmake -G \"%s\" %s %s" % ( self.cmakeMakefileGenerator, workdir, defines )
            print cmd
            utils.system(cmd)
        return True

    def make( self ):
        cmd = "cd " + self.workdir + "&& " + self.cmakeMakeProgramm
        utils.system( cmd )
        return True

    def compile( self ):
        ret = self.preconfigure()
        if not ret:
            return ret
        ret = self.configure()
        if not ret:
            return ret
        return self.make()

    def install( self ):
        for pkg in self.subinfo.languages.split():
            workdir = os.path.join( self.workdir, pkg )
            cmd = "cd %s && cmake -DCMAKE_INSTALL_PREFIX=%s/%s" % \
                  ( workdir, self.imagedir, pkg )
            utils.system( cmd )
        return True

    def uninstall( self ):
        for pkg in self.subinfo.languages.split():
            workdir = os.path.join( self.workdir, pkg )
            cmd = "cd %s && cmake -P cmake_uninstall.cmake" % ( workdir )
            utils.system( cmd )
        return True

    def make_package( self ):
        self.svnpath=os.path.join( self.kdesvndir,self.subinfo.svnTargets['svnHEAD'])
        self.filesdir = os.path.join(self.packagedir,"files")
        dstpath = os.getenv( "EMERGE_PKGDSTDIR" )
        if not dstpath:
            dstpath = os.path.join( self.rootdir, "tmp" )

        if not utils.test4application( "kdewin-packager" ):
            utils.die( "kdewin-packager not found - please make sure it is in your path" )

        for pkg in self.subinfo.languages.split():
            workdir = os.path.join( self.workdir, pkg )
            cmd = "kdewin-packager -name kde-i18n-%s -version %s -hashfirst -compression 2 -root %s/%s -destdir %s" % \
                  ( pkg, self.version, self.imagedir, pkg, dstpath )
            utils.system( cmd )
        return True

    def qmerge( self ):
        for pkg in self.subinfo.languages.split():
            utils.mergeImageDirToRootDir( os.path.join( self.imagedir, pkg ), self.rootdir )
        return True
        
    def unmerge( self ):
        for pkg in self.subinfo.languages.split():
            print "implement unmerge for " + pkg
            #utils.unmerge( self.rootdir, self.package, self.forced )
            #utils.remInstalled( self.category, self.package, self.version )
        return True


if __name__ == '__main__':
    subclass().execute()

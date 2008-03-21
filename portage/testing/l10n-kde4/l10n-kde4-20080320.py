import base
import utils
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/l10n-kde4'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['dev-util/cmake'] = 'default'
        self.hardDependencies['testing/gettext-tools'] = 'default'
        # self provided kdewin-packager 
        #self.hardDependencies['kdewin-installer'] = 'default'
        return 0
        
class subclass(base.baseclass):
    def __init__( self ):
        base.baseclass.__init__( self, "" )
        self.subinfo = subinfo()

    def toCygwinSeparator( self,path):
        return path.replace("\\","/")

    def toCygwinPath( self,path):
        _path = '/' + path[0] + path[2:]
        return _path.replace("\\","/")

    def setupCygwin( self ):
        self.filesdir = os.path.join(self.packagedir,"files")
        self.shell = os.path.join(self.filesdir,"sh.exe")+" -c "
        self.svnpath=os.path.join( self.kdesvndir,self.subinfo.svnTargets['svnHEAD'])
        self.cmdprefix="PATH=.:"+self.toCygwinPath(self.filesdir)+":"+self.toCygwinPath(os.path.join(self.rootdir,"bin"))
        self.envsettings=self.cmdprefix

    def unpack( self ):
        print "!!!!! Note !!!!!: edit %s to limit affected languages" % (os.path.join( self.kdesvndir,self.subinfo.svnTargets['svnHEAD']))
        return self.kdeSvnUnpack()

    def preconfigure( self ):
        self.setupCygwin()

        shellscript=self.toCygwinSeparator(os.path.join( self.svnpath,"scripts","autogen.sh"))
        cmd = "'"+self.cmdprefix+";cd "+self.toCygwinSeparator(self.svnpath)+";"+shellscript+"'"

        print self.shell + cmd
        utils.system(self.shell + cmd)
        return True
               
    def configure( self ):
        self.svnpath=os.path.join( self.kdesvndir,self.subinfo.svnTargets['svnHEAD'])
        f = open( os.path.join(self.svnpath,"subdirs"), "r" )
        for line in f.read().splitlines():
            defines = "-DCMAKE_INCLUDE_PATH=%s/include -DCMAKE_LIBRARY_PATH=%s/lib -DCMAKE_INSTALL_PREFIX=%s" % (self.rootdir,self.rootdir,self.rootdir)
            # does not work because source dir does not fit
            #defines = self.kdeDefaultDefines()
            workdir = os.path.join(self.workdir,line)
            if not os.path.exists( workdir ):
                os.mkdir(workdir)
            cmd = "cd %s && cmake -G \"%s\" %s/%s %s" % (workdir, self.cmakeMakefileGenerator, self.svnpath, line, defines ) 
            print cmd
            utils.system(cmd)
        f.close()
        return True

    def make( self ):
        self.svnpath=os.path.join( self.kdesvndir,self.subinfo.svnTargets['svnHEAD'])
        f = open( os.path.join(self.svnpath,"subdirs"), "r" )
        for line in f.read().splitlines():
            workdir = os.path.join(self.workdir,line)
            cmd = "cd " + workdir + "&& " + self.cmakeMakeProgramm
            print cmd
            utils.system(cmd)
        f.close()
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
        self.svnpath=os.path.join( self.kdesvndir,self.subinfo.svnTargets['svnHEAD'])
        f = open( os.path.join(self.svnpath,"subdirs"), "r" )
        for line in f.read().splitlines():
            workdir = os.path.join(self.workdir,line)
            cmd = "cd %s && cmake.exe -DCMAKE_INSTALL_PREFIX=%s/%s -P cmake_install.cmake" % (workdir,self.imagedir,line)
            print cmd
            utils.system(cmd) or utils.die( "while installing. cmd: %s" % cmd )
        f.close()
        return True

    def uninstall( self ):
        self.svnpath=os.path.join( self.kdesvndir,self.subinfo.svnTargets['svnHEAD'])
        f = open( os.path.join(self.svnpath,"subdirs"), "r" )
        for line in f.read().splitlines():
            workdir = os.path.join(self.workdir,line)
            cmd = "cd %s && cmake.exe -P cmake_uninstall.cmake" % (workdir)
            print cmd
            utils.system(cmd) or utils.die( "while installing. cmd: %s" % cmd )
        f.close()
        return True

    def make_package( self ):
        self.svnpath=os.path.join( self.kdesvndir,self.subinfo.svnTargets['svnHEAD'])
        self.filesdir = os.path.join(self.packagedir,"files")
        dstpath = os.getenv( "EMERGE_PKGDSTDIR" )
        if not dstpath:
            dstpath = os.path.join( self.rootdir, "tmp" )

        f = open( os.path.join(self.svnpath,"subdirs"), "r" )
        for line in f.read().splitlines():
            workdir = os.path.join(self.workdir,line)
            self.packager = os.path.join(self.filesdir,"kdewin-packager") 
            cmd = self.packager + " -name kde-i18n-%s -version %s -hashfirst -compression 2 -root %s/%s -destdir %s" % (line,self.version,self.imagedir,line,dstpath)
            print cmd
            utils.system(cmd)
        f.close()
        return True

    def qmerge( self ):
        self.svnpath=os.path.join( self.kdesvndir,self.subinfo.svnTargets['svnHEAD'])
        f = open( os.path.join(self.svnpath,"subdirs"), "r" )
        for line in f.read().splitlines():
            utils.mergeImageDirToRootDir( os.path.join(self.imagedir,line), self.rootdir )
        f.close()
        return True
        
    def unmerge( self ):
        self.svnpath=os.path.join( self.kdesvndir,self.subinfo.svnTargets['svnHEAD'])
        f = open( os.path.join(self.svnpath,"subdirs"), "r" )
        for line in f.read().splitlines():
            print "implement unmerge for " + line 
            #utils.unmerge( self.rootdir, self.package, self.forced )
            #utils.remInstalled( self.category, self.package, self.version )
        f.close()
        return True
        
        

if __name__ == '__main__':
    subclass().execute()

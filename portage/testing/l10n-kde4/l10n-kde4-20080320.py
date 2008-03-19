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
        # FIXME: if enabled, let targets fails
        #self.hardDependencies['cmake'] = 'default'
        #self.hardDependencies['gettext-tools'] = 'default'
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
        return path.replace("\\","/").replace("c:","/c")

    def setupCygwin( self ):
        self.filesdir = os.path.join(self.packagedir,"files")
        self.shell = os.path.join(self.filesdir,"sh.exe")+" -c "
        self.svnpath=os.path.join( self.kdesvndir,self.subinfo.svnTargets['svnHEAD'])
        self.cmdprefix="PATH=.:"+self.toCygwinPath(self.filesdir)+":"+self.toCygwinPath(os.getenv( "KDEROOT" )+"/bin")
        self.envsettings=self.cmdprefix

    def unpack( self ):
        ret = self.kdeSvnUnpack()
        if not ret:
            return false

        self.setupCygwin()

        shellscript=self.toCygwinSeparator(os.path.join( self.svnpath,"scripts","autogen.sh"))
        cmd = "'"+self.cmdprefix+";cd "+self.toCygwinSeparator(self.svnpath)+";"+shellscript+"'"

        print self.shell + cmd
        utils.system(self.shell + cmd)
        return True
               
    def compile( self ):
        self.svnpath=os.path.join( self.kdesvndir,self.subinfo.svnTargets['svnHEAD'])
        self.kderoot = os.getenv( "KDEROOT" )
        f = open( os.path.join(self.svnpath,"subdirs"), "r" )
        for line in f.read().splitlines():
            defines = "-DCMAKE_INCLUDE_PATH=%s/include -DCMAKE_LIBRARY_PATH=%s/lib -DCMAKE_INSTALL_PREFIX=%s/%s" % (self.kderoot,self.kderoot,self.imagedir,line)
            workdir = os.path.join(self.workdir,line)
            if not os.path.exists( workdir ):
                os.mkdir(workdir)
            cmd = "cd " + workdir + "&& " + os.path.join(self.kderoot,"bin","cmake") +" -G \"%s\" %s/%s %s" % (self.cmakeMakefileGenerator, self.svnpath, line, defines ) 
            print cmd
            utils.system(cmd)
        f.close()
        f = open( os.path.join(self.svnpath,"subdirs"), "r" )
        for line in f.read().splitlines():
            workdir = os.path.join(self.workdir,line)
            cmd = "cd " + workdir + "&& " + self.cmakeMakeProgramm
            print cmd
            utils.system(cmd)
        f.close()
        return True

    def install( self ):
        self.svnpath=os.path.join( self.kdesvndir,self.subinfo.svnTargets['svnHEAD'])
        self.kderoot = os.getenv( "KDEROOT" )
        f = open( os.path.join(self.svnpath,"subdirs"), "r" )
        for line in f.read().splitlines():
            workdir = os.path.join(self.workdir,line)
            cmd = "cd " + workdir + "&& " + self.cmakeMakeProgramm + " install"
            print cmd
            utils.system(cmd)
        f.close()
        return True

    def make_package( self ):
        self.svnpath=os.path.join( self.kdesvndir,self.subinfo.svnTargets['svnHEAD'])
        self.kderoot = os.getenv( "KDEROOT" )
        self.filesdir = os.path.join(self.packagedir,"files")
        dstpath = os.getenv( "EMERGE_PKGDSTDIR" )
        if not dstpath:
            dstpath = os.path.join( self.rootdir, "tmp" )

        f = open( os.path.join(self.svnpath,"subdirs"), "r" )
        for line in f.read().splitlines():
            workdir = os.path.join(self.workdir,line)
            self.packager = os.path.join(self.filesdir,"kdewin-packager") 
            cmd = self.packager + " -name kde-i18n-%s -version %s -root %s/%s -destdir %s" % (line,self.version,self.imagedir,line,dstpath)
            print cmd
            utils.system(cmd)
        f.close()
        return True

if __name__ == '__main__':
    subclass().execute()

import base
import utils
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'branches/stable/l10n-kde4/'
        for ver in ['80', '96']:
          self.targets['4.1.' + ver] = 'ftp://ftp.kde.org/pub/kde/unstable/4.1.' + ver + '/src/kde-l10n/'
        self.defaultTarget = 'svnHEAD'

        # all targets in svn
        self.languages  = 'af ar be bg bn bn_IN br ca cs csb cy da de '
        self.languages += 'el en_GB eo es et eu fa fi fr fy ga gl gu '
        self.languages += 'ha he hi hr hsb hu hy is it ja ka kk km kn ko ku '
        self.languages += 'lb lt lv mk ml ms mt nb nds ne nl nn nso oc '
        self.languages += 'pa pl pt pt_BR ro ru rw se sk sl sr sv '
        self.languages += 'ta te tg th tr uk uz vi wa xh zh_CN zh_HK zh_TW '

        # released target in 4.1.96
        self.languages  = 'ar bg ca cs csb da de '
        self.languages += 'el en_GB eo es et '
        self.languages += 'fi fr fy ga gl gu he hi hu '
        self.languages += 'it ja kk km ko ku '
        self.languages += 'lt lv mk ml nb nds nl nn '
        self.languages += 'pa pl pt pt_BR ro ru sl sr sv '
        self.languages += 'ta th tr uk wa zh_CN zh_TW '

        self.languages  = 'pa pl pt pt_BR ro ru sl sr sv ta th tr uk wa zh_CN zh_TW'

    def setDependencies( self ):
        self.hardDependencies['dev-util/cmake'] = 'default'
        self.hardDependencies['dev-util/gettext-tools'] = 'default'
        self.hardDependencies['kde-4.2/kdelibs'] = 'default'
        
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()

    def fetch( self ):
        if self.noFetch:
            return True
        svnpath = self.kdeSvnPath()
        if svnpath:
            return base.baseclass.fetch( self )

        if len( self.subinfo.targets ) and self.subinfo.buildTarget in self.subinfo.targets.keys():
            for pkg in self.subinfo.languages.split():
                tgt = self.subinfo.buildTarget
                filename = self.subinfo.targets[ tgt ] + 'kde-l10n-' + pkg + '-' + tgt + '.tar.bz2' 
                return utils.getFiles( filename, self.downloaddir )
        else:
            return False

        return True

    def unpack( self ):
        svnpath = self.kdeSvnPath()
        utils.cleanDirectory( self.workdir )

        if svnpath:
            if not self.kdeSvnUnpack( svnpath, "scripts" ):
                return False
                
            for pkg in self.subinfo.languages.split():
                if not self.kdeSvnUnpack( svnpath, pkg ):
                    return False
                else:
                    print "Unpacked %s" % pkg
            autogen = os.path.join( self.packagedir , "autogen.py" )
            svnpath = os.path.join( self.kdesvndir, svnpath )
    
    
            # execute autogen.py and generate the CMakeLists.txt files
            cmd = "cd %s && %s %s" % \
                  (svnpath , autogen, self.subinfo.languages )
            utils.system( cmd )

        else:
            filenames = []
            for pkg in self.subinfo.languages.split():
                if not self.subinfo.buildTarget in self.subinfo.targets.keys():
                    return False
                tgt = self.subinfo.buildTarget
                filenames.append( 'kde-l10n-' + pkg + '-' + tgt + '.tar.bz2' )
            if not utils.unpackFiles( self.downloaddir, filenames, self.workdir ):
                return False
            # no need for autogen.py - CMake scripts are already created
        return True

    def compile( self ):
        self.kde.nocopy = False
        sourcePath = self.kde.sourcePath
        svnpath = self.kdeSvnPath()
        for pkg in self.subinfo.languages.split():
            self.kde.buildNameExt = pkg
            if svnpath:
                self.kde.sourcePath = os.path.join( sourcePath, pkg )
            else:
                pkg_dir = 'kde-l10n-' + pkg + '-' + self.subinfo.buildTarget
                self.kde.sourcePath = os.path.join( sourcePath, pkg_dir )
            self.kdeCompile()
        return True

    def install( self ):
        self.kde.nocopy = False
        imgdir = self.kde.imagedir
        for pkg in self.subinfo.languages.split():
            self.kde.buildNameExt = pkg
            self.kde.imagedir = os.path.join( imgdir, pkg )
            self.kdeInstall()
        return True

    def qmerge( self ):
        imgdir = self.kde.imagedir
        for pkg in self.subinfo.languages.split():
            self.kde.buildNameExt = pkg
            self.kde.imagedir = os.path.join( imgdir, pkg )
            utils.mergeImageDirToRootDir( self.kde.imagedir, self.rootdir )
        return True

    def make_package( self ):
        self.svnpath = os.path.join( self.kdesvndir, self.subinfo.svnTargets['svnHEAD'] )
        self.filesdir = os.path.join( self.packagedir, "files" )
        dstpath = os.getenv( "EMERGE_PKGDSTDIR" )
        if not dstpath:
            dstpath = os.path.join( self.rootdir, "tmp" )

        if not utils.test4application( "kdewin-packager" ):
            utils.die( "kdewin-packager not found - please make sure it is in your path" )

        for pkg in self.subinfo.languages.split():
            workdir = os.path.join( self.workdir, pkg )
            cmd = "kdewin-packager -name kde-l10n-%s -version %s -hashfirst -compression 2 -root %s/%s -destdir %s" % \
                  ( pkg, self.buildTarget, self.imagedir, pkg, dstpath )
            utils.system( cmd )
        return True

if __name__ == '__main__':
    subclass().execute()

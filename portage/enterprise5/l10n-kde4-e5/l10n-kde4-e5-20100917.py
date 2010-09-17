import base
import utils
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['20091111'] = 'tags/kdepim/pe5.20091111/l10n-kde4/'
        self.svnTargets['20091123'] = 'tags/kdepim/pe5.20091123/l10n-kde4/'
        self.svnTargets['20091201'] = 'tags/kdepim/pe5.20091201/l10n-kde4/'
        self.svnTargets['20100101'] = 'tags/kdepim/enterprise5.0.20100101.1068602/l10n-kde4'
        self.svnTargets['20100115'] = 'tags/kdepim/enterprise5.0.20100115.1075215/l10n-kde4'
        self.svnTargets['20100122'] = 'tags/kdepim/enterprise5.0.20100122.1078631/l10n-kde4'
        self.svnTargets['20100129'] = 'tags/kdepim/enterprise5.0.20100129.1082020/l10n-kde4'
        self.svnTargets['20100205'] = 'tags/kdepim/enterprise5.0.20100205.1085631/l10n-kde4'
        self.svnTargets['20100212'] = 'tags/kdepim/enterprise5.0.20100212.1089060/l10n-kde4'
        self.svnTargets['20100219'] = 'tags/kdepim/enterprise5.0.20100219.1092868/l10n-kde4'
        self.svnTargets['20100226'] = 'tags/kdepim/enterprise5.0.20100226.1096279/l10n-kde4'
        self.svnTargets['20100305'] = 'tags/kdepim/enterprise5.0.20100305.1099232/l10n-kde4'
        self.svnTargets['20100312'] = 'tags/kdepim/enterprise5.0.20100312.1102371/l10n-kde4'
        self.svnTargets['20100319'] = 'tags/kdepim/enterprise5.0.20100319.1105074/l10n-kde4'
        self.svnTargets['20100326'] = 'tags/kdepim/enterprise5.0.20100326.1107645/l10n-kde4'
        self.svnTargets['20100401'] = 'tags/kdepim/enterprise5.0.20100401.1110042/l10n-kde4'
        self.svnTargets['20100409'] = 'tags/kdepim/enterprise5.0.20100409.1112952/l10n-kde4'
        self.svnTargets['20100507'] = 'tags/kdepim/enterprise5.0.20100507.1123982/l10n-kde4'
        self.svnTargets['20100528'] = 'tags/kdepim/enterprise5.0.20100528.1131643/l10n-kde4'
        self.svnTargets['20100604'] = 'tags/kdepim/enterprise5.0.20100604.1134428/l10n-kde4'
        self.svnTargets['20100611'] = 'tags/kdepim/enterprise5.0.20100611.1136974/l10n-kde4'
        self.svnTargets['20100618'] = 'tags/kdepim/enterprise5.0.20100618.1139547/l10n-kde4'
        self.svnTargets['20100625'] = 'tags/kdepim/enterprise5.0.20100625.1142603/l10n-kde4'
        self.svnTargets['20100701'] = 'tags/kdepim/enterprise5.0.20100701.1144979/l10n-kde4'
        self.svnTargets['20100709'] = 'tags/kdepim/enterprise5.0.20100709.1148001/l10n-kde4'
        self.svnTargets['20100716'] = 'tags/kdepim/enterprise5.0.20100716.1150616/l10n-kde4'
        self.svnTargets['20100723'] = 'tags/kdepim/enterprise5.0.20100723.1153624/l10n-kde4'
        self.svnTargets['20100730'] = 'tags/kdepim/enterprise5.0.20100730.1157241/l10n-kde4'
        self.svnTargets['20100805'] = 'tags/kdepim/enterprise5.0.20100805.1159431/l10n-kde4'
        self.svnTargets['20100813'] = 'tags/kdepim/enterprise5.0.20100813.1163234/l10n-kde4'
        self.svnTargets['20100820'] = 'tags/kdepim/enterprise5.0.20100820.1165957/l10n-kde4'
        self.svnTargets['20100827'] = 'tags/kdepim/enterprise5.0.20100827.1168749/l10n-kde4'
        self.svnTargets['20100903'] = 'tags/kdepim/enterprise5.0.20100903.1171282/l10n-kde4'
        self.svnTargets['20100910'] = 'tags/kdepim/enterprise5.0.20100910.1173808/l10n-kde4'
        self.svnTargets['20100917'] = 'tags/kdepim/enterprise5.0.20100917.1176291/l10n-kde4'
        self.defaultTarget = '20100917'

        # all targets 
        self.languages  = 'de'
    
    def setDependencies( self ):
        self.hardDependencies['dev-util/cmake'] = 'default'
        self.hardDependencies['dev-util/gettext-tools'] = 'default'
        self.hardDependencies['enterprise5/kdelibs-e5'] = 'default'
        
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
            autogen = os.path.join( self.packagedir , "autogen.py" )
            svnpath = os.path.join( self.kdesvndir, svnpath )
    
    
            # execute autogen.py and generate the CMakeLists.txt files
            cmd = "cd %s && python %s %s" % \
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
            if not self.kdeCompile():
                return False
        return True

    def install( self ):
        self.kde.nocopy = False
        imgdir = self.kde.imagedir
        for pkg in self.subinfo.languages.split():
            self.kde.buildNameExt = pkg
            self.kde.imagedir = os.path.join( imgdir, pkg )
            if not self.kdeInstall():
                return False
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

import base
import utils
import os
import sys
import info
import shutil

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdebase/workspace/cursors/src'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kdesupport/kdewin32'] = 'default'
        self.hardDependencies['gnuwin32/sed'] = 'default'
        
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        srcdir = os.path.join(self.workdir, os.getenv("KDECOMPILER")+"-"+self.buildType, "wincursors")
        destdir = os.path.join(self.cmakeInstallPrefix, "share", "icons")
        utils.copySrcDirToDestDir(srcdir, destdir)
        
        srcreg = os.path.join(self.packagedir, "cursor.reg")
        dstreg = os.path.join(self.workdir, "cursor.reg")
        shutil.copy(srcreg, dstreg)

        utils.sedFile(self.workdir, "cursor.reg", "s/CHANGEME/%s/g"%destdir.replace("\\", "\\\\\\\\").replace("/", "\\\\\\\\"))
        utils.system("regedit /S %s"%os.path.join(self.workdir, "cursor.reg"))
        return True

if __name__ == '__main__':
    subclass().execute()

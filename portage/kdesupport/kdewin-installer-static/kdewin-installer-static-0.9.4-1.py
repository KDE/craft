import base
import utils
import sys
import info
import os.path

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['libs/qt-static'] = 'default'
        self.hardDependencies['dev-util/upx'] = 'default'

    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/kdewin-installer'
        self.defaultTarget = 'svnHEAD'

class subclass(base.baseclass):
    def __init__(self, **args):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "kdewin-installer"
        self.buildType = "Release"
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        self.kdeCustomDefines = "-DQT_QMAKE_EXECUTABLE:FILEPATH=%s" \
            % os.path.join(self.rootdir, "qt-static", "bin", "qmake.exe").replace('\\', '/')
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        return self.doPackaging( "kdewin-installer", utils.cleanPackageName( sys.argv[0], "kdewin-installer" ), True )

if __name__ == '__main__':
    subclass().execute()

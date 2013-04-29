import info
import kdedefaults as kd

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['0', '1', '2', '3', '4', '5']:
            self.targets[kd.kdeversion + ver] = "http://download.kde.org/stable/" + kd.kdeversion + ver + "/src/kde-l10n/" + self.package + "-" + kd.kdeversion + ver + ".tar.xz"
            self.targetInstSrc[kd.kdeversion + ver] = self.package + '-' + kd.kdeversion + ver

        self.defaultTarget = kd.kdeversion + '0'

    def setDependencies( self ):
        self.buildDependencies['dev-util/cmake'] = 'default'
        self.buildDependencies['kde/kdelibs'] = 'default'
        self.buildDependencies['dev-util/gettext-tools'] = 'default'


from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

    def install( self ):
        if not CMakePackageBase.install( self ):
            return False
        meinproc = os.path.join( self.rootdir, "bin", "meinproc4.exe" )
        docdir=os.path.join(self.installDir(), "share", "doc", "HTML", "de", "kleopatra")
        utils.system([meinproc, os.path.join(docdir, "index.docbook")],
                cwd=docdir)
        return True


if __name__ == '__main__':
    Package().execute()

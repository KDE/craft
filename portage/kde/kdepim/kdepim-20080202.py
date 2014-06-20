import info
import kdedefaults as kd

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:%s|%s|' % (self.package, kd.kdebranch)
        self.svnTargets['gpg4win'] = '[git]kde:kdepim|gpg4win|'
        for ver in ['0', '1', '2', '3', '4', '5']:
            self.targets[kd.kdeversion + ver] = "http://download.kde.org/stable/" + kd.kdeversion + ver + "/src/" + self.package + "-" + kd.kdeversion + ver + ".tar.xz"
            self.targetInstSrc[kd.kdeversion + ver] = self.package + '-' + kd.kdeversion + ver
            self.targetDigestUrls[ kd.kdeversion + ver  ] = 'http://download.kde.org/stable/' + kd.kdeversion + ver + '/src/' + self.package + '-' + kd.kdeversion + ver + '.tar.xz.sha1'
            self.patchToApply[kd.kdeversion + ver] = [('fix_introduction_screen.diff', 1),  # not to be upstreamed, this is an ugly hack, the fix is somewhere else (ref. bug 302342)
                                                      ('0001-fixed-windows-x64-build.patch', 1),# reverted upstream (does not compile on Linux)
                                                      ('0002-fixed-windows-x64-build.patch', 1),
                                                      ("fixknote.diff",1)] #this needs some review

        self.defaultTarget = 'gpg4win'

        self.patchToApply['gitHEAD'] = [('fix_introduction_screen.diff', 1),
                                        ('0001-fixed-windows-x64-build.patch', 1)]

    def setDependencies( self ):
        self.runtimeDependencies['kde/kde-runtime'] = 'default'
#        self.runtimeDependencies['kde/kdepim-runtime'] = 'default'
        self.dependencies['kde/kdepimlibs'] = 'default'
#        self.dependencies['kdesupport/grantlee'] = 'default'
#        self.dependencies['kde/nepomuk-widgets'] = 'default'
        self.shortDescription = "KDE's Personal Information Management suite"

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

        self.subinfo.options.configure.defines = ( " -DKDEPIM_ONLY_KLEO=True"
                " -DBUILD_doc=TRUE"
                " -DBUILD_kleopatra=TRUE" )

    # For kleo only we want a html handbook
    def install( self ):
        if not CMakePackageBase.install( self ):
            return False
        meinproc = os.path.join( self.rootdir, "bin", "meinproc4.exe" )
        docdir=os.path.join(self.installDir(), "share", "doc", "HTML", "en", "kleopatra")
        utils.system([meinproc, os.path.join(docdir, "index.docbook")],
                cwd=docdir)
        return True
if __name__ == '__main__':
    Package().execute()

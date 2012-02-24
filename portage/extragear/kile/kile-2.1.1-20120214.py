import info
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:kile'
        self.svnTargets['gitStable-2.1'] = '[git]kde:kile|2.1|'
        for ver in ['2.1.1']:
            self.targets[ver] = 'http://downloads.sourceforge.net/kile/kile-' + ver + '.tar.bz2'
            self.targetInstSrc[ver] = 'kile-' + ver
        self.shortDescription = "a user friendly TeX/LaTeX editor for KDE"
        self.defaultTarget = 'gitStable-2.1'

    def setDependencies( self ):
        self.dependencies['kde/kde-runtime'] = 'default'
        self.dependencies['kdesupport/poppler'] = 'default' # this is only a dependency for kile > 2.1, but we keep it like that for now
        self.dependencies['kde/okular'] = 'default'         # this is only a dependency for kile > 2.1, but we keep it like that for now
        self.runtimeDependencies['extragear/kate'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
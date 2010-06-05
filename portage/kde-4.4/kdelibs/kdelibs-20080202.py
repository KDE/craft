import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'branches/KDE/4.4/kdelibs'
        for ver in ['90', '95']:
          self.targets['4.3.' + ver] = 'ftp://ftp.kde.org/pub/kde/unstable/4.3.' + ver + '/src/kdelibs-4.3.' + ver + '.tar.bz2'
          self.targetInstSrc['4.3.' + ver] = 'kdelibs-4.3.' + ver
        for ver in ['0', '1', '2', '3', '4']:
          self.targets['4.4.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.4.' + ver + '/src/kdelibs-4.4.' + ver + '.tar.bz2'
          self.targetInstSrc['4.4.' + ver] = 'kdelibs-4.4.' + ver
        self.patchToApply['4.3.90'] = ("kdelibs-4.3.90.diff", 1)
        self.patchToApply['4.3.95'] = ("kdelibs-4.3.95.diff", 1)
        self.patchToApply['4.4.0'] = ("kdelibs-4.4.0.diff", 1)
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kdesupport/kdewin'] = 'default'
        self.hardDependencies['kdesupport/qimageblitz'] = 'default'
        self.hardDependencies['kdesupport/soprano'] = 'default'
        self.hardDependencies['kdesupport/strigi'] = 'default'
        self.hardDependencies['kdesupport/phonon'] = 'default'
        self.hardDependencies['kdesupport/attica'] = 'default'
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['dev-util/perl'] = 'default'
        self.hardDependencies['virtual/kdelibs-base'] = 'default'
    
from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        if self.compiler() == "mingw":
          self.subinfo.options.configure.defines = " -DKDE_DISTRIBUTION_TEXT=\"MinGW 3.4.5\" "
        elif self.compiler() == "mingw4":
          self.subinfo.options.configure.defines = " -DKDE_DISTRIBUTION_TEXT=\"MinGW 4.4.0\" "
        elif self.compiler() == "msvc2005":
          self.subinfo.options.configure.defines = " -DKDE_DISTRIBUTION_TEXT=\"MS Visual Studio 2005 SP1\" "
        elif self.compiler() == "msvc2008":
          self.subinfo.options.configure.defines = " -DKDE_DISTRIBUTION_TEXT=\"MS Visual Studio 2008 SP1\" "


if __name__ == '__main__':
    Package().execute()


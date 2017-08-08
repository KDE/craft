import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["qt-libs/phonon"] = "default"

    def setTargets(self):
        self.svnTargets['master'] = '[git]kde:phonon-directshow'
        self.description = "the DirectShow based phonon multimedia backend"
        self.defaultTarget = 'master'


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = ' -DPHONON_BUILD_PHONON4QT5=ON -DPHONON_BUILDSYSTEM_DIR=\"%s\" ' % (
        os.path.join(CraftStandardDirs.craftRoot(), 'share', 'phonon', 'buildsystem').replace('\\', '/'))

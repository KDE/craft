import info


class subinfo(info.infoclass):
    def setDependencies(self):
        craftDebug.log.debug("craftbuildsystem:subinfo.setDependencies not implemented yet")
        # we need at least qmake
        # self.runtimeDependencies['libs/qt'] = 'default'
        self.buildDependencies['dev-util/jom'] = 'default'

        if craftCompiler.isMinGW():
            self.buildDependencies['dev-util/mingw-w64'] = 'default'


from Package.InternalPackageBase import *


class Package(InternalPackageBase):
    def __init__(self):
        InternalPackageBase.__init__(self)

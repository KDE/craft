import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'https://github.com/KDAB/KDStateMachineEditor.git'
        self.svnTargets['1.2'] = 'https://github.com/KDAB/KDStateMachineEditor.git|1.2'
        for ver in ["1.2.0", "1.2.1"]:
            self.targets[ver] = 'https://github.com/KDAB/KDStateMachineEditor/archive/v%s.tar.gz' % ver
            self.archiveNames[ver] = "kdstatemachineeditor-%s.tar.gz" % ver
            self.targetInstSrc[ver] = 'KDStateMachineEditor-%s' % ver

        self.targetDigests['1.2.0'] = (
            ['c43b864e60c025b1d4eb03f0b3073e00ebb642aecf10dd8b5b29f4a2da2b1c07'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['1.2.1'] = (
            ['a97597aa3c67356bba7f6c1503018ddf3369ada5534f33129adab29a53f6ed11'], CraftHash.HashAlgorithm.SHA256)

        self.description = "The KDAB State Machine Editor Library is a framework that can be used to help develop full-featured State Machine Editing graphical user interfaces and tools."
        self.defaultTarget = "1.2.1"

    def setDependencies(self):
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["libs/qt5/qtdeclarative"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = "-DWITH_INTERNAL_GRAPHVIZ=OFF"

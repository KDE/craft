import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['1.1.6']:
            self.targets[ver] = "http://downloads.sourceforge.net/sourceforge/fluidsynth/fluidsynth-%s.tar.bz2" % ver
            self.targetInstSrc[ver] = 'fluidsynth-%s' % ver
        self.targetDigests['1.1.6'] = (
            ['d28b47dfbf7f8e426902ae7fa2981d821fbf84f41da9e1b85be933d2d748f601'], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply['1.1.6'] = [('fluidsynth-1.1.6-20160908.diff', 1)]

        self.description = "FluidSynth is a real-time software synthesizer based on the SoundFont 2 specifications and has reached widespread distribution."
        self.webpage = "http://www.fluidsynth.org/"
        self.defaultTarget = '1.1.6'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/pkg-config"] = "default"
        self.runtimeDependencies["win32libs/glib"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)

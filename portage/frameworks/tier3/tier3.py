import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = ''
        self.defaultTarget = 'master'
        self.description = 'kf5 tier3'

    def setDependencies(self):
        self.runtimeDependencies["frameworks/tier3/kactivities"] = "default"
        self.runtimeDependencies["frameworks/tier3/kbookmarks"] = "default"
        self.runtimeDependencies["frameworks/tier3/kcmutils"] = "default"
        self.runtimeDependencies["frameworks/tier3/kconfigwidgets"] = "default"
        self.runtimeDependencies["frameworks/tier3/kdeclarative"] = "default"
        self.runtimeDependencies["frameworks/tier3/kded"] = "default"
        self.runtimeDependencies["frameworks/tier3/kdesignerplugin"] = "default"
        self.runtimeDependencies["frameworks/tier3/kdewebkit"] = "default"
        self.runtimeDependencies["frameworks/tier3/kemoticons"] = "default"
        self.runtimeDependencies["frameworks/tier3/khtml"] = "default"
        self.runtimeDependencies["frameworks/tier3/kiconthemes"] = "default"
        self.runtimeDependencies["frameworks/tier3/kinit"] = "default"
        self.runtimeDependencies["frameworks/tier3/kio"] = "default"
        self.runtimeDependencies["frameworks/tier3/kjs"] = "default"
        self.runtimeDependencies["frameworks/tier3/kjsembed"] = "default"
        self.runtimeDependencies["frameworks/tier3/kmediaplayer"] = "default"
        self.runtimeDependencies["frameworks/tier3/knewstuff"] = "default"
        self.runtimeDependencies["frameworks/tier3/knotifications"] = "default"
        self.runtimeDependencies["frameworks/tier3/knotifyconfig"] = "default"
        self.runtimeDependencies["frameworks/tier3/kparts"] = "default"
        self.runtimeDependencies["frameworks/tier3/kross"] = "default"
        self.runtimeDependencies["frameworks/tier3/krunner"] = "default"
        self.runtimeDependencies["frameworks/tier3/kservice"] = "default"
        self.runtimeDependencies["frameworks/tier3/ktexteditor"] = "default"
        self.runtimeDependencies["frameworks/tier3/ktextwidgets"] = "default"
        self.runtimeDependencies["frameworks/tier3/kwallet"] = "default"
        self.runtimeDependencies["frameworks/tier3/kxmlgui"] = "default"
        self.runtimeDependencies["frameworks/tier3/plasma-framework"] = "default"
        self.runtimeDependencies["frameworks/tier3/kglobalaccel"] = "default"


from Package.VirtualPackageBase import *


class Package(VirtualPackageBase):
    def __init__(self):
        VirtualPackageBase.__init__(self)

import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = ''
        self.defaultTarget = 'master'
        self.shortDescription = 'kf5 tier3'

    def setDependencies(self):
        self.runtimeDependencies['frameworks/kactivities'] = 'default'
        self.runtimeDependencies['frameworks/kbookmarks'] = 'default'
        self.runtimeDependencies['frameworks/kcmutils'] = 'default'
        self.runtimeDependencies['frameworks/kconfigwidgets'] = 'default'
        self.runtimeDependencies['frameworks/kdeclarative'] = 'default'
        self.runtimeDependencies['frameworks/kded'] = 'default'
        self.runtimeDependencies['frameworks/kdesignerplugin'] = 'default'
        self.runtimeDependencies['frameworks/kdewebkit'] = 'default'
        self.runtimeDependencies['frameworks/kemoticons'] = 'default'
        self.runtimeDependencies['frameworks/khtml'] = 'default'
        self.runtimeDependencies['frameworks/kiconthemes'] = 'default'
        self.runtimeDependencies['frameworks/kinit'] = 'default'
        self.runtimeDependencies['frameworks/kio'] = 'default'
        self.runtimeDependencies['frameworks/kjs'] = 'default'
        self.runtimeDependencies['frameworks/kjsembed'] = 'default'
        self.runtimeDependencies['frameworks/kmediaplayer'] = 'default'
        self.runtimeDependencies['frameworks/knewstuff'] = 'default'
        self.runtimeDependencies['frameworks/knotifications'] = 'default'
        self.runtimeDependencies['frameworks/knotifyconfig'] = 'default'
        self.runtimeDependencies['frameworks/kparts'] = 'default'
        self.runtimeDependencies['frameworks/kross'] = 'default'
        self.runtimeDependencies['frameworks/krunner'] = 'default'
        self.runtimeDependencies['frameworks/kservice'] = 'default'
        self.runtimeDependencies['frameworks/ktexteditor'] = 'default'
        self.runtimeDependencies['frameworks/ktextwidgets'] = 'default'
        self.runtimeDependencies['frameworks/kwallet'] = 'default'
        self.runtimeDependencies['frameworks/kxmlgui'] = 'default'
        self.runtimeDependencies['frameworks/plasma-framework'] = 'default'
        self.runtimeDependencies['frameworks/kglobalaccel'] = 'default'


from Package.VirtualPackageBase import *


class Package(VirtualPackageBase):
    def __init__(self):
        VirtualPackageBase.__init__(self)

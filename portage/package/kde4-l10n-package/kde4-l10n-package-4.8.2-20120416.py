import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['4.8.2'] = ''
        self.defaultTarget = '4.8.2'

    def setDependencies( self ):
        self.dependencies['package/kde4-l10n-package-ar'] = 'default'
        self.dependencies['package/kde4-l10n-package-bg'] = 'default'
        self.dependencies['package/kde4-l10n-package-bs'] = 'default'
        self.dependencies['package/kde4-l10n-package-ca'] = 'default'
        self.dependencies['package/kde4-l10n-package-ca@valencia'] = 'default'
        self.dependencies['package/kde4-l10n-package-cs'] = 'default'
        self.dependencies['package/kde4-l10n-package-da'] = 'default'
        self.dependencies['package/kde4-l10n-package-de'] = 'default'
        self.dependencies['package/kde4-l10n-package-el'] = 'default'
        self.dependencies['package/kde4-l10n-package-en_GB'] = 'default'
        self.dependencies['package/kde4-l10n-package-es'] = 'default'
        self.dependencies['package/kde4-l10n-package-et'] = 'default'
        self.dependencies['package/kde4-l10n-package-eu'] = 'default'
        self.dependencies['package/kde4-l10n-package-fi'] = 'default'
        self.dependencies['package/kde4-l10n-package-fr'] = 'default'
        self.dependencies['package/kde4-l10n-package-ga'] = 'default'
        self.dependencies['package/kde4-l10n-package-gl'] = 'default'
        self.dependencies['package/kde4-l10n-package-he'] = 'default'
        self.dependencies['package/kde4-l10n-package-hr'] = 'default'
        self.dependencies['package/kde4-l10n-package-hu'] = 'default'
        self.dependencies['package/kde4-l10n-package-ia'] = 'default'
        self.dependencies['package/kde4-l10n-package-id'] = 'default'
        self.dependencies['package/kde4-l10n-package-is'] = 'default'
        self.dependencies['package/kde4-l10n-package-it'] = 'default'
        self.dependencies['package/kde4-l10n-package-ja'] = 'default'
        self.dependencies['package/kde4-l10n-package-kk'] = 'default'
        self.dependencies['package/kde4-l10n-package-km'] = 'default'
        self.dependencies['package/kde4-l10n-package-kn'] = 'default'
        self.dependencies['package/kde4-l10n-package-ko'] = 'default'
        self.dependencies['package/kde4-l10n-package-lt'] = 'default'
        self.dependencies['package/kde4-l10n-package-lv'] = 'default'
        self.dependencies['package/kde4-l10n-package-nb'] = 'default'
        self.dependencies['package/kde4-l10n-package-nds'] = 'default'
        self.dependencies['package/kde4-l10n-package-nl'] = 'default'
        self.dependencies['package/kde4-l10n-package-nn'] = 'default'
        self.dependencies['package/kde4-l10n-package-pa'] = 'default'
        self.dependencies['package/kde4-l10n-package-pl'] = 'default'
        self.dependencies['package/kde4-l10n-package-pt'] = 'default'
        self.dependencies['package/kde4-l10n-package-pt_BR'] = 'default'
        self.dependencies['package/kde4-l10n-package-ro'] = 'default'
        self.dependencies['package/kde4-l10n-package-ru'] = 'default'
        self.dependencies['package/kde4-l10n-package-sk'] = 'default'
        self.dependencies['package/kde4-l10n-package-sl'] = 'default'
        self.dependencies['package/kde4-l10n-package-sr'] = 'default'
        self.dependencies['package/kde4-l10n-package-sv'] = 'default'
        self.dependencies['package/kde4-l10n-package-th'] = 'default'
        self.dependencies['package/kde4-l10n-package-tr'] = 'default'
        self.dependencies['package/kde4-l10n-package-ug'] = 'default'
        self.dependencies['package/kde4-l10n-package-uk'] = 'default'
        self.dependencies['package/kde4-l10n-package-wa'] = 'default'
        self.dependencies['package/kde4-l10n-package-zh_CN'] = 'default'
        self.dependencies['package/kde4-l10n-package-zh_TW'] = 'default'

from Package.VirtualPackageBase import *

class Package( VirtualPackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        VirtualPackageBase.__init__( self )


if __name__ == '__main__':
    Package().execute()

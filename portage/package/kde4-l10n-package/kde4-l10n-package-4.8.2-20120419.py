import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['4.8.2'] = ''
        self.defaultTarget = '4.8.2'

    def setDependencies( self ):
        self.dependencies['package/kde4-l10n-ar-package'] = 'default'
        self.dependencies['package/kde4-l10n-bg-package'] = 'default'
        self.dependencies['package/kde4-l10n-bs-package'] = 'default'
        self.dependencies['package/kde4-l10n-ca-package'] = 'default'
        self.dependencies['package/kde4-l10n-ca@valencia-package'] = 'default'
        self.dependencies['package/kde4-l10n-cs-package'] = 'default'
        self.dependencies['package/kde4-l10n-da-package'] = 'default'
        self.dependencies['package/kde4-l10n-de-package'] = 'default'
        self.dependencies['package/kde4-l10n-el-package'] = 'default'
        self.dependencies['package/kde4-l10n-en_GB-package'] = 'default'
        self.dependencies['package/kde4-l10n-es-package'] = 'default'
        self.dependencies['package/kde4-l10n-et-package'] = 'default'
        self.dependencies['package/kde4-l10n-eu-package'] = 'default'
        self.dependencies['package/kde4-l10n-fi-package'] = 'default'
        self.dependencies['package/kde4-l10n-fr-package'] = 'default'
        self.dependencies['package/kde4-l10n-ga-package'] = 'default'
        self.dependencies['package/kde4-l10n-gl-package'] = 'default'
        self.dependencies['package/kde4-l10n-he-package'] = 'default'
        self.dependencies['package/kde4-l10n-hr-package'] = 'default'
        self.dependencies['package/kde4-l10n-hu-package'] = 'default'
        self.dependencies['package/kde4-l10n-ia-package'] = 'default'
        self.dependencies['package/kde4-l10n-id-package'] = 'default'
        self.dependencies['package/kde4-l10n-is-package'] = 'default'
        self.dependencies['package/kde4-l10n-it-package'] = 'default'
        self.dependencies['package/kde4-l10n-ja-package'] = 'default'
        self.dependencies['package/kde4-l10n-kk-package'] = 'default'
        self.dependencies['package/kde4-l10n-km-package'] = 'default'
        self.dependencies['package/kde4-l10n-ko-package'] = 'default'
        self.dependencies['package/kde4-l10n-lt-package'] = 'default'
        self.dependencies['package/kde4-l10n-lv-package'] = 'default'
        self.dependencies['package/kde4-l10n-nb-package'] = 'default'
        self.dependencies['package/kde4-l10n-nds-package'] = 'default'
        self.dependencies['package/kde4-l10n-nl-package'] = 'default'
        self.dependencies['package/kde4-l10n-nn-package'] = 'default'
        self.dependencies['package/kde4-l10n-pa-package'] = 'default'
        self.dependencies['package/kde4-l10n-pl-package'] = 'default'
        self.dependencies['package/kde4-l10n-pt-package'] = 'default'
        self.dependencies['package/kde4-l10n-pt_BR-package'] = 'default'
        self.dependencies['package/kde4-l10n-ro-package'] = 'default'
        self.dependencies['package/kde4-l10n-ru-package'] = 'default'
        self.dependencies['package/kde4-l10n-sk-package'] = 'default'
        self.dependencies['package/kde4-l10n-sl-package'] = 'default'
        self.dependencies['package/kde4-l10n-sr-package'] = 'default'
        self.dependencies['package/kde4-l10n-sv-package'] = 'default'
        self.dependencies['package/kde4-l10n-th-package'] = 'default'
        self.dependencies['package/kde4-l10n-tr-package'] = 'default'
        self.dependencies['package/kde4-l10n-ug-package'] = 'default'
        self.dependencies['package/kde4-l10n-uk-package'] = 'default'
        self.dependencies['package/kde4-l10n-wa-package'] = 'default'
        self.dependencies['package/kde4-l10n-zh_CN-package'] = 'default'
        self.dependencies['package/kde4-l10n-zh_TW-package'] = 'default'

from Package.VirtualPackageBase import *

class Package( VirtualPackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        VirtualPackageBase.__init__( self )


if __name__ == '__main__':
    Package().execute()

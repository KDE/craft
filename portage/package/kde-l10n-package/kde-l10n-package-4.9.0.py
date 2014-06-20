import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['4.9.0'] = ''
        self.defaultTarget = '4.9.0'

    def setDependencies( self ):
        self.dependencies['package/kde-l10n-ar-package'] = 'default'
        self.dependencies['package/kde-l10n-bg-package'] = 'default'
        self.dependencies['package/kde-l10n-bs-package'] = 'default'
        self.dependencies['package/kde-l10n-ca-package'] = 'default'
        self.dependencies['package/kde-l10n-ca@valencia-package'] = 'default'
        self.dependencies['package/kde-l10n-cs-package'] = 'default'
        self.dependencies['package/kde-l10n-da-package'] = 'default'
        self.dependencies['package/kde-l10n-de-package'] = 'default'
        self.dependencies['package/kde-l10n-el-package'] = 'default'
        self.dependencies['package/kde-l10n-en_GB-package'] = 'default'
        self.dependencies['package/kde-l10n-es-package'] = 'default'
        self.dependencies['package/kde-l10n-et-package'] = 'default'
        self.dependencies['package/kde-l10n-eu-package'] = 'default'
        self.dependencies['package/kde-l10n-fi-package'] = 'default'
        self.dependencies['package/kde-l10n-fr-package'] = 'default'
        self.dependencies['package/kde-l10n-ga-package'] = 'default'
        self.dependencies['package/kde-l10n-gl-package'] = 'default'
        self.dependencies['package/kde-l10n-he-package'] = 'default'
        self.dependencies['package/kde-l10n-hr-package'] = 'default'
        self.dependencies['package/kde-l10n-hu-package'] = 'default'
        self.dependencies['package/kde-l10n-ia-package'] = 'default'
        self.dependencies['package/kde-l10n-id-package'] = 'default'
        self.dependencies['package/kde-l10n-is-package'] = 'default'
        self.dependencies['package/kde-l10n-it-package'] = 'default'
        self.dependencies['package/kde-l10n-ja-package'] = 'default'
        self.dependencies['package/kde-l10n-kk-package'] = 'default'
        self.dependencies['package/kde-l10n-km-package'] = 'default'
        self.dependencies['package/kde-l10n-ko-package'] = 'default'
        self.dependencies['package/kde-l10n-lt-package'] = 'default'
        self.dependencies['package/kde-l10n-lv-package'] = 'default'
        self.dependencies['package/kde-l10n-nb-package'] = 'default'
        self.dependencies['package/kde-l10n-nds-package'] = 'default'
        self.dependencies['package/kde-l10n-nl-package'] = 'default'
        self.dependencies['package/kde-l10n-nn-package'] = 'default'
        self.dependencies['package/kde-l10n-pa-package'] = 'default'
        self.dependencies['package/kde-l10n-pl-package'] = 'default'
        self.dependencies['package/kde-l10n-pt-package'] = 'default'
        self.dependencies['package/kde-l10n-pt_BR-package'] = 'default'
        self.dependencies['package/kde-l10n-ro-package'] = 'default'
        self.dependencies['package/kde-l10n-ru-package'] = 'default'
        self.dependencies['package/kde-l10n-sk-package'] = 'default'
        self.dependencies['package/kde-l10n-sl-package'] = 'default'
        self.dependencies['package/kde-l10n-sr-package'] = 'default'
        self.dependencies['package/kde-l10n-sv-package'] = 'default'
        self.dependencies['package/kde-l10n-th-package'] = 'default'
        self.dependencies['package/kde-l10n-tr-package'] = 'default'
        self.dependencies['package/kde-l10n-ug-package'] = 'default'
        self.dependencies['package/kde-l10n-uk-package'] = 'default'
        self.dependencies['package/kde-l10n-wa-package'] = 'default'
        self.dependencies['package/kde-l10n-zh_CN-package'] = 'default'
        self.dependencies['package/kde-l10n-zh_TW-package'] = 'default'

from Package.VirtualPackageBase import *

class Package( VirtualPackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        VirtualPackageBase.__init__( self )


if __name__ == '__main__':
    Package().execute()

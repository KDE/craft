import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['4.9.0'] = ''
        self.defaultTarget = '4.9.0'

    def setDependencies( self ):
        self.dependencies['kde/kde-l10n-ar'] = 'default'
        self.dependencies['kde/kde-l10n-bg'] = 'default'
        self.dependencies['kde/kde-l10n-bs'] = 'default'
        self.dependencies['kde/kde-l10n-ca'] = 'default'
        self.dependencies['kde/kde-l10n-ca@valencia'] = 'default'
        self.dependencies['kde/kde-l10n-cs'] = 'default'
        self.dependencies['kde/kde-l10n-da'] = 'default'
        self.dependencies['kde/kde-l10n-de'] = 'default'
        self.dependencies['kde/kde-l10n-el'] = 'default'
        self.dependencies['kde/kde-l10n-en_GB'] = 'default'
        self.dependencies['kde/kde-l10n-es'] = 'default'
        self.dependencies['kde/kde-l10n-et'] = 'default'
        self.dependencies['kde/kde-l10n-eu'] = 'default'
        self.dependencies['kde/kde-l10n-fi'] = 'default'
        self.dependencies['kde/kde-l10n-fr'] = 'default'
        self.dependencies['kde/kde-l10n-ga'] = 'default'
        self.dependencies['kde/kde-l10n-gl'] = 'default'
        self.dependencies['kde/kde-l10n-he'] = 'default'
        self.dependencies['kde/kde-l10n-hr'] = 'default'
        self.dependencies['kde/kde-l10n-hu'] = 'default'
        self.dependencies['kde/kde-l10n-ia'] = 'default'
        self.dependencies['kde/kde-l10n-id'] = 'default'
        self.dependencies['kde/kde-l10n-is'] = 'default'
        self.dependencies['kde/kde-l10n-it'] = 'default'
        self.dependencies['kde/kde-l10n-ja'] = 'default'
        self.dependencies['kde/kde-l10n-kk'] = 'default'
        self.dependencies['kde/kde-l10n-km'] = 'default'
        self.dependencies['kde/kde-l10n-ko'] = 'default'
        self.dependencies['kde/kde-l10n-lt'] = 'default'
        self.dependencies['kde/kde-l10n-lv'] = 'default'
        self.dependencies['kde/kde-l10n-nb'] = 'default'
        self.dependencies['kde/kde-l10n-nds'] = 'default'
        self.dependencies['kde/kde-l10n-nl'] = 'default'
        self.dependencies['kde/kde-l10n-nn'] = 'default'
        self.dependencies['kde/kde-l10n-pa'] = 'default'
        self.dependencies['kde/kde-l10n-pl'] = 'default'
        self.dependencies['kde/kde-l10n-pt'] = 'default'
        self.dependencies['kde/kde-l10n-pt_BR'] = 'default'
        self.dependencies['kde/kde-l10n-ro'] = 'default'
        self.dependencies['kde/kde-l10n-ru'] = 'default'
        self.dependencies['kde/kde-l10n-sk'] = 'default'
        self.dependencies['kde/kde-l10n-sl'] = 'default'
        self.dependencies['kde/kde-l10n-sr'] = 'default'
        self.dependencies['kde/kde-l10n-sv'] = 'default'
        self.dependencies['kde/kde-l10n-th'] = 'default'
        self.dependencies['kde/kde-l10n-tr'] = 'default'
        self.dependencies['kde/kde-l10n-ug'] = 'default'
        self.dependencies['kde/kde-l10n-uk'] = 'default'
        self.dependencies['kde/kde-l10n-wa'] = 'default'
        self.dependencies['kde/kde-l10n-zh_CN'] = 'default'
        self.dependencies['kde/kde-l10n-zh_TW'] = 'default'

from Package.VirtualPackageBase import *

class Package( VirtualPackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        VirtualPackageBase.__init__( self )


if __name__ == '__main__':
    Package().execute()

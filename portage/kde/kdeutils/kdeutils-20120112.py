import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = ''
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['ark'] = 'default'
        self.dependencies['filelight'] = 'default'
        self.dependencies['kcalc'] = 'default'
        self.dependencies['kcharselect'] = 'default'
        self.dependencies['kdiskfree'] = 'default'
        self.dependencies['kfloppy'] = 'default'
        self.dependencies['kgpg'] = 'default'
        self.dependencies['kremotecontrol'] = 'default'
        self.dependencies['ksecretsservice'] = 'default'
        self.dependencies['ktimer'] = 'default'
        self.dependencies['kwallet'] = 'default'
        self.dependencies['printer-applet'] = 'default'
        self.dependencies['superkaramba'] = 'default'
        self.dependencies['sweeper'] = 'default'

from Package.VirtualPackageBase import *

class Package( VirtualPackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        VirtualPackageBase.__init__( self )


if __name__ == '__main__':
    Package().execute()

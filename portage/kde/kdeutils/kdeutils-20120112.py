import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = ''
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['kde/ark'] = 'default'
        self.dependencies['kde/filelight'] = 'default'
        self.dependencies['kde/kcalc'] = 'default'
        self.dependencies['kde/kcharselect'] = 'default'
        self.dependencies['kde/kdiskfree'] = 'default'
        self.dependencies['kde/kfloppy'] = 'default'
        self.dependencies['kde/kgpg'] = 'default'
        self.dependencies['kde/kremotecontrol'] = 'default'
        self.dependencies['kde/ksecretsservice'] = 'default'
        self.dependencies['kde/ktimer'] = 'default'
        self.dependencies['kde/kwallet'] = 'default'
        self.dependencies['kde/printer-applet'] = 'default'
        self.dependencies['kde/superkaramba'] = 'default'
        self.dependencies['kde/sweeper'] = 'default'

from Package.VirtualPackageBase import *

class Package( VirtualPackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        VirtualPackageBase.__init__( self )


if __name__ == '__main__':
    Package().execute()

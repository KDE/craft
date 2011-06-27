import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = ''
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['kde/okular'] = 'default'
        self.dependencies['kde/gwenview'] = 'default'
        self.dependencies['kde/kolourpaint'] = 'default'
        self.dependencies['kde/kruler'] = 'default'
        self.dependencies['kde/ksnapshot'] = 'default'

from Package.VirtualPackageBase import *

if __name__ == '__main__':
    Package(subinfo()).execute()

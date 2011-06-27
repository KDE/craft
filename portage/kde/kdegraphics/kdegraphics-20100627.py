import info
import base

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = ''
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['kde/libksane'] = 'default'
        self.dependencies['kde/libkexiv2'] = 'default'
        self.dependencies['kde/libkdcraw'] = 'default'
        self.dependencies['kde/libkipi'] = 'default'      
        self.dependencies['kde/okular'] = 'default'
        self.dependencies['kde/gwenview'] = 'default'
        self.dependencies['kde/kolourpaint'] = 'default'
        self.dependencies['kde/kruler'] = 'default'
        self.dependencies['kde/ksnapshot'] = 'default'
        self.dependencies['kde/svgpart'] = 'default'
        self.dependencies['kde/ksaneplugin'] = 'default'
        self.dependencies['kde/kdegraphics-thumbnailers'] = 'default'  
        
        #doesnt work because of missing dependency gphoto2
        #self.dependencies['kde/kamera'] = 'default'
        

from Package.VirtualPackageBase import *

class Package( VirtualPackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        VirtualPackageBase.__init__( self )


if __name__ == '__main__':
    Package().execute()

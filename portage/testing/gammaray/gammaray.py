import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'git://github.com/KDAB/GammaRay.git'
        self.targets['1.0.1'] = 'https://github.com/KDAB/GammaRay/tarball/v1.0.1'
        self.archiveNames['1.0.1'] = 'GammaRay-v1.0.1.tar.gz'
        self.targetInstSrc['1.0.1'] = 'KDAB-GammaRay-6d4549b'
        self.targetDigests['1.0.1'] = 'bccded4e9764c69774811826497c133985e8dc53'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.shortDescription = "GammaRay is a tool to poke around in a Qt-application and also to manipulate the application to some extent"
        self.dependencies['libs/qt'] = 'default'
        self.dependencies['testing/vtk'] = 'default'
        self.buildDependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DGIT_EXECUTABLE=%s" % os.path.join(os.getenv("KDEROOT"),"dev-utils","git","bin","git.exe").replace("\\","/")

if __name__ == '__main__':
    Package().execute()

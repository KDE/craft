import info

class subinfo(info.infoclass):
    def setTargets( self ):
        for v in [ '0.15' ]:
          self.targets[v] = 'http://icon-theme.freedesktop.org/releases/hicolor-icon-theme-' + v + '.tar.xz'
        self.targetDigests['0.15'] = '368ecc47521e1a2f72cef0171bee02aae876ff53'
        
        self.shortDescription = "High-color icon theme shell from the FreeDesktop project"
        self.defaultTarget = '0.15'
        
    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"

from Package.BinaryPackageBase import *

from Package.CMakePackageBase import *
 
class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__(self)
 
    def configure(self): return True
    def make(self): return True
 
    def install(self):
        hicolorDir = os.path.join(self.imageDir(), "share", "icons", "hicolor");
        utils.createDir(hicolorDir)
        utils.copyFile(os.path.join(self.sourceDir(), "hicolor-icon-theme-" + self.version, "index.theme"),
                        os.path.join(hicolorDir, "index.theme"))
        return True
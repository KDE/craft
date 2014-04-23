import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets["0.7.0"] = "http://telepathy.freedesktop.org/releases/telepathy-haze/telepathy-haze-0.7.0.tar.gz"
        self.targetInstSrc["0.7.0"] = "telepathy-haze-0.7.0"
        self.targetDigests['0.7.0'] = '260d7a50934614570d543916241f880b0dfd2d43'
        self.patchToApply["0.7.0"] = ("telepathy-haze-0.7.0-20130726.diff",1)
        self.defaultTarget = "0.7.0"
        

    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'        
        self.buildDependencies['dev-util/pkg-config'] = 'default'
            


from Package.AutoToolsPackageBase import *

class Package( AutoToolsPackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        self.subinfo.options.make.supportsMultijob = False
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.defines = "--enable-static=no --enable-shared=yes " 


        
if __name__ == '__main__':
    Package().execute()

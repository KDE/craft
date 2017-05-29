import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['HEAD'] = 'http://the.earth.li/~sgtatham/putty/latest/x86/putty.zip'
        for ver in ['0.62', '0.63', '0.64', '0.65', '0.66']:
            self.targets[ver] = 'http://the.earth.li/~sgtatham/putty/' + ver + '/x86/putty.zip'
            self.archiveNames[ver] = "putty-%s.zip" % ver
            self.targetInstallPath[ver] = os.path.join("dev-utils", "bin")

        self.targetDigests['0.62'] = '953e7b2eb7844184ccfb24651c7829f3e1e30558'
        self.targetDigests['0.63'] = '573ffcaa7f3205ca77ee5f3502b7def3b0ec7e79'
        self.targetDigests['0.64'] = '66717b0acb20528e313657b3c69efc3badfe985c'
        self.targetDigests['0.66'] = 'e63298b4ea1db518677a234b185ae12066c89dc0'
        self.defaultTarget = '0.66'

    def setDependencies( self ):
        self.dependencies['virtual/bin-base'] = 'default'


from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self ):
        BinaryPackageBase.__init__( self )





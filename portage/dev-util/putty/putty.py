import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['HEAD'] = 'http://the.earth.li/~sgtatham/putty/latest/x86/putty.zip'
        for ver in ['0.62', '0.63']:
            self.targets[ver] = 'http://the.earth.li/~sgtatham/putty/' + ver + '/x86/putty.zip'
            self.targetInstallPath[ver] = "bin"
        self.targetDigests['0.62'] = '953e7b2eb7844184ccfb24651c7829f3e1e30558'
        self.targetDigests['0.63'] = '573ffcaa7f3205ca77ee5f3502b7def3b0ec7e79'
        self.defaultTarget = '0.63'

    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'


from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self ):
        BinaryPackageBase.__init__( self )
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = 'dev-utils'
        self.subinfo.options.package.withCompiler = False

if __name__ == '__main__':
    Package().execute()




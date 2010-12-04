import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['libs/qt'] = 'default'
        self.dependencies['kdesupport/qjson'] = 'default'

    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'git://gitorious.org/dbusmenu/dbusmenu-qt.git'
        
        for ver in ['0.6.4']:
          self.targets[ver] ='http://launchpad.net/libdbusmenu-qt/trunk/' + ver + '/+download/libdbusmenu-qt-' + ver + '.tar.bz2'
          self.targetInstSrc[ver] = 'libdbusmenu-qt-' + ver 
        
        
        self.defaultTarget = 'gitHEAD'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        
        self.subinfo.options.configure.defines = "-DBUILD_TESTS=OFF "
        qmake = os.path.join(self.mergeDestinationDir(), "bin", "qmake.exe")
        if not os.path.exists(qmake):
            utils.warning("could not find qmake in <%s>" % qmake)
        ## \todo a standardized way to check if a package is installed in the image dir would be good.
        self.subinfo.options.configure.defines += "-DQT_QMAKE_EXECUTABLE:FILEPATH=%s " \
            % qmake.replace('\\', '/')
            
        self.subinfo.options.configure.defines += "-DHOST_BINDIR=%s " \
            % os.path.join(ROOTDIR, "bin")

if __name__ == '__main__':
    Package().execute()

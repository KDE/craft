import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.buildDependencies['dev-util/doxygen'] = 'default'
        self.dependencies['libs/qtbase'] = 'default'
        # self.dependencies['kdesupport/qjson'] = 'default'

    def setTargets( self ):
        # Dbusmenu-qt moved to bazaar in launchpad
        # check https://launchpad.net/libdbusmenu-qt for the trunk sources

        for ver in ['0.9.2']:
          self.targets[ver] = "https://launchpad.net/libdbusmenu-qt/trunk/" + ver +"/+download/libdbusmenu-qt-" +ver + ".tar.bz2"
          self.targetInstSrc[ver] = 'libdbusmenu-qt-' + ver
        for ver in ['0.6.4']:
          self.targets[ver] ='http://launchpad.net/libdbusmenu-qt/trunk/' + ver + '/+download/libdbusmenu-qt-' + ver + '.tar.bz2'
          self.targetInstSrc[ver] = 'libdbusmenu-qt-' + ver
        self.shortDescription = "a Qt implementation of the DBusMenu spec"

        self.patchToApply['0.9.2'] = [('dbusmenu-qt-0.9.2.diff', 1)]
        self.defaultTarget = '0.9.2'

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

import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'git://anongit.freedesktop.org/git/dbus/dbus-python'
        self.defaultTarget = 'gitHEAD'
        self.patchToApply['gitHEAD'] = [
            ('0001-add-cmake-buildsystem.patch', 1),
            ('0002-win32-msvc-port.patch', 1),
            ('0003-fix-install-path-to-support-autoloading-of-_dbus_bin.patch',1)
        ]
        
        

    def setDependencies( self ):
        self.hardDependencies['win32libs/dbus'] = 'default'

from Package.CMakePackageBase import *        
        
class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        self.subinfo.options.make.supportsMultijob = False
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()

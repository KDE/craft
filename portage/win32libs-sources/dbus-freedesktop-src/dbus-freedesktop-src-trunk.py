import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'git://anongit.freedesktop.org/git/dbus/dbus'
        self.targetConfigurePath['svnHEAD'] = 'cmake'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['win32libs-bin/expat'] = 'default'
        self.hardDependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *        
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = "-DDBUS_USE_EXPAT=ON -DDBUS_DISABLE_EXECUTABLE_DEBUG_POSTFIX=ON"
        self.subinfo.options.make.slnBaseName = "dbus"
        self.subinfo.options.package.packageName = 'dbus-freedesktop'
        
if __name__ == '__main__':
    Package().execute()

import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['dbus4win-frank'] = 'ftp://ftp.kdab.net/pub/dbus4win/dbus4win-20090527-3.zip'
        self.targets['dbus4win-noncetcp'] = 'ftp://ftp.kdab.net/pub/dbus4win/dbus4win-noncetcp-20090612.zip'
        self.targetInstSrc['dbus4win-frank'] = os.path.join( "dbus4win-20090527-3", "cmake" )
        self.targetInstSrc['dbus4win-noncetcp'] = os.path.join( "dbus4win-noncetcp-20090612", "cmake" )
        self.svnTargets['svnhead'] = 'git://repo.or.cz/dbus4win.git'
        self.targetConfigurePath['svnHEAD'] = 'cmake'
       
        self.defaultTarget = 'svnHEAD'
        #self.defaultTarget = 'dbus4win-frank'
    
    def setDependencies( self ):
        self.hardDependencies['win32libs-bin/expat'] = 'default'
        self.hardDependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *        
        
class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = "-DDBUS_USE_EXPAT=ON -DDBUS_DISABLE_EXECUTABLE_DEBUG_POSTFIX=ON"

if __name__ == '__main__':
    Package().execute()

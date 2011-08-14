import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['libs/qt'] = 'default'

    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'git://gitorious.org/qjson/qjson.git'
        for ver in ['6.0.1']:
            self.targets[ ver ] = "http://downloads.sourceforge.net/qwt/qwt-" + ver + ".zip"
            self.targetInstSrc[ ver ] = "qwt-" + ver

        self.targetDigests['6.0.1'] = '7ea84ee47339809c671a456b5363d941c45aea92'
        self.patchToApply['6.0.1'] = ("qwt-6.0.1-20110807.diff", 1)
        self.shortDescription = ""
        self.defaultTarget = '6.0.1'

from Package.QMakePackageBase import *

class Package( QMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        QMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = ""
        if self.buildType() == "Release":
            self.subinfo.options.configure.defines += ' "CONFIG -= debug"'
            self.subinfo.options.configure.defines += ' "CONFIG += release"'
            self.subinfo.options.configure.defines += ' "CONFIG -= debug_and_release"'
        if self.buildType() == "Debug":
            self.subinfo.options.configure.defines += ' "CONFIG += debug"'
            self.subinfo.options.configure.defines += ' "CONFIG -= release"'
            self.subinfo.options.configure.defines += ' "CONFIG -= debug_and_release"'
        if self.buildType() == "RelWithDebInfo":
            self.subinfo.options.configure.defines += ' "CONFIG -= debug"'
            self.subinfo.options.configure.defines += ' "CONFIG -= release"'
            self.subinfo.options.configure.defines += ' "CONFIG += debug_and_release"'
        self.subinfo.options.configure.defines += ' "QWT_INSTALL_PREFIX = ' + self.imageDir() + '"'

	def install( self ):
		if not QMakePackageBase.install( self ):
			return False
		if not os.path.exists( os.path.join( self.imageDir(), "bin" ) ):
			os.mkdirs()
		return True
        
if __name__ == '__main__':
    Package().execute()

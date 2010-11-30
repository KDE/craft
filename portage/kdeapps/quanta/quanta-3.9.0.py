import info

class subinfo(info.infoclass):
	def setTargets( self ):
		self.svnTargets['gitHEAD'] = 'git://gitorious.org/kdevelop/quanta.git'
		self.defaultTarget = 'gitHEAD'

	def setDependencies( self ):
		self.dependencies['virtual/kdebase-runtime'] = 'default'
		self.dependencies['testing/kdevplatform'] = 'default'
		self.dependencies['testing/kdevelop'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
	def __init__( self ):
		self.subinfo = subinfo()
		CMakePackageBase.__init__(self)

if __name__ == '__main__':
	Package().execute()


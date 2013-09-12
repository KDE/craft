import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.6.5'] = "http://subversion.tigris.org/files/documents/15/47906/svn-win32-1.6.5.zip"
        for ver in ['1.7.6', '1.8.1']:
            self.targets[ver] = 'http://downloads.sourceforge.net/win32svn/' + ver + '/apache22/svn-win32-' + ver + '.zip'
        for ver in ['1.6.5', '1.7.6', '1.8.1']:
            # this location affects class SvnSource
            self.targetMergePath[ver] = "dev-utils/svn";
            self.targetMergeSourcePath[ver] = "svn-win32-" + ver;
        self.targetDigests['1.6.5'] = '0df7b20e0bf0fa82ca3a9ededb9207ba50df063e'
        self.targetDigests['1.7.6'] = '3a18decdf971268abdec34ab459147a8139241db'
        self.targetDigests['1.8.1'] = 'ecc4f3b05322641b68f4285236fb58add227cc71'
        self.defaultTarget = '1.8.1'

    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'

    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        BinaryPackageBase.__init__(self)

    def unpack(self):
        if not BinaryPackageBase.unpack(self):
            return False
        utils.copyFile(os.path.join(self.packageDir(),"svn.bat"),os.path.join(self.rootdir,"dev-utils","bin","svn.bat"))
        return True
	
if __name__ == '__main__':
    Package().execute()

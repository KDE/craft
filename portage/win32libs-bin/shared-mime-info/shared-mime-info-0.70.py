from Package.BinaryPackageBase import *
import os
import info
import shutil
import utils
import compiler

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for version in ['0.51-1', '0.51-2', '0.60', '0.70']:
            self.targets[ version ] = repoUrl + """/shared-mime-info-""" + version + """-bin.tar.bz2"""
        self.defaultTarget = '0.70'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
        self.hardDependencies['win32libs-bin/gettext'] = 'default'
        self.hardDependencies['win32libs-bin/libxml2'] = 'default'
        if compiler.isMinGW():
            self.hardDependencies['dev-util/uactools'] = 'default'

class Package(BinaryPackageBase):
    def __init__(self):
        self.subinfo = subinfo()
        BinaryPackageBase.__init__( self )

    def install( self ):
        BinaryPackageBase.install( self )
        manifest = os.path.join( self.packageDir(), "update-mime-database.exe.manifest" )
        patch = os.path.join( self.imageDir(), "bin", "update-mime-database.exe" )
        cmd = "mt.exe -nologo -manifest %s -outputresource:%s;1" % ( manifest, patch )
        utils.system( cmd )

        return True

if __name__ == '__main__':
    Package().execute()

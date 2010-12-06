import base
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://winkde.org/pub/kde/ports/win32/repository/aspell"""
        
        self.targets[ '0.60' ] = (repoUrl + """/aspell-en-6.0-41-bin.tar.bz2 """
                                + repoUrl + """/aspell-de-0.60.20030222.1-10-bin.tar.bz2 """
                                + """ http://files.kolab.org/local/windows-ce/aspell-0.60.6-codepages.zip""")

        self.defaultTarget = '0.60'
            
    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'

from Package.BinaryPackageBase import *
        
class Package(BinaryPackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()

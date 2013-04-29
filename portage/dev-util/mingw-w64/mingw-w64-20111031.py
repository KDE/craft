import utils
import shutil
import os
import info
import emergePlatform

class subinfo(info.infoclass):
    def setTargets( self ):
        ver = "4.8.0"
        rev = "2"
        if emergePlatform.buildArchitecture() == 'x64':
            self.targets[ "%s-%s" % ( ver, rev ) ] = "http://downloads.sourceforge.net/sourceforge/mingwbuilds/x64-%s-release-posix-seh-rev%s.7z" % ( ver, rev )
        else:
            self.targets[ "%s-%s" % ( ver, rev )] = "http://downloads.sourceforge.net/sourceforge/mingwbuilds/x32-%s-release-posix-sjlj-rev%s.7z" % ( ver, rev )
        self.defaultTarget = "%s-%s" % ( ver, rev )

    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        BinaryPackageBase.__init__(self)


if __name__ == '__main__':
    Package().execute()

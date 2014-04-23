# -*- coding: utf-8 -*-
import info

#
class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['4.7.4'] = """
			http://downloads.sourceforge.net/project/kde-windows/qt-static/release/4.7.4/qt-static-vc100-4.7.4-bin.tar.bz2
			http://downloads.sourceforge.net/project/kde-windows/qt-static/release/4.7.4/qt-static-vc100-4.7.4-lib.tar.bz2
		"""
        self.targetDigests['4.7.4'] = ['1299e38b2d689a8496712220069728e012b11449',
                                       '215a7d00138a1ac622ec5f8893fc527e0f4d6a82']	
        self.defaultTarget = '4.7.4'

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        BinaryPackageBase.__init__(self)
        self.subinfo.options.merge.destinationPath = "qt-static"

if __name__ == '__main__':
    Package().execute()

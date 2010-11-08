# -*- coding: utf-8 -*-
import info
import os
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['libs/qt'] = 'default'

        
    def setTargets( self ):
        self.targets['2.7_1'] = 'http://get.qt.nokia.com/qt/solutions/lgpl/qtsoap-2.7_1-opensource.zip'
        self.patchToApply['2.7_1'] = ('qtsoap-2.7_1-opensource-20101108.diff',1)
        self.targetDigests['2.7_1'] = '933ffd4215052af7eed48fc9492a1cd6996c7641'
        self.targetInstSrc['2.7_1'] = 'qtsoap-2.7_1-opensource'
        self.defaultTarget = '2.7_1'
         

class Package( CMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()

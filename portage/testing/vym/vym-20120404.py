# -*- coding: utf-8 -*-
import info

class subinfo(info.infoclass):
    def setTargets( self ):        
        self.shortDescription = "VYM (View Your Mind) is a tool to generate and manipulate maps which show your thoughts"
        self.svnTargets['gitHEAD'] = "git://vym.git.sourceforge.net/gitroot/vym/vym"
        for ver in ["2.0.10", "2.2.4", "2.3.15"]:
            self.targets[ver] = "http://downloads.sourceforge.net/sourceforge/vym/vym-" + ver + ".tar.bz2"
            self.targetInstSrc[ver] = "vym-" + ver
        self.patchToApply["2.0.10"] = ("vym-2.0.10-20120404.diff", 1)
        self.targetDigests['2.0.10'] = '9f23a258b5ea0a326570499b5e9723681deafa7c'
        self.defaultTarget = "2.0.10"

    def setDependencies( self ):
        self.dependencies['libs/qt'] = 'default'


from Package.QMakePackageBase import *

class Package( QMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        QMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = ' "PREFIX = %s" ' % self.imageDir().replace("\\","/")

if __name__ == '__main__':
    Package().execute()

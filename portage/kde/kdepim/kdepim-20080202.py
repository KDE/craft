# -*- coding: utf-8 -*-
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['4.0.0'] = 'tags/KDE/4.0.0/kdepim'
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdepim'
        for ver in ['80', '83', '85']:
          self.targets['4.0.' + ver] = 'ftp://ftp.kde.org/pub/kde/unstable/4.0.' + ver + '/src/kdepim-4.0.' + ver + '.tar.bz2'
          self.targetInstSrc['4.0.' + ver] = 'kdepim-4.0.' + ver
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        if not platform.isCrossCompilingEnabled():
            self.hardDependencies['kde/kdebase-runtime'] = 'default'
        self.hardDependencies['kde/kdepimlibs'] = 'default'
        self.hardDependencies['kdesupport/grantlee'] = 'default'
        self.hardDependencies['win32libs-bin/sqlite'] = 'default'
        
    def setBuildOptions( self ):
        self.disableHostBuild = True
        self.disableTargetBuild = False

from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DKLEO_SYNCHRONOUS_API_HOTFIX=ON "

        if platform.isCrossCompilingEnabled():
            self.subinfo.options.configure.defines += "-DDISABLE_ALL_OPTIONAL_SUBDIRECTORIES=TRUE "
            self.subinfo.options.configure.defines += " -DKDEPIM_MOBILE_UI=TRUE "
            self.subinfo.options.configure.defines += " -DBUILD_mobile=ON -DBUILD_messagecomposer=ON  -DBUILD_runtime=ON "
            self.subinfo.options.configure.defines += " -DMESSAGEVIEWER_NO_WEBKIT=ON "
            self.subinfo.options.configure.defines += " -DTEMPLATEPARSER_NO_WEBKIT=ON "
            self.subinfo.options.configure.defines += " -DIMAPRESOURCE_NO_SOLID=ON "
            self.subinfo.options.configure.defines += " -DRUNTIME_PLUGINS_STATIC=ON "
            self.subinfo.options.configure.defines += " -DKDEQMLPLUGIN_STATIC=ON "
            self.subinfo.options.configure.defines += " -DACCOUNTWIZARD_NO_GHNS=ON "

        self.subinfo.options.configure.defines += "-DHOST_BINDIR=%s " \
            % os.path.join(ROOTDIR, "bin")

    def execute(self):
        (command, option) = self.getAction()
        if self.isTargetBuild() and command == "qmerge":
            # Probably a good idea for host / normal build, too?
            ret = self.runAction(command) == 0
            mime_update = os.path.join(ROOTDIR, "bin",
                    "update-mime-database.exe")
            if not os.path.isfile(mime_update):
                return ret
            else:
                target_mimedb = os.path.join(ROOTDIR, self.buildPlatform(),
                        "share", "mime")
                utils.debug("calling update-mime-database: on %s " %\
                        target_mimedb, 1)
                cmd = "%s %s" % (mime_update, target_mimedb)
                return utils.system(cmd)
        return self.runAction(command) == 0

if __name__ == '__main__':
    Package().execute()

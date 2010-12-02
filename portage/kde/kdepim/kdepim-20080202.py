# -*- coding: utf-8 -*-
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdepim'
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        if not emergePlatform.isCrossCompilingEnabled():
            self.dependencies['kde/kdebase-runtime'] = 'default'
        else:
            self.dependencies['kdesupport/oxygen-icons'] = 'default'
        self.dependencies['kde/kdepimlibs'] = 'default'
        if not emergePlatform.isCrossCompilingEnabled():
            self.dependencies['kdesupport/grantlee'] = 'default'
        self.dependencies['win32libs-bin/sqlite'] = 'default'
        
    def setBuildOptions( self ):
        self.disableHostBuild = True
        self.disableTargetBuild = False

from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DKLEO_SYNCHRONOUS_API_HOTFIX=ON "

        if emergePlatform.isCrossCompilingEnabled():
            self.subinfo.options.configure.defines += "-DDISABLE_ALL_OPTIONAL_SUBDIRECTORIES=TRUE "
            self.subinfo.options.configure.defines += " -DKDEPIM_MOBILE_UI=TRUE "
            self.subinfo.options.configure.defines += " -DBUILD_mobile=ON -DBUILD_messagecomposer=ON  -DBUILD_runtime=ON -DBUILD_strigi-analyzer=ON "
            self.subinfo.options.configure.defines += " -DMESSAGEVIEWER_NO_WEBKIT=ON "
            self.subinfo.options.configure.defines += " -DTEMPLATEPARSER_NO_WEBKIT=ON "
            #self.subinfo.options.configure.defines += " -DIMAPRESOURCE_NO_SOLID=ON "
            self.subinfo.options.configure.defines += " -DRUNTIME_PLUGINS_STATIC=ON "
            self.subinfo.options.configure.defines += " -DKDEQMLPLUGIN_STATIC=ON "
            self.subinfo.options.configure.defines += " -DACCOUNTWIZARD_NO_GHNS=ON "
            self.subinfo.options.configure.defines += " -DBUILD_kmail=ON "
            self.subinfo.options.configure.defines += " -DKDEPIM_NO_NEPOMUK=ON "
            self.subinfo.options.configure.defines += " -DKDE4_BUILD_TESTS=OFF "
            self.subinfo.options.configure.defines += " -DBUILD_kleopatra=ON "
            self.subinfo.options.configure.defines += " -DBUILD_korganizer=ON "
            self.subinfo.options.configure.defines += " -DKDEPIM_ENTERPRISE_BUILD=ON "
            self.subinfo.options.configure.defines += " -DKORGAC_AKONADI_AGENT=ON "
            self.subinfo.options.configure.defines += " -DBUILD_NEW_MAIL_NOTIFIER_AGENT=ON "
        else:
            self.subinfo.options.configure.defines += " -DKDEPIM_BUILD_MOBILE=FALSE "

        self.subinfo.options.configure.defines += "-DHOST_BINDIR=%s " \
            % os.path.join(ROOTDIR, "bin")


    def qmerge(self):
        ret = CMakePackageBase.qmerge(self)
        if self.isTargetBuild():
            mime_update = os.path.join(ROOTDIR, "bin",
                    "update-mime-database.exe")
            if os.path.isfile(mime_update):
                target_mimedb = os.path.join(ROOTDIR, self.buildPlatform(),
                        "share", "mime")
                utils.debug("calling update-mime-database: on %s " %\
                        target_mimedb, 1)
                cmd = "%s %s" % (mime_update, target_mimedb)
                return utils.system(cmd)
        return ret


if __name__ == '__main__':
    Package().execute()

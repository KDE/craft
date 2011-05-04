# -*- coding: utf-8 -*-
import info
import os

class subinfo(info.infoclass):
    def apply_branding( self, envVar ):
        """ Apply all Patches from the directory set as envVar """
        brandingDir = os.getenv( envVar )
        if not brandingDir:
            return
        else:
            brandingPatches = []
            for fname in os.listdir( brandingDir ):
                if fname.endswith(".patch") or fname.endswith( ".diff" ):
                    brandingPatches.append( (
                        os.path.join(brandingDir, fname), 1 ) )
            for target in self.svnTargets.iterkeys():
                if self.patchToApply.get(target):
                    self.patchToApply[target] += brandingPatches
                else:
                    self.patchToApply[target] = brandingPatches

    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:kdepim'
        self.svnTargets['20091111'] = 'tags/kdepim/pe5.20091111/kdepim'
        self.svnTargets['20091123'] = 'tags/kdepim/pe5.20091123/kdepim'
        self.svnTargets['20091201'] = 'tags/kdepim/pe5.20091201/kdepim'
        self.svnTargets['20100101'] = 'tags/kdepim/enterprise5.0.20100101.1068602/kdepim'
        self.svnTargets['20100115'] = 'tags/kdepim/enterprise5.0.20100115.1075215/kdepim'
        self.svnTargets['20100122'] = 'tags/kdepim/enterprise5.0.20100122.1078631/kdepim'
        self.svnTargets['20100129'] = 'tags/kdepim/enterprise5.0.20100129.1082020/kdepim'
        self.svnTargets['20100205'] = 'tags/kdepim/enterprise5.0.20100205.1085631/kdepim'
        self.svnTargets['20100212'] = 'tags/kdepim/enterprise5.0.20100212.1089060/kdepim'
        self.svnTargets['20100219'] = 'tags/kdepim/enterprise5.0.20100219.1092868/kdepim'
        self.svnTargets['20100226'] = 'tags/kdepim/enterprise5.0.20100226.1096279/kdepim'
        self.svnTargets['20100305'] = 'tags/kdepim/enterprise5.0.20100305.1099232/kdepim'
        self.svnTargets['20100312'] = 'tags/kdepim/enterprise5.0.20100312.1102371/kdepim'
        self.svnTargets['20100319'] = 'tags/kdepim/enterprise5.0.20100319.1105074/kdepim'
        self.svnTargets['20100326'] = 'tags/kdepim/enterprise5.0.20100326.1107645/kdepim'
        self.svnTargets['20100401'] = 'tags/kdepim/enterprise5.0.20100401.1110042/kdepim'
        self.svnTargets['20100409'] = 'tags/kdepim/enterprise5.0.20100409.1112952/kdepim'
        self.svnTargets['20100507'] = 'tags/kdepim/enterprise5.0.20100507.1123982/kdepim'
        self.svnTargets['20100528'] = 'tags/kdepim/enterprise5.0.20100528.1131643/kdepim'
        self.svnTargets['20100604'] = 'tags/kdepim/enterprise5.0.20100604.1134428/kdepim'
        self.svnTargets['20100611'] = 'tags/kdepim/enterprise5.0.20100611.1136974/kdepim'
        self.svnTargets['20100618'] = 'tags/kdepim/enterprise5.0.20100618.1139547/kdepim'
        self.svnTargets['20100625'] = 'tags/kdepim/enterprise5.0.20100625.1142603/kdepim'
        self.svnTargets['20100701'] = 'tags/kdepim/enterprise5.0.20100701.1144979/kdepim'
        self.svnTargets['20100709'] = 'tags/kdepim/enterprise5.0.20100709.1148001/kdepim'
        self.svnTargets['20100716'] = 'tags/kdepim/enterprise5.0.20100716.1150616/kdepim'
        self.svnTargets['20100723'] = 'tags/kdepim/enterprise5.0.20100723.1153624/kdepim'
        self.svnTargets['20100730'] = 'tags/kdepim/enterprise5.0.20100730.1157241/kdepim'
        self.svnTargets['20100805'] = 'tags/kdepim/enterprise5.0.20100805.1159431/kdepim'
        self.svnTargets['20100813'] = 'tags/kdepim/enterprise5.0.20100813.1163234/kdepim'
        self.svnTargets['20100820'] = 'tags/kdepim/enterprise5.0.20100820.1165957/kdepim'
        self.svnTargets['20100827'] = 'tags/kdepim/enterprise5.0.20100827.1168749/kdepim'
        self.svnTargets['20100903'] = 'tags/kdepim/enterprise5.0.20100903.1171282/kdepim'
        self.svnTargets['20100910'] = 'tags/kdepim/enterprise5.0.20100910.1173808/kdepim'
        self.svnTargets['20100917'] = 'tags/kdepim/enterprise5.0.20100917.1176291/kdepim'
        self.svnTargets['20100927'] = 'tags/kdepim/enterprise5.0.20100927.1180225/kdepim'
        self.svnTargets['20101001'] = 'tags/kdepim/enterprise5.0.20101001.1181557/kdepim'
        self.svnTargets['20101008'] = 'tags/kdepim/enterprise5.0.20101008.1183806/kdepim'
        self.svnTargets['20101015'] = 'tags/kdepim/enterprise5.0.20101015.1186246/kdepim'
        self.svnTargets['20101022'] = 'tags/kdepim/enterprise5.0.20101022.1188481/kdepim'
        self.svnTargets['20101029'] = 'tags/kdepim/enterprise5.0.20101029.1191061/kdepim'
        self.svnTargets['20101112'] = 'tags/kdepim/enterprise5.0.20101112.1196098/kdepim'
        self.svnTargets['20101122'] = 'tags/kdepim/enterprise5.0.20101122.1199662/kdepim'
        self.svnTargets['20101126'] = 'tags/kdepim/enterprise5.0.20101126.1201045/kdepim'
        self.svnTargets['20101129'] = 'tags/kdepim/enterprise5.0.20101129.1201940/kdepim'
        self.svnTargets['20101129'] = 'tags/kdepim/enterprise5.0.20101129.1201945/kdepim'
        self.svnTargets['20101203'] = 'tags/kdepim/enterprise5.0.20101203.1203322/kdepim'
        self.svnTargets['20101217'] = 'tags/kdepim/enterprise5.0.20101217.1207336/kdepim'
        self.svnTargets['20110110'] = 'tags/kdepim/.20110110.enterprise5.0/kdepim'
        self.svnTargets['20110117'] = 'tags/kdepim/.20110117.enterprise5.0/kdepim'
        self.defaultTarget = 'gitHEAD'
        self.patchToApply['gitHEAD'] = [
                ('disable-crypto-backend.patch', 1),
        # Necessary until we know how to build a stable gpgme for windows
                ('add-full-shutdown-button.patch', 1)]
        # Testing
        self.apply_branding("EMERGE_KDEPIME5_BRANDING_PATCHES")

    def setDependencies( self ):
        self.hardDependencies['enterprise5/kdepimlibs-e5'] = 'default'
        self.hardDependencies['enterprise5/kderuntime-e5'] = 'default'
        self.hardDependencies['enterprise5/grantlee-e5'] = 'default'
        self.hardDependencies['win32libs-bin/sqlite'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = (
                " -DKLEO_SYNCHRONOUS_API_HOTFIX=ON "
                " -DKDEPIM_ENTERPRISE_BUILD=ON ")

    def qmerge( self ):
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


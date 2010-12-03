import base
import utils
import sys
import info

class subinfo(info.infoclass):
    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['libs/qt'] = 'default'
        self.hardDependencies['win32libs-sources/clucene-core-src'] = 'default'
        if not emergePlatform.isCrossCompilingEnabled:
            self.hardDependencies['win32libs-sources/exiv2-src'] = 'default'
        self.hardDependencies['win32libs-sources/libbzip2-src'] = 'default'
        self.hardDependencies['win32libs-sources/win_iconv-src'] = 'default'
        self.hardDependencies['win32libs-bin/libxml2'] = 'default'
        self.hardDependencies['win32libs-bin/zlib'] = 'default'

    def setTargets( self ):
        self.svnTargets['0.5.7'] = 'tags/strigi/strigi/0.5.7'
        self.svnTargets['0.5.8'] = 'tags/strigi/strigi/0.5.8'
        self.svnTargets['0.5.9'] = 'tags/strigi/strigi/0.5.9'
        self.svnTargets['0.5.10'] = 'tags/strigi/strigi/0.5.10'
        self.svnTargets['0.5.11'] = 'tags/strigi/strigi/0.5.11'
        self.svnTargets['0.6.3']  = 'tags/strigi/strigi/0.6.3'
        self.svnTargets['0.6.4']  = 'tags/strigi/strigi/strigi-0.6.4'
        self.svnTargets['0.6.5']  = 'tags/strigi/strigi/0.6.5'
        self.svnTargets['4.4'] = 'tags/kdesupport-for-4.4/strigi'
        self.svnTargets['20091111'] = 'tags/kdepim/pe5.20091111/kdesupport/strigi'
        self.svnTargets['20091123'] = 'tags/kdepim/pe5.20091123/kdesupport/strigi'
        self.svnTargets['20091201'] = 'tags/kdepim/pe5.20091201/kdesupport/strigi'
        self.svnTargets['20100101'] = 'tags/kdepim/enterprise5.0.20100101.1068602/kdesupport/strigi'
        self.svnTargets['20100115'] = 'tags/kdepim/enterprise5.0.20100115.1075215/kdesupport/strigi'
        self.svnTargets['20100122'] = 'tags/kdepim/enterprise5.0.20100122.1078631/kdesupport/strigi'
        self.svnTargets['20100129'] = 'tags/kdepim/enterprise5.0.20100129.1082020/kdesupport/strigi'
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/strigi'
        self.svnTargets['20100205'] = 'tags/kdepim/enterprise5.0.20100205.1085631/kdesupport/strigi'
        self.svnTargets['20100212'] = 'tags/kdepim/enterprise5.0.20100212.1089060/kdesupport/strigi'
        self.svnTargets['20100219'] = 'tags/kdepim/enterprise5.0.20100219.1092868/kdesupport/strigi'
        self.svnTargets['20100226'] = 'tags/kdepim/enterprise5.0.20100226.1096279/kdesupport/strigi'
        self.svnTargets['20100305'] = 'tags/kdepim/enterprise5.0.20100305.1099232/kdesupport/strigi'
        self.svnTargets['20100312'] = 'tags/kdepim/enterprise5.0.20100312.1102371/kdesupport/strigi'
        self.svnTargets['20100319'] = 'tags/kdepim/enterprise5.0.20100319.1105074/kdesupport/strigi'
        self.svnTargets['20100326'] = 'tags/kdepim/enterprise5.0.20100326.1107645/kdesupport/strigi'
        self.svnTargets['20100401'] = 'tags/kdepim/enterprise5.0.20100401.1110042/kdesupport/strigi'
        self.svnTargets['20100409'] = 'tags/kdepim/enterprise5.0.20100409.1112952/kdesupport/strigi'
        self.svnTargets['20100507'] = 'tags/kdepim/enterprise5.0.20100507.1123982/kdesupport/strigi'
        self.svnTargets['20100528'] = 'tags/kdepim/enterprise5.0.20100528.1131643/kdesupport/strigi'
        self.svnTargets['20100604'] = 'tags/kdepim/enterprise5.0.20100604.1134428/kdesupport/strigi'
        self.svnTargets['20100611'] = 'tags/kdepim/enterprise5.0.20100611.1136974/kdesupport/strigi'
        self.svnTargets['20100618'] = 'tags/kdepim/enterprise5.0.20100618.1139547/kdesupport/strigi'
        self.svnTargets['20100625'] = 'tags/kdepim/enterprise5.0.20100625.1142603/kdesupport/strigi'
        self.svnTargets['20100701'] = 'tags/kdepim/enterprise5.0.20100701.1144979/kdesupport/strigi'
        self.svnTargets['20100709'] = 'tags/kdepim/enterprise5.0.20100709.1148001/kdesupport/strigi'
        self.svnTargets['20100716'] = 'tags/kdepim/enterprise5.0.20100716.1150616/kdesupport/strigi'
        self.svnTargets['20100723'] = 'tags/kdepim/enterprise5.0.20100723.1153624/kdesupport/strigi'
        self.svnTargets['20100730'] = 'tags/kdepim/enterprise5.0.20100730.1157241/kdesupport/strigi'
        self.svnTargets['20100805'] = 'tags/kdepim/enterprise5.0.20100805.1159431/kdesupport/strigi'
        self.svnTargets['20100813'] = 'tags/kdepim/enterprise5.0.20100813.1163234/kdesupport/strigi'
        self.svnTargets['20100820'] = 'tags/kdepim/enterprise5.0.20100820.1165957/kdesupport/strigi'
        self.svnTargets['20100827'] = 'tags/kdepim/enterprise5.0.20100827.1168749/kdesupport/strigi'
        self.svnTargets['20100903'] = 'tags/kdepim/enterprise5.0.20100903.1171282/kdesupport/strigi'
        self.svnTargets['20100910'] = 'tags/kdepim/enterprise5.0.20100910.1173808/kdesupport/strigi'
        self.svnTargets['20100917'] = 'tags/kdepim/enterprise5.0.20100917.1176291/kdesupport/strigi'
        self.svnTargets['20100927'] = 'tags/kdepim/enterprise5.0.20100927.1180225/kdesupport/strigi'
        self.svnTargets['20101001'] = 'tags/kdepim/enterprise5.0.20101001.1181557/kdesupport/strigi'
        self.svnTargets['20101008'] = 'tags/kdepim/enterprise5.0.20101008.1183806/kdesupport/strigi'
        self.svnTargets['20101015'] = 'tags/kdepim/enterprise5.0.20101015.1186246/kdesupport/strigi'
        self.svnTargets['20101022'] = 'tags/kdepim/enterprise5.0.20101022.1188481/kdesupport/strigi'
        self.svnTargets['20101029'] = 'tags/kdepim/enterprise5.0.20101029.1191061/kdesupport/strigi'
        self.svnTargets['20101112'] = 'tags/kdepim/enterprise5.0.20101112.1196098/kdesupport/strigi'
        self.svnTargets['20101122'] = 'tags/kdepim/enterprise5.0.20101122.1199662/kdesupport/strigi'
        self.svnTargets['20101126'] = 'tags/kdepim/enterprise5.0.20101126.1201045/kdesupport/strigi'
        self.svnTargets['20101129'] = 'tags/kdepim/enterprise5.0.20101129.1201940/kdesupport/strigi'
        self.svnTargets['20101129'] = 'tags/kdepim/enterprise5.0.20101129.1201945/kdesupport/strigi'
        self.svnTargets['20101203'] = 'tags/kdepim/enterprise5.0.20101203.1203322/kdesupport/strigi'
        self.defaultTarget = '20101203'

        if emergePlatform.isCrossCompilingEnabled():
            self.defaultTarget = '4.4'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = ""
        if emergePlatform.isCrossCompilingEnabled():
            self.subinfo.options.configure.defines = "-DBUILD_DAEMON=OFF "
            self.subinfo.options.configure.defines += "-DBUILD_DEEPTOOLS=OFF "
            self.subinfo.options.configure.defines += "-DBUILD_UTILS=OFF "
            self.subinfo.options.configure.defines += "-DENABLE_CLUECENE=OFF "
            self.subinfo.options.configure.defines += "-DENABLE_CPPUNIT=OFF "
            if self.isTargetBuild():
                self.subinfo.options.configure.defines += \
                        "-DICONV_SECOND_ARGUMENT_IS_CONST=ON "

        qmake = os.path.join(self.mergeDestinationDir(), "bin", "qmake.exe")
        if not os.path.exists(qmake):
            utils.warning("could not find qmake in <%s>" % qmake)
        ## \todo a standardized way to check if a package is installed in the image dir would be good.
        self.subinfo.options.configure.defines += "-DQT_QMAKE_EXECUTABLE:FILEPATH=%s " \
            % qmake.replace('\\', '/')

if __name__ == '__main__':
    Package().execute()
